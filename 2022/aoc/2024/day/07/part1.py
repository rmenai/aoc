from aoc.utils.parsers import get_data


def parse(data: str) -> list[list[int, list]]:
    lines = []
    for line in data.splitlines():
        result, nums = line.split(":")
        lines.append([
            int(result), [int(num)for num in nums.strip().split(" ")]
        ])

    return lines


def calculate(data: list[list[int, list]]) -> int:
    total = 0
    for expected, nums in data:
        num_operators = len(nums) - 1
        configurations = 2 ** num_operators
        while configurations > 0:
            binary = "{0:b}".format(configurations - 1).zfill(num_operators)
            result = nums[0]

            for i in range(num_operators):
                result = result + \
                    nums[i + 1] if binary[i] == "0" else result * nums[i + 1]

            if result == expected:
                total += expected
                break

            configurations -= 1

    return total


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 7)
    DATA: list[list[int, list]] = parse(RAW_DATA)

    result = calculate(DATA)

    print("--- Part 1: Bridge Repair ---")
    print(f"Their total calibration result is {result}")
    print()
