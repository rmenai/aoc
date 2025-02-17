from aoc.utils.parsers import get_data

VERTICE = " "
EMPTY = "*"
SEEN = "+"


def transform(coordinate: int) -> int:
    return 2 * coordinate + 1


def enhanceMap(map: list[list[str]]) -> list[list[str]]:
    length = transform(len(map))
    enhancedMap = [[VERTICE for j in range(length)] for i in range(length)]

    for i in range(len(map)):
        for j in range(len(map)):
            x = transform(i)
            y = transform(j)

            enhancedMap[x][y] = map[i][j]

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if 0 <= ni < len(map) and 0 <= nj < len(map) and map[ni][nj] == map[i][j]:
                    enhancedMap[x + dx][y + dy] = EMPTY

    return enhancedMap


def explore(MAP: list[list[str]], isolatedMap: list[list[str]], visited, i, j) -> int:
    if visited[i][j]:
        return 0

    symbol = MAP[i][j]
    visited[i][j] = True
    isolatedMap[transform(i)][transform(j)] = symbol

    area = 1
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        ni, nj = i + dx, j + dy
        if 0 <= ni < len(MAP) and 0 <= nj < len(MAP) and not visited[ni][nj] and MAP[ni][nj] == symbol:
            area += explore(MAP, isolatedMap, visited, ni, nj)

    return area


def countRow(map: list[list[str]], y: int, symbol: str) -> int:
    count = 0
    consecutive = 0
    pastId = ""
    for x in range(1, len(map), 2):
        id = ""
        if y > 0:
            id += map[x][y - 1]

        if y < len(map) - 1:
            id += map[x][y + 1]

        if x == 1:
            pastId = id

        # print("Info:", symbol, pastId, id)
        if symbol not in id or id == symbol * 2:
            if consecutive > 0:
                count += 1
                consecutive = 0

            pastId = id
            continue

        if symbol in pastId and pastId != symbol * 2 and id != pastId:
            count += 1
            consecutive = 1
        else:
            consecutive += 1

        pastId = id

    if consecutive > 0:
        count += 1

    # print("Count:", count)
    # print()

    return count


def countColumn(map: list[list[str]], x: int, symbol: str) -> int:
    count = 0
    consecutive = 0
    pastId = ""
    for y in range(1, len(map), 2):
        id = ""
        if x > 0:
            id += map[x - 1][y]

        if x < len(map) - 1:
            id += map[x + 1][y]

        if y == 1:
            pastId = id

        # print("Info:", symbol, pastId, id)
        if symbol not in id or id == symbol * 2:
            if consecutive > 0:
                count += 1
                consecutive = 0

            pastId = id
            continue

        if symbol in pastId and pastId != symbol * 2 and id != pastId:
            count += 1
            consecutive = 1
        else:
            consecutive += 1

        pastId = id

    if consecutive > 0:
        count += 1

    # print("Count:", count)
    # print()

    return count


def countSides(map: list[list[str]], symbol: str) -> int:
    n = 0
    for k in range(0, len(map), 2):
        n += countRow(map, k, symbol)
        n += countColumn(map, k, symbol)

    return n


def clearMap(map: list[list[str]]):
    for x in range(len(map)):
        for y in range(len(map)):
            map[x][y] = VERTICE


def calculatePrice(MAP: list[list[str]]) -> int:
    length = transform(len(MAP))
    isolatedMap = [[VERTICE for _ in range(length)] for _ in range(length)]
    visited = [[False for _ in range(len(MAP))] for _ in range(len(MAP))]

    total = 0
    for i in range(len(MAP)):
        for j in range(len(MAP)):
            if not visited[i][j]:  # Only explore unvisited cells
                area = explore(MAP, isolatedMap, visited, i, j)
                if area > 0:
                    sides = countSides(isolatedMap, MAP[i][j])
                    # print(MAP[i][j], area, sides)
                    clearMap(isolatedMap)
                    total += area * sides

    return total


if __name__ == "__main__":
    MAP: str = [list(line) for line in get_data(2024, 12).splitlines()]

    price = calculatePrice(MAP)

    print("--- Part 2: HARD Garden Groups ---")
    print(f"The total price is {price}")
    print()
