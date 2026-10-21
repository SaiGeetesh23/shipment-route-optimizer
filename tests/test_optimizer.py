
import pandas as pd

from src.optimizer import optimize_shipment


CONSTRAINTS = {
    "max_budget": 650000,
    "max_transit_days": 22,
    "max_delay_probability": 0.50,
    "max_risk_score": 30,
}

WEIGHTS = {
    "cost": 0.40,
    "time": 0.35,
    "risk": 0.25,
}


def make_routes():
    return pd.DataFrame([
        {
            "route_id": "R1",
            "total_cost": 500000,
            "transit_days": 25,
            "delay_probability": 0.20,
            "risk_score": 20,
        },
        {
            "route_id": "R2",
            "total_cost": 600000,
            "transit_days": 20,
            "delay_probability": 0.40,
            "risk_score": 25,
        },
        {
            "route_id": "R3",
            "total_cost": 550000,
            "transit_days": 18,
            "delay_probability": 0.30,
            "risk_score": 15,
        },
    ])


def test_recommends_best_feasible_route():
    result = optimize_shipment(
        make_routes(), CONSTRAINTS, WEIGHTS
    )

    assert result["status"] == "SUCCESS"
    assert result["recommended_route"]["route_id"] == "R3"

    assert len(result["ranked_routes"]) == 2
    assert len(result["rejected_routes"]) == 1


def test_returns_no_feasible_route():
    routes = make_routes()

    routes["total_cost"] = 900000

    result = optimize_shipment(
        routes, CONSTRAINTS, WEIGHTS
    )

    assert result["status"] == "NO_FEASIBLE_ROUTE"
    assert result["recommended_route"] is None
    assert len(result["rejected_routes"]) == 3


def test_invalid_weights_are_rejected():
    invalid_weights = {
        "cost": 0.5,
        "time": 0.5,
        "risk": 0.5,
    }

    try:
        optimize_shipment(
            make_routes(), CONSTRAINTS, invalid_weights
        )
        assert False, "Expected ValueError"
    except ValueError:
        pass
