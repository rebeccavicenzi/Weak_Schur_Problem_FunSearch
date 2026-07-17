### SYSTEM PROMPT 
r"""You are a state-of-the-art python code completion system that will be used as part of a genetic algorithm to create weakly-sum-free templates.
You will be given a list of functions, and you should improve the incomplete last function in the list.
1. Make only incremental changes but be sure to make some change.
2. Try to keep the code concise and any comments concise.
3. Your response should be an implementation of the function function_to_evolve_v# (where # is the current iteration number); do not include any examples or extraneous functions.
4. You may use numpy and itertools.
The code you generate will be appended to the user prompt and run as a python program.
Some useful background: 
A $b$-weakly-sum-free with width $a$ and $n$ colors is a partition of the integers 1 through $a+b$ into $n$ sets where
1. Each set $A_i$ is weakly sum free i.e. for all distinct $a,b \in A_i$ we have $a + b \not \in A_i$.
2. For each $A_i$, taking away the integers 1 through $b$ from $A_i$ (denoted $A_i \setminus \mathbb [1, b \mathbb ]$) leaves $A_i$ STRICTLY sum free i.e. $a,b \in A_i \setminus \mathbb [1, b\mathbb ]$ implies $a+b \not \in A_i$
3. For some special set $A_n$, we have that $$\forall x,y \in A_n, x+y > b + 2a \implies x + y - 2a \not \in A_n$$
4. For the other sets, $A_i$ with $i \neq n$, we have that for all $x,y \in A_i$, $$x+y > a + b \implies x \text{mod} a + a * \mathbb 1_{\mathbb [1, b \mathbb ]} (x \text{mod} a) \not \in A_i$$
Your goal is to code a priority function determines which integeres should be placed in which set to create a b-WS template that maximizes the quantity (13 * a) + b
Auxillary code you do not have access to will take the priority function you code and ensure it creates some valid WS-template. 
"""
### END SYSTEM PROMPT
"""Finds weakly sum-free templates with the aim of improving bounds on WS(n).
Important note: some parameters (such as the n we're aiming to get a bound for) are hard coded. This needs to be fixed at somepoint"""

import copy
import itertools
import numpy as np
import funsearch

def part_size(partition):
    """returns the number of elements in a partition"""
    elts = 0 
    for int_set in partition:
        for _ in int_set:
            elts += 1
    return elts

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

def mostly_sum_free(int_set, b):
    """checks if 'int_set,' with the integers 1 through b removed, is (strongly) sum free"""
    int_set = copy.deepcopy(int_set)
    int_set = [elt for elt in int_set if elt > b]
    for elt1 in int_set:
        for elt2 in int_set:
            if elt1 + elt2 in int_set:
                return False
    return True

def pop_partition(partition):
    """Removes largest number from a partition"""
    to_remove = part_size(partition)
    for int_set in partition:
        if to_remove in int_set:
            int_set.remove(to_remove)
    return partition

def pi(a,b,x):
    """pi projection defined in Ageron et al."""
    total = x % a 
    if (x % a) <= b: 
        total += a 
    return total 

def is_template(partition, b):
    """Checks if the (assumed weakly sum-free) partition provided is a b-WS template"""
    a = part_size(partition) - b
    for int_set in partition: 
        if not mostly_sum_free(int_set,b):
            return False
    for int_set1 in partition:
        spcl_cdtn_flag = True
        for x in int_set1:
            for y in int_set1:
                if x + y  > b + 2 * a and int(x + y - 2 * a) in int_set1:
                    spcl_cdtn_flag = False
        if not spcl_cdtn_flag:
            continue

        for int_set2 in partition:
            if int_set2 != int_set1:
                for xp in int_set2:
                    for yp in int_set2:
                        if (xp + yp) > (a + b) and pi(a, b, (xp + yp)) in int_set2:
                            spcl_cdtn_flag = False
        if spcl_cdtn_flag:
            return True
    return False

def template_to_bound(template, num_bins):
    """Employs Thm 3.17 to convert b-WS template to bound on WS('num_bins')"""
    schur_number = {1: 1, 2: 4, 3: 13, 4: 44, 5: 160, 6: 536, 7: 1696, 8: 5286}
    partition, b = template
    a = part_size(partition) - b
    k = num_bins - (len(partition) - 1)
    return schur_number[k] * a + b

def best_template(partition):
    """Finds WS template within 'partition' that gives the best bound on WS(k + n)"""
    partition_log = [([[]], 0)]
    partition = copy.deepcopy(partition)
    while part_size(partition) > 0:
        b = 1 
        while b < part_size(partition) - 1:
            if is_template(partition, b):
                partition_log.append((copy.deepcopy(partition), b))
            b += 1
        partition = pop_partition(partition)
    max = 0
    max_template = ([[]], 0)
    for template in partition_log:
        if template_to_bound(template, 6) > max:                                     
            max = template_to_bound(template, 6)
            max_template = template
    return max_template

@funsearch.run
def evaluate(n) -> int:
    """Returns the number of integers in a partition"""
    default_score = {5: 0, 4: 125, 6: 0, 7: 0, 3: 0}
    partition = solve(n)
    template = best_template(partition)
    score = template_to_bound(template, 6)
    if score == default_score[n]: # meant to punish programs that are identical to the default
        return 0 
    return score

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
    """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition.' 
    When constructing the b-WS template, 'k' will be added to higher priority sets if possible. 
    """
    return 0.0

