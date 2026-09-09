def evaluate_natal_promise(chart_obj, domain: str, event_type: str) -> str:
    """
    V5 Natal Promise Matrix: Answers 'Can this event occur in this chart?'
    Returns: STRONG_PROMISE, CONDITIONAL_PROMISE, WEAK_PROMISE, WITHHELD
    """
    if not chart_obj or not hasattr(chart_obj, 'planets') or not chart_obj.planets:
        return "CONDITIONAL_PROMISE"

    score = 0.5
    for p, pdata in chart_obj.planets.items():
        dignity = getattr(pdata, 'dignity', 'Neutral')
        if dignity in ["Exalted", "Moolatrikona", "Own Sign"]:
            score += 0.15
        elif dignity in ["Debilitated"]:
            score -= 0.15

    if score >= 0.75:
        return "STRONG_PROMISE"
    elif score >= 0.5:
        return "CONDITIONAL_PROMISE"
    elif score >= 0.3:
        return "WEAK_PROMISE"
    else:
        return "WITHHELD"
