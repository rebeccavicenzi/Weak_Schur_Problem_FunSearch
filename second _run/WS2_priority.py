"""
Obtained using n = 2, target = 
Score is 
2:-1
3:-3
4:-7
5:-15
6:-41
"""
def priority(n: int, k: int, partition: list[list]) -> list[float]:
  """Returns the priority, as a tuple of floats with length 'n', of the integer 'k'. 
    The ith element in the output tuple is the priority of placing 'k' into the set with index i
    The sum-free partition will be constructed by selecting the highest priority integer/bin (k, i) combo
    at any step, verifying that it does not cause disallowed sums in bin i and then adding k to bin i.
  """
  return [0.0 for x in range(n)]
