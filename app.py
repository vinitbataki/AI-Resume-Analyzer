import streamlit as st
import os
import re  # Added for bulletproof score extraction
from pypdf import PdfReader
from dotenv import load_dotenv
from src.ai_engine import generate_resume_analysis

# 1. Load environment variables instantly before rendering elements
load_dotenv(override=True)

def extract_text_from_pdf(file):
    """Safely extracts text data from an uploaded PDF file wrapper."""
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

# Initialize Session State variables to prevent data disappearing on download click
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

# 2. Global UI Window Layout & Tab Configuration
st.set_page_config(page_title="SmartScan ATS", layout="wide")

# 3. Custom Premium CSS Styling Injection
st.markdown("""
    <style>
    .main .block-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        padding-top: 2rem;
    }
    h1 {
        color: #1E3A8A !important; 
        font-weight: 700 !important;
    }
    h2, h3 {
        color: #4B5563 !important; 
    }
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        font-size: 16px;
        font-weight: 600;
        padding: 0.6rem 2rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #1D4ED8; 
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.15);
    }
    </style>
""", unsafe_allow_html=True)

# 4. Main Banner Headings
st.title("🚀 SmartScan ATS Optimizer")
st.subheader("Powered by Gemini 3.5 Flash")

# 5. Interactive Control Panel Sidebar Configuration
with st.sidebar:
    st.markdown("# ⚙️ Control Panel")
    st.info("""
    **User Instructions:**
    1. **Paste** the target role's core job requirements on the left area.
    2. **Upload** your current resume document in PDF configuration.
    3. **Click** the primary action matching evaluation button.
    """)
    
    st.markdown("---")
    st.markdown("### 🌐 System Node Status")
    
    if os.getenv("GEMINI_API_KEY"):
        st.success("Gemini 3.5 API Node: Connected")
    else:
        st.error("Gemini 3.5 API Node: Disconnected")

# 6. Primary Structural Split Columns Configuration
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📋 Target Job Description")
    job_description = st.text_area("Paste the full job description text here...", height=300, key="jd_input")

with col2:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume file (PDF format only)", type=["pdf"], key="resume_input")

st.markdown("---")

# 7. Processing Pipeline Logic Execution 
if st.button("Analyze System Match", type="primary"):
    if not job_description:
        st.warning("Please paste a Job Description before proceeding.")
    elif not uploaded_file:
        st.warning("Please upload your Resume PDF file before proceeding.")
    else:
        with st.spinner("Extracting text contents from your resume..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            
        if "Error reading PDF" in resume_text:
            st.error(resume_text)
        else:
            with st.spinner("Analyzing resume structure against Gemini 3.5..."):
                raw_report = generate_resume_analysis(resume_text, job_description)
                
            # Defensive RegEx score parsing: extracts digits following "[SCORE:" safely
            score_match = re.search(r"\[SCORE:\s*(\d+)", raw_report)
            score_value = int(score_match.group(1)) if score_match else 50
            
            # Strip out the raw score line tag cleanly so the user doesn't see it
            clean_report = re.sub(r"\[SCORE:.*?\]", "", raw_report).strip()
            
            # Save results permanently into session state storage
            st.session_state.analysis_results = {
                "score": score_value,
                "report": clean_report
            }
            st.success("Analysis Complete!")

# 8. Render Results from State (Ensures persistent display during UI clicks)
if st.session_state.analysis_results:
    results = st.session_state.analysis_results
    
    st.markdown("## 📊 System Match Analytics")
    col_metric, col_progress = st.columns([1, 3])
    
    with col_metric:
        st.metric(label="Overall ATS Match Score", value=f"{results['score']}%")
        
    with col_progress:
        st.markdown("<br>", unsafe_allow_html=True) 
        st.progress(results['score'] / 100.0)
    
    st.markdown("---")
    
    st.markdown("## 📋 Detailed Evaluation Report")
    st.markdown(results['report'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        label="📥 Export Evaluation Report",
        data=results['report'],
        file_name="ATS_Optimization_Report.txt",
        mime="text/plain",
        help="Click here to download this evaluation report as a plain text file."
    )