from aoc.utils.parsers import get_data


def parse(data: str) -> list[list[int]]:
    return data.splitlines()


def check_xmas(board: str, i: int, j: int):
    first = board[i][j] + board[i + 1][j + 1] + board[i + 2][j + 2]
    second = board[i + 2][j] + board[i + 1][j + 1] + board[i][j + 2]

    return first in ("MAS", "SAM") and second in ("MAS", "SAM")


def find_occurences(lines: list[str]) -> int:
    xmas_count = 0
    for i in range(len(lines) - 2):
        for j in range(len(lines[i]) - 2):
            if check_xmas(lines, i, j):
                xmas_count += 1

    return xmas_count


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 4)  # Update year and day as needed.
    WORD_SEARCH = parse(RAW_DATA)

    occurences = find_occurences(WORD_SEARCH)

    print("--- Part 2: Word Search Occurences ---")
    print(f"There are {occurences} occurences of X-MAS")
    print()
