"""Finds large weakly sum free partitions, i.e., partitions of 1,2,3,...,k (with k large) into n sets such that a + b = c does not hold for distinct a,b,c in any one set"""

import itertools
import numpy as np
from decimal import Decimal, getcontext
getcontext().prec = 50

default_score = {5: 124, 4: 43, 6: 367, 7: 1096}
target_score = {5: 196, 4: 66, 6: 646, 7: 2146}
def evaluate(n) -> int:
    """Returns the number of integers in a partition"""
    partition = solve(n)
    score = 0
    for tup in partition:
        for num in tup:
            score += 1 
    if score == default_score[n]: # meant to punish programs that are identical to the default
        return 0 
    if score >= target_score[n]:
        print(partition)
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
            chosen_index = prio_to_bin(priorities)
            if sum_free_addition(partition[chosen_index], curr_int):
                partition[chosen_index].append(curr_int)
                # If we succesfully place a number in a set, we set all other priorities for that number to -inf
                Failed = False
                break
            else:
                # Deals with prohibited number/bin combination.
                priorities[chosen_index] = -np.inf
        curr_int += 1 
        if counter1 > 2500:
            break
    return partition

def priority(i: int, k: int, partition: list) -> float:
    """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition.' 
        When constructing the weakly sum-free partition, 'k' will be added to higher priority sets if possible. 
    """
    set_max = max(partition[i]) if partition[i] else 0
    arr = np.array(partition[i])
    window_count = np.sum(np.abs(arr - k/2) <= 2)
    conflict_penalty = np.sum(np.isin(arr[:, None] + arr, k)) * (k ** 0.48) / 2.9
    near_k = np.sum(arr >= k - 11) * np.exp(0.02 * (k - arr.min())) if arr.size > 0 else 0
    diversity_bonus = np.std(arr) * 0.17 if arr.size > 2 else 0
    return 1 * float(set_max) + 3 * window_count - 2.5 * conflict_penalty + 0.95 * near_k + 1 * diversity_bonus

def prio_to_bin(priorities):
    """Stochastically picks a bin based on the priority function"""
    weights = []
    for prio in priorities:
        """
        Our choice of function here determines how often we stray from the 'canonical' highest priority decision.
        Exponential functions are nice because they naturally sort out the messiness of negative priorities. 
        """
        # if prio <= 0:
        #     weights.append(Decimal(0.01))
        # else:
            # weights.append(Decimal(prio))
            # weights.append(Decimal(prio) ** 2)
        weights.append(Decimal('3.5') ** Decimal(prio)) 
         # weights.append(Decimal(prio) ** Decimal(1.1))
    sum = Decimal(0) 
    for weight in weights:
        sum += weight
    for i, weight in enumerate(weights):
        if sum != 0:
            weights[i] = weight/sum 
    if sum == 0: 
        return 0
    else: 
        return np.random.choice(a=len(weights), p=weights)  

max_WS = 0
iterations = 10000
for i in range(iterations):
    curr_score = evaluate(5)
    if curr_score > max_WS:
        max_WS = curr_score
    if i % (iterations//100) == 0:
        print(max_WS)