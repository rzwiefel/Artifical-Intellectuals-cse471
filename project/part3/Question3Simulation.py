import random

if __name__ == '__main__':
    V = 100
    C_atk = 100
    C_def = 100
    N = 500
    M_atk = 5
    M_def = 5

    P_def = 0
    P_atk = 0

    S_atk = 1.0
    S_def = 1.0

    #simulates the game k times
    k = 100
    mean_attacker_payoff = 0
    mean_defender_payoff = 0
    for k in range(0, k):
        atk_vectors = []
        def_vectors = []
        M_atk_vectors = []
        M_def_vectors = []
        for i in range(0, 100):
            atk_vectors.append(i)
            def_vectors.append(i)

        current_atk_v = -1
        current_def_v = -1

        successful_atks = 0
        for i in range(0, N):
            #Attacker chooses attack vector
            if i < M_atk:
                current_atk_v = atk_vectors[int(random.random()*len(atk_vectors))]
                M_atk_vectors.append(current_atk_v)

            else:
                prob = random.random()
                if prob <= S_atk:
                    chosen_index = int(random.random()*len(M_atk_vectors))
                    current_atk_v = M_atk_vectors[chosen_index]
                    M_atk_vectors.pop(0)
                    M_atk_vectors.append(current_atk_v)
                else:
                    remaining_atk_vectors = list(atk_vectors)
                    for j in range(0, len(M_atk_vectors)):
                        if M_atk_vectors[j] in remaining_atk_vectors:
                            remaining_atk_vectors.remove(M_atk_vectors[j])

                    current_atk_v = remaining_atk_vectors[int(random.random()*len(remaining_atk_vectors))]
                    M_atk_vectors.pop(0)
                    M_atk_vectors.append(current_atk_v)

            #Defender chooses defense vector
            if i < M_def:
                current_def_v = int(random.random()*len(def_vectors))
                M_def_vectors.append(current_def_v)

            else:
                prob = random.random()
                if prob <= S_def:
                    chosen_index = int(random.random()*len(M_def_vectors))
                    current_def_v = M_def_vectors[chosen_index]
                    M_def_vectors.pop(0)
                    M_def_vectors.append(current_def_v)
                else:
                    remaining_def_vectors = list(def_vectors)
                    for j in range(0, len(M_def_vectors)):
                        if M_def_vectors[j] in remaining_def_vectors:
                            remaining_def_vectors.remove(M_def_vectors[j])

                    current_def_v = remaining_def_vectors[int(random.random()*len(remaining_def_vectors))]
                    M_def_vectors.pop(0)
                    M_def_vectors.append(current_def_v)

            #See if attack was successful or not
            if current_atk_v == current_def_v: #successful defense
                P_atk += -C_atk
                P_def += -C_def
            else: #successful attack
                successful_atks += 1
                P_atk += 10000 - C_atk
                P_def += -10000 - C_def

        mean_attacker_payoff += P_atk
        mean_defender_payoff += P_def

        #print("done iteration " + str(k))

        #print("Successful Attacks:  " + str(successful_atks))
        #print("Successful Defenses: " + str(N - successful_atks))
        #print("Attacker Payoff:     " + str(P_atk))
        #print("CactusCard Payoff:   " + str(P_def))

    mean_attacker_payoff = float(mean_attacker_payoff) / float(k)
    mean_defender_payoff = float(mean_defender_payoff) / float(k)

    print(mean_attacker_payoff)
    print(mean_defender_payoff)