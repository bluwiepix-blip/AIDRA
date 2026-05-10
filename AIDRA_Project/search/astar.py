import heapq


# ==========================================
# HEURISTIC FUNCTION
# ==========================================
def heuristic(a, b):

    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ==========================================
# A* SEARCH
# ==========================================
def astar(grid, start, goal):

    pq = [(0, start, [])]

    visited = set()

    while pq:

        cost, (x, y), path = heapq.heappop(pq)

        # GOAL FOUND
        if (x, y) == goal:

            return path + [(x, y)]

        # ALREADY VISITED
        if (x, y) in visited:

            continue

        visited.add((x, y))

        # NEIGHBORS
        for dx, dy in [

            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)

        ]:

            nx, ny = x + dx, y + dy

            if (
                0 <= nx < len(grid)
                and
                0 <= ny < len(grid[0])
            ):

                # BLOCKED CELL
                if grid[nx][ny] != 'X':

                    new_cost = (
                        len(path)
                        + 1
                        + heuristic((nx, ny), goal)
                    )

                    # RISKY ROAD
                    if grid[nx][ny] == 'R':

                        new_cost += 3

                    heapq.heappush(

                        pq,

                        (
                            new_cost,
                            (nx, ny),
                            path + [(x, y)]
                        )
                    )

    return None