import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

# Get API key from .env or Streamlit Secrets
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    API_KEY = st.secrets.get("GEMINI_API_KEY")

st.write("DEBUG KEY PREFIX:", API_KEY[:10] if API_KEY else "NONE")

# Configure Gemini
if API_KEY:
    genai.configure(api_key=API_KEY)


def generate_resume_analysis(resume_text, job_description):
    if not API_KEY:
        return "Error: Gemini API key not found."

    prompt = f"""
You are an expert HR Manager and Senior Applicant Tracking System (ATS) consultant.

Analyze the following resume explicitly against the provided job description.

CRITICAL INSTRUCTION:
You must start your response with a score line formatted exactly like this:

[SCORE: XX]

Where XX is a realistic integer match percentage from 0 to 100 based on the resume alignment.

Then provide the rest of your feedback using this structure:

### 🔍 Missing Keywords & Skills
- List important skills or keywords missing from the resume.

### 📝 Resume Optimization Strategy
- Give actionable ATS optimization suggestions.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        st.error(repr(e))
        return f"Gemini Engine Connection Error: {str(e)}"