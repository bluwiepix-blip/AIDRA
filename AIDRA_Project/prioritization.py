def prioritize_victims(victims):
    priority_map = {
        "critical": 3,
        "moderate": 2,
        "minor": 1
    }

    return sorted(victims, key=lambda v: priority_map[v[1]], reverse=True)
