import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.symptom_agent import analyze_symptoms
from agents.literature_agent import retrieve_literature
from agents.risk_agent import assess_risk
from langchain_groq import ChatGroq
import json

load_dotenv()

# Define shared state between agents
class MedAgentState(TypedDict):
    patient_input: str
    symptom_analysis: dict
    literature_findings: dict
    risk_assessment: dict
    final_report: str
    error: str

# Node 1 — Symptom Analysis
def symptom_node(state: MedAgentState) -> MedAgentState:
    print("\n🔍 Running Symptom Analyzer Agent...")
    try:
        result = analyze_symptoms(state["patient_input"])
        state["symptom_analysis"] = result
    except Exception as e:
        state["error"] = f"Symptom analysis failed: {str(e)}"
        state["symptom_analysis"] = {}
    return state

# Node 2 — Literature Retrieval
def literature_node(state: MedAgentState) -> MedAgentState:
    print("\n📚 Running Literature Retrieval Agent...")
    try:
        conditions = state["symptom_analysis"].get("possible_conditions", [])
        symptoms = state["symptom_analysis"].get("symptoms", [])
        result = retrieve_literature(conditions, symptoms)
        state["literature_findings"] = result
    except Exception as e:
        state["error"] = f"Literature retrieval failed: {str(e)}"
        state["literature_findings"] = {}
    return state

# Node 3 — Risk Assessment
def risk_node(state: MedAgentState) -> MedAgentState:
    print("\n⚠️ Running Risk Assessment Agent...")
    try:
        literature_summary = state["literature_findings"].get("literature_summary", "")
        result = assess_risk(state["symptom_analysis"], literature_summary)
        state["risk_assessment"] = result
    except Exception as e:
        state["error"] = f"Risk assessment failed: {str(e)}"
        state["risk_assessment"] = {}
    return state

# Node 4 — Final Report Generation
def report_node(state: MedAgentState) -> MedAgentState:
    print("\n📋 Generating Final Clinical Report...")
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        prompt = f"""You are a senior clinician. Generate a structured clinical summary report based on the multi-agent analysis below.

Patient Description: {state['patient_input']}

Symptom Analysis: {json.dumps(state['symptom_analysis'], indent=2)}

Literature Findings: {state['literature_findings'].get('literature_summary', 'N/A')[:400]}

Risk Assessment: {json.dumps(state['risk_assessment'], indent=2)}

Generate a clear, structured clinical report with these sections:
1. PATIENT SUMMARY
2. IDENTIFIED CONDITIONS
3. RISK LEVEL & URGENCY
4. RECOMMENDED ACTIONS
5. SPECIALIST REFERRAL
6. EVIDENCE BASIS
7. DISCLAIMER

Keep it professional and clear."""

        response = llm.invoke(prompt)
        state["final_report"] = response.content

    except Exception as e:
        state["error"] = f"Report generation failed: {str(e)}"
        state["final_report"] = "Report generation failed."
    return state

# Build LangGraph
def build_graph():
    graph = StateGraph(MedAgentState)

    # Add nodes
    graph.add_node("symptom_analyzer", symptom_node)
    graph.add_node("literature_retrieval", literature_node)
    graph.add_node("risk_assessment", risk_node)
    graph.add_node("report_generator", report_node)

    # Add edges (sequential flow)
    graph.set_entry_point("symptom_analyzer")
    graph.add_edge("symptom_analyzer", "literature_retrieval")
    graph.add_edge("literature_retrieval", "risk_assessment")
    graph.add_edge("risk_assessment", "report_generator")
    graph.add_edge("report_generator", END)

    return graph.compile()

def run_medagent(patient_input: str) -> dict:
    print("🏥 MedAgent Starting...")
    print(f"Patient: {patient_input}\n")

    graph = build_graph()

    initial_state = MedAgentState(
        patient_input=patient_input,
        symptom_analysis={},
        literature_findings={},
        risk_assessment={},
        final_report="",
        error=""
    )

    final_state = graph.invoke(initial_state)

    print("\n" + "="*50)
    print("📋 FINAL CLINICAL REPORT")
    print("="*50)
    print(final_state["final_report"])

    return final_state

if __name__ == "__main__":
    run_medagent("I have been experiencing severe headache, high fever of 103F, stiff neck, and sensitivity to light for the past 2 days")