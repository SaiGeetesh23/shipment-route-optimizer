"""Recommended-route summary and KPI cards."""
import streamlit as st
from services.optimization_service import format_route_path

def render_summary(result, recommended, controls):
    st.markdown('<div class="aiqon-section-kicker">02 / Optimizer output</div>', unsafe_allow_html=True)
    st.header("Route decision")
    if result.get("status") != "SUCCESS" or recommended is None:
        st.warning("No route satisfies all current constraints. Review rejected routes or adjust the operating limits.")
        return

    rid = str(recommended.get("route_id", "Unknown"))
    left, right = st.columns([1.05, 2.2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown('<div class="aiqon-route-label">Recommended route</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="aiqon-route-id">{rid}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="aiqon-route-path">{format_route_path(recommended)}</div>', unsafe_allow_html=True)
            st.divider()
            st.markdown("**Why this route?**")
            st.write("It passed the hard constraints and ranked first under the configured cost, time, and risk weights.")
            if recommended.get("weighted_score") is not None:
                st.metric("Weighted score", f"{float(recommended['weighted_score']):.4f}",
                          help="Lower is better among feasible routes.")
    with right:
        st.markdown("#### Recommended route at a glance")
        cols = st.columns(4)
        cols[0].metric("Total cost", f"₹{float(recommended['total_cost']):,.0f}")
        cols[1].metric("Transit time", f"{float(recommended['transit_days']):.2f} days")
        cols[2].metric("Delay probability", f"{float(recommended['delay_probability']):.1%}")
        cols[3].metric("Risk score", f"{float(recommended['risk_score']) / 10:.1f}/10")
        budget_left = controls["max_cost"] - float(recommended["total_cost"])
        time_left = controls["max_days"] - float(recommended["transit_days"])
        risk_left = controls["max_risk_100"] - float(recommended["risk_score"])
        delay_left = controls["delay_pct"] / 100 - float(recommended["delay_probability"])
        st.markdown("#### Remaining constraint headroom")
        cols = st.columns(4)
        cols[0].metric("Budget remaining", f"₹{budget_left:,.0f}")
        cols[1].metric("Time remaining", f"{time_left:.2f} days")
        cols[2].metric("Risk remaining", f"{risk_left / 10:.1f} pts")
        cols[3].metric("Delay margin", f"{delay_left * 100:.1f} pp")
