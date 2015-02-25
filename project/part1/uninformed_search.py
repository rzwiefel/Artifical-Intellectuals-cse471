# Project, Part 1, Uninformed Search

from networkx import nx
# import matplotlib.pyplot as plt
from queue import PriorityQueue
import time


MAX_CARDS = 10


def load_data():
    G = nx.Graph()
    with open("348.edges.txt", "r") as f:
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
    exposed_people = nx.Graph()
    for i, person in enumerate(node):
        n_exposed = exposed_people.number_of_nodes()
        n_given_card = i

        new_exposed_people = G.neighbors(person)
        new_exposed = len(new_exposed_people)

        adoption_probability = max(.1, 1 - 1 / (n_exposed + n_given_card)) if n_exposed + n_given_card != 0 else .1
        cost += population - 1 - new_exposed * adoption_probability

        exposed_people.add_nodes_from(new_exposed_people)

    return cost


def card_candidates(G, node):
    H = exposed_graph(G, node)
    I = G.copy()
    I.remove_nodes_from(H)
    return I.nodes()


def goal_test(G, node):
    if len(node) == MAX_CARDS:
        return True

    return len(card_candidates(G, node)) == 0


def uniform_cost_search(G):
    frontier = PriorityQueue()

    frontier.put((0, []))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        cost, node = frontier.get()
        if goal_test(G, node):
            return node

        for candidate in card_candidates(G, node):
            child = node[:] + [candidate]
            frontier.put((path_cost(G, child), child))


def main():
    print("running project.part1.uninformed_search")

    start = time.time()

    G = load_data()
    solution = uniform_cost_search(G)
    print(solution)
    print("Time: " + str(time.time() - start))

if __name__ == '__main__':
    main()
