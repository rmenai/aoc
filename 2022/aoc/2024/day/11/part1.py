# from aoc.utils.parsers import get_data
#
#
# def simulate(stones: list[int], times: int) -> int:
#     for _ in range(times):
#         size = len(stones)
#         i = 0
#         while i < size:
#             length = len(str(stones[i]))
#             if stones[i] == 0:
#                 stones[i] = 1
#             elif length % 2 == 0:
#                 stones.insert(i + 1, int(str(stones[i])[length // 2:]))
#                 stones[i] = int(str(stones[i])[:length // 2])
#                 i += 1
#                 size += 1
#             else:
#                 stones[i] *= 2024
#
#             i += 1
#
#     return len(stones)
#
#
# if __name__ == "__main__":
#     STONES: list[int] = list(map(int, get_data(2024, 11).split(" ")))
#
#     stones = simulate(STONES, 25)
#
#     print("--- Part 1: Plutonian Pebbles ---")
#     print(f"After blinking 25 times, there are {stones} stones")
#     print()
