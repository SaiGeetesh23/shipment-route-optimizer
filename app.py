"""Aiqon Streamlit entry point: orchestrates UI, services, and optimizer."""
import streamlit as st

from config import PAGE_TITLE, PAGE_ICON, DEFAULT_SHIPMENT_ID
from services.data_service import load_data
from services.optimization_service import run_optimization
from ui.styles import apply_styles
from ui.sidebar import select_shipment, render_constraints
from ui.summary import render_summary
from ui.route_inspection import render_route_inspection
from ui.charts import render_charts
from ui.route_table import render_route_table
from ui.chatbot import render_chatbot

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide",
                   initial_sidebar_state="collapsed")
apply_styles()

st.markdown("""
<div class="aiqon-hero">
  <div class="aiqon-brand">AIQON / OPERATIONS INTELLIGENCE</div>
  <div class="aiqon-hero-title">Shipment Route Intelligence</div>
  <p class="aiqon-hero-subtitle">Evaluate candidate routes against hard constraints, understand
  the cost–time–risk trade-off, and inspect the optimizer's decision.</p>
</div>""", unsafe_allow_html=True)

try:
    shipments, routes = load_data()
except Exception as exc:
    st.error(f"Could not load project data: {exc}")
    st.stop()

shipment_id = select_shipment(shipments)
shipment_rows = shipments[shipments["shipment_id"].astype(str) == str(shipment_id)]
if shipment_rows.empty:
    st.error(f"Shipment {shipment_id} could not be found.")
    st.stop()
shipment = shipment_rows.iloc[0]
candidate_routes = routes[routes["shipment_id"].astype(str) == str(shipment_id)].copy()
if candidate_routes.empty:
    st.warning(f"No candidate routes found for shipment {shipment_id}.")
    st.stop()

origin = shipment.get("origin", "Origin not specified")
destination = shipment.get("destination", "Destination not specified")
a, b = st.columns([2.2, 1.8])
with a:
    st.markdown('<div class="aiqon-section-kicker">Current shipment</div>', unsafe_allow_html=True)
    st.markdown("### Shipment overview")
    st.markdown(f"**{origin}** <span style='color:#A79786'>→</span> **{destination}**", unsafe_allow_html=True)
    st.caption(f"{len(candidate_routes)} candidate routes available")
with b:
    st.markdown('<div class="aiqon-section-kicker">Route selection</div>', unsafe_allow_html=True)
    st.markdown(f"### {shipment_id}")
st.divider()

constraints, weights, controls = render_constraints(shipment)
weight_total = sum(weights.values())
if weight_total <= 0:
    st.error("The shipment's optimization weights must have a positive sum.")
    st.stop()
weights = {name: value / weight_total for name, value in weights.items()}

try:
    prepared = run_optimization(candidate_routes, constraints, weights)
except Exception as exc:
    st.error(f"The optimizer failed: {exc}")
    st.stop()

result = prepared["result"]
comparison = prepared["comparison"]
recommended = prepared["recommended"]

scenario_key = (
    str(shipment_id), float(controls["max_cost"]), float(controls["max_days"]),
    int(controls["max_risk_10"]), int(controls["delay_pct"]),
)

render_summary(result, recommended, controls)
render_route_inspection(comparison, recommended)
render_charts(comparison, controls)
render_route_table(comparison)
render_chatbot(shipment_id, scenario_key, constraints, weights, result, comparison)

st.divider()
st.markdown("""
<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;
color:#A79786;font-size:.78rem;padding:4px 0 12px">
<span>AIQON · Route Intelligence</span>
<span>Deterministic optimization · LLM-assisted explanation</span>
</div>""", unsafe_allow_html=True)
