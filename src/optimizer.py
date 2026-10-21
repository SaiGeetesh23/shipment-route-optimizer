
# import pandas as pd

# from src.constraints import filter_feasible_routes
# from src.scoring import score_routes


# def optimize_shipment(
#     routes: pd.DataFrame,
#     constraints: dict,
#     weights: dict,
# ) -> dict:
#     """
#     Evaluate candidate routes and recommend the best feasible route.

#     Returns a dictionary containing the recommendation,
#     ranked alternatives, rejected routes, and status.
#     """

#     feasible_routes, rejected_routes = filter_feasible_routes(
#         routes, constraints
#     )

#     # No route satisfies every hard constraint.
#     if feasible_routes.empty:
#         return {
#             "status": "NO_FEASIBLE_ROUTE",
#             "recommended_route": None,
#             "ranked_routes": [],
#             "rejected_routes": rejected_routes.to_dict(
#                 orient="records"
#             ),
#             "message": (
#                 "No candidate route satisfies all mandatory "
#                 "constraints. Review the rejected routes or "
#                 "revise the shipment requirements."
#             ),
#         }

#     ranked_routes = score_routes(feasible_routes, weights)

#     recommended_route = ranked_routes.iloc[0].to_dict()

#     return {
#         "status": "SUCCESS",
#         "recommended_route": recommended_route,
#         "ranked_routes": ranked_routes.to_dict(
#             orient="records"
#         ),
#         "rejected_routes": rejected_routes.to_dict(
#             orient="records"
#         ),
#         "message": "A feasible route was successfully selected.",
#     }


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
