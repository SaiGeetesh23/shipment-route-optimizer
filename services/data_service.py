"""Read and validate the application's CSV data."""
import pandas as pd
import streamlit as st
from config import SHIPMENTS_PATH, ROUTES_PATH

REQUIRED_SHIPMENT_COLUMNS = {
    "shipment_id", "max_budget", "max_transit_days", "max_risk_score"
}
REQUIRED_ROUTE_COLUMNS = {
    "shipment_id", "route_id", "total_cost", "transit_days",
    "delay_probability", "risk_score"
}

@st.cache_data
def load_data():
    """Load CSV files once per Streamlit cache key."""
    shipments = pd.read_csv(SHIPMENTS_PATH)
    routes = pd.read_csv(ROUTES_PATH)
    validate_data(shipments, routes)
    return shipments, routes

def validate_data(shipments: pd.DataFrame, routes: pd.DataFrame) -> None:
    """Raise a clear error if required input data is missing."""
    if shipments.empty:
        raise ValueError("No shipments are available in data/shipments.csv.")
    missing_shipments = REQUIRED_SHIPMENT_COLUMNS - set(shipments.columns)
    if missing_shipments:
        raise ValueError(
            f"shipments.csv is missing required columns: {sorted(missing_shipments)}"
        )
    missing_routes = REQUIRED_ROUTE_COLUMNS - set(routes.columns)
    if missing_routes:
        raise ValueError(
            f"routes.csv is missing required columns: {sorted(missing_routes)}"
        )
