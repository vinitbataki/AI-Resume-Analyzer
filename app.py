import streamlit as st
import os
from src.ai_engine import generate_resume_analysis, enhance_and_align_resume
from pypdf import PdfReader

# Page Configuration
st.set_page_config(page_title="AI ATS Optimizer", page_icon="📄")
st.title("📄 AI Resume ATS Optimizer")

# Sidebar for Setup
st.sidebar.header("Configuration")
job_description = st.sidebar.text_area("Paste Job Description here:")

# File Uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Main Logic
if uploaded_file and job_description:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            analysis = generate_resume_analysis(resume_text, job_description)
            st.session_state.analysis_results = analysis
            st.rerun()

# Display Results
if "analysis_results" in st.session_state:
    st.markdown("---")
    st.subheader("📊 Analysis Results")
    st.markdown(st.session_state.analysis_results)
    
    # Enhancement Section
    st.markdown("---")
    st.subheader("✨ Need a better version?")
    if st.button("Generate Enhanced & Aligned Resume"):
        with st.spinner("Reformatting and aligning..."):
            enhanced = enhance_and_align_resume(resume_text, job_description)
            st.session_state.enhanced_resume = enhanced
            st.rerun()

# Display Enhanced Resume
if "enhanced_resume" in st.session_state:
    st.markdown("## 📄 Your Enhanced & Aligned Resume")
    st.markdown(st.session_state.enhanced_resume)
    st.download_button("📥 Download Enhanced Resume (Markdown)", 
                       data=st.session_state.enhanced_resume, 
                       file_name="Enhanced_Resume.md")