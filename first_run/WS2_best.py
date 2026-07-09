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
    sum_small = sum(1 for x in partition[i] if x < k // 2)
    penalty = sum_small * 0.5
    return float(size_bonus - penalty)
