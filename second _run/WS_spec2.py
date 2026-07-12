### SYSTEM PROMPT 
"""You are a state-of-the-art python code completion system that will be used as part of a genetic algorithm to evolve sum free partitions.
You will be given a list of functions, and you should improve the incomplete last function in the list.
1. Make only small changes but be sure to make some change.
2. Try to keep the code short and any comments concise.
3. Your response should be an implementation of the function function_to_evolve_v# (where # is the current iteration number); do not include any examples or extraneous functions.
4. You may use numpy and itertools.
The code you generate will be appended to the user prompt and run as a python program."""
### END SYSTEM PROMPT
"""Finds large weakly sum free partitions, i.e., partitions of 1,2,3,...,k (with k large) into n sets such that a + b = c does not hold for distinct a,b,c in any one set"""

import itertools
import numpy as np
import funsearch

"""
Hard coded dictionary of targets for each n. If WS(n) is known then that is used. Otherwise
uses 1 above the best known lower bound.
"""
target_dict = {2: 8, 3: 23, 4: 66, 5: 197, 6: 647, 7: 2147, 8: 6977}
@funsearch.run
def evaluate(n) -> int:
    """Returns the negative of the number of integers missing from the partition"""
    target = target_dict[n]
    partition = solve(n, target)
    score = 0
    for bin in partition:
        for _ in bin:
            score += 1
    return score - target 

def sum_free_addition(curr_set, curr_int: int) -> bool: 
    """Checks if adding curr_int to a sum-free curr_set will result in a sum-free set"""
    for term1 in curr_set:
        for term2 in curr_set:
            if term1 != term2 and term1 + term2 == curr_int:
                return False
            if term1 + curr_int == term2:
                return False
    return True

def solve(n: int, target: int) -> np.ndarray: 
    """Attempts to create a sum free partition of the integers 1 through 'target' into 'n' sets."""
    # Note: verify this code creates a multi-dimensional array and not an array of pointers
    partition = []
    for _ in range(n):
        partition.append([])
    priorities = np.array([np.asarray(priority(n, schur_int, partition)) for schur_int in range(1, target)],dtype=float)
    bad_indices = set()
    Failed = False
    # Build partition greedily, using priorities for prioritization.
    while not Failed:
        priorities = np.array([np.asarray(priority(n, schur_int, partition)) for schur_int in range(1, target)],dtype=float)
        for index in bad_indices:
            priorities[index] = -np.inf
        Failed = True
        while np.any(priorities != -np.inf):
            # Add an integer with maximum priority to the appropriate bin.  
            max_index = np.unravel_index(np.argmax(priorities), priorities.shape)
            curr_int = max_index[0] + 1 
            curr_set = partition[max_index[1]]
            if sum_free_addition(curr_set, curr_int):
                partition[max_index[1]].append(curr_int)
                # Prevents a number being added to multiple sets.
                for i in range(n):
                    bad_indices.add((max_index[0], i))
                break
            else:
                priorities[max_index[0]][max_index[1]] = -np.inf
                bad_indices.add(max_index)
    return partition

@funsearch.evolve
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """
  Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
  The ith element in the output tuple is the priority of placing 'k' into the set with index i
  The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
  at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i. 
  """
  return [0.0 for x in range(n)]
