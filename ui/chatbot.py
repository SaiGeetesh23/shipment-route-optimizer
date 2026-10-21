"""Streamlit chat interface for route decision questions."""
import streamlit as st
from services.chat_service import build_chat_context, get_route_answer

SUGGESTIONS = [
    "Why was this route selected?",
    "Compare the best alternatives",
    "Why was a route rejected?",
]

def render_chatbot(shipment_id, scenario_key, constraints, weights, result, comparison):
    st.divider()
    st.markdown('<div class="aiqon-section-kicker">06 / Decision support</div>', unsafe_allow_html=True)
    st.header("Route Decision Assistant")
    st.caption("Ask why a route was selected, compare alternatives, understand constraint violations, or explore a what-if scenario. The Python optimizer remains the source of truth.")
    if st.session_state.get("chat_scenario_key") != scenario_key:
        st.session_state["route_chat_messages"] = []
        st.session_state["chat_scenario_key"] = scenario_key

    evidence = build_chat_context(shipment_id, constraints, weights, result, comparison)
    with st.container(border=True):
        st.markdown("**Try asking**")
        cols = st.columns(3)
        selected = None
        for i, suggestion in enumerate(SUGGESTIONS):
            if cols[i].button(suggestion, key=f"route_chat_suggestion_{i}", width="stretch"):
                selected = suggestion

        for message in st.session_state["route_chat_messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("Ask about the recommendation, trade-offs, or constraints...", key="route_decision_chat_input")
        if selected:
            prompt = selected
        if prompt:
            st.session_state["route_chat_messages"].append({"role":"user","content":prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            try:
                with st.chat_message("assistant"):
                    with st.spinner("Reviewing the route evidence..."):
                        answer = get_route_answer(prompt, st.session_state["route_chat_messages"], evidence)
                    st.markdown(answer)
                st.session_state["route_chat_messages"].append({"role":"assistant","content":answer})
            except Exception:
                message = ("I couldn't reach the AI service. Check that `GROQ_API_KEY` is set in your `.env` file "
                           "and that the Groq dependency is installed. The optimizer's recommendation and route comparison remain available.")
                with st.chat_message("assistant"):
                    st.warning(message)
                st.session_state["route_chat_messages"].append({"role":"assistant","content":message})
        if st.session_state["route_chat_messages"] and st.button("Clear conversation", key="clear_route_chat"):
            st.session_state["route_chat_messages"] = []
            st.rerun()
