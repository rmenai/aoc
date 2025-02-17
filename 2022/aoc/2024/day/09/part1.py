from aoc.utils.parsers import get_data


def swap(arr: list, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp


def calculate_checksum(disk_map: str) -> int:
    map = []
    for i in range(0, len(disk_map) // 2):
        block = int(disk_map[2 * i])
        free = int(disk_map[2 * i + 1])

        for _ in range(block):
            map.append(i)

        for _ in range(free):
            map.append(".")

    for _ in range(int(disk_map[-1])):
        map.append(i + 1)

    j = len(map) - 1
    i = 0
    while i < j:
        if map[i] == ".":
            while (j > i and map[j] == "."):
                j -= 1

            swap(map, i, j)

        i += 1

    checksum = 0
    for i in range(len(map)):
        if map[i] != ".":
            checksum += i * int(map[i])

    return checksum


if __name__ == "__main__":
    DISK_MAP: str = get_data(2024, 9)

    checksum = calculate_checksum(DISK_MAP)

    print("--- Part 1: Disk Fragmenter ---")
    print(f"The resulting filesystem checksum is {checksum}")
    print()
