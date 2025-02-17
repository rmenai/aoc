from z3 import Int, Solver, sat

from aoc.utils.parsers import get_data

x = Int("x")
y = Int("y")


def parse(raw: str):
    equations = []
    for part in raw.split("\n\n"):
        first, second, prize = part.split("\n")
        a, c = int(first.split(",")[0][11:]), int(first.split(",")[1][3:])
        b, d = int(second.split(",")[0][11:]), int(second.split(",")[1][3:])
        k, kp = int(prize.split(",")[0][9:]), int(prize.split(",")[1][3:])

        s = Solver()

        k += 10000000000000
        kp += 10000000000000

        s.add(a * x + b * y == k)
        s.add(c * x + d * y == kp)

        equations.append(s)

    return equations


def calculate_tokens(equations) -> int:
    total = 0
    for solver in equations:
        while solver.check() == sat:
            result = solver.model()
            total += 3 * result[x].as_long() + result[y].as_long()

            solver.add(x != result[x], y != result[y])

    return total


if __name__ == "__main__":
    DATA: str = get_data(2024, 13)

    equations = parse(DATA)
    tokens = calculate_tokens(equations)

    print("--- Part 2: Claw Contraption++ ---")
    print(f"The fewest you would have to spend is {tokens}")
    print()

