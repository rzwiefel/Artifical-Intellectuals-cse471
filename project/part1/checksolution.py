from networkx import nx
import genetic


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


def is_valid(solution, G):
    valid = True
    previous_exposed_graph = nx.Graph()

    for i in range(0, len(solution)):
        if solution[i] in previous_exposed_graph.nodes():
            print(solution[i])
            valid = False
            break
        previous_exposed_graph = exposed_graph(G, solution[0:i+1])

    return valid


def check_fitness(solution, G):
    print(genetic.fitness_function(G, solution))


if __name__ == '__main__':
    G = load_data("348.edges.txt")
    # for checking a list of solutions
    # with open("geneticout.txt") as f:
    #    solutions = []
    #    for line in f.readlines():
    #        solutions.append(list(map(int, line.split(".")[2].strip().split(" "))))
    #    print(filter(is_valid, solutions))
    #    print(map(lambda node: genetic.fitness_function(G, node), filter(is_valid, solutions)))


    # set solution here
    solution = [382, 534, 464, 362, 532, 198, 504, 369, 493, 376]
    # prints if solution is valid and its fitness
    print(is_valid(solution, G))
    check_fitness(solution, G)