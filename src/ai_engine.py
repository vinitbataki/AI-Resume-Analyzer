import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        API_KEY = None

# Create Gemini client
client = genai.Client(api_key=API_KEY) if API_KEY else None


def generate_resume_analysis(resume_text, job_description):
    if not API_KEY:
        return "Error: GEMINI_API_KEY not found."

    prompt = f"""
You are an expert HR Manager and Senior Applicant Tracking System (ATS) consultant.

Analyze the following resume explicitly against the provided job description.

CRITICAL INSTRUCTION:
You must start your response with a score line formatted exactly like this:

[SCORE: XX]

Where XX is a realistic integer match percentage from 0 to 100.

Then provide:

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
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    except Exception as e:
        st.error(repr(e))
        return f"Gemini Engine Connection Error: {str(e)}"