"""
evolved form n = 2
n = 2
score 8 
partition [[1, 2, 4, 8], [3, 5, 6, 7]]

n = 3 
score 21
partition [[1, 2, 4, 8, 11, 21], [3, 5, 6, 7, 19], [9, 10, 12, 13, 14, 15, 16, 17, 18, 20]]
"""
def priority(i: int, k: int, partition: list[list]) -> float:
    """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition' 
    
        Hint: The sum-free partition will be constructed by assigning 'k' to the set of highest priority 
        that will remain sum-free after the addition of 'k'. As such, the priority function need not check if
        k's addition will immediately make bin i not sum-free.
    """
    """Improved version of `priority_v0`."""
    # Prefer larger sets, but penalize sets that already contain many
    # small numbers (which can cause conflicts with future large k).
    size_bonus = len(partition[i])
    print(f"Size bonus for set {i} is {size_bonus}.")
    sum_small = sum(1 for x in partition[i] if x < k // 2)
    penalty = sum_small * 0.5
    print(f"Penalty for set {i} is {penalty}.")
    return float(size_bonus - penalty)
"""
Say we're trying to find large partitions into two sets and
we have a partition of 5 numbers into two sets stored as a list of lists:
"""
partition = [[1,2], [3,4,5]]
"""
Our goal is to add 6 to this partition.Our solve algorithm (found in WS_perfect_info_float_spec.py) 
will accomplish this by calling the priority function on 6 for each set (or more precisely, for
each set index 0 and 1)
"""
print(f"priority for bin 0 is {priority(0, 6, partition)}")
print(f"priority for bin 1 is {priority(1, 6, partition)}")
"""
The priority of bin 0 is 1.0 while the priority of bin 1 is 3.0.
Because of this, we'd try to add 6 to bin 1 first. Our solve algorithm would check that adding
6 maintains bin 1's sum-freeness. Once this is verified, 6 will be added to set 1. 
"""