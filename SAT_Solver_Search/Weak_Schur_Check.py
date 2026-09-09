#!/usr/bin/env python3

from itertools import combinations

# ---------------------------------------------------------------------------
# Put your partition here -- one list per color class.
# ---------------------------------------------------------------------------
partition = [
    # Color 1
    [1, 3, 5, 7, 9, 11, 13, 15, 19, 21, 38, 46, 50, 54, 58, 62, 66, 70, 74, 90,
     94, 98, 102, 106, 110, 114, 118, 122, 126, 130, 134, 138, 154, 158, 162,
     166, 170, 174, 178, 182, 190, 207],

    # Color 2
    [2, 6, 10, 14, 18, 36, 40, 41, 44, 45, 48, 49, 52, 53, 56, 57, 60, 61, 64,
     65, 68, 69, 72, 73, 155, 156, 159, 160, 163, 164, 167, 168, 171, 172, 175,
     176, 179, 180, 183, 184, 187, 188],

    # Color 3
    [4, 8, 16, 17, 22, 23, 32, 37, 42, 43, 76, 77, 96, 97, 131, 132, 151, 152,
     185, 186, 191, 192, 205, 206],

    # Color 4
    [12, 20, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 78, 79, 80, 81, 82,
     83, 84, 85, 86, 87, 88, 89, 139, 140, 141, 142, 143, 144, 145, 146, 147,
     148, 149, 150, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204],

    # Color 5
    [39, 47, 51, 55, 59, 63, 67, 71, 75, 91, 92, 93, 95, 99, 100, 101, 103,
     104, 105, 107, 108, 109, 111, 112, 113, 115, 116, 117, 119, 120, 121, 123,
     124, 125, 127, 128, 129, 133, 135, 136, 137, 153, 157, 161, 165, 169, 173,
     177, 181, 189],
]

def find_violation(block):
    """Return (x, y, z) with x < y, x + y = z, all in block; else None."""
    block_set = set(block)
    for x, y in combinations(sorted(block_set), 2):
        z = x + y
        if z in block_set:
            return (x, y, z)
    return None


def validate_range(partition):
    """
    Check that the classes together form a valid partition of {1, ..., n}
    for some n: every integer from 1 to n appears, each exactly once
    (no gaps, no duplicates, nothing below 1).

    Returns (is_valid, n, duplicates, missing).
    """
    seen = set()
    duplicates = set()
    covered = set()

    for block in partition:
        for e in block:
            if e in seen:
                duplicates.add(e)
            seen.add(e)
            covered.add(e)

    below_one = sorted(e for e in covered if e < 1)
    n = max(covered) if covered else 0
    missing = sorted(set(range(1, n + 1)) - covered)

    is_valid = not duplicates and not missing and not below_one
    return is_valid, n, sorted(duplicates), missing, below_one


def check(partition):
    print("--- Range check ---")
    is_valid, n, duplicates, missing, below_one = validate_range(partition)
    if is_valid:
        print(f"Covers {{1, ..., {n}}} exactly: OK")
    else:
        print(f"Covers {{1, ..., {n}}} exactly: FAILED")
        if below_one:
            print(f"  elements below 1: {below_one}")
        if duplicates:
            print(f"  elements in more than one class: {duplicates}")
        if missing:
            print(f"  missing from the middle/end: {missing}")

    print("\n--- Weak Schur check (per class) ---")
    sum_free = True
    for i, block in enumerate(partition):
        violation = find_violation(block)
        if violation is None:
            status = "OK"
        else:
            x, y, z = violation
            status = f"VIOLATION: {x} + {y} = {z}"
            sum_free = False
        print(f"Class {i + 1} ({len(block)} elements): {status}")

    ok = is_valid and sum_free
    print()
    print("Result:", "SATISFIES the weak Schur property" if ok else "VIOLATES the weak Schur property")
    return ok


if __name__ == "__main__":
    check(partition)

