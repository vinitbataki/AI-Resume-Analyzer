import streamlit as st
import os
import re
from pypdf import PdfReader
from dotenv import load_dotenv
from src.ai_engine import generate_resume_analysis

# Load environment variables
load_dotenv(override=True)

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Initialize Session State
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

st.set_page_config(page_title="SmartScan ATS", layout="wide")

# CSS Styling
st.markdown("""
    <style>
    .main .block-container { font-family: sans-serif; padding-top: 2rem; }
    h1 { color: #1E3A8A !important; }
    div.stButton > button:first-child { background-color: #1E3A8A; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 SmartScan ATS Optimizer")
st.subheader("Powered by Groq API")

# Sidebar
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    st.markdown("### 🌐 System Node Status")
    
    # Check for GROQ_API_KEY
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if api_key:
        st.success("Groq API Node: Connected")
    else:
        st.error("Groq API Node: Disconnected")

# Main Layout
col1, col2 = st.columns(2)
with col1:
    job_description = st.text_area("Paste the job description here...", height=300)
with col2:
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if st.button("Analyze System Match", type="primary"):
    if not job_description or not uploaded_file:
        st.warning("Please provide both a Job Description and a Resume.")
    else:
        with st.spinner("Analyzing..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            raw_report = generate_resume_analysis(resume_text, job_description)
            
            # Parsing logic
            score_match = re.search(r"\[SCORE:\s*(\d+)", raw_report)
            score_value = int(score_match.group(1)) if score_match else 50
            clean_report = re.sub(r"\[SCORE:.*?\]", "", raw_report).strip()
            
            st.session_state.analysis_results = {"score": score_value, "report": clean_report}
            st.rerun()

# Display Results
if st.session_state.analysis_results:
    res = st.session_state.analysis_results
    st.markdown("## 📊 System Match Analytics")
    st.metric("Overall ATS Match Score", f"{res['score']}%")
    st.progress(res['score'] / 100.0)
    st.markdown("---")
    st.markdown("## 📋 Detailed Evaluation Report")
    st.markdown(res['report'])
    st.download_button("📥 Export Report", data=res['report'], file_name="Report.txt")