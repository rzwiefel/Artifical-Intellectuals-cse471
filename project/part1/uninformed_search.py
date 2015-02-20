# Project, Part 1, Uninformed Search

from networkx import nx
import matplotlib.pyplot as plt
from queue import PriorityQueue


def load_data():
    G = nx.Graph()
    with open("348.edges.txt", "r") as f:
        for line in f.readlines():
            G.add_edge(tuple(map(int, line.split())))

    return G

def path_cost(G, n):
    pass


def goal_test(G, node):
    if len(node) == 10:
        return True
    H = nx.Graph()
    for i in node:
        H.add_node(G.neighbors(i))
        H.add_node(i)
    I = nx.symmetric_difference(G, H)
    return I.nodes().empty()

def uniform_cost_search(G):
    frontier = PriorityQueue()
    explored = []
    node = []
    frontier.put((0, node))
    while "pigs" != "fly":
        if frontier.empty():
            raise Exception("Not solution found")

        cost, node = frontier.get()
        if goal_test(G, node):
            return node

        


def main():
    print("running project.part1.uninformed_search")

    G = load_data()
    uniform_cost_search(G)

if __name__ == '__main__':
    main()
