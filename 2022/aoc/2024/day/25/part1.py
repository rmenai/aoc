from aoc.utils.parsers import get_data


def parse(raw: str):
    return raw


def calculate(data: str):
    return 0


if __name__ == "__main__":
    DATA: str = get_data(2024, 15)

    data = parse(DATA)
    result = calculate(data)

    print("--- Part 1: ---")
    print(f"{result}")
    print()
