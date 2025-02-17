from aoc.utils.parsers import get_data


def parse(data: str):
    return [list(line) for line in data.splitlines()]


GROUND = "."


def find_antinodes(antinodes, first: tuple[int, int], second: tuple[int, int]):
    width = second[1] - first[1]
    height = second[0] - first[0]

    antinodes[first[0]][first[1]] = 1
    antinodes[second[0]][second[1]] = 1

    anti1 = (first[0] - height, first[1] - width)
    while 0 <= anti1[0] < len(antinodes) and 0 <= anti1[1] < len(antinodes[anti1[0]]):
        antinodes[anti1[0]][anti1[1]] = 1
        anti1 = (anti1[0] - height, anti1[1] - width)

    anti2 = (second[0] + height, second[1] + width)
    while 0 <= anti2[0] < len(antinodes) and 0 <= anti2[1] < len(antinodes[anti2[0]]):
        antinodes[anti2[0]][anti2[1]] = 1
        anti2 = (anti2[0] + height, anti2[1] + width)


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

    print("--- Part 2: Resonant Collinearity ---")
    print(f"There are {antinodes} updated unique antinodes.")
    print()
