import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import json
import re

load_dotenv()

# Red flag symptoms that always need immediate care
RED_FLAG_SYMPTOMS = [
    "chest pain", "difficulty breathing", "shortness of breath",
    "severe headache", "stiff neck", "high fever", "loss of consciousness",
    "seizure", "stroke", "paralysis", "severe bleeding", "confusion",
    "sensitivity to light", "severe abdominal pain"
]

def assess_risk(symptom_analysis: dict, literature_summary: str) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    symptoms = symptom_analysis.get("symptoms", [])
    conditions = symptom_analysis.get("possible_conditions", [])
    urgency = symptom_analysis.get("urgency_level", "medium")

    # Check red flags
    red_flags_found = []
    for symptom in symptoms:
        for red_flag in RED_FLAG_SYMPTOMS:
            if red_flag.lower() in symptom.lower():
                red_flags_found.append(symptom)

    prompt = f"""You are a clinical risk assessment specialist. Based on the symptom analysis and medical literature, provide a structured risk assessment.

Symptoms: {symptoms}
Possible Conditions: {conditions}
Initial Urgency: {urgency}
Red Flag Symptoms Found: {red_flags_found}
Literature Summary: {literature_summary[:500]}

Respond in this EXACT JSON format:
{{
    "risk_score": 7,
    "risk_level": "high",
    "red_flags": ["flag1", "flag2"],
    "recommended_action": "Go to emergency room immediately",
    "specialist_referral": "Neurologist",
    "timeframe": "Within 1 hour",
    "monitoring_parameters": ["parameter1", "parameter2"],
    "differential_diagnosis": ["diagnosis1", "diagnosis2"]
}}"""

    response = llm.invoke(prompt)
    text = response.content
    json_match = re.search(r'\{.*\}', text, re.DOTALL)

    if json_match:
        result = json.loads(json_match.group())
    else:
        result = {
            "risk_score": 5,
            "risk_level": urgency,
            "red_flags": red_flags_found,
            "recommended_action": "Consult a doctor",
            "specialist_referral": "General Practitioner",
            "timeframe": "Within 24 hours",
            "monitoring_parameters": ["Temperature", "Blood pressure"],
            "differential_diagnosis": conditions
        }

    # Override if critical red flags found
    if len(red_flags_found) >= 3:
        result["risk_level"] = "critical"
        result["risk_score"] = min(result.get("risk_score", 5) + 2, 10)
        result["recommended_action"] = "EMERGENCY: Go to ER immediately"
        result["timeframe"] = "Immediately"

    print("⚠️ Risk Assessment Complete!")
    print(f"   Risk Level: {result['risk_level']}")
    print(f"   Risk Score: {result['risk_score']}/10")
    print(f"   Action: {result['recommended_action']}")
    return result

if __name__ == "__main__":
    # Test with symptom agent output
    test_symptom_analysis = {
        "symptoms": ["severe headache", "high fever", "stiff neck", "sensitivity to light"],
        "possible_conditions": ["meningitis", "encephalitis"],
        "body_systems_affected": ["nervous system", "immune system"],
        "urgency_level": "high",
        "needs_immediate_care": True
    }
    test_literature = "Meningitis is a serious condition requiring immediate medical attention."

    result = assess_risk(test_symptom_analysis, test_literature)
    print("\nFull Risk Assessment:", result)