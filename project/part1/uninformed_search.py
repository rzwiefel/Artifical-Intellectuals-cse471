# Project, Part 1, Uninformed Search

from networkx import nx
# import matplotlib.pyplot as plt
from queue import PriorityQueue
import time


# MAX_CARDS = 1


def load_data():
    G = nx.Graph()
    with open("input.txt", "r") as f:
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


# running in about T(n, c) = .009 * n^(c - 1) where n of friendships and c is the number of cards given out
def uniform_cost_search(G, num_cards):
    frontier = PriorityQueue()

    count = 0
    frontier.put((0, []))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        cost, node = frontier.get()

        candidates = card_candidates(G, node)
        if goal_test(G, node, num_cards, candidates):
            print("Nodes expanded: " + str(count))
            return node

        count += 1
        for candidate in candidates:
            child = node[:] + [candidate]
            frontier.put((path_cost(G, child), child))


def main():
    print("running project.part1.uninformed_search")


    G = load_data()
    for i in range(1, 4):
        start = time.time()

        solution = uniform_cost_search(G, i)

        print(solution)
        print("Time: " + str(time.time() - start))
        print()

if __name__ == '__main__':
    main()
