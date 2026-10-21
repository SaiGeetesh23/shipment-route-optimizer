
import numpy as np
import pandas as pd


METRICS = ["total_cost", "transit_days", "risk_score"]
REFERENCE_SCALES = {
    "total_cost": (0.0, 1_000_000.0),
    "transit_days": (0.0, 60.0),
    "risk_score": (0.0, 100.0),
}


def normalize_metrics(
    routes: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normalize cost, transit time, and risk to [0, 1].

    All three metrics are costs: lower is better.

    Fixed reference scales prevent a single feasible route
    from automatically receiving a score of zero.

    Values are clipped to [0, 1] so metrics outside the
    reference range do not produce scores outside that range.
    """

    if routes.empty:
        return routes.copy()

    missing = set(METRICS) - set(routes.columns)

    if missing:
        raise ValueError(
            f"Missing metric columns: {sorted(missing)}"
        )

    result = routes.copy()

    for metric in METRICS:
        values = pd.to_numeric(
            result[metric], errors="coerce"
        )

        if values.isna().any() or not np.isfinite(values).all():
            raise ValueError(
                f"{metric} must contain finite numeric values."
            )

        minimum, maximum = REFERENCE_SCALES[metric]

        normalized_values = (
            (values - minimum) / (maximum - minimum)
        )

        result[f"{metric}_norm"] = normalized_values.clip(
            lower=0.0,
            upper=1.0,
        )

    return result


def validate_weights(weights: dict) -> None:
    """Validate optimization weights."""

    required = {"cost", "time", "risk"}

    if not isinstance(weights, dict) or set(weights) != required:
        raise ValueError(
            "Weights must contain exactly cost, time, and risk."
        )

    values = list(weights.values())

    if any(
        isinstance(value, bool)
        or not isinstance(value, (int, float, np.number))
        or not np.isfinite(value)
        for value in values
    ):
        raise ValueError("Weights must be finite numbers.")

    if any(value < 0 for value in values):
        raise ValueError("Weights cannot be negative.")

    if not np.isclose(sum(values), 1.0):
        raise ValueError("Weights must sum to 1.")


def score_routes(
    routes: pd.DataFrame,
    weights: dict,
) -> pd.DataFrame:
    """
    Calculate a weighted score for each feasible route.

    Lower scores indicate more preferred routes.
    The fixed normalization scales support scoring when
    only one feasible route remains.
    """

    validate_weights(weights)

    if routes.empty:
        result = routes.copy()
        result["weighted_score"] = pd.Series(dtype=float)
        result["rank"] = pd.Series(dtype=int)
        return result

    if "route_id" not in routes.columns:
        raise ValueError("Missing required column: route_id")

    normalized = normalize_metrics(routes)

    normalized["weighted_score"] = (
        weights["cost"] * normalized["total_cost_norm"]
        + weights["time"] * normalized["transit_days_norm"]
        + weights["risk"] * normalized["risk_score_norm"]
    )

    normalized = normalized.sort_values(
        by=["weighted_score", "total_cost", "route_id"],
        ascending=True,
    ).reset_index(drop=True)

    normalized["rank"] = np.arange(
        1, len(normalized) + 1
    )

    return normalized
