import json
import sys
from pathlib import Path

def verify_partition(path):
    data = json.loads(Path(path).read_text())
    n = data["n"]
    k = data["k"]
    partition = data["partition"]

    if len(partition) != k:
        raise ValueError(f"Expected {k} classes, found {len(partition)}")

    flat = [x for cls in partition for x in cls]

    if sorted(flat) != list(range(1, n + 1)):
        raise ValueError("Partition does not cover 1..n exactly once")

    for colour, cls in enumerate(partition, 1):
        s = set(cls)
        vals = sorted(cls)
        for i, a in enumerate(vals):
            for b in vals[i + 1:]:
                if a + b in s:
                    raise ValueError(
                        f"Colour {colour} invalid: {a} + {b} = {a+b}"
                    )

    print(f"PASS: valid weakly sum-free partition of [1, {n}] into {k} classes.")
    print(f"Therefore this certificate establishes WS({k}) >= {n}.")

if __name__ == "__main__":
    verify_partition(
        sys.argv[1] if len(sys.argv) > 1 else "partition_207.json"
    )
