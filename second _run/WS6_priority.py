"""
Obtained using n = 6, target = 647
Scores:
2: -2
3: -3
4: -4
5: -4
6: -4
"""
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
    The ith element in the output tuple is the priority of placing 'k' into the set with index i
    The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
    at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i.
  """
  """Improved version of `priority_v2`. Adds a diversity term to avoid local optima."""
  priorities = []
  for bin_idx in range(n):
    bin_set = set(partition[bin_idx])
    penalty = 0
    for a in bin_set:
      if k - a in bin_set and a != k - a:
        penalty += 1
      if a + k in bin_set:
        penalty += 1
    if k % 2 == 0 and (k // 2) in bin_set:
      penalty += 1
    # Diversity: prefer bins with fewer numbers near k (to spread out values)
    near_count = sum(1 for a in bin_set if abs(a - k) < 5)
    diversity_bonus = near_count * 0.05
    priorities.append(-penalty + diversity_bonus)
  return priorities
