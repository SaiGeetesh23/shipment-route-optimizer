"""Detailed comparison table for all candidate routes."""
import streamlit as st

def render_route_table(comparison):
    st.divider()
    st.markdown('<div class="aiqon-section-kicker">05 / Detailed data</div>', unsafe_allow_html=True)
    st.header("Route evaluation table")
    columns = [c for c in [
        "route_id", "profile", "hubs", "total_cost", "transit_days",
        "delay_probability_pct", "risk_out_of_10", "weighted_score", "rank",
        "status", "rejection_reasons"
    ] if c in comparison.columns]
    table = comparison[columns].copy().rename(columns={
        "route_id":"Route", "profile":"Profile", "hubs":"Route path",
        "total_cost":"Cost (₹)", "transit_days":"Transit (days)",
        "delay_probability_pct":"Delay probability (%)", "risk_out_of_10":"Risk (0–10)",
        "weighted_score":"Weighted score", "rank":"Feasible rank",
        "status":"Status", "rejection_reasons":"Rejection reason"
    })
    st.dataframe(table, width="stretch", hide_index=True, column_config={
        "Cost (₹)": st.column_config.NumberColumn(format="₹%.0f"),
        "Transit (days)": st.column_config.NumberColumn(format="%.2f"),
        "Delay probability (%)": st.column_config.NumberColumn(format="%.1f%%"),
        "Risk (0–10)": st.column_config.NumberColumn(format="%.2f"),
        "Weighted score": st.column_config.NumberColumn(format="%.4f"),
        "Feasible rank": st.column_config.NumberColumn(format="%d"),
    })
