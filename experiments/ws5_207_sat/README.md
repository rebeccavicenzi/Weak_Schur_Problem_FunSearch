# WS(5) >= 207 SAT reproduction

This directory contains a computationally verified weakly sum-free
partition of {1, ..., 207} into five colour classes.

The partition was recovered with the SLIME5 SAT solver using our
reconstruction of the n=207 SAT formulation based on Rowley's method.

On the same SAT instance:

- SLIME5: SAT in 107.1 s
- Glucose4: timeout after 600 s

The recovered certificate was independently checked to contain every
integer from 1 to 207 exactly once and to satisfy the weakly sum-free
condition in every class.

This establishes the lower bound:

    WS(5) >= 207

It does not claim that WS(5) = 207.

## Files

- `partition_207.json` - machine-readable certificate
- `partition_207.txt` - human-readable certificate
- `verify_partition.py` - standalone verifier

## Verification

Run:

    python3 verify_partition.py
