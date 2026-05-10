def fuzzy_decision(risk_score, path_time, survival_probability=0.5):
    """Return a simple route label from fuzzy risk, time, and survival signals."""
    if risk_score >= 3 and path_time > 10 and survival_probability < 0.5:
        return "AVOID"
    if risk_score >= 1 or path_time > 12:
        return "RISKY"
    return "SAFE"


def fuzzy_route_score(metrics, ml_risk=0, survival_probability=0.5):
    """Lower score is better for route selection."""
    if not metrics or metrics.get("length") in (None, 999):
        return 9999.0

    length = metrics["length"]
    risk = metrics["risk"]
    time = metrics["time"]
    ml_penalty = 8 if ml_risk else 0
    survival_bonus = survival_probability * 10
    return round((length * 0.35) + (time * 0.30) + (risk * 4.0) + ml_penalty - survival_bonus, 2)
