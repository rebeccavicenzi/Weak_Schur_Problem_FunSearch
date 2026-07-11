"""
Obtained using n = 4, target = 66
Score is 
2:-2
3:-3
4:-2
5:-26
6:-96
"""
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
    The ith element in the output tuple is the priority of placing 'k' into the set with index i
    The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
    at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i.
  """
  """Improved version of `priority_v2`."""
  priorities = []
  target_size = (k + n - 1) // n
  for i in range(n):
    bin_set = partition[i]
    size = len(bin_set)
    conflict_count = 0
    seen = set()
    for a in bin_set:
      if (k - a) in seen:
        conflict_count += 1
      seen.add(a)
    if k % 2 == 0 and k // 2 in bin_set:
      conflict_count += 1
    # Reward for clustering: prefer bins that already contain k-1 or k+1
    cluster_reward = 0.0
    if k - 1 in bin_set:
      cluster_reward += 0.5
    if k + 1 in bin_set:
      cluster_reward += 0.4
    # Penalty for size imbalance relative to target, with stronger weight
    balance_penalty = 0.1 * abs(size - target_size)
    # Encourage smaller bins slightly more
    size_penalty = 0.15 * size
    # Slight negative bonus for max value to encourage spreading early numbers
    diversity_bonus = -0.02 * (max(bin_set) if bin_set else 0)
    priorities.append(-conflict_count - size_penalty + cluster_reward - balance_penalty + diversity_bonus)
  return priorities

