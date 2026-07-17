### SYSTEM PROMPT 
"""You are a state-of-the-art python code completion system that will be used as part of a genetic algorithm to create very large weakly sum free partitions.
Weakly sum free partitions are partitions of 1,2,3,...,k (with k as large as possible) into n sets such that a + b = c does not hold for distinct a,b,c in any one set.

You will be given a list of functions, and you should improve the incomplete last function in the list.
1. Make only incremental changes but be sure to make some change.
2. Try to keep the code concise and any comments concise.
3. Your response should be an implementation of the function function_to_evolve_v# (where # is the current iteration number); do not include any examples or extraneous functions.
4. You may use numpy and itertools.
The code you generate will be appended to the user prompt and run as a python program."""
### END SYSTEM PROMPT
"""Finds large weakly sum free partitions, i.e., partitions of 1,2,3,...,k (with k large) into n sets such that a + b = c does not hold for distinct a,b,c in any one set"""

import itertools
import numpy as np
import funsearch
default_score = {5: 124, 4: 43, 6: 367, 7: 1096}
@funsearch.run
def evaluate(n) -> int:
    """Returns the number of integers in a partition"""
    partition = solve(n)
    score = 0
    for tup in partition:
        for num in tup:
            score += 1 
    if score == default_score[n]: # meant to punish programs that are identical to the default
        return 0 
    return score

def sum_free_addition(curr_set: list, curr_int: int) -> bool: 
    """Tests whether 'curr_set' will remain sum-free if 'curr_int' is added to it"""
    for term1 in curr_set:
        for term2 in curr_set:
            # Case 1: curr int is the sum
            if term1 != term2 and term1 + term2 == curr_int:
                return False
            # Case 2: curr int is a term
            if term1 + curr_int == term2:
                return False
    return True

def solve(n: int) -> np.ndarray: 
    """Creates a sum free partition into 'n' sets."""
    partition = []
    for _ in range(n):
        partition.append([])
    Failed = False
    curr_int = 1
    # Build partition greedily, using priorities for prioritization.
    counter1 = 0
    while not Failed:
        counter1 += 1
        priorities = np.array([priority(i, curr_int, partition) for i in range(n)],dtype=float)
        # Prevents LLM from cheating by "skipping" a number
        for prio in priorities:
            if prio == -np.inf:
                return [[]]
        while np.any(priorities != -np.inf):
            Failed = True
            max_index = np.argmax(priorities)
            if sum_free_addition(partition[max_index], curr_int):
                partition[max_index].append(curr_int)
                # If we succesfully place a number in a set, we set all other priorities for that number to -inf
                Failed = False
                break
            else:
                # Deals with prohibited number/bin combination.
                priorities[max_index] = -np.inf
        curr_int += 1 
        if counter1 > 2500:
            break
    return partition

@funsearch.evolve
def priority(i: int, k: int, partition: list[list]) -> float:
    """
    Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition.' 
    When constructing the weakly sum-free partition, 'k' will be added to higher priority sets if possible. 
    
    (Hint) Some ideas that may work well:
    1. A priority function that leans towards sets with larger max elements
    2. A priority function that leans towards sets with more numbers closer to k
    If all these ideas are already implemented, don't be afraid to try something new and creative!
    """
    return 0.0