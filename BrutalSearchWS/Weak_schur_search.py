Color = 4
Number = 66

from itertools import combinations

from pysat.formula import CNF
from pysat.solvers import Solver


def variable(number, color):
    """
    Def SAT variable as (number, color).

    True means that `number` is assigned to `color`.
    """
    return (number - 1) * Color + color


def build_formula():
    formula = CNF()

    ''' Condition 1: every number has one and exactly one color.'''
    for number in range(1, Number + 1):
        formula.append(
            [variable(number, color) for color in range(1, Color + 1)]
        )

        for color_1, color_2 in combinations(range(1, Color + 1), 2):
            formula.append(
                [
                    -variable(number, color_1),
                    -variable(number, color_2),
                ]
            )

    ''' Condition 2: each color is weakly sum-free.'''
    for x in range(1, Number + 1):
        for y in range(x + 1, Number + 1):
            total = x + y
            if total > Number:
                break

            for color in range(1, Color + 1):
                formula.append(
                    [
                        -variable(x, color),
                        -variable(y, color),
                        -variable(total, color),
                    ]
                )

    return formula


def main():
    formula = build_formula()
    '''glucose4 is a SAT solver u can try others.'''
    with Solver(name="glucose4", bootstrap_with=formula.clauses) as solver:
        if not solver.solve():
            print(f"UNSAT: 1..{Number} cannot be split into {Color} weakly sum-free colors.")
            return

        model = set(solver.get_model())

    partition = [[] for _ in range(Color)]
    for number in range(1, Number + 1):
        for color in range(1, Color + 1):
            if variable(number, color) in model:
                partition[color - 1].append(number)

    print(f"SAT: 1..{Number} can be split into {Color} weakly sum-free colors.")
    print("partition =", partition)


if __name__ == "__main__":
    main()
