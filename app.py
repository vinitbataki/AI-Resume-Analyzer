import streamlit as st
from src.ai_engine import generate_resume_analysis, enhance_and_align_resume
from pypdf import PdfReader

st.set_page_config(page_title="AI ATS Optimizer", page_icon="📄")
st.title("📄 AI Resume ATS Optimizer")

# --- 1. Sidebar ---
job_description = st.sidebar.text_area("Paste Job Description here:")
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    return "".join([page.extract_text() for page in reader.pages])

# --- 2. Logic & Buttons ---
if uploaded_file and job_description:
    resume_text = extract_text_from_pdf(uploaded_file)
    
    # Analyze Button
    if st.button("🚀 Analyze Resume"):
        with st.spinner("Analyzing..."):
            st.session_state.analysis_results = generate_resume_analysis(resume_text, job_description)
    
    # --- 3. Results Section ---
    if "analysis_results" in st.session_state:
        st.markdown("---")
        st.subheader("📊 Analysis Results")
        st.markdown(st.session_state.analysis_results)
        
        # Enhanced Resume Button (Jo aapko add karna tha)
        st.markdown("---")
        if st.button("✨ Generate Enhanced & Aligned Resume"):
            with st.spinner("Reformatting and aligning..."):
                st.session_state.enhanced_resume = enhance_and_align_resume(resume_text, job_description)
                st.rerun()

# --- 4. Enhanced Resume Display ---
if "enhanced_resume" in st.session_state:
    st.markdown("## 📄 Your Enhanced & Aligned Resume")
    st.markdown(st.session_state.enhanced_resume)
    st.download_button("📥 Download Enhanced Resume", 
                       data=st.session_state.enhanced_resume, 
                       file_name="Enhanced_Resume.md")