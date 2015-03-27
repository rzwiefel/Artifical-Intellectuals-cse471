import networkx as nx
import time
import random
import multiprocessing
import functools


lock = multiprocessing.Lock()


def load_data(file):
    G = nx.Graph()
    with open(file, "r") as f:
        for line in f.readlines():
            G.add_edge(*tuple(map(int, line.split())))

    return G


def fitness_function(G, node):
    fitness = 0
    unexposed_people = G.copy()
    for i, person in enumerate(node):
        if person not in unexposed_people.nodes():
            continue

        n_exposed = G.number_of_nodes() - unexposed_people.number_of_nodes()
        n_given_card = i

        new_exposed_people = unexposed_people.neighbors(person)
        new_exposed = len(new_exposed_people)

        adoption_probability = max(.1, 1 - 1 / (n_exposed + n_given_card)) if n_exposed + n_given_card != 0 else .1
        fitness += 1 + new_exposed * adoption_probability

        unexposed_people.remove_nodes_from(new_exposed_people)
        unexposed_people.remove_node(person)

    return fitness


def crossover_function(node1, node2):
    crossover_point = random.randint(1, len(node1))
    return node1[:crossover_point] + node2[crossover_point:], node2[:crossover_point] + node1[crossover_point:]


def mutate(G, node):
    rand_index = random.randint(0, len(node) - 1)
    random_person = rand_person(G)
    if random_person not in node:
        node[rand_index] = random_person
    else:
        mutate(G, node)


def reproduction_probability_distribution(fitnesses):
    fitness_sum = sum(fitnesses)
    return [fitness / fitness_sum for fitness in fitnesses]


def get_reproduction_candidate(repro_prob_dist, exclude=None):
    max_prob = 1
    if exclude is not None:
        repro_prob_dist = repro_prob_dist[:]
        max_prob -= repro_prob_dist.pop(exclude)

    rand = random.random() * max_prob

    prob_sum = 0
    for i, prob in enumerate(repro_prob_dist):
        prob_sum += prob
        if rand < prob_sum:
            return i


def rand_person(G):
    return G.nodes()[random.randint(0, G.number_of_nodes() - 1)]


def rand_node(G, size):
    node = []
    if size > G.number_of_nodes():
        print("There aren't enough people for that stupid")
        quit()

    while len(node) < size:
        random_person = rand_person(G)
        if random_person not in node:
            node.append(random_person)

    return node


def worker(G, population, repro_prob, mutation_prob, i):
    node1_index = get_reproduction_candidate(repro_prob)
    node2_index = get_reproduction_candidate(repro_prob, node1_index)
    child_node1, child_node2 = crossover_function(population[node1_index], population[node2_index])

    if random.random() < mutation_prob:
        # print("Mutation")
        mutate(G, child_node1)
    if random.random() < mutation_prob:
        # print("Mutation")
        mutate(G, child_node2)

    return child_node1, child_node2


def mt_fitness(args):
    return fitness_function(*args)


def genetic_algorithm(G, n, k, iterations, mutation_prob):
    population = [rand_node(G, n) for i in range(k)]

    max_fitness = 0
    max_fitness_node = []

    with multiprocessing.Pool() as pool:
        for i in range(iterations):
            # start = time.time()
            fitnesses = list(pool.map(mt_fitness, [(G, node) for node in population]))

            if i % 1000 == 0:
                print("Fitness {!s}: avg: {!s}, min: {!s}, max: {!s}".format(i, sum(fitnesses) / k, min(fitnesses), max(fitnesses)))

            current_max_fitness = max(fitnesses)
            if max_fitness < current_max_fitness:
                max_fitness = current_max_fitness
                max_fitness_node = population[fitnesses.index(max_fitness)]
                print("New max: " + str(max_fitness))

            repro_prob = reproduction_probability_distribution(fitnesses)

            new_pop_func = functools.partial(worker, G, population, repro_prob, mutation_prob)
            population = list(pool.map(new_pop_func, [i for i in range(len(population) // 2)]))
            population = functools.reduce(lambda x, y: x + [i for i in y], population, [])
            # print(time.time() - start)

    return max_fitness, max_fitness_node


if __name__ == '__main__':
    print("running project.part1.genetic")

    G = load_data("348.edges.txt")
    # for i in range(2, 7, 2):
    # start = time.time()
    # print(i, end=": ")
    print(genetic_algorithm(G, 7, 8, 1000, .05))

    # print(solution)
    # print(time.time() - start)
