from aoc.utils.parsers import get_data


def parse(raw: str):
    robots = []
    for part in raw.splitlines():
        first, second = part.replace("p=", "").replace("v=", "").split(" ")
        x, y = list(map(int, first.split(",")))
        a, b = list(map(int, second.split(",")))

        robots.append(([x, y], [a, b]))

    return robots


def simulate(robots, seconds) -> int:
    width = 101
    height = 103

    bathroom = [[0 for i in range(width)] for j in range(height)]

    for p, v in robots:
        x = (p[0] + seconds * v[0]) % width
        y = (p[1] + seconds * v[1]) % height
        bathroom[y][x] += 1

    quadrants = [(0, 0), (1, 0), (0, 1), (1, 1)]
    qwidth = width // 2
    qheight = height // 2

    safety = 1
    for x, y in quadrants:
        sum = 0
        for i in range(qwidth):
            for j in range(qheight):
                a, b = (j + y * (qheight + 1), i + x * (qwidth + 1))
                sum += bathroom[a][b]

        safety *= sum

    return safety


if __name__ == "__main__":
    DATA: str = get_data(2024, 14)

    robots: list[list[int]] = parse(DATA)
    safety = simulate(robots, 100)

    print("--- Part 1: Restroom Redoubt ---")
    print(f"After 100 seconds, the safety facter is {safety}")
    print()
