"""Cost, transit, risk, and delay-probability comparison charts."""
import plotly.express as px
import streamlit as st
from config import FEASIBLE_COLOR, REJECTED_COLOR, INK, PANEL

def render_charts(comparison, controls):
    st.divider()
    st.markdown('<div class="aiqon-section-kicker">04 / Compare alternatives</div>', unsafe_allow_html=True)
    st.header("Candidate route comparison")
    st.caption("All candidate routes are included. Dashed lines show active limits; hover over a bar for exact values.")
    color_map = {"Feasible": FEASIBLE_COLOR, "Rejected": REJECTED_COLOR}
    tabs = st.tabs(["Cost", "Transit time", "Risk", "Delay probability"])
    specs = [
        ("total_cost", "Total cost by candidate route", "Cost (₹)", controls["max_cost"], "Budget ceiling"),
        ("transit_days", "Transit duration by candidate route", "Transit time (days)", controls["max_days"], "Delivery deadline"),
        ("risk_out_of_10", "Risk score by candidate route", "Risk (0–10)", controls["max_risk_10"], "Risk limit"),
        ("delay_probability_pct", "Estimated delay probability by candidate route", "Delay probability (%)", controls["delay_pct"], "Delay limit"),
    ]
    for tab, (metric, title, label, limit, limit_label) in zip(tabs, specs):
        with tab:
            fig = px.bar(
                comparison, x="route_id", y=metric, color="status",
                color_discrete_map=color_map,
                hover_data=[c for c in ["profile", "hubs", "total_cost", "transit_days", "risk_score", "delay_probability"] if c in comparison],
                title=title,
                labels={"route_id": "Candidate route", metric: label, "status": "Feasibility"},
                category_orders={"route_id": comparison["route_id"].astype(str).tolist()},
            )
            fig.add_hline(y=limit, line_dash="dash", line_color=INK, annotation_text=limit_label, annotation_position="top left")
            layout = dict(template="plotly_white", height=410, margin=dict(l=15,r=20,t=65,b=35),
                legend_title_text="Route status", font=dict(family="DM Sans, sans-serif", color="#59483C"),
                title_font=dict(size=17, color=INK), xaxis=dict(showgrid=False,title=None),
                yaxis=dict(gridcolor="#E7DCCB",zeroline=False), plot_bgcolor=PANEL, paper_bgcolor=PANEL)
            if metric == "risk_out_of_10":
                layout["yaxis"]["range"] = [0, 10]
            fig.update_layout(**layout)
            st.plotly_chart(fig, width="stretch")
