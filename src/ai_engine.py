import os
import streamlit as st
from groq import Groq

def get_groq_client():
    """Groq API client ko secure tarike se initialize karta hai."""
    api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def generate_resume_analysis(resume_text, job_description):
    """Resume ka analysis aur score nikalne ke liye."""
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not found."

    prompt = f"""
    You are an expert HR Manager and Senior Applicant Tracking System (ATS) consultant.
    Analyze the following resume against the provided job description.
    
    CRITICAL INSTRUCTION:
    Start your response with: [SCORE: XX] (where XX is 0-100 integer match percentage).
    
    Then provide:
    ### 🔍 Missing Keywords & Skills
    - List important skills or keywords missing from the resume.
    
    ### 📝 Resume Optimization Strategy
    - Give actionable ATS optimization suggestions.
    
    RESUME TEXT: {resume_text}
    JOB DESCRIPTION: {job_description}
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are a professional resume analyzer."},
                      {"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def enhance_and_align_resume(resume_text, job_description):
    """Resume ko professionally reformat aur align karne ke liye."""
    client = get_groq_client()
    if not client:
        return "Error: GROQ_API_KEY not found."

    prompt = f"""
    You are an expert Resume Editor. 
    Task: Rewrite the provided 'RESUME TEXT' into a perfectly aligned, ATS-friendly format.
    
    Guidelines:
    1. Organize into sections: Professional Summary, Skills, Experience, Education.
    2. Use strong action verbs and quantify achievements.
    3. Ensure keyword alignment with the 'JOB DESCRIPTION'.
    4. Return the result in clean, well-structured Markdown format.
    
    JOB DESCRIPTION: {job_description}
    RESUME TEXT: {resume_text}
    """
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are an expert resume editor."},
                      {"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error enhancing resume: {str(e)}"