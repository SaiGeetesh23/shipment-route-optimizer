"""Interactive inspection of one candidate route."""
import pandas as pd
import streamlit as st
from services.optimization_service import format_route_path, rejection_text

def render_route_inspection(comparison, recommended):
    st.divider()
    st.markdown('<div class="aiqon-section-kicker">03 / Candidate analysis</div>', unsafe_allow_html=True)
    st.header("Inspect any candidate")
    options = comparison["route_id"].astype(str).tolist()
    recommended_id = str(recommended.get("route_id")) if recommended else None
    index = options.index(recommended_id) if recommended_id in options else 0
    selected_id = st.selectbox("Choose a route", options=options, index=index, key="selected_route_id")
    row = comparison[comparison["route_id"].astype(str) == str(selected_id)].iloc[0]
    left, right = st.columns([1.4, 2.2], gap="large")
    with left:
        with st.container(border=True):
            st.markdown(f"#### {selected_id}")
            st.markdown(f"**Path:** {format_route_path(row)}")
            a, b = st.columns(2)
            a.metric("Cost", f"₹{float(row['total_cost']):,.0f}")
            b.metric("Transit", f"{float(row['transit_days']):.2f} days")
            a, b = st.columns(2)
            a.metric("Delay probability", f"{float(row['delay_probability']):.1%}")
            b.metric("Risk", f"{float(row['risk_score']) / 10:.1f}/10")
    with right:
        with st.container(border=True):
            st.markdown("#### Constraint assessment")
            if row["status"] == "Feasible":
                st.success("This route satisfies all active hard constraints.")
                if pd.notna(row.get("rank")):
                    st.write(f"Ranked **#{int(row['rank'])}** among feasible routes.")
            else:
                st.error("This route is rejected under the current constraints.")
                st.markdown("**Rejection reason**")
                st.write(rejection_text(row.get("rejection_reasons")))
            if recommended_id and str(selected_id) == recommended_id:
                st.info("This is the optimizer's recommended route.")
            elif recommended_id:
                st.caption(f"The optimizer still recommends {recommended_id}. Selecting a route here is for inspection only.")
