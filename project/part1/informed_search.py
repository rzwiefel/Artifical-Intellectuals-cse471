# Project, Part 1, Informed Search

from networkx import nx
import heapq
# import matplotlib.pyplot as plt
from queue import PriorityQueue
import time


# MAX_CARDS = 1


def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


def exposed_graph(G, node):
    H = nx.Graph()
    for i in node:
        H.add_edges_from([(i, n) for n in G.neighbors(i)])

    return H


def path_cost(G, node):
    population = G.number_of_nodes()

    cost = 0
    unexposed_people = G.copy()
    for i, person in enumerate(node):
        n_exposed = G.number_of_nodes() - unexposed_people.number_of_nodes()
        n_given_card = i

        new_exposed_people = unexposed_people.neighbors(person)
        new_exposed = len(new_exposed_people)

        adoption_probability = max(.1, 1 - 1 / (n_exposed + n_given_card)) if n_exposed + n_given_card != 0 else .1
        cost += population - 1 - new_exposed * adoption_probability

        unexposed_people.remove_nodes_from(new_exposed_people)
        unexposed_people.remove_node(person)

    return cost


def heuristic_function(G, node, max_cards, candidates=None):
    candidates = card_candidates(G, node) if candidates is None else candidates
    cards_remaining = max_cards - len(node)

    return G.number_of_nodes() * cards_remaining - cards_remaining - sum(heapq.nlargest(cards_remaining, G.degree(candidates).values()))


def evaluation_function(G, node, max_cards, candidates=None):
    return heuristic_function(G, node, max_cards, candidates) + path_cost(G, node)


def card_candidates(G, node):
    H = exposed_graph(G, node)
    I = G.copy()
    I.remove_nodes_from(H)
    return I.nodes()


def goal_test(G, node, max_cards, candidates=None):
    if len(node) == max_cards:
        return True

    if candidates is None:
        candidates = card_candidates(G, node)
    return len(candidates) == 0


def a_star_search(G, num_cards):
    frontier = PriorityQueue()

    count = 0
    frontier.put((0, []))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        cost, node = frontier.get()

        candidates = card_candidates(G, node)
        if goal_test(G, node, num_cards, candidates):
            print(count, end=" ")
            return node

        count += 1
        # print("\nnum candidates: " + str(len(candidates)))
        for candidate in candidates:
            child = node[:] + [candidate]

            exposed_nodes = set(G.neighbors(candidate) + [candidate])
            child_candidates = filter(lambda n: n not in exposed_nodes, candidates[:])
            frontier.put((evaluation_function(G, child, num_cards, child_candidates), child))


def main():
    print("running project.part1.informed_search")


    G = load_data("348.edges.txt")
    for i in range(1, 11):
        start = time.time()
        print(i, end=": ")
        a_star_search(G, i)

        # print(solution)
        print(time.time() - start)

if __name__ == '__main__':
    main()
