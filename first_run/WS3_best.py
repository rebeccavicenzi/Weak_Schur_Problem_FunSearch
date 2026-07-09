"""
evolved from n = 3
n = 3
score 23 
partition: [[1, 2, 4, 8, 11, 22], [3, 5, 6, 7, 19, 21, 23], [9, 10, 12, 13, 14, 15, 16, 17, 18, 20]]

n = 2
score 8
partition: [[1, 2, 4, 8], [3, 5, 6, 7]]
"""
# 
def priority(i: int, k: int, partition: list[list]) -> float:
  """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition' 
  
      Hint: The sum-free partition will be constructed by assigning 'k' to the set of highest priority 
      that will remain sum-free after the addition of 'k'. As such, the priority function need not check if
      k's addition will immediately make bin i not sum-free.
  """
  # Prefer larger bins (to fill them evenly) and small gaps
  size_bonus = len(partition[i])
  if partition[i]:
    last = max(partition[i])
    gap_penalty = abs(k - last - 1)
  else:
    gap_penalty = k  # empty bin penalty proportional to k
  return float(size_bonus - gap_penalty)
