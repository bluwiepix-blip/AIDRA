# -*- coding: utf-8 -*-
"""
Created on Fri May  8 13:48:21 2026

@author: DELL
"""

from collections import deque

def bfs(grid, start, goal):
    """
    Breadth-First Search for pathfinding
    Returns path from start to goal or None if no path exists
    """
    if start == goal:
        return [start]
    
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        (x, y), path = queue.popleft()
        
        # Check all 4 directions
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if not (0 <= nx < rows and 0 <= ny < cols):
                continue
            
            # Check if goal reached
            if (nx, ny) == goal:
                return path + [(nx, ny)]
            
            # Check if valid and unvisited
            if grid[nx][ny] != 'X' and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))
    
    return None  # No path found