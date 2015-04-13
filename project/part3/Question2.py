import random


def simulate_mucm(cost, atk_vectors, def_vectors):
    V = 100
    B_atk = 10000
    C_atk = cost
    C_def = 100
    X_atk = atk_vectors
    X_def = def_vectors

    #simulates the game k times
    k = 10000
    mean_attacker_payoff = 0
    mean_defender_payoff = 0
    for a in range(0, k):
        atk_vectors = []
        def_vectors = []

        for i in range(0, 100):
            atk_vectors.append(i)
            def_vectors.append(i)

        current_atk_vectors = []
        current_def_vectors = []

        # attacker chooses X_atk random attack vectors
        for i in range(0, X_atk):
            chosen_atk_v_index = int(random.random()*len(atk_vectors))
            current_atk_vectors.append(atk_vectors[chosen_atk_v_index])
            atk_vectors.remove(atk_vectors[chosen_atk_v_index])

        # defender chooses X_def random defense vectors
        for i in range(0, X_def):
            chosen_def_v_index = int(random.random()*len(def_vectors))
            current_def_vectors.append(def_vectors[chosen_def_v_index])
            def_vectors.remove(def_vectors[chosen_def_v_index])

        succ_atks = len(set(current_atk_vectors).difference(set(current_def_vectors)))

        mean_attacker_payoff += B_atk * succ_atks - C_atk * X_atk
        mean_defender_payoff += -B_atk * succ_atks - C_def * X_def

        #print("done iteration " + str(k))

        #print("Successful Attacks:  " + str(successful_atks))
        #print("Successful Defenses: " + str(N - successful_atks))
        #print("Attacker Payoff:     " + str(P_atk))
        #print("CactusCard Payoff:   " + str(P_def))

    mean_attacker_payoff = float(mean_attacker_payoff) / float(k)
    mean_defender_payoff = float(mean_defender_payoff) / float(k)

    print(mean_attacker_payoff)
    print(mean_defender_payoff)


if __name__ == '__main__':
    simulate_mucm(10000, 1, 1)