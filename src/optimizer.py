import pandas as pd

from src.constraints import filter_feasible_routes
from src.scoring import score_routes
from src.explain import explain_decision


def optimize_shipment(
    routes: pd.DataFrame,
    constraints: dict,
    weights: dict,
) -> dict:
    """Evaluate routes, rank feasible options, and explain the result."""

    feasible_routes, rejected_routes = filter_feasible_routes(
        routes, constraints
    )

    rejected_records = rejected_routes.to_dict(orient="records")

    if feasible_routes.empty:
        explanation = explain_decision(
            recommendation=None,
            ranked_routes=[],
            rejected_routes=rejected_records,
            constraints=constraints,
        )

        return {
            "status": "NO_FEASIBLE_ROUTE",
            "recommended_route": None,
            "ranked_routes": [],
            "rejected_routes": rejected_records,
            "explanation": explanation,
        }

    ranked_routes = score_routes(feasible_routes, weights)
    ranked_records = ranked_routes.to_dict(orient="records")

    recommendation = ranked_records[0]

    explanation = explain_decision(
        recommendation=recommendation,
        ranked_routes=ranked_records,
        rejected_routes=rejected_records,
        constraints=constraints,
    )

    return {
        "status": "SUCCESS",
        "recommended_route": recommendation,
        "ranked_routes": ranked_records,
        "rejected_routes": rejected_records,
        "explanation": explanation,
    }
