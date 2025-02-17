from heapq import heappop, heappush

from aoc.utils.parsers import get_data


def parse(raw: str):
    return [list(line) for line in raw.splitlines()]


class consts:
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    WALL = "#"
    EMPTY = "."
    SEEN = "*"
    PLAYER = "S"
    END = "E"


def solve_best_score(maze: list[list[str]]) -> int:
    return 0


if __name__ == "__main__":
    DATA: str = get_data(2024, 16)

    maze = parse(DATA)
    points = solve_best_score(maze)

    print("--- Part 2: Reindeer Maze :skull: ---")
    print(f"The shortest path can be atteinted with {points} points")
    print()
