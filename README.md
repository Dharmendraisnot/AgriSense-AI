# 🌾 AgriSense AI – Agentic AI-Powered Smart Farming Advisor

> **IBM SkillsBuild Final Internship Project**

AgriSense AI is a production-ready, agentic AI-powered web application that helps small-scale farmers make better agricultural decisions. It combines IBM watsonx.ai (Granite models), Retrieval-Augmented Generation (RAG), real-time Weather & Market APIs, and a Langflow-orchestrated multi-agent workflow.

---

## 🚀 Features

| Feature | Description |
|---|---|
| 🤖 AI Chat | Conversational farming advisor powered by IBM Granite |
| 🌦️ Weather Agent | Real-time weather data with crop impact analysis |
| 🌾 Crop Recommendation | ML-based crop suggestion from soil & climate data |
| 🧪 Soil Health Analysis | Soil parameter evaluation with remediation advice |
| 🐛 Pest & Disease Guidance | PlantVillage-backed pest detection and treatment |
| 📈 Live Mandi Prices | Real-time market price data via Agmarknet |
| 📚 RAG Knowledge Base | ICAR, FAO, MoA document retrieval via ChromaDB |
| 🧠 Coordinator Agent | Routes queries to the appropriate specialist agent |

---

## 🏗️ Architecture

```
User Query
    │
    ▼
Streamlit UI (frontend/)
    │
    ▼
FastAPI Backend (backend/)
    │
    ▼
Coordinator Agent (agents/coordinator_agent.py)
    │
    ├──► Weather Agent        → OpenWeather API
    ├──► Crop Agent           → ML Model + RAG
    ├──► Soil Health Agent    → RAG + Rules
    ├──► Pest & Disease Agent → PlantVillage + RAG
    ├──► Market Price Agent   → Agmarknet API
    └──► RAG Agent            → ChromaDB + IBM Granite
                                      │
                                      ▼
                              IBM watsonx.ai (Granite)
                                      │
                                      ▼
                              Explainable Response
```

---

## 📁 Folder Structure

```
AgriSense-AI/
├── frontend/           # Streamlit UI pages
├── backend/            # FastAPI app & routes
├── agents/             # Individual AI agents
├── rag/                # RAG pipeline & ChromaDB
├── datasets/           # Crop, Soil, PlantVillage datasets
├── apis/               # Weather & Agmarknet API wrappers
├── utils/              # Shared utilities
├── langflow/           # Langflow workflow JSON exports
├── docs/               # Project documentation
├── tests/              # Unit & integration tests
├── config/             # Configuration & environment templates
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/agrisense-ai.git
cd agrisense-ai

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp config/.env.example config/.env
# Edit config/.env with your API keys

# 5. Run the application
streamlit run frontend/app.py
```

---

## 🔑 Required API Keys

| Service | Key Variable | Where to Get |
|---|---|---|
| IBM watsonx.ai | `WATSONX_API_KEY` | cloud.ibm.com |
| IBM Project ID | `WATSONX_PROJECT_ID` | watsonx.ai project settings |
| OpenWeather | `OPENWEATHER_API_KEY` | openweathermap.org |
| Agmarknet | `AGMARKNET_API_KEY` | data.gov.in |

---

## 🧠 Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI + Python
- **AI Model**: IBM Granite (via watsonx.ai)
- **Orchestration**: Langflow
- **Vector DB**: ChromaDB
- **Embeddings**: sentence-transformers
- **APIs**: OpenWeatherMap, Agmarknet (data.gov.in)
- **Deployment**: IBM Cloud (Code Engine / Cloud Foundry)

---

## 📄 License

MIT License – Built for IBM SkillsBuild Internship Program.
