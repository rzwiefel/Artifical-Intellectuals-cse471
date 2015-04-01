import math


def probability(num_correct_picks, total_picks, num_atk_vectors, V):
    prob = 1
    for i in range(0, num_correct_picks):
        prob *= float(num_atk_vectors)/float(V)
        num_atk_vectors -= 1
        V -= 1

    for i in range(num_correct_picks, total_picks):
        prob *= float(V - num_atk_vectors)/float(V)
        V -= 1
    return prob


def nCr(n, r):
    return math.factorial(n)/(math.factorial(r) * math.factorial(n - r))


def compute_payoff(num_atk_vectors, num_def_vectors, V, B_atk):
    payoff = 0

    for i in range(0, num_def_vectors):
        payoff += nCr(num_def_vectors, i) * probability(i, num_def_vectors, num_atk_vectors, V) * (num_atk_vectors - i) * B_atk

    return payoff


def is_nash_equilibrium(iIndex, jIndex, payoff_matrix, V):
    result = True
    current_atk_payoff = payoff_matrix[iIndex][jIndex][0]
    current_def_payoff = payoff_matrix[iIndex][jIndex][1]
    for i in range(0, V):
        if i != iIndex and payoff_matrix[i][jIndex][0] > current_atk_payoff:
            result = False
    for j in range(0, V):
        if j != jIndex and payoff_matrix[iIndex][j][1] > current_def_payoff:
            result = False
    return result


def compute_payoff_matrix(attacker_cost):
    V = 100 #constant
    B_atk = 10000 #constant
    C_atk = attacker_cost
    C_def = 100 #constant

    payoff_matrix = []

    #i = attacker, j = defender
    for i in range(1, V + 1):
        payoff_mat_row = []
        for j in range(1, V + 1):
            #attacker, defender (CactusCard)
            payoff = compute_payoff(i, j, V, B_atk)
            if i == 1 and j == 2:
                print(payoff)
            payoff = [-C_atk * i + payoff, -C_def * j - payoff]
            payoff_mat_row.append(payoff)
        payoff_matrix.append(payoff_mat_row)
        #uncomment this line to see the payoff matrix row by row
        print(payoff_mat_row)

    for i in range(0, V):
        for j in range(0, V):
            if is_nash_equilibrium(i, j, payoff_matrix, V):
                print("Nash Equilibrium at " + str(i) + ", " + str(j) + ": " + str(payoff_matrix[i][j]))


if __name__ == '__main__':
    #matrix = [[[-4, -4], [0, -5]], [[-5, 0], [-1, -1]]] #prisoner's dilemma
    #print(is_nash_equilibrium(0, 0, matrix, 2))
    compute_payoff_matrix(5000) #try some more values of C_atk here
