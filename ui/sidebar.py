"""Shipment selector and operating-limit controls."""
import streamlit as st
from config import DEFAULT_SHIPMENT_ID

def select_shipment(shipments):
    ids = shipments["shipment_id"].astype(str).tolist()
    index = ids.index(DEFAULT_SHIPMENT_ID) if DEFAULT_SHIPMENT_ID in ids else 0
    return st.selectbox("Shipment ID", options=ids, index=index, key="shipment_selector")

def render_constraints(shipment):
    st.markdown('<div class="aiqon-section-kicker">01 / Set the operating limits</div>', unsafe_allow_html=True)
    st.header("Optimization constraints")
    st.caption("Routes that breach any hard constraint are excluded before scoring.")
    default_budget = float(shipment["max_budget"])
    default_days = float(shipment["max_transit_days"])
    default_risk = max(1, min(10, int(round(float(shipment["max_risk_score"]) / 10))))
    cost_col, time_col, risk_col, delay_col = st.columns(4)

    with cost_col:
        with st.container(border=True):
            st.markdown("#### Budget ceiling")
            max_cost = st.number_input("Maximum shipment cost (₹)", min_value=0.0,
                max_value=100_000_000.0, value=default_budget, step=10_000.0,
                format="%.0f", help="Routes costing more than this limit are rejected.")
            st.caption("Hard constraint · lower is stricter")
    with time_col:
        with st.container(border=True):
            st.markdown("#### Delivery deadline")
            max_days = st.number_input("Maximum transit time (days)", min_value=1.0,
                max_value=60.0, value=default_days, step=0.5,
                help="Routes exceeding this duration are rejected.")
            st.caption("Hard constraint · shorter is stricter")
    with risk_col:
        with st.container(border=True):
            st.markdown("#### Risk tolerance")
            max_risk_10 = st.slider("Maximum risk (1–10)", min_value=1, max_value=10,
                value=default_risk, help="A lower limit is stricter. Internal scale is 0–100.")
            st.caption(f"Internal optimizer limit · {max_risk_10 * 10}/100")
    with delay_col:
        with st.container(border=True):
            st.markdown("#### Delay tolerance")
            delay_pct = st.slider("Maximum delay probability (%)", min_value=0,
                max_value=100, value=30, step=5,
                help="Routes with a higher estimated delay probability will be rejected.")
            st.caption("Hard constraint · lower is stricter")

    max_risk_100 = max_risk_10 * 10
    st.markdown(f"""<div class="aiqon-note"><strong>Active rules</strong> ·
    Cost ≤ ₹{max_cost:,.0f} · Transit ≤ {max_days:g} days ·
    Risk ≤ {max_risk_10}/10 · Delay probability ≤ {delay_pct}%</div>""",
        unsafe_allow_html=True)
    return {
        "max_budget": float(max_cost),
        "max_transit_days": float(max_days),
        "max_risk_score": float(max_risk_100),
        "max_delay_probability": delay_pct / 100.0,
    }, {"cost": max(0.0, float(shipment.get("cost_weight", .40))),
         "time": max(0.0, float(shipment.get("time_weight", .35))),
         "risk": max(0.0, float(shipment.get("risk_weight", .25)))}, {
        "max_cost": max_cost, "max_days": max_days, "max_risk_10": max_risk_10,
        "delay_pct": delay_pct, "max_risk_100": max_risk_100,
    }
