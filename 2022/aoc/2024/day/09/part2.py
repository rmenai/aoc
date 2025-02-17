from aoc.utils.parsers import get_data


def swap(arr: list, i, j, size):
    for k in range(size):
        temp = arr[i + k]
        arr[i + k] = arr[j + k]
        arr[j + k] = temp


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

    free = []
    current = 0
    for i in range(len(map)):
        if map[i] == ".":
            current += 1
        else:
            if current != 0:
                free.append([i - current, current])
                current = 0

    j = len(map) - 1
    index = -1
    size = 0

    while j >= 0:
        if map[j] != index:
            if size > 0:
                for i, block in enumerate(free):
                    if block[1] >= size and block[0] < j:
                        swap(map, block[0], j + 1, size)
                        if block[1] == size:
                            free.pop(i)
                        else:
                            free[i][1] -= size
                            free[i][0] += size

                        break

            if map[j] == ".":
                size = 0
                index = -1
            else:
                size = 1
                index = map[j]
        else:
            size += 1

        j -= 1

    checksum = 0
    for i in range(len(map)):
        if map[i] != ".":
            checksum += i * int(map[i])

    return checksum


if __name__ == "__main__":
    DISK_MAP: str = get_data(2024, 9)

    checksum = calculate_checksum(DISK_MAP)

    print("--- Part 2: Disk Fragmenter Whole Files ---")
    print(f"The resulting filesystem checksum is {checksum}")
    print()
