"""
Generated from n = 6
NB We actually get a better bound on WS(6) from WS5_best
2:8
3: 22
4: 63
5: 185
6: 550
7: 1606
"""
def priority(i: int, k: int, partition: list[list]) -> float:
  """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition' 
    
      Hint: The sum-free partition will be constructed by assigning 'k' to the set of highest priority 
      that will remain sum-free after the addition of 'k'. As such, the priority function need not check if
      k's addition will immediately make bin i not sum-free.
  """
  """Improved version of `priority_v1`."""
  if not partition[i]:
    return -1.0
  set_i = set(partition[i])
  max_val = max(partition[i])
  # Count conflicts: numbers a and b in set such that a+b=k
  conflicts = sum(1 for a in set_i if (k - a) in set_i and a != k - a)
  # Count numbers that are exactly half of k (potential conflict with itself)
  half_conflicts = 1 if k % 2 == 0 and (k // 2) in set_i else 0
  # Encourage sets with lower max to spread numbers
  max_penalty = max_val * 0.1
  return max_val + 3 * conflicts + half_conflicts - max_penalty