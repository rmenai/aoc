from aoc.utils.parsers import get_data


def parse_input(data: str):
    return [list(map(int, line)) for line in data.splitlines()]


def next_path(maps: list[list[int]], x: int, y: int) -> set:
    next = maps[x][y] + 1

    if next == 10:
        # Use Cantor Pairing function to hash the x and y
        # return {(x, y)}
        return {((x + y) * (x + y + 1)) // 2 + y}

    sum = set()

    if x < len(maps[x]) - 1:
        if maps[x + 1][y] == next:
            sum.update(next_path(maps, x + 1, y))

    if x > 0:
        if maps[x - 1][y] == next:
            sum.update(next_path(maps, x - 1, y))

    if y < len(maps) - 1:
        if maps[x][y + 1] == next:
            sum.update(next_path(maps, x, y + 1))

    if y > 0:
        if maps[x][y - 1] == next:
            sum.update(next_path(maps, x, y - 1))

    return sum


def count_points(maps):
    sum = 0
    for i in range(len(maps)):
        for j in range(len(maps)):
            if maps[i][j] == 0:
                print(next_path(maps, i, j))
                sum += len(next_path(maps, i, j))

    return sum


if __name__ == "__main__":
    DISK_MAP: str = get_data(2024, 10)
    MAP = parse_input(DISK_MAP)

    count = count_points(MAP)

    print("--- Part 1: Hoof It ---")
    print(f"The resulting sum is {count}")
    print()
