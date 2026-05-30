import os
from google import genai
from dotenv import load_dotenv

load_dotenv(override=True)
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

def generate_resume_analysis(resume_text, job_description):
    if not api_key or client is None:
        return "Error: Gemini API key 'GEMINI_API_KEY' could not be loaded from your .env file."
        
    prompt = f"""
    You are an expert HR Manager and Senior Applicant Tracking System (ATS) consultant. 
    Analyze the following resume explicitly against the provided job description.
    
    CRITICAL INSTRUCTION: You must start your response with a score line formatted exactly like this:
    [SCORE: XX] 
    Where XX is a realistic integer match percentage from 0 to 100 based on the resume alignment. Do not put text before this tag.
    
    Then provide the rest of your feedback using this structure:
    ### 🔍 Missing Keywords & Skills
    - List vital skills missing from the resume.
    
    ### 📝 Resume Optimization Strategy
    - Actionable feedback to pass an ATS scan.

    RESUME TEXT: {resume_text}
    JOB DESCRIPTION: {job_description}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"Gemini 3.5 Engine Connection Error: {str(e)}"