
from pathlib import Path

import numpy as np
import pandas as pd


RANDOM_SEED = 42
NUM_SHIPMENTS = 30
ROUTES_PER_SHIPMENT = 4

rng = np.random.default_rng(RANDOM_SEED)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


LOCATIONS = [
    ("Hyderabad", "London"),
    ("Mumbai", "Rotterdam"),
    ("Chennai", "Singapore"),
    ("Delhi", "New York"),
    ("Bengaluru", "Frankfurt"),
    ("Shanghai", "Los Angeles"),
    ("Tokyo", "Sydney"),
    ("Dubai", "Amsterdam"),
    ("Kolkata", "Hamburg"),
    ("Singapore", "Toronto"),
]

HUBS = [
    ["Mumbai", "Suez Canal"],
    ["Colombo", "Suez Canal"],
    ["Singapore", "Rotterdam"],
    ["Dubai", "Mediterranean Hub"],
    ["Hong Kong", "Panama Canal"],
    ["Jebel Ali", "Antwerp"],
    ["Singapore", "Suez Canal"],
    ["Colombo", "Rotterdam"],
]

ROUTE_PROFILES = [
    {
        "profile": "economical",
        "cost_multiplier": 0.80,
        "time_multiplier": 1.25,
        "risk_bias": 12,
    },
    {
        "profile": "express",
        "cost_multiplier": 1.30,
        "time_multiplier": 0.75,
        "risk_bias": -8,
    },
    {
        "profile": "balanced",
        "cost_multiplier": 1.00,
        "time_multiplier": 1.00,
        "risk_bias": -3,
    },
    {
        "profile": "alternative",
        "cost_multiplier": 1.10,
        "time_multiplier": 0.95,
        "risk_bias": 5,
    },
]


shipment_rows = []
route_rows = []

for shipment_number in range(1, NUM_SHIPMENTS + 1):
    shipment_id = f"SH{shipment_number:03d}"

    origin, destination = LOCATIONS[
        (shipment_number - 1) % len(LOCATIONS)
    ]

    base_cost = rng.uniform(300_000, 800_000)
    base_days = rng.uniform(12, 30)

    max_budget = round(
        base_cost * rng.uniform(1.00, 1.35), 2
    )

    max_transit_days = round(
        base_days * rng.uniform(0.95, 1.35), 1
    )

    max_risk_score = round(
        rng.uniform(35, 65), 1
    )

    weights = rng.dirichlet([4, 3, 3])

    shipment_rows.append(
        {
            "shipment_id": shipment_id,
            "origin": origin,
            "destination": destination,
            "max_budget": max_budget,
            "max_transit_days": max_transit_days,
            "max_risk_score": max_risk_score,
            "cost_weight": round(float(weights[0]), 4),
            "time_weight": round(float(weights[1]), 4),
            "risk_weight": round(float(weights[2]), 4),
        }
    )

    for route_number, profile in enumerate(
        ROUTE_PROFILES, start=1
    ):
        cost = (
            base_cost * profile["cost_multiplier"]
            * rng.uniform(0.95, 1.05)
        )

        transit_days = (
            base_days * profile["time_multiplier"]
            * rng.uniform(0.95, 1.05)
        )

        congestion_risk = float(rng.uniform(5, 85))
        geopolitical_risk = float(rng.uniform(5, 75))
        weather_risk = float(rng.uniform(5, 80))
        security_risk = float(rng.uniform(5, 70))

        risk_score = (
            0.25 * congestion_risk
            + 0.30 * geopolitical_risk
            + 0.20 * weather_risk
            + 0.25 * security_risk
            + profile["risk_bias"]
        )

        risk_score = float(np.clip(risk_score, 0, 100))

        delay_logit = (
            -3.0
            + 0.025 * congestion_risk
            + 0.018 * geopolitical_risk
            + 0.015 * weather_risk
        )

        delay_probability = 1 / (
            1 + np.exp(-delay_logit)
        )

        delay_probability = float(
            np.clip(delay_probability, 0.01, 0.85)
        )

        hub_list = HUBS[
            (shipment_number + route_number - 2)
            % len(HUBS)
        ]

        route_rows.append(
            {
                "route_id": f"{shipment_id}_R{route_number}",
                "shipment_id": shipment_id,
                "profile": profile["profile"],
                "hubs": " -> ".join(
                    [origin] + hub_list + [destination]
                ),
                "total_cost": round(float(cost), 2),
                "transit_days": round(float(transit_days), 2),
                "delay_probability": round(
                    delay_probability, 4
                ),
                "congestion_risk": round(congestion_risk, 2),
                "geopolitical_risk": round(
                    geopolitical_risk, 2
                ),
                "weather_risk": round(weather_risk, 2),
                "security_risk": round(security_risk, 2),
                "risk_score": round(risk_score, 2),
            }
        )


shipments_df = pd.DataFrame(shipment_rows)
routes_df = pd.DataFrame(route_rows)

shipments_path = DATA_DIR / "shipments.csv"
routes_path = DATA_DIR / "routes.csv"

shipments_df.to_csv(shipments_path, index=False)
routes_df.to_csv(routes_path, index=False)

print("Synthetic dataset generated successfully!")
print(f"Shipments: {len(shipments_df)}")
print(f"Routes: {len(routes_df)}")
print(f"Shipments file: {shipments_path}")
print(f"Routes file: {routes_path}")

print("\nShipment preview:")
print(shipments_df.head())

print("\nRoute preview:")
print(
    routes_df[
        [
            "route_id",
            "profile",
            "total_cost",
            "transit_days",
            "delay_probability",
            "risk_score",
        ]
    ].head(8)
)
