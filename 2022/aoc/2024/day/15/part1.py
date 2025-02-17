from aoc.utils.parsers import get_data


class consts:
    BOX = "O"
    AIR = "."
    WALL = "#"
    ROBOT = "@"

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def parse(raw: str):
    MAP, COMMANDS = raw.split("\n\n")
    return ([list(line) for line in MAP.splitlines()], COMMANDS.replace("\n", ""))


def score(map: list[list[str]]):
    total = 0
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            if map[i][j] == consts.BOX:
                total += 100 * i + j

    return total


def calculate(map: list[list[str]], commands):
    y, x = -1, -1

    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j] == consts.ROBOT:
                y, x = i, j
                break
        else:
            continue
        break

    directions = {
        consts.UP: (-1, 0),
        consts.DOWN: (1, 0),
        consts.LEFT: (0, -1),
        consts.RIGHT: (0, 1),
    }

    for command in commands:
        dy, dx = directions[command]

        i, j = y + dy, x + dx
        block = map[i][j]
        while block != consts.AIR:
            if block == consts.WALL:
                break

            i, j = i + dy, j + dx
            block = map[i][j]
        else:
            map[i][j] = consts.BOX
            map[y + dy][x + dx] = consts.AIR

        i, j = y + dy, x + dx
        block = map[i][j]

        if block == consts.AIR:
            map[y][x] = consts.AIR
            map[i][j] = consts.ROBOT
            y, x = i, j

    return score(map)


if __name__ == "__main__":
    DATA: str = get_data(2024, 15)

    map, commands = parse(DATA)
    result = calculate(map, commands)

    print("--- Part 1: Warehouse Woes ---")
    print(f"The total score is {result}")
    print()
