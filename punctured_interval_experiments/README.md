# Punctured interval experiments

Hand-designed priority functions testing whether the "punctured interval" structure from Rafilipojaona's Weak Schur constructions helps the FunSearch greedy solver.

H0, H1 and H2 are hand-written heuristics, not evolved by FunSearch.

## Results (n=5)

- best evolved FunSearch priority: 195
- H0 (rigid m-blocking): 180
- H1 (m-target + gap tolerance): 88
- H2 (gap tolerance only): 88

`structural_metrics.py` decomposes a partition into punctured-interval-like segments and compares segment size to each class's minimum, to check how closely a partition resembles the paper's structure.
