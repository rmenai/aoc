
from aoc.utils.parsers import get_data


def parse_input(data: str):
    return [list(map(int, line)) for line in data.splitlines()]


def next_path(maps: list[list[int]], x: int, y: int) -> set:
    next = maps[x][y] + 1

    if next == 10:
        return 1

    sum = 0

    if x < len(maps[x]) - 1:
        if maps[x + 1][y] == next:
            sum += next_path(maps, x + 1, y)

    if x > 0:
        if maps[x - 1][y] == next:
            sum += next_path(maps, x - 1, y)

    if y < len(maps) - 1:
        if maps[x][y + 1] == next:
            sum += next_path(maps, x, y + 1)

    if y > 0:
        if maps[x][y - 1] == next:
            sum += next_path(maps, x, y - 1)

    return sum


def count_points(maps):
    sum = 0
    for i in range(len(maps)):
        for j in range(len(maps)):
            if maps[i][j] == 0:
                sum += next_path(maps, i, j)

    return sum


if __name__ == "__main__":
    DISK_MAP: str = get_data(2024, 10)
    MAP = parse_input(DISK_MAP)

    # MAP = [
    #     [8, 9, 0, 1, 0, 1, 2, 3],
    #     [7, 8, 1, 2, 1, 8, 7, 4],
    #     [8, 7, 4, 3, 0, 9, 6, 5],
    #     [9, 6, 5, 4, 9, 8, 7, 4],
    #     [4, 5, 6, 7, 8, 9, 0, 3],
    #     [3, 2, 0, 1, 9, 0, 1, 2],
    #     [0, 1, 3, 2, 9, 8, 0, 1],
    #     [1, 0, 4, 5, 6, 7, 3, 2]
    # ]

    count = count_points(MAP)

    print("--- Part 1: Hoof It ---")
    print(f"The resulting sum is {count}")
    print()
