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
        configurations = 3 ** num_operators

        while configurations > 0:
            base3 = []
            temp = configurations - 1
            for _ in range(num_operators):
                base3.append(temp % 3)
                temp //= 3
            base3.reverse()

            result = nums[0]
            for i in range(num_operators):
                if base3[i] == 0:
                    result += nums[i + 1]
                elif base3[i] == 1:
                    result *= nums[i + 1]
                elif base3[i] == 2:
                    result = int(str(result) + str(nums[i + 1]))

            if result == expected:
                total += expected
                break

            configurations -= 1

    return total


if __name__ == "__main__":
    RAW_DATA: str = get_data(2024, 7)
    DATA: list[list[int, list]] = parse(RAW_DATA)

    result = calculate(DATA)

    print("--- Part 2: Bridge Repair ---")
    print(f"Their total calibration result with || is {result}")
    print()

