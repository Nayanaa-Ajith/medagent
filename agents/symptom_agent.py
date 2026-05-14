from langchain_groq import ChatGroq
from langchain_classic.prompts import PromptTemplate
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Structured output schema
class SymptomAnalysis(BaseModel):
    symptoms: List[str]
    possible_conditions: List[str]
    body_systems_affected: List[str]
    urgency_level: str  # low, medium, high, critical
    needs_immediate_care: bool

def analyze_symptoms(patient_input: str) -> dict:
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = f"""You are a clinical symptom analyzer. Analyze the following patient description and extract structured medical information.

Patient Description: {patient_input}

Respond in this EXACT JSON format, nothing else:
{{
    "symptoms": ["symptom1", "symptom2"],
    "possible_conditions": ["condition1", "condition2", "condition3"],
    "body_systems_affected": ["system1", "system2"],
    "urgency_level": "low/medium/high/critical",
    "needs_immediate_care": true/false
}}"""

    response = llm.invoke(prompt)
    
    import json
    import re
    
    # Extract JSON from response
    text = response.content
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        result = json.loads(json_match.group())
    else:
        result = {
            "symptoms": [patient_input],
            "possible_conditions": ["Unable to determine"],
            "body_systems_affected": ["Unknown"],
            "urgency_level": "medium",
            "needs_immediate_care": False
        }
    
    print("🔍 Symptom Analysis Complete!")
    print(f"   Possible conditions: {result['possible_conditions']}")
    print(f"   Urgency: {result['urgency_level']}")
    return result

if __name__ == "__main__":
    test_input = "I have been experiencing severe headache, high fever of 103F, stiff neck, and sensitivity to light for the past 2 days"
    result = analyze_symptoms(test_input)
    print("\nFull Analysis:", result)