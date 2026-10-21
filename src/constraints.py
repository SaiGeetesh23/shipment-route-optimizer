import math
import numbers

import pandas as pd


REQUIRED_ROUTE_COLUMNS = {
    "route_id",
    "total_cost",
    "transit_days",
    "delay_probability",
    "risk_score",
}

REQUIRED_CONSTRAINTS = {
    "max_budget",
    "max_transit_days",
    "max_delay_probability",
    "max_risk_score",
}

NUMERIC_ROUTE_COLUMNS = [
    "total_cost",
    "transit_days",
    "delay_probability",
    "risk_score",
]


def validate_inputs(
    routes: pd.DataFrame,
    constraints: dict,
) -> None:
    """Validate route data and shipment constraints."""

    if not isinstance(routes, pd.DataFrame):
        raise TypeError("routes must be a pandas DataFrame.")

    if not isinstance(constraints, dict):
        raise TypeError("constraints must be a dictionary.")

    missing_columns = REQUIRED_ROUTE_COLUMNS - set(routes.columns)
    if missing_columns:
        raise ValueError(
            f"Missing route columns: {sorted(missing_columns)}"
        )

    missing_constraints = REQUIRED_CONSTRAINTS - set(constraints)
    if missing_constraints:
        raise ValueError(
            f"Missing constraints: {sorted(missing_constraints)}"
        )

    # Validate constraints are real, finite, non-negative numbers.
    for key in REQUIRED_CONSTRAINTS:
        value = constraints[key]

        if isinstance(value, bool) or not isinstance(value, numbers.Real):
            raise ValueError(f"{key} must be numeric.")

        if not math.isfinite(float(value)):
            raise ValueError(f"{key} must be a finite numeric value.")

        if value < 0:
            raise ValueError(f"{key} must be non-negative.")

    if constraints["max_budget"] <= 0:
        raise ValueError("max_budget must be greater than zero.")

    if constraints["max_transit_days"] <= 0:
        raise ValueError("max_transit_days must be greater than zero.")

    if constraints["max_risk_score"] > 100:
        raise ValueError("max_risk_score must be between 0 and 100.")

    if constraints["max_delay_probability"] > 1:
        raise ValueError(
            "max_delay_probability must be between 0 and 1."
        )

    if routes.empty:
        return

    # Validate route metrics: numeric, finite, non-negative, and in range.
    for column in NUMERIC_ROUTE_COLUMNS:
        values = pd.to_numeric(routes[column], errors="coerce")

        if values.isna().any():
            raise ValueError(
                f"{column} contains missing or non-numeric values."
            )

        if not values.map(lambda value: math.isfinite(float(value))).all():
            raise ValueError(f"{column} must contain only finite values.")

        if (values < 0).any():
            raise ValueError(f"{column} cannot contain negative values.")

        if column == "delay_probability" and (values > 1).any():
            raise ValueError("delay_probability must be between 0 and 1.")

        if column == "risk_score" and (values > 100).any():
            raise ValueError("risk_score must be between 0 and 100.")

    if routes["route_id"].isna().any():
        raise ValueError("route_id cannot contain missing values.")

    if routes["route_id"].duplicated().any():
        raise ValueError("route_id values must be unique.")


def filter_feasible_routes(
    routes: pd.DataFrame,
    constraints: dict,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split routes into feasible and rejected groups.

    Returns:
        feasible_routes: routes satisfying all hard constraints
        rejected_routes: routes with explicit rejection reasons
    """

    validate_inputs(routes, constraints)

    result = routes.copy()

    # Use numeric values in comparisons, even if CSV columns were loaded
    # as strings.
    for column in NUMERIC_ROUTE_COLUMNS:
        result[column] = pd.to_numeric(result[column], errors="raise")

    if result.empty:
        result["budget_ok"] = pd.Series(dtype=bool)
        result["time_ok"] = pd.Series(dtype=bool)
        result["delay_ok"] = pd.Series(dtype=bool)
        result["risk_ok"] = pd.Series(dtype=bool)
        result["rejection_reasons"] = pd.Series(dtype=str)
        return result, result.copy()

    budget_ok = result["total_cost"] <= constraints["max_budget"]
    time_ok = result["transit_days"] <= constraints["max_transit_days"]
    delay_ok = (
        result["delay_probability"] <= constraints["max_delay_probability"]
    )
    risk_ok = result["risk_score"] <= constraints["max_risk_score"]

    result["budget_ok"] = budget_ok
    result["time_ok"] = time_ok
    result["delay_ok"] = delay_ok
    result["risk_ok"] = risk_ok

    # Record every reason a route was rejected.
    result["rejection_reasons"] = result.apply(
        lambda row: "; ".join(
            reason
            for condition, reason in [
                (row["budget_ok"], "Budget exceeded"),
                (row["time_ok"], "Transit deadline exceeded"),
                (row["delay_ok"], "Delay probability exceeded"),
                (row["risk_ok"], "Risk limit exceeded"),
            ]
            if not condition
        ),
        axis=1,
    )

    feasible_mask = budget_ok & time_ok & delay_ok & risk_ok

    feasible_routes = result.loc[feasible_mask].copy()
    rejected_routes = result.loc[~feasible_mask].copy()

    return feasible_routes, rejected_routes
