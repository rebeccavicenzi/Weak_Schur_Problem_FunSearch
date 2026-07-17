"""
Achieves bounds WS(5) >= 195 and WS(6) >= 565
"""
def priority(i: int, k: int, partition: list[list]) -> float:
  """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition.' 
      When constructing the weakly sum-free partition, 'k' will be added to higher priority sets if possible. 
      
      (Hint) Some ideas that may work well:
      1. A priority function that leans towards sets with larger max elements
      2. A priority function that leans towards sets with more numbers closer to k
      If all these ideas are already implemented, don't be afraid to try something new and creative!
  """
  set_max = max(partition[i]) if partition[i] else 0
  arr = np.array(partition[i])
  window_count = np.sum(np.abs(arr - k/2) <= 2.2)
  conflict_penalty = np.sum(np.isin(arr[:, None] + arr, k)) * (k ** 0.48) / 2.9
  near_k = np.sum(arr >= k - 9) * np.exp(0.015 * (k - arr.min())) if arr.size > 0 else 0
  size_penalty = len(partition[i]) ** 0.33 if len(partition[i]) > 20 else 0
  diversity_bonus = np.std(arr) * 0.17 if arr.size > 2 else 0
  growth_penalty = -0.078 if set_max > 0.84 * k else 0
  return float(set_max) + 2.1 * window_count - 1.95 * conflict_penalty + 0.85 * near_k - size_penalty + diversity_bonus + growth_penalty