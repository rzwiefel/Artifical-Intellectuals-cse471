from networkx import nx


def exposed_graph(G, node): #returns graph of exposed people
    H = nx.Graph()
    for i in node:
        H.add_edges_from([(i, n) for n in G.neighbors(i)])

    return H


def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


if __name__ == '__main__':
    G = load_data("348.edges.txt")
    # set solution here
    solution = []
    valid = True
    previous_exposed_graph = nx.Graph()

    for i in range(0, len(solution)):
        if solution[i] in list(previous_exposed_graph):
            valid = False
            break
        previous_exposed_graph = exposed_graph(G, solution[0:i+1])

    print(valid)