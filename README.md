# Weak_Schur_Problem_FunSearch
## Current best bounds on WS(n) found by funsearch
$$\text{WS}(2) \geq 8 $$
$$\text{WS}(3) \geq 23 $$
$$\text{WS}(4) \geq 66 $$
$$\text{WS}(5) \geq 195 $$
$$\text{WS}(6) \geq 551 $$
$$\text{WS}(7) \geq 1609 $$

## SAT reproduction of WS(5) >= 207

We independently reproduced the lower bound **WS(5) >= 207** using a SAT formulation based on Rowley's construction.

On the same n=207 SAT instance:
- **SLIME5** found a valid solution in **107.1 s**
- **Glucose4** timed out after **600 s**

The recovered partition was independently verified as a valid weakly sum-free partition of {1, ..., 207} into five classes.

The certificate and a standalone verifier are available in [`experiments/ws5_207_sat`](experiments/ws5_207_sat).

This establishes **WS(5) >= 207**, not WS(5) = 207.
