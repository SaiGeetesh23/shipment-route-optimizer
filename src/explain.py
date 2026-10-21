
def explain_decision(
    recommendation: dict | None,
    ranked_routes: list[dict],
    rejected_routes: list[dict],
    constraints: dict,
) -> dict:
    """
    Generate evidence-based explanations for a route recommendation.

    All explanations are based on route metrics and actual
    constraint checks.
    """

    if recommendation is None:
        reasons = []

        if not rejected_routes:
            reasons.append(
                "No candidate routes were available for evaluation."
            )
        else:
            for route in rejected_routes:
                route_id = route.get("route_id", "Unknown route")
                rejection = route.get(
                    "rejection_reasons", "Unknown reason"
                )

                reasons.append(
                    f"{route_id} was rejected because: {rejection}."
                )

        return {
            "summary": (
                "No feasible route was found. "
                "No recommendation can satisfy all current constraints."
            ),
            "reasons": reasons,
            "comparison": [],
        }

    route_id = recommendation["route_id"]
    cost = float(recommendation["total_cost"])
    days = float(recommendation["transit_days"])
    risk = float(recommendation["risk_score"])

    reasons = [
        f"{route_id} was selected from "
        f"{len(ranked_routes)} feasible route(s)."
    ]

    reasons.append(
        f"Estimated cost is {cost:,.2f}, within the budget "
        f"limit of {constraints['max_budget']:,.2f}."
    )

    reasons.append(
        f"Estimated transit time is {days:.2f} days, "
        f"within the {constraints['max_transit_days']}-day deadline."
    )

    reasons.append(
        f"Risk score is {risk:.2f}/100, within the permitted "
        f"limit of {constraints['max_risk_score']}."
    )

    if len(ranked_routes) == 1:
        reasons.append(
            "This is the only feasible route. Its selection "
            "does not establish that it is better than every "
            "alternative on cost, time, and risk."
        )
    else:
        reasons.append(
            "Among feasible routes, this route has the lowest "
            "weighted score under the configured preferences."
        )

    comparison = []

    for alternative in ranked_routes:
        if alternative["route_id"] == route_id:
            continue

        alternative_id = alternative["route_id"]

        cost_difference = (
            float(alternative["total_cost"]) - cost
        )

        time_difference = (
            float(alternative["transit_days"]) - days
        )

        risk_difference = (
            float(alternative["risk_score"]) - risk
        )

        comparison.append({
            "route_id": alternative_id,
            "cost_difference": round(cost_difference, 2),
            "time_difference_days": round(time_difference, 2),
            "risk_difference": round(risk_difference, 2),
            "explanation": (
                f"Compared with {alternative_id}, "
                f"the recommended route costs "
                f"{abs(cost_difference):,.2f} "
                f"{'less' if cost_difference > 0 else 'more' if cost_difference < 0 else 'the same'}; "
                f"takes {abs(time_difference):.2f} "
                f"{'fewer' if time_difference > 0 else 'more' if time_difference < 0 else 'the same number of'} days; "
                f"and has a risk score "
                f"{abs(risk_difference):.2f} points "
                f"{'lower' if risk_difference > 0 else 'higher' if risk_difference < 0 else 'equal'}."
            ),
        })

    for route in rejected_routes:
        reasons.append(
            f"{route.get('route_id', 'Unknown route')} was rejected: "
            f"{route.get('rejection_reasons', 'constraint violation')}."
        )

    return {
        "summary": (
            f"{route_id} is the recommended route because it "
            "satisfies the shipment's mandatory constraints "
            "and ranks best among the feasible alternatives."
        ),
        "reasons": reasons,
        "comparison": comparison,
    }
