import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Get API key
# Note: In Streamlit Cloud, ensure your secret is named GROQ_API_KEY
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    try:
        API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        API_KEY = None

# Create Groq client
client = Groq(api_key=API_KEY) if API_KEY else None

def generate_resume_analysis(resume_text, job_description):
    if not API_KEY:
        return "Error: GROQ_API_KEY not found."

    prompt = f"""
    You are an expert HR Manager and Senior Applicant Tracking System (ATS) consultant.
    
    Analyze the following resume against the provided job description.
    
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
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume analyzer."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error communicating with Groq API: {e}"