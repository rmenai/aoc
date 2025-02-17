def solve_best_score(maze: list[list[str]], dy: int = 0, dx: int = 1) -> int:
    y, x = -1, -1

    # Locate the player's starting position
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == consts.PLAYER:
                y, x = i, j
                break

    # Min-heap for prioritizing paths with lower scores
    heap = []
    heappush(heap, (0, y, x, dy, dx))  # (current score, y, x, prev_dy, prev_dx)

    # Keep track of visited states with their minimum scores
    visited = {}

    while heap:
        score, cy, cx, cdy, cdx = heappop(heap)

        # If we've reached the endpoint, return the score
        if maze[cy][cx] == consts.END:
            return score

        # Check if we've visited this state with a better score
        if (cy, cx, cdy, cdx) in visited and visited[(cy, cx, cdy, cdx)] <= score:
            continue

        visited[(cy, cx, cdy, cdx)] = score

        # Explore all possible directions
        for dy, dx in consts.DIRECTIONS:
            ny, nx = cy + dy, cx + dx

            # Check if the cell is empty or the endpoint
            if maze[ny][nx] not in (consts.EMPTY, consts.END):
                continue

            # Calculate the weight for this move
            direction_change = 1001 if (dy, dx) != (cdy, cdx) else 1
            new_score = score + direction_change

            # Push the new state into the heap
            heappush(heap, (new_score, ny, nx, dy, dx))

    return -1  # If no path is found
