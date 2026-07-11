# AgriSense AI – Developer Guide

## Table of Contents

1. [Project Structure](#project-structure)
2. [Setup & Installation](#setup--installation)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Adding Knowledge Documents (RAG)](#adding-knowledge-documents-rag)
6. [Training the Crop ML Model](#training-the-crop-ml-model)
7. [Running Tests](#running-tests)
8. [API Reference](#api-reference)
9. [Deployment](#deployment)

---

## Project Structure

```
agrisense-ai/
├── frontend/           # Streamlit UI
│   ├── app.py          # Entry point
│   ├── pages/          # Home, Chat, Crop, Weather, Soil, Pest, Market, About
│   └── components/     # Sidebar, Styles
├── backend/            # FastAPI REST API
│   ├── main.py
│   ├── routes/         # One file per feature
│   └── models/schemas.py
├── agents/             # 7 AI Agents
│   ├── base_agent.py
│   ├── coordinator_agent.py
│   ├── weather_agent.py
│   ├── crop_agent.py
│   ├── soil_agent.py
│   ├── pest_agent.py
│   ├── market_agent.py
│   └── rag_agent.py
├── rag/                # RAG Pipeline
│   ├── vector_store.py
│   ├── embedder.py
│   ├── ingestor.py
│   └── retriever.py
├── datasets/
│   ├── train_crop_model.py
│   └── crop/           # Place Crop_recommendation.csv here
├── langflow/           # Langflow workflow JSON
├── config/
│   ├── settings.py
│   └── .env.example
└── tests/
    ├── unit/
    └── integration/
```

---

## Setup & Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

---

## Configuration

```bash
cp config/.env.example config/.env
# Edit config/.env with your actual API keys
```

Required keys:

| Key | Service |
|-----|---------|
| `WATSONX_API_KEY` | IBM Cloud IAM key |
| `WATSONX_PROJECT_ID` | watsonx.ai project |
| `OPENWEATHER_API_KEY` | openweathermap.org |
| `AGMARKNET_API_KEY` | data.gov.in |

---

## Running the Application

**Option 1 – Streamlit only (no backend required):**
```bash
streamlit run frontend/app.py
```

**Option 2 – Full stack:**
```bash
# Terminal 1 – Backend
uvicorn backend.main:app --reload

# Terminal 2 – Frontend
streamlit run frontend/app.py
```

**Option 3 – PowerShell script:**
```powershell
.\run.ps1
```

---

## Adding Knowledge Documents (RAG)

1. Place PDF, DOCX, TXT, or MD files in the `docs/` directory.
2. Run the ingestion pipeline:

```bash
python -m rag.ingestor
```

Recommended documents:
- ICAR crop production guides
- FAO soil health documents
- Ministry of Agriculture advisories
- Pest management bulletins

---

## Training the Crop ML Model

1. Download the [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
2. Place `Crop_recommendation.csv` in `datasets/crop/`
3. Run the training script:

```bash
python datasets/train_crop_model.py
```

This will produce `datasets/crop/crop_model.joblib` and `datasets/crop/crop_labels.json`.

---

## Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/

# Integration tests
pytest tests/integration/

# With coverage
pytest --cov=. --cov-report=html
```

---

## API Reference

Base URL: `http://localhost:8000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| POST | `/api/chat/` | AI chat (coordinator) |
| POST | `/api/crop/recommend` | Crop recommendation |
| POST | `/api/weather/` | Weather + advisory |
| POST | `/api/soil/analyze` | Soil health analysis |
| POST | `/api/pest/identify` | Pest identification |
| POST | `/api/market/prices` | Live mandi prices |

Interactive docs: `http://localhost:8000/api/docs`

---

## Deployment

### IBM Cloud Code Engine

```bash
# Build Docker image
docker build -t agrisense-ai .

# Push to IBM Container Registry
ibmcloud cr push us.icr.io/your-namespace/agrisense-ai:latest

# Deploy to Code Engine
ibmcloud ce application create \
  --name agrisense-ai \
  --image us.icr.io/your-namespace/agrisense-ai:latest \
  --env-from-secret agrisense-secrets \
  --port 8501
```
