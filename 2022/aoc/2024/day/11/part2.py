from aoc.utils.parsers import get_data

from functools import cache


@cache
def find_size(num: int, k: int) -> int:
    if k == 0:
        return 1

    length = len(str(num))
    if num == 0:
        return find_size(1, k - 1)
    elif length % 2 == 0:
        part1 = int(str(num)[length // 2:])
        part2 = int(str(num)[:length // 2])
        return find_size(part1, k - 1) + find_size(part2, k - 1)
    else:
        return find_size(num * 2024, k - 1)


def simulate(stones: list[int], times: int) -> int:
    total = 0
    for stone in stones:
        total += find_size(stone, times)

    return total


if __name__ == "__main__":
    STONES: list[int] = list(map(int, get_data(2024, 11).split(" ")))

    stones = simulate(STONES, 75)

    print("--- Part 2: Plutonian Pebbles ---")
    print(f"After blinking 75 times, there are {stones} stones")
    print()
