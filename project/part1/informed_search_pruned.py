# Project, Part 1, Informed Search

from networkx import nx
import heapq
# import matplotlib.pyplot as plt
from Queue import PriorityQueue
import time
import multiprocessing
import gc


# MAX_CARDS = 1

def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


def exposed_graph(G, node):  # returns graph of exposed people
    H = nx.Graph()
    for i in node:
        H.add_edges_from([(i, n) for n in G.neighbors(i)])

    return H


def add_rem_nodes(G, unex_g):
    unex_list = []
    for node in G:
        if node not in unex_g:
            unex_g.add_node(node)
            unex_list.append(node)

    return unex_list


def path_cost(G, node, exposed_rates, exposed_number):
    population = G.number_of_nodes()
    cost = 0

    for i in range(0, len(exposed_number)):
        cost += population - 1 - exposed_rates[i] * exposed_number[i]

    old_exposed = exposed_graph(G, node[0:len(node)-1])
    new_exposed_people = G.neighbors(node[len(node)-1])
    num_new_exposed = len(set(new_exposed_people).difference(set(old_exposed)))

    adoption_probability = max(.1, 1 - float(1)/float(sum(exposed_number) + len(node) + num_new_exposed))
    cost += population - 1 - num_new_exposed * exposed_rates[len(exposed_rates)-1]
    return [cost, adoption_probability, num_new_exposed]


def heuristic_function(G, node, max_cards, adopt_rate, exposed_number, candidates=None):
    candidates = card_candidates(G, node) if candidates is None else candidates
    cards_remaining = max_cards - len(node)

    if cards_remaining < 0:
        return 0

    new_node = list(node)
    pop_people = []
    pop_nums = []
    for i in range(0, cards_remaining):

        exp = list(exposed_graph(G, new_node))
        res = heapq.nlargest(1, candidates, key=(lambda x: len(set(G.neighbors(x)).difference(set(exp)))))
        pop_people.append(res[0])

        pop_neighbors = G.neighbors(pop_people[i])
        pop_nums.append(len(set(pop_neighbors).difference(set(exp))))
        new_node.append(res[0])

        candidates = card_candidates(G, list(new_node)) if candidates is None else candidates

    est_cost = 0

    total_exposed_people = sum(exposed_number) + len(node) + len(G.neighbors(node[len(node)-1]))

    for i in range(0, cards_remaining):
        est_cost += G.number_of_nodes() - 1 - pop_nums[cards_remaining - i - 1]
        total_exposed_people += pop_nums[cards_remaining - i - 1] + 1

    if est_cost >= 0:
        return est_cost
    else:
        return 0


def evaluation_function(G, node, max_cards, current_adopt, current_exposed, candidates=None):
    path_cost_values = path_cost(G, node, current_adopt, current_exposed)
    return [heuristic_function(G, node, max_cards, current_adopt, current_exposed, candidates) + path_cost_values[0], path_cost_values[1], path_cost_values[2]]


def card_candidates_graph(G, node):  # should return remaining unexposed population graph
    H = exposed_graph(G, node)

    add_rem_nodes(G, H)

    start = time.clock()
    I = nx.difference(G, H)
    end = time.clock()
    print(end - start)
    for n in range(0, len(node)):
        I.remove_nodes_from(G.neighbors(node[n]))
        I.remove_node(node[n])

    return I


def card_candidates(G, node):  # should return remaining unexposed population
    H = exposed_graph(G, node)
    add_rem_nodes(G, H)
    I = nx.difference(G, H)
    for n in range(0, len(node)):
        I.remove_nodes_from(G.neighbors(node[n]))
        I.remove_node(node[n])
    return I.nodes()


def goal_test(G, node, max_cards, candidates=None):
    if len(node) == max_cards:
        return True

    if candidates is None:
        candidates = card_candidates(G, node)
    return len(candidates) == 0


# 0: G
# 1: node
# 2: num_cards
# 3: cost
# 4: current adopt rate
# 5: new exposed people
def multithread_for(args):

    final_result = []
    candidates = card_candidates(args[0], args[1])

    if goal_test(args[0], args[1], args[2], candidates):
        final_result.append(args[3])  # node is a possible goal node, so put its cost
        # until results of other threads are checked, just return it
        final_result.append(args[1])
    else:
        final_result.append(1000000000)
        final_result.append(0)

    results = []

    for candidate in candidates:
        child = (args[1])[:] + [candidate]
        exposed_nodes = set((args[0]).neighbors(candidate) + [candidate])
        child_candidates = filter(lambda n: n not in exposed_nodes, candidates[:])
        eval_results = evaluation_function(args[0], child, args[2], args[4], args[5], child_candidates)
        results.append([eval_results[0], child, (args[4])[:]+[eval_results[1]], (args[5])[:]+[eval_results[2]]])

    final_result.append(results)
    return final_result


def a_star_search(G, num_cards, pool):
    frontier = PriorityQueue()

    count = 0
    #cost, list of people to give cards, list of adoption rates, list of exposed people counts
    frontier.put((0, [[], [0.1], []]))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        num_nodes = 0
        node_list = []
        while num_nodes < 12 and not frontier.empty(): #set num of processes here
            cost, info = frontier.get()
            node = info[0]
            adopt_rate = info[1]
            new_exposed = info[2]
            node_list.append([G, node, num_cards, cost, adopt_rate, new_exposed])
            num_nodes += 1
            count += 1

        evalResults = pool.map(multithread_for, node_list)

        minimum = 1000000000  # nothing should cost more than this
        minimumI = -1
        for i in range(0, num_nodes):
            if evalResults[i][0] < minimum:
                minimum = evalResults[i][0]
                minimumI = i

        if minimum < 1000000000: #answer was found!
            return evalResults[minimumI][1]

        for i in range(0, num_nodes):
            evalResults[i][2] = sorted(evalResults[i][2], key=lambda x: x[0])
            for j in range(0, min(4, len(evalResults[i][2]))):
                frontier.put((evalResults[i][2][j][0], [evalResults[i][2][j][1], evalResults[i][2][j][2], evalResults[i][2][j][3]]))

        gc.collect()


def main():
    print("running project.part1.informed_search")
    pool = multiprocessing.Pool(12)

    G = load_data("348.edges.txt")
    for i in range(1, 11):
        start = time.time()

        solution = a_star_search(G, i, pool)

        print(solution)
        print(time.time() - start)


if __name__ == '__main__':
    main()
