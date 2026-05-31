import streamlit as st
import os
import re
from pypdf import PdfReader
from dotenv import load_dotenv
# Naye functions import kiye hain
from src.ai_engine import generate_resume_analysis, enhance_and_align_resume

load_dotenv(override=True)

# Page Config
st.set_page_config(page_title="SmartScan ATS", layout="wide")

# CSS Styling
st.markdown("""
    <style>
    .main .block-container { font-family: sans-serif; padding-top: 2rem; }
    h1 { color: #1E3A8A !important; }
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; }
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "analysis_results" not in st.session_state: st.session_state.analysis_results = None
if "enhanced_resume" not in st.session_state: st.session_state.enhanced_resume = None

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        return "".join([page.extract_text() for page in reader.pages])
    except: return "Error reading PDF"

st.title("🚀 SmartScan ATS Optimizer")

# Sidebar
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    st.success("Groq API Node: Connected" if api_key else "Groq API Node: Disconnected")

# Layout (Job Description left, Upload right)
col1, col2 = st.columns(2)
with col1:
    job_description = st.text_area("Paste the job description here...", height=300)
with col2:
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Analysis Logic
if st.button("Analyze System Match", type="primary"):
    if not job_description or not uploaded_file:
        st.warning("Please provide both a Job Description and a Resume.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text # Save for later use
            raw_report = generate_resume_analysis(resume_text, job_description)
            
            score_match = re.search(r"\[SCORE:\s*(\d+)", raw_report)
            score_value = int(score_match.group(1)) if score_match else 50
            st.session_state.analysis_results = {"score": score_value, "report": raw_report}
            st.rerun()

# Display Results
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.markdown("---")
    st.markdown("## 📊 System Match Analytics")
    st.metric("Overall ATS Match Score", f"{res['score']}%")
    st.progress(res['score'] / 100.0)
    st.markdown(res['report'])
    
    # Enhancement Button
    if st.button("✨ Generate Enhanced & Aligned Resume"):
        with st.spinner("Optimizing..."):
            st.session_state.enhanced_resume = enhance_and_align_resume(st.session_state.resume_text, job_description)
            st.rerun()

if st.session_state.enhanced_resume:
    st.markdown("---")
    st.markdown("## 📄 Enhanced Resume")
    st.markdown(st.session_state.enhanced_resume)
    st.download_button("📥 Download Enhanced Resume", st.session_state.enhanced_resume, "Enhanced_Resume.md")