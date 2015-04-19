import networkx as nx


def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


def main():

    G = load_data("348.edges.txt")
    print(G.number_of_nodes())
    b = sum(map(lambda node: len(G.neighbors(node)), G.nodes()))/float(G.number_of_nodes())

    p = G.number_of_nodes()
    total = 1
    for i in range(10):
        total += total*(p - i*b)
    print(b)
    print(total)

if __name__ == '__main__':
    main()
