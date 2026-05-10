def analyze_path(path, grid):
    if not path:
        return {"length": None, "risk": None, "time": None}

    length = len(path)
    risk = 0
    time = 0

    for x, y in path:
        if grid[x][y] == 'R':
            risk += 1
            time += 3
        else:
            time += 1

    return {"length": length, "risk": risk, "time": time}


def safe(v):
    return v if v is not None else "N/A"


def print_section(title, subtitle=None):
    """Print a clear console section header."""
    width = 92
    print("\n" + "=" * width)
    print(title.center(width))
    if subtitle:
        print(subtitle.center(width))
    print("=" * width)


def print_table(headers, rows, title=None, subtitle=None):
    """Print a readable dependency-free table with automatic column widths."""
    if title:
        print_section(title, subtitle)

    text_rows = [[str(value) for value in row] for row in rows]
    widths = [len(str(header)) for header in headers]
    for row in text_rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))

    line = "+" + "+".join("-" * (width + 2) for width in widths) + "+"
    print(line)
    print("| " + " | ".join(str(header).ljust(widths[index]) for index, header in enumerate(headers)) + " |")
    print(line)
    for row in text_rows:
        print("| " + " | ".join(value.ljust(widths[index]) for index, value in enumerate(row)) + " |")
    print(line)


def print_comparison(victim, bfs, astar, greedy, hill, dfs, grid):

    bfs_d = analyze_path(bfs, grid)
    astar_d = analyze_path(astar, grid)
    greedy_d = analyze_path(greedy, grid)
    hill_d = analyze_path(hill, grid)
    dfs_d = analyze_path(dfs, grid)

    print("\n================= DECISION TABLE =================")
    print(f"Victim: {victim}")
    print("--------------------------------------------------")
    print(f"{'Algo':<10}{'Length':<10}{'Time':<10}{'Risk':<10}")
    print("--------------------------------------------------")

    print(f"{'BFS':<10}{safe(bfs_d['length']):<10}{safe(bfs_d['time']):<10}{safe(bfs_d['risk']):<10}")
    print(f"{'A*':<10}{safe(astar_d['length']):<10}{safe(astar_d['time']):<10}{safe(astar_d['risk']):<10}")
    print(f"{'Greedy':<10}{safe(greedy_d['length']):<10}{safe(greedy_d['time']):<10}{safe(greedy_d['risk']):<10}")
    print(f"{'Hill':<10}{safe(hill_d['length']):<10}{safe(hill_d['time']):<10}{safe(hill_d['risk']):<10}")
    print(f"{'DFS':<10}{safe(dfs_d['length']):<10}{safe(dfs_d['time']):<10}{safe(dfs_d['risk']):<10}")

    print("--------------------------------------------------")

    return bfs_d, astar_d, greedy_d, hill_d, dfs_d


def print_algorithm_table(rows, title="ALGORITHM COMPARISON TABLE"):
    """Print a dependency-free console table for route comparison."""
    headers = ["Algorithm", "Length", "Time", "Risk", "KNN Risk", "NB Survival", "Fuzzy Score", "Decision"]
    table_rows = []
    for row in rows:
        table_rows.append([
            row["algorithm"],
            row["length"],
            row["time"],
            row["risk"],
            row["knn_risk"],
            row["nb_survival"],
            row["fuzzy"],
            "SELECTED" if row.get("selected") else "-",
        ])

    print_table(headers, table_rows, title)
