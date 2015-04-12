# Project, Part 1, Informed Search

from networkx import nx
import heapq
# import matplotlib.pyplot as plt
from Queue import PriorityQueue
import time
import sets
import threading
import multiprocessing
import gc


# MAX_CARDS = 1

def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


def exposed_graph(G, node): #returns graph of exposed people
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

    #no
    population = G.number_of_nodes()

    #start = time.time()
    cost = 0

    #no, this loop is cheap - as intended
    for i in range(0, len(exposed_number)):
        cost += population - 1 - exposed_rates[i] * exposed_number[i]

    #no
    old_exposed = exposed_graph(G, node[0:len(node)-1])


    #new idea
    new_exposed_people = G.neighbors(node[len(node)-1])

    num_new_exposed = len(set(new_exposed_people).difference(set(old_exposed)))
    #num_new_exposed = len(new_exposed_people)

    #for n in range(0, len(new_exposed_people)):
    #    if new_exposed_people[n] in old_exposed:
    #        num_new_exposed -= 1

    #no
    adoption_probability = max(.1, 1 - float(1)/float(sum(exposed_number) + len(node) + num_new_exposed))

    #no
    cost += population - 1 - num_new_exposed * exposed_rates[len(exposed_rates)-1]

    return [cost, adoption_probability, num_new_exposed]


def heuristic_key(candidate):
    return


def heuristic_function(G, node, max_cards, adopt_rate, exposed_number, candidates=None):

    #no - this costs practically nothing
    candidates = card_candidates(G, node) if candidates is None else candidates

    #no - this costs practically nothing
    cards_remaining = max_cards - len(node)

    if cards_remaining < 0:
        return 0

    new_node = list(node)
    pop_people = []
    pop_nums = []
    for i in range(0, cards_remaining):

        exp = list(exposed_graph(G, new_node))
        #res = heapq.nlargest(1, candidates, key=(lambda x: len(G.neighbors(x)) - len(set(G.neighbors(x)).intersection(set(exp)))))
        res = heapq.nlargest(1, candidates, key=(lambda x: len(set(G.neighbors(x)).difference(set(exp)))))
        pop_people.append(res[0])

        pop_neighbors = G.neighbors(pop_people[i])
        #pop_nums.append(len(pop_neighbors) - len(set(pop_neighbors).intersection(set(exp))))
        pop_nums.append(len(set(pop_neighbors).difference(set(exp))))
        new_node.append(res[0])

        candidates = card_candidates(G, list(new_node)) if candidates is None else candidates

    est_cost = 0
    # est_adopt_rate = adopt_rate[len(adopt_rate)-1]

    total_exposed_people = sum(exposed_number) + len(node) + len(G.neighbors(node[len(node)-1]))

    for i in range(0, cards_remaining):
        est_adopt_rate = max(.1, 1 - float(1)/float(total_exposed_people))
        est_cost += G.number_of_nodes() - 1 - pop_nums[cards_remaining - i - 1]
        total_exposed_people += pop_nums[cards_remaining - i - 1] + 1

    if est_cost >= 0:
        return est_cost
    else:
        return 0


def evaluation_function(G, node, max_cards, current_adopt, current_exposed, candidates=None):
    #print(str(path_cost(G, node)) + " " + str(heuristic_function(G, node, max_cards, candidates)) + " = " + str(heuristic_function(G, node, max_cards, candidates) + path_cost(G, node)))

    #0.022 seconds - pretty good, but can do better
    path_cost_values = path_cost(G, node, current_adopt, current_exposed)


    #0.022
    #heuristic_function(G, node, max_cards, candidates)

    return [heuristic_function(G, node, max_cards, current_adopt, current_exposed, candidates) + path_cost_values[0], path_cost_values[1], path_cost_values[2]]


def card_candidates_graph(G, node): #should return remaining unexposed population graph
    #start = time.clock()
    #0.0002 seconds at most, but often much less
    H = exposed_graph(G, node)
    #end = time.clock()
    #print(end - start)


    #0.0003 seconds
    add_rem_nodes(G, H)

    start = time.clock()
    I = nx.difference(G, H)
    end = time.clock()
    print(end - start)
    for n in range(0, len(node)):
        I.remove_nodes_from(G.neighbors(node[n]))
        I.remove_node(node[n])
    #print(len(list(I.edges())))

    #I.remove_nodes_from(H) #remove exposed people
    return I


def card_candidates(G, node): #should return remaining unexposed population
    H = exposed_graph(G, node)
    #I = G.copy()
    #I.remove_nodes_from(H) #remove exposed people
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


#0: G
#1: node
#2: num_cards
#3: cost
#4: current adopt rate
#5: new exposed people


def multithread_for(args):

    final_result = []
    candidates = card_candidates(args[0], args[1])

    if goal_test(args[0], args[1], args[2], candidates):
        #print(count, end=" ")
        final_result.append(args[3]) #node is a possible goal node, so put its cost
        #until results of other threads are checked, just return it
        final_result.append(args[1])
    else:
        final_result.append(1000000000)
        final_result.append(0)

    results = []

    #for candidate in candidates:
        #    child = node[:] + [candidate] #local

        #    exposed_nodes = set(G.neighbors(candidate) + [candidate]) # local
        #    child_candidates = filter(lambda n: n not in exposed_nodes, candidates[:])
        #    frontier.put((evalResults[index], child))
        #    index += 1

    #start = time.time()
    for candidate in candidates:
        child = (args[1])[:] + [candidate]

        exposed_nodes = set((args[0]).neighbors(candidate) + [candidate])

        child_candidates = filter(lambda n: n not in exposed_nodes, candidates[:])


        #0.045 seconds, as expected

        start = time.time()
        eval_results = evaluation_function(args[0], child, args[2], args[4], args[5], child_candidates)
        end = time.time()
        #print(end - start)
        results.append([eval_results[0], child, (args[4])[:]+[eval_results[1]], (args[5])[:]+[eval_results[2]]])
        #print("here")
    #end = time.time()
    #print(str(end - start) + " " + str(len(candidates)))

    final_result.append(results)
    #print(time.time() - start)
    return final_result


def a_star_search(G, num_cards, pool):
    frontier = PriorityQueue()

    c = 1
    count = 0
    start = time.time()
    #cost, list of people to give cards, list of adoption rates, list of exposed people counts
    frontier.put((0, [[], [0.1], []]))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        #start = time.time()

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

#        cost1, node1 = frontier.get()

#        cost2, node2 = frontier.get()

#        cost3, node3 = frontier.get()

#        cost4, node4 = frontier.get()

#        cost5, node5 = frontier.get()

#        cost6, node6 = frontier.get()

#        cost7, node7 = frontier.get()

        #candidates = card_candidates(G, node)
        #if goal_test(G, node, num_cards, candidates):
            #print(count, end=" ")
        #    return node

        # print("\nnum candidates: " + str(len(candidates)))

        #multithreaded experiment
        #n = len(candidates)
        #c1 = candidates[0:int(n/7)]
        #c2 = candidates[int(n/7):int(2*n/7)]
        #c3 = candidates[int(2*n/7):int(3*n/7)]
        #c4 = candidates[int(3*n/7):int(4*n/7)]
        #c5 = candidates[int(4*n/7):int(5*n/7)]
        #c6 = candidates[int(5*n/7):int(6*n/7)]
        #c7 = candidates[int(6*n/7):n]

        #a1 = [G, node1, num_cards, cost1]
        #a2 = [G, node2, num_cards, cost2]
        #a3 = [G, node3, num_cards, cost3]
        #a4 = [G, node4, num_cards, cost4]
        #a5 = [G, node5, num_cards, cost5]
        #a6 = [G, node6, num_cards, cost6]
        #a7 = [G, node7, num_cards, cost7]

        #evalResults = pool.map(multithread_for, [a1, a2, a3, a4, a5, a6, a7])

        evalResults = pool.map(multithread_for, node_list)
        #threads
        #p1 = multiprocessing.Process(target=multithread_for, args=(G, c1, candidates, 0, node, num_cards,))
        #p2 = multiprocessing.Process(target=multithread_for, args=(G, c2, candidates, int(n/8), node, num_cards,))
        #p3 = multiprocessing.Process(target=multithread_for, args=(G, c3, candidates, int(2*n/8), node, num_cards,))
        #p4 = multiprocessing.Process(target=multithread_for, args=(G, c4, candidates, int(3*n/8), node, num_cards,))
        #p5 = multiprocessing.Process(target=multithread_for, args=(G, c5, candidates, int(4*n/8), node, num_cards,))
        #p6 = multiprocessing.Process(target=multithread_for, args=(G, c6, candidates, int(5*n/8), node, num_cards,))
        #p7 = multiprocessing.Process(target=multithread_for, args=(G, c7, candidates, int(6*n/8), node, num_cards,))
        #p8 = multiprocessing.Process(target=multithread_for, args=(G, c8, candidates, int(7*n/8), node, num_cards,))

        #print(evalResults)
        index = 0

        minimum = 1000000000 #nothing should cost more than this
        minimumI = -1
        for i in range(0, num_nodes):
            #find minimum answer
            #print(evalResults[i][0])
            if evalResults[i][0] < minimum:
                minimum = evalResults[i][0]
                minimumI = i

        if minimum < 1000000000: #answer was found!
            end = time.time()
            print(end - start)
            print(count)
            return evalResults[minimumI][1]

        #otherwise start adding to the priority queue
        #parallelize this
        #multiple heaps
        args = []
        #for i in range(0, num_nodes):
            #args.append(evalResults[i][2])
        #    args.append(evalResults[i][2])
        #pool.map(lambda x: (frontier.put((y[0], [y[1], y[2], y[3]])) for y in x), args)



        #old
        for i in range(0, num_nodes):
            for j in range(0, len(evalResults[i][2])):
                frontier.put((evalResults[i][2][j][0], [evalResults[i][2][j][1], evalResults[i][2][j][2], evalResults[i][2][j][3]]))


            #for j in range(0, len(evalResults[i])):
            #    frontier.put((evalResults[i][j], child))
            #    index += 1

        #end = time.time()
        #print(count)
        #print(end - start)
        gc.collect()
        #for candidate in candidates:
        #    child = node[:] + [candidate] #local

        #    exposed_nodes = set(G.neighbors(candidate) + [candidate]) # local
        #    child_candidates = filter(lambda n: n not in exposed_nodes, candidates[:])
        #    frontier.put((evalResults[index], child))
        #    index += 1


def test(a):
    return sum(a)


def main():
    print("running project.part1.informed_search")
    pool = multiprocessing.Pool(12)

    G = load_data("348.edges.txt")

    #test = [["a", 1], ["f", 0]]
    #new = heapq.nlargest(1, test, key=key_sort)
    #print(new)

    #G = load_data("input2.txt")
    for i in range(1, 8):
        start = time.time()
        #print(i, end=": ")

        solution = a_star_search(G, i, pool)

        print(solution)
        #print(time.time() - start)



    #solution = a_star_search(G, 10)
    #print(solution)

    #total = []
    #for i in range(0, 10):
    #    a = G.neighbors(solution[i])
    #    a.append(solution[i])
    #    b = list(total)
    #    total = list(set(a) | set(b))
    #total.sort()
    #print(total)



if __name__ == '__main__':
    main()
