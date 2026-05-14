# MedAgent AI — Multi-Agent Clinical Decision Support System

A multi-agent AI system that analyzes patient symptoms, retrieves evidence from medical literature, and generates structured clinical recommendations with explainability.

---

## Why MedAgent Exists

During my research internship at IIIT Kottayam, I worked on retinal disease detection using deep learning. What struck me wasn't just the technical challenge — it was the human gap underneath it.

Doctors in smaller hospitals and rural clinics often can't access specialist opinions quickly. A patient experiencing a severe headache and stiff neck at 2am doesn't know if they should rush to the ER or wait until morning. A nurse in a district hospital doesn't always have a neurologist on call.

Enterprise clinical AI tools exist — Microsoft, IBM, Infermedica — but they are closed source, expensive, and black boxes. A hospital in a developing region can't afford them, and a doctor can't verify their reasoning.

MedAgent bridges that gap. It is open source, explainable, and designed as a triage assistant — not a replacement for doctors.

---

## How It Works

A patient or clinician describes symptoms in natural language. MedAgent runs 3 specialized AI agents in sequence, orchestrated by LangGraph:

Agent 1 — Symptom Analyzer
Extracts symptoms from natural language, identifies possible conditions, flags urgency level using clinical NLP.

Agent 2 — Literature Agent
Performs RAG over WHO medical guidelines and clinical documents. Retrieves evidence-based information relevant to the identified conditions.

Agent 3 — Risk Assessor
Scores severity from 1 to 10, detects red flag symptoms, recommends specialist referral and timeframe for care.

Orchestrator — LangGraph Pipeline
Combines all three agent outputs into a structured 7-section clinical report with evidence basis and safety disclaimer.

---

## Key Features

- Multi-agent architecture with 3 specialized agents, each with a distinct clinical role
- RAG pipeline that retrieves answers from real medical documents, not hallucinated facts
- Explainability layer showing exactly which document chunks influenced each recommendation
- Red flag detection that automatically identifies critical symptoms requiring immediate care
- Structured clinical reports validated with Pydantic
- Honest uncertainty handling — says "I don't know" rather than producing confident wrong answers
- Fast inference powered by Groq LLaMA 3.3 70B

---

## Tech Stack

- Agent Orchestration: LangGraph
- LLM: Groq — LLaMA 3.3 70B Versatile
- RAG Framework: LangChain
- Vector Database: FAISS
- Embeddings: Sentence Transformers (all-MiniLM-L6-v2)
- Structured Output: Pydantic
- PDF Processing: PyMuPDF
- Frontend: Streamlit
- Language: Python 3.13

---

## Project Structure

```
medagent/
├── agents/
│   ├── symptom_agent.py       # Agent 1: Clinical NLP symptom extraction
│   ├── literature_agent.py    # Agent 2: RAG over medical literature
│   └── risk_agent.py          # Agent 3: Risk scoring and red flag detection
├── data/                      # Medical PDF documents
├── vectorstore/               # FAISS vector index (auto-generated)
├── orchestrator.py            # LangGraph multi-agent pipeline
├── ingest.py                  # PDF ingestion and embedding pipeline
├── app.py                     # Streamlit frontend
├── main.py                    # FastAPI backend
└── .env                       # API keys (not committed)
```

---

## Getting Started

Prerequisites: Python 3.9+, Groq API key (free at console.groq.com)

```bash
# Clone the repository
git clone https://github.com/Nayanaa-Ajith/medagent.git
cd medagent

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Create a .env file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Run:
```bash
# Step 1: Ingest medical documents
python ingest.py

# Step 2: Launch the application
streamlit run app.py
```

---

## Sample Test Cases

Cardiac Emergency:
"I have severe chest pain radiating to my left arm, shortness of breath, sweating, and nausea for the past 30 minutes"

Neurological:
"I have severe headache, high fever of 103F, stiff neck, and sensitivity to light for the past 2 days"

Diabetic Crisis:
"I feel extremely thirsty, urinate frequently, have blurred vision and my blood sugar reads 380 mg/dL"

---

## How It Handles Uncertainty

MedAgent is designed to be honest, not overconfident.

Grounded answers — RAG architecture ensures responses come from real medical documents, not hallucinated facts. Source transparency — every answer shows which document chunks were retrieved. Honest uncertainty — when information is not in the knowledge base, it says so clearly. Safety-first — critical symptoms always trigger emergency escalation regardless of LLM output.

---

## Limitations and Future Work

Current limitations:
- Knowledge base limited to ingested PDFs and needs hospital-specific protocols for production use
- Stateless with no patient history tracking between sessions
- Uses a general LLM rather than a medical fine-tuned model like MedPaLM

Planned improvements:
- Patient session memory for longitudinal symptom tracking
- RAGAS evaluation framework for quantitative faithfulness scoring
- FHIR integration for compatibility with existing hospital systems
- Fine-tuned medical LLM for improved clinical accuracy
- Docker containerization for easy deployment

---

## Architecture Decisions

Why multi-agent over single chain?
Each agent can be improved, replaced, or evaluated independently. The risk agent logic can be updated without touching the literature retrieval pipeline.

Why RAG over plain LLM?
Grounded answers from real documents are more trustworthy than an LLM's parametric memory, which can hallucinate medical facts with dangerous confidence.

Why Groq and LLaMA?
Free inference, fast response times, and open model weights — making this deployable without enterprise API costs.

---

## Disclaimer

MedAgent is an AI-powered triage assistant for informational and research purposes only. It is not a substitute for professional medical diagnosis, advice, or treatment. Always consult a qualified healthcare professional for medical decisions.