def calculate_risk(open_ports):
    risk_weights = {
        21: 4,
        22: 2,
        23: 6,
        80: 1,
        443: 1,
        3306: 5,
        3389: 6
    }

    score = sum(risk_weights.get(p, 1) for p in open_ports)

    if score <= 5:
        severity = "Low"
    elif score <= 15:
        severity = "Medium"
    else:
        severity = "High"

    return {
        "score": score,
        "severity": severity,
        "exposed_ports": len(open_ports)
    }