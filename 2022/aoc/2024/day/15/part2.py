from aoc.utils.parsers import get_data


class consts:
    BOX = "[]"
    AIR = "."
    WALL = "#"
    ROBOT = "@"

    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"


def parse(raw: str):
    MAP, COMMANDS = raw.split("\n\n")

    MAP = MAP.replace("#", "##")
    MAP = MAP.replace("O", "[]")
    MAP = MAP.replace(".", "..")
    MAP = MAP.replace("@", "@.")

    return ([list(line) for line in MAP.splitlines()], COMMANDS.replace("\n", ""))


def score(map: list[list[str]]):
    total = 0
    for i in range(1, len(map) - 1):
        for j in range(2, len(map[i]) - 2):
            if map[i][j] == "[":
                total += 100 * i + j

    return total


def can_move(map: list[list[str]], y, x, dy, dx):
    if map[y][x] == consts.WALL:
        return False

    if map[y][x] == consts.AIR:
        return True

    if map[y][x] in consts.BOX:
        m = x if map[y][x] == "[" else x - 1
        n = x + 1 if map[y][x] == "[" else x

        match dy, dx:
            case 0, 1:
                return can_move(map, y, n + 1, dy, dx)

            case 0, -1:
                return can_move(map, y, m - 1, dy, dx)

            case _, 0:
                a = can_move(map, y + dy, m, dy, dx)
                b = can_move(map, y + dy, n, dy, dx)
                return a and b

    else:
        if map[y][x] != consts.ROBOT:
            raise ValueError(f"This is weird, there is a {map[y][x]}")

        return can_move(map, y + dy, x + dx, dy, dx)


def move(map: list[list[str]], y, x, dy, dx):
    if not can_move(map, y, x, dy, dx):
        return

    if map[y][x] in (consts.AIR, consts.WALL):
        return

    if map[y][x] in consts.BOX:
        m = x if map[y][x] == "[" else x - 1
        n = x + 1 if map[y][x] == "[" else x

        match dy, dx:
            case 0, 1:
                move(map, y, n + 1, dy, dx)

                if map[y][n + 1] == consts.AIR:
                    map[y][m] = consts.AIR
                    map[y][n] = "["
                    map[y][n + 1] = "]"

            case 0, -1:
                move(map, y, m - 1, dy, dx)

                if map[y][m - 1] == consts.AIR:
                    map[y][n] = consts.AIR
                    map[y][m] = "]"
                    map[y][m - 1] = "["

            case _, 0:
                move(map, y + dy, m, dy, dx)
                move(map, y + dy, n, dy, dx)

                if map[y + dy][m] == consts.AIR and map[y + dy][n] == consts.AIR:
                    map[y][m] = consts.AIR
                    map[y][n] = consts.AIR
                    map[y + dy][m] = "["
                    map[y + dy][n] = "]"

    else:
        if map[y][x] != consts.ROBOT:
            raise ValueError(f"This is weird, there is a {map[y][x]}")

        move(map, y + dy, x + dx, dy, dx)
        if map[y + dy][x + dx] == consts.AIR:
            map[y][x] = consts.AIR
            map[y + dy][x + dx] = consts.ROBOT


def calculate(map: list[list[str]], commands):
    y, x = -1, -1

    for i in range(len(map)):
        for j in range(len(map[i])):
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
        move(map, y, x, dy, dx)

        if map[y + dy][x + dx] == consts.ROBOT:
            y += dy
            x += dx

    return score(map)


if __name__ == "__main__":
    DATA: str = get_data(2024, 15)

    map, commands = parse(DATA)
    result = calculate(map, commands)

    print("--- Part 2: Seconds Warehouse Woes ---")
    print(f"The total score is {result}")
    print()
