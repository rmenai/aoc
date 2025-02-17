from aoc.utils.parsers import get_data
import re


def parse(data: str) -> list[list[int]]:
    return data.splitlines()


def find_line_occurences(line: str):
    matches = re.findall(r"XMAS", line) + re.findall(r"SAMX", line)
    return len(matches)


def find_occurences(lines: list[str]) -> int:
    length = len(lines)
    total_occurences = 0

    columns = ["".join(lines[i][j] for i in range(length))
               for j in range(length)]

    tl_diagonals = []
    for k in range(2 * length - 1):
        diagonal = ""
        for i in range(length):
            j = k - i
            if 0 <= j < length:
                diagonal += lines[i][j]
        if diagonal:
            tl_diagonals.append(diagonal)

    tr_diagonals = []
    for k in range(2 * length - 1):
        diagonal = ""
        for i in range(length):
            j = i + k - (length - 1)
            if 0 <= j < length:
                diagonal += lines[i][j]
        if diagonal:
            tr_diagonals.append(diagonal)

    # Count occurrences in all directions
    total_occurences += sum(find_line_occurences(line)
                            for line in lines)  # Horizontal
    total_occurences += sum(find_line_occurences(col)
                            for col in columns)  # Vertical
    total_occurences += sum(find_line_occurences(diag)
                            # Top-left to bottom-right
                            for diag in tl_diagonals)
    total_occurences += sum(find_line_occurences(diag)
                            # Top-right to bottom-left
                            for diag in tr_diagonals)

    return total_occurences


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 4)  # Update year and day as needed.
    WORD_SEARCH = parse(RAW_DATA)

    occurences = find_occurences(WORD_SEARCH)

    print("--- Part 1: Word Search Occurences ---")
    print(f"There are {occurences} occurences of XMAS")
    print()
