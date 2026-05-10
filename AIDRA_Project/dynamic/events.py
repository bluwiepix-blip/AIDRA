import random

def block_road(grid):
    for _ in range(10):
        x = random.randint(0, len(grid)-1)
        y = random.randint(0, len(grid[0])-1)

        if grid[x][y] == '.':
            grid[x][y] = 'X'
            return (x, y)

    return None