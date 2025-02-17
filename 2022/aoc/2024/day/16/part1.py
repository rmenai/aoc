from collections import deque
from heapq import heappop, heappush
from typing import Deque

from aoc.utils.parsers import get_data


class consts:
    DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    WALL = "#"
    EMPTY = "."
    SEEN = "*"
    PLAYER = "S"
    END = "E"


class Path:
    def __init__(self, dy: int, dx: int, dfy: int, dfx: int, score: int) -> None:
        self.dest: tuple[int, int] = (dy, dx)
        self.origin: tuple[int, int] = (dfy, dfx)

        self.weight: int = score
        self.crossed: bool = False


class Player:
    def __init__(self, y: int, x: int, dy: int, dx: int) -> None:
        self.y = y
        self.x = x

        self.dy = dy
        self.dx = dx

        self.score = 0

    def move(self, maze: list[list[str]], path: Path):
        if maze[self.y + path.dest[0]][self.x + path.dest[1]] != consts.EMPTY:
            raise ValueError("It is not possible to move")

        maze[self.y][self.x] = consts.SEEN

        self.dy = path.dest[0]
        self.dx = path.dest[1]
        self.y += self.dy
        self.x += self.dx

        maze[self.y][self.x] = consts.PLAYER
        self.score += path.weight

    def revert(self, maze: list[list[str]], backtrack: Deque[Path]):
        if not backtrack:
            raise ValueError("Nothing to backtrack")

        while backtrack and backtrack[-1].crossed:
            path = backtrack.pop()
            maze[self.y][self.x] = consts.EMPTY

            self.y -= path.dest[0]
            self.x -= path.dest[1]

            self.dy = path.origin[0]
            self.dx = path.origin[1]

            self.score -= path.weight
            maze[self.y][self.x] = consts.PLAYER

    def won(self, maze: list[list[str]]):
        for dy, dx in consts.DIRECTIONS:
            if maze[self.y + dy][self.x + dx] == consts.END:
                return True

        return False


def parse(raw: str):
    return [list(line) for line in raw.splitlines()]


def show(player: Player, maze: list[list[str]]):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == consts.EMPTY:
                print(" ", end=" ")
            elif maze[i][j] == consts.PLAYER:
                match (player.dy, player.dx):
                    case (-1, 0):
                        print("^", end=" ")
                    case (1, 0):
                        print("v", end=" ")
                    case (0, 1):
                        print(">", end=" ")
                    case (0, -1):
                        print("<", end=" ")
            else:
                print(maze[i][j], end=" ")
        print()
    print()


def search(maze: list[list[str]], player: Player):
    paths = []
    for dy, dx in consts.DIRECTIONS:
        if not (0 <= player.y + dy < len(maze)):
            raise ValueError("Out of bounds, y")

        if not (0 <= player.x + dx < len(maze[player.y + dy])):
            raise ValueError("Out of bounds, x")

        if maze[player.y + dy][player.x + dx] == consts.EMPTY:
            if player.dy + dy == 0 and player.dx + dx == 0:
                raise ValueError("Weird direction bug")

            weight = 1001 if player.dy != dy and player.dx != dx else 1
            paths.append(Path(dy, dx, player.dy, player.dx, weight))

    return paths


def solve(maze: list[list[str]], dy: int = 0, dx: int = 1):
    y, x = -1, -1
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == consts.PLAYER:
                y, x = i, j

    player = Player(y, x, dy, dx)
    paths: Deque[Path] = deque()

    highscore: float = float("inf")

    for path in search(maze, player):
        paths.append(path)

    while paths:
        path = paths.pop()
        player.move(maze, path)

        path.crossed = True
        paths.append(path)

        candidates = search(maze, player)
        for path in candidates:
            paths.append(path)

        if not candidates:
            if player.won(maze):
                highscore = min(player.score + 1, highscore)

            player.revert(maze, paths)

    return int(highscore)


def solve_best_score(maze: list[list[str]], dy: int = 0, dx: int = 1) -> int:
    y, x = -1, -1

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == consts.PLAYER:
                y, x = i, j
                break

    heap = []
    heappush(heap, (0, y, x, dy, dx))
    visited = {}

    while heap:
        score, y, x, dy, dx = heappop(heap)

        if maze[y][x] == consts.END:
            return score

        if (y, x, dy, dx) in visited and visited[(y, x, dy, dx)] <= score:
            continue

        visited[(y, x, dy, dx)] = score

        for cdy, cdx in consts.DIRECTIONS:
            cy, cx = y + cdy, x + cdx

            if maze[cy][cx] not in (consts.EMPTY, consts.END):
                continue

            direction_change = 1001 if (cdy, cdx) != (dy, dx) else 1
            new_score = score + direction_change
            heappush(heap, (new_score, cy, cx, cdy, cdx))

    return -1


if __name__ == "__main__":
    DATA: str = get_data(2024, 16)

    maze = parse(DATA)
    points = solve_best_score(maze)

    print("--- Part 1: Reindeer Maze ---")
    print(f"The shortest path can be atteinted with {points} points")
    print()
