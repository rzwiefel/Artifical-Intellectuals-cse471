# Homework 1 -- Chapter 3, Question 9
# 3 Missionaries and 3 Cannibals
import operator
from pprint import pprint

# (Missionaries, Cannibals, Boat on this side)
start_state = (3, 3, True)
goal_state = (0, 0, False)

actions = ((1, 1), (2, 0), (0, 2), (1, 0), (0, 1))

def valid(state):
    return all((0 <= state[0] <= 3,     # Must be valid number of missionaries
            0 <= state[1] <= 3,         # Must be valid number of cannibals
            (state[0] >= state[1] or state[0] == 0),    # Must be equal or more M's than C's or no M's (left side)
            (state[0] <= state[1] or state[0] == 3)))   # The other side must follow same conditions

def dfs(state, seen):
    if state in seen:  # Check if we've seen this state already
        return []
    if not valid(state):
        return []
    if goal_state == state:
        return [state]
    seen.append(state)  # Add current state to seen list
    op = operator.sub if state[2] else operator.add  # Choose the operator based on if the boat is here
    for action in actions:  # iterate  through each of the actions
        res = dfs((op(state[0], action[0]), op(state[1], action[1]), not state[2]), seen)
        if res:
            return [state] + res


if __name__ == '__main__':
    print("running hw1.c3.p9")
    seen_states = []
    result = dfs(start_state, seen_states)
    print("Result:")
    pprint(result)
