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

    maxMAXCount = 0
    bathroom = [[0 for i in range(width)] for j in range(height)]
    for _ in range(seconds):
        bathroom = [[0 for i in range(width)] for j in range(height)]

        for p, v in robots:
            p[0] = (p[0] + v[0]) % width
            p[1] = (p[1] + v[1]) % height
            bathroom[p[1]][p[0]] += 1

        found = False
        maxCount = 0
        for j in range(height):
            count = 0
            for i in range(width):
                if bathroom[j][i] != 1:
                    if count > maxCount:
                        maxCount = count
                    count = 0
                else:
                    count += 1

        # if (_ + 1) % 1000 == 0:
        #     print(_ + 1)

        if maxCount > maxMAXCount:
            maxMAXCount = maxCount
            for j in range(height):
                for i in range(width):
                    if bathroom[j][i] == 1:
                        print("*", end=" ")
                    else:
                        print(" ", end=" ")
                print()

            print()
            print("-" * width, _ + 1, maxCount)
            print()
            input()


if __name__ == "__main__":
    DATA: str = get_data(2024, 14)

    robots: list[list[int]] = parse(DATA)
    safety = simulate(robots, 1000000000)

    print("--- Part 1: Restroom Redoubt ---")
    print(f"After 100 seconds, the safety facter is {safety}")
    print()

