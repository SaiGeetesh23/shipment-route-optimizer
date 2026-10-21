
import pandas as pd

from src.constraints import filter_feasible_routes


def test_filters_routes_correctly():
    routes = pd.DataFrame([
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
            "total_cost": 700000,
            "transit_days": 15,
            "delay_probability": 0.30,
            "risk_score": 10,
        },
        {
            "route_id": "R4",
            "total_cost": 550000,
            "transit_days": 18,
            "delay_probability": 0.50,
            "risk_score": 55,
        },
    ])

    constraints = {
        "max_budget": 650000,
        "max_transit_days": 22,
        "max_delay_probability": 0.50,
        "max_risk_score": 40,
    }

    feasible, rejected = filter_feasible_routes(
        routes, constraints
    )

    assert set(feasible["route_id"]) == {"R2"}
    assert set(rejected["route_id"]) == {"R1", "R3", "R4"}

    
    assert (
        rejected.loc[
            rejected["route_id"] == "R1",
            "rejection_reasons",
        ].iloc[0]
        == "Transit deadline exceeded"
    )

    
    assert (
        rejected.loc[
            rejected["route_id"] == "R3",
            "rejection_reasons",
        ].iloc[0]
        == "Budget exceeded"
    )

    
    assert (
        rejected.loc[
            rejected["route_id"] == "R4",
            "rejection_reasons",
        ].iloc[0]
        == "Risk limit exceeded"
    )


def test_empty_routes():
    routes = pd.DataFrame(
        columns=[
            "route_id",
            "total_cost",
            "transit_days",
            "delay_probability",
            "risk_score",
        ]
    )

    constraints = {
        "max_budget": 650000,
        "max_transit_days": 22,
        "max_delay_probability": 0.50,
        "max_risk_score": 40,
    }

    feasible, rejected = filter_feasible_routes(
        routes, constraints
    )

    assert feasible.empty
    assert rejected.empty
