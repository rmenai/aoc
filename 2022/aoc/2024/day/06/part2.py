from aoc.utils.parsers import get_data
import types
import copy


def parse(data: str):
    return [list(line) for line in data.splitlines()]


consts = types.SimpleNamespace()

consts.GUARD_UP = "^"
consts.GUARD_RIGHT = ">"
consts.GUARD_LEFT = "<"
consts.GUARD_DOWN = "v"

consts.SEEN = "X"
consts.OBSTACLE = "#"


def is_infinite(map: list[list[str]]) -> bool:
    rows = len(map)
    columns = len(map[0])

    x = -1
    y = -1

    for i in range(rows):
        for j in range(columns):
            if map[i][j] == consts.GUARD_UP:
                x = i
                y = j

    MAX_COUNT = 10000
    count = 0

    while 0 <= x < rows and 0 <= y < columns and count < MAX_COUNT:
        count += 1
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

    if count >= MAX_COUNT:
        print("AHA")
        return True

    return False


def count_infinite(map: list[list[str]]):
    count = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == consts.GUARD_UP:
                continue

            map_copy = copy.deepcopy(map)
            map_copy[i][j] = consts.OBSTACLE

            if is_infinite(map_copy):
                count += 1

            print(i, j)

    return count


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 6)
    MAP: list[str] = parse(RAW_DATA)

    paths = count_infinite(MAP)

    print("--- Part 2: Guard Gallivant Obstructed ---")
    print(f"There are {paths} different time loops")
    print()
