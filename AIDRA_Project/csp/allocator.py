from search.astar import astar


# ==========================================
# SEVERITY SCORE
# ==========================================
def severity_score(level):

    scores = {
        "critical": 10,
        "moderate": 6,
        "minor": 3
    }

    return scores[level]


# ==========================================
# DYNAMIC AMBULANCE ALLOCATION
# ==========================================
def allocate(victims, grid, ambulance_positions):

    allocation = {}

    # COPY POSITIONS
    available = ambulance_positions.copy()

    # PROCESS EACH VICTIM
    for victim, severity in victims:

        best_ambulance = None

        best_cost = float("inf")

        # CHECK EACH AMBULANCE
        for amb_id, amb_pos in available.items():

            # FIND PATH
            path = astar(
                grid,
                amb_pos,
                victim
            )

            # INVALID PATH
            if not path:
                continue

            # DISTANCE
            distance = len(path)

            # RISK
            risk = sum(
                1
                for x, y in path
                if grid[x][y] == 'R'
            )

            # ==========================================
            # COST FUNCTION
            # ==========================================
            cost = (
                distance
                + (risk * 2)
                - severity_score(severity)
            )

            # BEST AMBULANCE
            if cost < best_cost:

                best_cost = cost

                best_ambulance = amb_id

        # ASSIGN
        allocation[victim] = best_ambulance

        # UPDATE POSITION
        if best_ambulance:
            available[best_ambulance] = victim

    return allocation