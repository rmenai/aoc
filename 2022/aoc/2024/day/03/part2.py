from aoc.utils.parsers import get_data
import re


def prod(s: str) -> int:
    nums = s[4:-1]
    a, b = nums.split(",")
    return int(a) * int(b)


def calculate(data: str) -> int:
    pattern = r"mul\(\d+\,\d+\)|do\(\)|don't\(\)"
    matches = re.findall(pattern, data)

    result = 0
    allowed = True
    for match in matches:
        if match == "do()":
            allowed = True
        elif match == "don't()":
            allowed = False
        else:
            if allowed:
                result += prod(match)

    return result


if __name__ == "__main__":
    CORRUPTED_DATA: str = get_data(2024, 3)  # Update year and day as needed.
    result = calculate(CORRUPTED_DATA)

    print("--- Part 2: Corrupted Data ---")
    print(f"Uncorrupted multiplication result is {result}")
    print()
