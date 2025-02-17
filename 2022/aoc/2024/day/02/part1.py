from aoc.utils.parsers import get_data


def parse_input(data: str) -> tuple[list[int], list[int]]:
    return [list(map(int, line.split(" "))) for line in data.splitlines()]


def count_safe_reports(reports: list[list[int]]) -> int:
    total = 0
    for report in reports:
        sign = 1 if report[1] - report[0] > 0 else -1
        for i in range(1, len(report)):
            diff = report[i] - report[i - 1]
            if not (diff * sign > 0 and 1 <= abs(diff) <= 3):
                break
        else:
            total += 1

    return total


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 2)  # Update year and day as needed.
    REPORTS: list[list[int]] = parse_input(RAW_DATA)

    count = count_safe_reports(REPORTS)

    print("--- Part 1: Total Safe Reports ---")
    print(f"Total safe reports count is {count}")
    print()
