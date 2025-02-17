from aoc.utils.parsers import get_data
import types


def parse(data: str):
    return [list(line) for line in data.splitlines()]


consts = types.SimpleNamespace()

consts.GUARD_UP = "^"
consts.GUARD_RIGHT = ">"
consts.GUARD_LEFT = "<"
consts.GUARD_DOWN = "v"

consts.SEEN = "X"
consts.OBSTACLE = "#"


def count_paths(map: list[list[str]]) -> int:
    rows = len(map)
    columns = len(map[0])

    x = -1
    y = -1

    for i in range(rows):
        for j in range(columns):
            if map[i][j] == consts.GUARD_UP:
                x = i
                y = j

    while 0 <= x < rows and 0 <= y < columns:
        match map[x][y]:
            case consts.GUARD_LEFT:
                if y == 0:
                    break

                if map[x][y - 1] == consts.OBSTACLE:
                    map[x][y] = consts.GUARD_UP
                else:
                    map[x][y] = consts.SEEN
                    map[x][y - 1] = consts.GUARD_LEFT
                    y -= 1

            case consts.GUARD_RIGHT:
                if y == columns - 1:
                    break

                if map[x][y + 1] == consts.OBSTACLE:
                    map[x][y] = consts.GUARD_DOWN
                else:
                    map[x][y] = consts.SEEN
                    map[x][y + 1] = consts.GUARD_RIGHT
                    y += 1

            case consts.GUARD_DOWN:
                if x == rows - 1:
                    break

                if map[x + 1][y] == consts.OBSTACLE:
                    map[x][y] = consts.GUARD_LEFT
                else:
                    map[x][y] = consts.SEEN
                    map[x + 1][y] = consts.GUARD_DOWN
                    x += 1

            case consts.GUARD_UP:
                if x == 0:
                    break

                if map[x - 1][y] == consts.OBSTACLE:
                    map[x][y] = consts.GUARD_RIGHT
                else:
                    map[x][y] = consts.SEEN
                    map[x - 1][y] = consts.GUARD_UP
                    x -= 1

    seen = 1  # Because it will leave
    for i in range(rows):
        for j in range(columns):
            if map[i][j] == consts.SEEN:
                seen += 1

    return seen


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 6)
    MAP: list[str] = parse(RAW_DATA)

    paths = count_paths(MAP)

    print("--- Part 1: Guard Gallivant ---")
    print(f"There are {paths} distinct paths")
    print()
