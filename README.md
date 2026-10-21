# Aiqon — Shipment Route Optimization

An interactive decision-support application that evaluates shipment routes under **cost, transit time, delay probability, and risk constraints**. The system filters infeasible routes, ranks feasible alternatives using weighted scoring, and uses an AI-powered chatbot to explain optimization results.

## Overview

Choosing a shipment route involves balancing competing objectives. The cheapest route may take longer, while a faster route may cost more or involve greater risk.

Aiqon addresses this problem through a two-stage optimization pipeline:

1. **Constraint filtering:** Reject routes that violate user-defined operational limits.
2. **Weighted scoring and ranking:** Rank feasible routes based on normalized cost, transit time, and risk scores.

The application provides an interactive dashboard where users can adjust constraints, compare routes, inspect recommendations, and ask questions about the results.

## Features

- **Interactive dashboard:** Select shipments and configure operational constraints.
- **Constraint-based filtering:** Evaluate budget, transit time, delay probability, and risk limits.
- **Weighted route scoring:** Rank feasible routes according to user-defined cost, time, and risk priorities.
- **Route comparison:** Inspect route metrics through interactive charts and tables.
- **Recommendation explanations:** Understand why routes are selected or rejected.
- **AI-powered chatbot:** Ask questions about recommendations, rejection reasons, and trade-offs using a Groq-hosted LLM.
- **Modular architecture:** Separate data services, optimization logic, UI components, and conversational AI.
- **Automated tests:** Test core constraint filtering and optimization behavior.

## System Architecture

<img width="546" height="474" alt="System Architecture Shipment Route Optimization - Visual 1" src="https://github.com/user-attachments/assets/33048333-2a2c-49e6-a5c2-8d1476e8d208" />



The optimization engine deterministically filters and ranks routes. The AI assistant explains the resulting evidence in natural language; it does not replace the optimization algorithm.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application and optimization logic |
| Streamlit | Interactive web dashboard |
| Pandas | Dataset loading and manipulation |
| Plotly | Interactive charts and visualizations |
| LangChain | Integration with the language model |
| Groq API | AI-powered conversational explanations |
| Pydantic | Structured data validation where used |
| Pytest | Automated testing |
| CSV | Shipment and route data storage |

## Project Structure

```text
aiqon/
├── app.py
├── config.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── shipments.csv
│   └── routes.csv
├── services/
│   ├── __init__.py
│   ├── data_service.py
│   ├── optimization_service.py
│   └── chat_service.py
├── src/
│   ├── generate_data.py
│   ├── constraints.py
│   ├── scoring.py
│   ├── optimizer.py
│   └── explain.py
├── tests/
│   ├── test_constraints.py
│   └── test_optimizer.py
└── ui/
    ├── __init__.py
    ├── styles.py
    ├── sidebar.py
    ├── summary.py
    ├── route_inspection.py
    ├── charts.py
    ├── route_table.py
    └── chatbot.py
```

## Optimization Methodology

### 1. Constraint Filtering

<img width="1774" height="887" alt="Route Feasibility Constraints Diagram" src="https://github.com/user-attachments/assets/118e735c-5a47-4ea6-a899-bcc6a92999d4" />
### 2. Weighted Scoring

<img width="1774" height="887" alt="Route Scoring and Ranking Workflow" src="https://github.com/user-attachments/assets/a31cd557-6c4c-461e-b421-ac5f86e4b88a" />
## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- A Groq API key for chatbot functionality

### Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/aiqon-shipment-route-optimizer.git
cd aiqon-shipment-route-optimizer
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace the placeholder with your own API key. Keep `.env` out of version control and never publish your API key.

### Run the Application

```powershell
streamlit run app.py
```

Open the local URL displayed in the terminal to access the dashboard.

### Run Tests

```powershell
pytest -q
```

## Limitations

- **Synthetic data:** The current datasets are generated for demonstration and do not establish real-world performance.
- **Input accuracy:** Recommendations depend on the accuracy and freshness of route attributes.
- **Fixed normalization:** Predefined reference scales may not reflect all operational conditions.
- **Subjective weights:** Rankings depend on user-defined objective weights.
- **No predictive modeling:** The application does not independently predict future costs, delays, or risks.
- **No real-time integration:** Live carrier prices, traffic, weather, and port conditions are not integrated.

## Future Improvements

- Integrate real-world and real-time logistics data.
- Develop validated models for predicting delays and risk.
- Calibrate scoring ranges using operational data.
- Add multi-shipment and fleet-level optimization.
- Evaluate recommendations against real-world baselines.
- Improve chatbot grounding and automated evaluation.

## Conclusion

Aiqon demonstrates a modular approach to shipment route decision support by combining hard-constraint filtering, weighted multi-criteria ranking, interactive visualization, and AI-generated explanations. It provides a foundation for exploring logistics optimization, with real-world deployment requiring validated data, calibrated objectives, and operational evaluation.

---

**Note:** This project is a prototype intended for demonstration and experimentation. Its recommendations should not be treated as validated operational guidance without further testing.
