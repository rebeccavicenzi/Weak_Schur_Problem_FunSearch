"""
Obtained while optimizing for n = 5
N.B. this program actually produced a priority function that achieved
WS(5) >= 190 but for some reason it doesn't fully load into wandb. 
scores:
2:8
3:23
4:66
5:189
6:551
7:1605
 
"""

def priority(i: int, k: int, partition: list[list]) -> float:
  """Returns the priority, as a float, of assigning the integer 'k' to the set with index 'i' in 'partition' 
    
      Hint: The sum-free partition will be constructed by assigning 'k' to the set of highest priority 
      that will remain sum-free after the addition of 'k'. As such, the priority function need not check if
      k's addition will immediately make bin i not sum-free.
  """
  """Improved version of `priority_v2`."""
  if not partition[i]:
    return -k  # prioritize empty sets
  s = set(partition[i])
  max_val = max(s)
  half = 1 if k % 2 == 0 and (k // 2) in s else 0
  comp_pairs = sum(1 for x in s if x < k - x and (k - x) in s)
  existing_conflicts = 0
  for a in s:
    for b in s:
      if a < b and (a + b) in s:
        existing_conflicts += 1
  # Penalize sets with many large numbers (more likely to cause future conflicts)
  large_count = sum(1 for x in s if x > k // 2)
  # Add penalty for sets that already have many elements near k (potential new conflicts)
  near_k = sum(1 for x in s if x > k - 20)  # tunable threshold
  return max_val + 3 * half + 4 * comp_pairs + 10 * existing_conflicts + 0.5 * large_count + 2 * near_k