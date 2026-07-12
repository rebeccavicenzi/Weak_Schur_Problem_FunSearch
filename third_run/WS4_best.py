"""
Obtained while optimizing for n = 4
2: 8
3: 23
4: 66
5: 184
6: 511
7: 1413
"""

def priority(i: int, k: int, partition: list[list]) -> float:
  """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition' 
    
      Hint: The sum-free partition will be constructed by assigning 'k' to the set of highest priority 
      that will remain sum-free after the addition of 'k'. As such, the priority function need not check if
      k's addition will immediately make bin i not sum-free.
  """
  """Improved version of `priority_v2`."""
  if not partition[i]:
    return 0.0
  # Encourage sets with a smaller range and fewer numbers just below k.
  size = len(partition[i])
  max_val = max(partition[i])
  near_penalty = sum(1 for x in partition[i] if k - 10 <= x < k)
  # Prefer sets that already have some structure but not too large near k.
  return float(size + max_val + 3 * near_penalty) / k