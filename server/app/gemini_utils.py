import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyAJlbXwlsKB-u2WWP14NLt4TvAK6DRFbuc"))
model = genai.GenerativeModel("gemini-1.5-flash")
 # ✅ works



def get_resume_feedback(resume, jd):
    prompt = f"""
    Here is a job description:
    {jd}

    And here is a resume:
    {resume}

    Suggest 3 ways to improve the resume based on the job description.
    """
    response = model.generate_content(prompt)
    return response.text.split('\n')

def generate_skill_sentences(missing_skills):
    skills = ", ".join(missing_skills)
    prompt = f"Write 2 resume sentences that show experience with: {skills}"
    response = model.generate_content(prompt)
    return response.text.split('\n')
