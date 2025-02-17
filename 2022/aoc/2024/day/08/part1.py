from aoc.utils.parsers import get_data


def parse(data: str):
    return [list(line) for line in data.splitlines()]


GROUND = "."


def find_antinodes(map, first: tuple[int, int], second: tuple[int, int]):
    width = second[1] - first[1]
    height = second[0] - first[0]

    anti1 = (first[0] - height, first[1] - width)
    anti2 = (second[0] + height, second[1] + width)

    if 0 <= anti1[0] < len(map) and 0 <= anti1[1] < len(map[anti1[0]]):
        map[anti1[0]][anti1[1]] = 1

    if 0 <= anti2[0] < len(map) and 0 <= anti2[1] < len(map[anti2[0]]):
        map[anti2[0]][anti2[1]] = 1


def total_antinodes(map: list[list[str]]) -> int:
    antinodes = [[0 for i in range(len(map))] for j in range(len(map[0]))]
    antennas = {}
    for i in range(len(map)):
        for j in range(len(map[i])):
            symbol = map[i][j]
            if symbol == GROUND:
                continue

            if not antennas.get(symbol, None):
                antennas[symbol] = [(i, j)]
            else:
                antennas[symbol].append((i, j))

    for frequency in antennas.keys():
        for a in range(len(antennas[frequency]) - 1):
            for b in range(a + 1, len(antennas[frequency])):
                first = antennas[frequency][a]
                second = antennas[frequency][b]

                find_antinodes(antinodes, first, second)

    return sum(sum(antinodes, []))


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 8)
    MAP: list[str] = parse(RAW_DATA)

    antinodes = total_antinodes(MAP)

    print("--- Part 1: Resonant Collinearity ---")
    print(f"There are {antinodes} antinodes.")
    print()
