import math


# probability of choosing exactly num_correct_picks out of total_picks attack vectors
def probability(num_correct_picks, total_picks, num_atk_vectors, V):

    # invalid input - at least one more pick will be correct
    if (total_picks - num_correct_picks) + num_atk_vectors > V:
        return 0
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
    # initial payoff
    payoff = num_atk_vectors * B_atk

    # probability of stopping any attack vector
    for i in range(1, min(num_def_vectors, num_atk_vectors) + 1):
        payoff -= i * B_atk * nCr(num_def_vectors, i) * probability(i, num_def_vectors, num_atk_vectors, V)

    # these are dollar amounts, and the floating point roundoff error makes the payoff
    # matrix extremely hard to read (for example 9999.999999999999996 instead of just 1000.00)
    return round(payoff, 2)


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
    V = 100 # constant
    B_atk = 10000 # constant
    C_atk = attacker_cost
    C_def = 100 # constant

    payoff_matrix = []

    # i = attacker, j = defender
    for i in range(1, V + 1):
        payoff_mat_row = []
        for j in range(1, V + 1):
            # attacker, defender (CactusCard)
            payoff = compute_payoff(i, j, V, B_atk)
            payoff = [-C_atk * i + payoff, -C_def * j - payoff]
            payoff_mat_row.append(payoff)
        payoff_matrix.append(payoff_mat_row)

        # this line prints the payoff matrix row by row
        print(payoff_mat_row)

    for i in range(0, V):
        for j in range(0, V):
            if is_nash_equilibrium(i, j, payoff_matrix, V):
                print("Nash Equilibrium at " + str(i+1) + ", " + str(j+1) + ": " + str(payoff_matrix[i][j]))


if __name__ == '__main__':
    # used to test if the Nash Equilibrium method was working correctly
    # matrix = [[[-4, -4], [0, -5]], [[-5, 0], [-1, -1]]] #prisoner's dilemma
    # print(is_nash_equilibrium(0, 0, matrix, 2))
    compute_payoff_matrix(100)  # try some more values of C_atk here