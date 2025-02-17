from aoc.utils.parsers import get_data
import re


def prod(s: str) -> int:
    nums = s[4:-1]
    a, b = nums.split(",")
    return int(a) * int(b)


def calculate(data: str) -> int:
    pattern = r"mul\(\d+\,\d+\)"
    matches = re.findall(pattern, data)

    return sum(map(prod, matches))


if __name__ == "__main__":
    CORRUPTED_DATA: str = get_data(2024, 3)  # Update year and day as needed.
    result = calculate(CORRUPTED_DATA)

    print("--- Part 1: Corrupted Data ---")
    print(f"Uncorrupted multiplication result is {result}")
    print()
