from aoc.utils.parsers import get_data
from functools import cmp_to_key


def parse(data: str):
    orders, pages = data.split("\n\n")
    return (
        [list(map(int, line.split("|"))) for line in orders.splitlines()],
        [list(map(int, line.split(","))) for line in pages.splitlines()]
    )


def calculate_sum(orders, pages):
    before = {}
    after = {}
    for a, b in orders:
        before.setdefault(b, set())
        after.setdefault(a, set())

        before[b].add(a)
        after[a].add(b)

    def smaller(x, y):
        if y in after.get(x, []) or x in before.get(y, []):
            return -1

        if x in after.get(y, []) or y in before.get(x, []):
            return 1

        return 0

    sum = 0

    for page in pages:
        sorted_page = list(sorted(page, key=cmp_to_key(smaller)))

        if sorted_page != page:
            sum += sorted_page[len(sorted_page) // 2]

    return sum


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 5)  # Update year and day as needed.
    ORDERS, PAGES = parse(RAW_DATA)

    sum = calculate_sum(ORDERS, PAGES)

    print("--- Part 2: Print Queue ---")
    print(f"The sum part 2 is {sum}")
    print()

