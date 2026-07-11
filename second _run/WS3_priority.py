"""
Obtained using n = 3, target = 23 
Score is 
2:-1
3:-1
4:-12
5:-63
6:-298
"""
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
    The ith element in the output tuple is the priority of placing 'k' into the set with index i
    The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
    at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i.
  """
  priorities = []
  max_len = max(len(s) for s in partition) if partition else 0
  for i in range(n):
    s = set(partition[i])
    conflict = 0
    # Count pairs that would sum to k
    for a in partition[i]:
      if k - a in s and k - a != a:
        conflict += 1
      if a * 2 == k:
        conflict += 1
    # Penalize full sets slightly and reward empty ones
    size_penalty = len(partition[i]) / (max_len + 1)
    priorities.append(conflict + size_penalty)
  return priorities
