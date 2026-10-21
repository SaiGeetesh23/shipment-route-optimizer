"""Application-level preparation around the deterministic optimizer."""
import pandas as pd
from src.optimizer import optimize_shipment

def as_dataframe(value) -> pd.DataFrame:
    """Normalize optimizer output to a DataFrame."""
    if isinstance(value, pd.DataFrame):
        return value.copy()
    if value is None:
        return pd.DataFrame()
    if isinstance(value, dict):
        return pd.DataFrame([value])
    if isinstance(value, list):
        return pd.DataFrame(value)
    return pd.DataFrame()

def normalize_route_record(route):
    """Normalize a route dict/Series to a dictionary."""
    if route is None:
        return None
    if isinstance(route, pd.Series):
        return route.to_dict()
    if isinstance(route, dict):
        return route
    if hasattr(route, "to_dict"):
        return route.to_dict()
    return None

def format_route_path(route) -> str:
    path = route.get("hubs") if route is not None else None
    if path is None or pd.isna(path) or not str(path).strip():
        return "Route path not provided"
    return str(path).replace(" -> ", "  →  ")

def rejection_text(value) -> str:
    if value is None or pd.isna(value) or not str(value).strip():
        return "No rejection reason recorded."
    return str(value)

def run_optimization(candidate_routes, constraints, weights):
    """Call the existing optimizer and prepare a unified comparison table."""
    result = optimize_shipment(candidate_routes, constraints, weights)
    ranked = as_dataframe(result.get("ranked_routes"))
    rejected = as_dataframe(result.get("rejected_routes"))

    feasible_ids = set()
    if not ranked.empty and "route_id" in ranked:
        feasible_ids = set(ranked["route_id"].dropna())

    rejection_lookup = {}
    if not rejected.empty and "route_id" in rejected:
        for _, row in rejected.iterrows():
            rejection_lookup[row["route_id"]] = row.get(
                "rejection_reasons", "Constraint violation"
            )

    comparison = candidate_routes.copy()
    comparison["status"] = comparison["route_id"].apply(
        lambda rid: "Feasible" if rid in feasible_ids else "Rejected"
    )
    comparison["rejection_reasons"] = comparison["route_id"].map(
        rejection_lookup
    ).fillna("")

    score_cols = [c for c in ["route_id", "weighted_score", "rank"] if c in ranked]
    comparison = comparison.drop(
        columns=[c for c in ["weighted_score", "rank"] if c in comparison],
        errors="ignore",
    )
    if score_cols:
        comparison = comparison.merge(ranked[score_cols], on="route_id", how="left")

    comparison["risk_out_of_10"] = comparison["risk_score"] / 10
    comparison["delay_probability_pct"] = comparison["delay_probability"] * 100
    recommended = normalize_route_record(result.get("recommended_route"))
    return {
        "result": result,
        "ranked_routes": ranked,
        "rejected_routes": rejected,
        "comparison": comparison,
        "recommended": recommended,
    }
