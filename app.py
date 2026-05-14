import streamlit as st
import os
from dotenv import load_dotenv
from orchestrator import run_medagent

load_dotenv()

# Page config
st.set_page_config(
    page_title="MedAgent AI",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
    }
    
    /* Hide streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Hero header */
    .hero-header {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 50%, #0096c7 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 119, 182, 0.4);
        border: 1px solid rgba(0, 180, 216, 0.3);
    }
    
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: white;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .hero-subtitle {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin-top: 0.5rem;
        letter-spacing: 1px;
    }
    
    .hero-badges {
        margin-top: 1rem;
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .badge {
        background: rgba(255,255,255,0.2);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
    }

    /* Agent cards */
    .agent-card {
        background: linear-gradient(135deg, rgba(0,119,182,0.15) 0%, rgba(0,180,216,0.08) 100%);
        border: 1px solid rgba(0,180,216,0.25);
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        border-color: rgba(0,180,216,0.6);
        box-shadow: 0 4px 20px rgba(0,180,216,0.2);
    }
    
    .agent-icon {
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    
    .agent-name {
        color: #00b4d8;
        font-weight: 700;
        font-size: 0.9rem;
    }
    
    .agent-desc {
        color: rgba(255,255,255,0.6);
        font-size: 0.75rem;
        margin-top: 0.2rem;
    }

    /* Input area */
    .input-container {
        background: linear-gradient(135deg, rgba(0,119,182,0.1) 0%, rgba(13,27,42,0.8) 100%);
        border: 1px solid rgba(0,180,216,0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        backdrop-filter: blur(20px);
    }
    
    .section-title {
        color: #00b4d8;
        font-size: 1.1rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    /* Result cards */
    .result-card {
        background: linear-gradient(135deg, rgba(0,119,182,0.12) 0%, rgba(13,27,42,0.9) 100%);
        border: 1px solid rgba(0,180,216,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
    }
    
    /* Critical alert */
    .critical-alert {
        background: linear-gradient(135deg, rgba(220,38,38,0.2) 0%, rgba(153,27,27,0.15) 100%);
        border: 1px solid rgba(220,38,38,0.5);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(220,38,38,0.4); }
        70% { box-shadow: 0 0 0 10px rgba(220,38,38,0); }
        100% { box-shadow: 0 0 0 0 rgba(220,38,38,0); }
    }
    
    .high-alert {
        background: linear-gradient(135deg, rgba(234,88,12,0.2) 0%, rgba(154,52,18,0.15) 100%);
        border: 1px solid rgba(234,88,12,0.5);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }
    
    .low-alert {
        background: linear-gradient(135deg, rgba(22,163,74,0.2) 0%, rgba(21,128,61,0.15) 100%);
        border: 1px solid rgba(22,163,74,0.5);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
    }

    /* Metric cards */
    .metric-card {
        background: rgba(0,119,182,0.15);
        border: 1px solid rgba(0,180,216,0.3);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00b4d8;
    }
    
    .metric-label {
        color: rgba(255,255,255,0.6);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Symptom tags */
    .symptom-tag {
        display: inline-block;
        background: rgba(0,119,182,0.25);
        border: 1px solid rgba(0,180,216,0.4);
        color: #90e0ef;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
    }
    
    .condition-tag {
        display: inline-block;
        background: rgba(139,92,246,0.2);
        border: 1px solid rgba(139,92,246,0.4);
        color: #c4b5fd;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
    }
    
    .redflag-tag {
        display: inline-block;
        background: rgba(220,38,38,0.2);
        border: 1px solid rgba(220,38,38,0.4);
        color: #fca5a5;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 3px;
    }

    /* Report section */
    .report-container {
        background: linear-gradient(135deg, rgba(0,77,130,0.15) 0%, rgba(13,27,42,0.95) 100%);
        border: 1px solid rgba(0,180,216,0.25);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        font-family: 'Courier New', monospace;
        color: rgba(255,255,255,0.85);
        line-height: 1.8;
    }

    /* Disclaimer */
    .disclaimer {
        background: rgba(234,179,8,0.1);
        border: 1px solid rgba(234,179,8,0.3);
        border-radius: 10px;
        padding: 0.8rem 1.2rem;
        color: rgba(253,224,71,0.8);
        font-size: 0.8rem;
        text-align: center;
        margin-top: 1rem;
    }

    /* Streamlit overrides */
    .stTextArea textarea {
        background: rgba(10,15,30,0.8) !important;
        border: 1px solid rgba(0,180,216,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: rgba(0,180,216,0.8) !important;
        box-shadow: 0 0 20px rgba(0,180,216,0.2) !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.7rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 20px rgba(0,119,182,0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 30px rgba(0,119,182,0.6) !important;
    }

    /* Divider */
    hr {
        border-color: rgba(0,180,216,0.15) !important;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1e 0%, #0d1b2a 100%) !important;
        border-right: 1px solid rgba(0,180,216,0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# Hero Header
st.markdown("""
<div class="hero-header">
    <div class="hero-title">🏥 MedAgent AI</div>
    <div class="hero-subtitle">MULTI-AGENT CLINICAL DECISION SUPPORT SYSTEM</div>
    <div class="hero-badges">
        <span class="badge">🤖 LangGraph Agents</span>
        <span class="badge">📚 RAG Pipeline</span>
        <span class="badge">⚡ Groq LLaMA 3.3</span>
        <span class="badge">🔬 Evidence-Based</span>
        <span class="badge">🛡️ Explainable AI</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size:2.5rem">🏥</div>
        <div style="color:#00b4d8; font-weight:800; font-size:1.2rem">MedAgent</div>
        <div style="color:rgba(255,255,255,0.5); font-size:0.75rem">Clinical AI Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown('<div class="section-title">AI Agents</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="agent-card">
        <div class="agent-icon">🔍</div>
        <div class="agent-name">Symptom Analyzer</div>
        <div class="agent-desc">Extracts & classifies symptoms using clinical NLP</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">📚</div>
        <div class="agent-name">Literature Agent</div>
        <div class="agent-desc">RAG over WHO & medical guidelines</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">⚠️</div>
        <div class="agent-name">Risk Assessor</div>
        <div class="agent-desc">Scores severity & flags red flag symptoms</div>
    </div>
    <div class="agent-card">
        <div class="agent-icon">📋</div>
        <div class="agent-name">Orchestrator</div>
        <div class="agent-desc">LangGraph pipeline → structured clinical report</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style="background:rgba(220,38,38,0.1); border:1px solid rgba(220,38,38,0.3); 
    border-radius:10px; padding:0.8rem; color:rgba(253,164,175,0.9); font-size:0.75rem; text-align:center;">
        ⚠️ AI assistant only.<br>Always consult a qualified doctor.
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    

# Sample symptoms
st.markdown('<div class="section-title">Try a Sample Case</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🫀 Cardiac Emergency"):
        st.session_state.sample = "I have severe chest pain radiating to my left arm, shortness of breath, sweating, and nausea for the past 30 minutes"
with col2:
    if st.button("🧠 Neurological"):
        st.session_state.sample = "I have severe headache, high fever of 103F, stiff neck, and sensitivity to light for the past 2 days"
with col3:
    if st.button("🩸 Diabetic"):
        st.session_state.sample = "I feel extremely thirsty, urinate frequently, have blurred vision and my blood sugar reads 380 mg/dL"

# Input
st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<div class="section-title">📝 Patient Symptom Description</div>', unsafe_allow_html=True)

default_text = st.session_state.get("sample", "")
patient_input = st.text_area(
    "",
    value=default_text,
    placeholder="Describe symptoms in natural language... e.g. 'I have been experiencing severe chest pain, shortness of breath and dizziness for the past hour'",
    height=130,
    label_visibility="collapsed"
)

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    analyze_btn = st.button("🚀 Analyze Now", use_container_width=True)

# Analysis
if analyze_btn and patient_input:
    with st.spinner(""):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🔍 Agent 1: Analyzing symptoms...")
        with col2:
            st.info("📚 Agent 2: Searching literature...")
        with col3:
            st.info("⚠️ Agent 3: Assessing risk...")

        result = run_medagent(patient_input)

    st.markdown("---")

    # Results
    symptom_data = result.get("symptom_analysis", {})
    risk_data = result.get("risk_assessment", {})
    literature_data = result.get("literature_findings", {})
    urgency = symptom_data.get("urgency_level", "medium")
    risk_score = risk_data.get("risk_score", 0)

    # Top metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{risk_score}/10</div>
            <div class="metric-label">Risk Score</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        urgency_emoji = {"low":"🟢","medium":"🟡","high":"🔴","critical":"🚨"}.get(urgency,"⚪")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{urgency_emoji}</div>
            <div class="metric-label">{urgency.upper()}</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        num_conditions = len(symptom_data.get("possible_conditions", []))
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{num_conditions}</div>
            <div class="metric-label">Conditions Found</div>
        </div>""", unsafe_allow_html=True)
    with m4:
        num_sources = literature_data.get("num_sources", 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{num_sources}</div>
            <div class="metric-label">Evidence Sources</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Alert box
    action = risk_data.get("recommended_action", "Consult a doctor")
    timeframe = risk_data.get("timeframe", "N/A")
    if urgency == "critical":
        st.markdown(f"""
        <div class="critical-alert">
            <span style="color:#f87171; font-weight:800; font-size:1.1rem">🚨 CRITICAL ALERT</span><br>
            <span style="color:white; font-size:0.95rem">{action}</span>
            <span style="color:rgba(255,255,255,0.6); font-size:0.8rem"> — {timeframe}</span>
        </div>""", unsafe_allow_html=True)
    elif urgency == "high":
        st.markdown(f"""
        <div class="high-alert">
            <span style="color:#fb923c; font-weight:800">⚠️ HIGH URGENCY</span><br>
            <span style="color:white">{action}</span>
            <span style="color:rgba(255,255,255,0.6); font-size:0.8rem"> — {timeframe}</span>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="low-alert">
            <span style="color:#4ade80; font-weight:800">✅ MODERATE/LOW</span><br>
            <span style="color:white">{action}</span>
            <span style="color:rgba(255,255,255,0.6); font-size:0.8rem"> — {timeframe}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Two columns detail
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">🔍 Symptom Analysis</div>', unsafe_allow_html=True)

        symptoms_html = "".join([f'<span class="symptom-tag">{s}</span>'
                                  for s in symptom_data.get("symptoms", [])])
        st.markdown(f"**Identified Symptoms:**<br>{symptoms_html}", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        conditions_html = "".join([f'<span class="condition-tag">{c}</span>'
                                    for c in symptom_data.get("possible_conditions", [])])
        st.markdown(f"**Possible Conditions:**<br>{conditions_html}", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        systems = symptom_data.get("body_systems_affected", [])
        st.markdown(f"**Systems Affected:** {', '.join(systems)}")

    with col2:
        st.markdown('<div class="section-title">⚠️ Risk Assessment</div>', unsafe_allow_html=True)

        red_flags = risk_data.get("red_flags", [])
        if red_flags:
            flags_html = "".join([f'<span class="redflag-tag">🚩 {f}</span>'
                                   for f in red_flags])
            st.markdown(f"**Red Flags:**<br>{flags_html}", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

        specialist = risk_data.get("specialist_referral", "N/A")
        st.markdown(f"**Specialist Referral:** 👨‍⚕️ {specialist}")

        differential = risk_data.get("differential_diagnosis", [])
        if differential:
            st.markdown("<br>", unsafe_allow_html=True)
            diff_html = "".join([f'<span class="condition-tag">{d}</span>'
                                  for d in differential])
            st.markdown(f"**Differential Diagnosis:**<br>{diff_html}",
                        unsafe_allow_html=True)

    st.markdown("---")

    # Literature sources
    st.markdown('<div class="section-title">📚 Evidence Sources</div>',
                unsafe_allow_html=True)
    sources = literature_data.get("sources", [])
    with st.expander(f"View {len(sources)} retrieved medical literature chunks"):
        for i, source in enumerate(sources):
            st.markdown(f"""
            <div class="result-card">
                <span style="color:#00b4d8; font-weight:700">Source {i+1}</span><br>
                <span style="color:rgba(255,255,255,0.7); font-size:0.85rem">
                {source.get('content', '')}
                </span>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Final report
    st.markdown('<div class="section-title">📋 Clinical Report</div>',
                unsafe_allow_html=True)
    st.markdown(f"""
    <div class="report-container">
    {result.get('final_report', '').replace(chr(10), '<br>')}
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
        ⚠️ MedAgent is an AI-powered triage assistant for informational purposes only.
        Always consult a qualified healthcare professional for medical diagnosis and treatment.
    </div>""", unsafe_allow_html=True)

elif analyze_btn and not patient_input:
    st.warning("⚠️ Please describe the patient's symptoms first!")