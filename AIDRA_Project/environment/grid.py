GRID_SIZE = 10


def create_grid():

    grid = [
        ['.' for _ in range(GRID_SIZE)]
        for _ in range(GRID_SIZE)
    ]

    # MORE obstacles to increase replanning chance
    obstacles = [
        (2, 2), (2, 3), (3, 3), (6, 2),
        (4, 7), (7, 8), (5, 6), (8, 3),
        (1, 2), (8, 7)  # Keep known patient start cells reachable.
    ]

    for x, y in obstacles:
        grid[x][y] = 'X'

    risky = [
        (1, 5), (2, 5), (7, 7),
        (4, 2), (5, 2), (3, 8), (6, 6)
    ]

    for x, y in risky:
        if grid[x][y] == '.':
            grid[x][y] = 'R'

    empty_cells = sum(1 for row in grid for cell in row if cell == '.')
    print(f"Grid: {GRID_SIZE}x{GRID_SIZE} | Empty: {empty_cells} | Obstacles: {len(obstacles)} | Risk: {len(risky)}")

    return grid
