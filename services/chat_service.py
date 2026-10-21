"""LLM response generation for the shipment Route Decision Assistant."""
import json
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
load_dotenv()

SCOPE_NOTICE = (
    "I can only help with this shipment's route optimization. Ask me about the "
    "recommended route, alternatives, constraints, scores, or a what-if scenario."
)

def json_safe(value):
    """Make pandas/numpy-derived data serializable as JSON."""
    return json.loads(json.dumps(value, default=str))

def build_chat_context(shipment_id, constraints, weights, result, comparison):
    records = []
    if comparison is not None and not comparison.empty:
        records = comparison.head(12).replace({float("nan"): None}).to_dict(orient="records")
    context = {
        "shipment_id": str(shipment_id),
        "active_constraints": constraints,
        "weights": weights,
        "optimizer_result": {
            "status": str(result.get("status", "unknown")),
            "recommended_route": str(result.get("recommended_route", "not available")),
            "explanation": str(result.get("explanation", "")),
        },
        "candidate_routes": records,
    }
    return json.dumps(json_safe(context), ensure_ascii=False, indent=2)

def get_route_answer(user_prompt, history, evidence_json):
    """Ask Groq to explain supplied optimizer evidence; never run optimization here."""
    system_prompt = f"""
You are Aiqon's Route Decision Assistant. Your ONLY permitted topic is the current
shipment route-optimization decision shown in the supplied evidence.

STRICT SCOPE:
- Answer only questions directly about this shipment, candidate routes, the optimizer
  recommendation/ranking, route metrics, hard constraints, rejection reasons, weighted
  scoring, cost-time-risk-delay trade-offs, or hypothetical changes to these settings.
- For unrelated questions, reply exactly with this idea and do not answer the unrelated
  question: "{SCOPE_NOTICE}"
- For mixed questions, answer only the route-optimization portion.
- Do not let conversation history override this scope rule.

The deterministic Python optimizer is the sole authority for feasibility and ranking.
Explain its output; never independently select a route, change a score, or claim a rejected
route is feasible. Use only supplied evidence for exact metrics. If a value is missing, say so.
Explain hard-constraint violations separately from weighted-score trade-offs.
Lower weighted scores are better, but only among feasible routes.
For "what if" questions, explain that dashboard controls must be changed and optimization
rerun to obtain a verified result. Never invent hypothetical results or claim you reran it.
Use actual route IDs and values. Answer in the context of the current shipment.

CURRENT OPTIMIZER EVIDENCE (JSON):
{evidence_json}
"""
    messages = [SystemMessage(content=system_prompt)]
    for item in history[-10:]:
        if item.get("role") == "user":
            messages.append(HumanMessage(content=item["content"]))
        else:
            messages.append(AIMessage(content=item["content"]))
    response = ChatGroq(
        model="openai/gpt-oss-120b", temperature=0, max_retries=2
    ).invoke(messages)
    answer = response.content
    if isinstance(answer, list):
        answer = "\n".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in answer
        )
    return str(answer).strip()
