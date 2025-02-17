from aoc.utils.parsers import get_data


def parse_input(data: str) -> tuple[list[int], list[int]]:
    left, right = [], []
    for line in data.splitlines():
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    return left, right


def calculate_total_similarity(left: list[int], right: list[int]) -> int:
    count = {}
    for num in right:
        count[num] = count.get(num, 0) + 1

    return sum(num * count.get(num, 0) for num in left)


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 1)  # Update year and day as needed.
    LEFT, RIGHT = parse_input(RAW_DATA)

    total_distance = calculate_total_similarity(LEFT, RIGHT)

    print("--- Part 1: Total Distance ---")
    print(f"Total distance is {total_distance}")
    print()
