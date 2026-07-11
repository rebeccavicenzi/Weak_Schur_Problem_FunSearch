"""
Obtained using n = 5, target = 
Scores:
2:-2
3:-3
4:-9
5:-4
6:-83
"""
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
    The ith element in the output tuple is the priority of placing 'k' into the set with index i
    The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
    at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i.
  """
  """Returns priority for each bin; minimizes conflicts, then prefers bins with smaller maximum element."""
  priorities = [0.0] * n
  for i in range(n):
    conflicts = 0
    set_i = set(partition[i])
    for a in partition[i]:
      if a < k and (k - a) in set_i:
        conflicts += 1
    # Large penalty for conflicts, then prefer bins with smaller max element to keep values low
    max_elem = max(partition[i]) if partition[i] else 0
    priorities[i] = -conflicts * (n + 2) - max_elem * 0.01
  return priorities
