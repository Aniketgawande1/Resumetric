# import os
# import google.generativeai as genai
# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from .pdf_parser import extract_text_from_pdf
# from .nlp_engine import analyze_resume
# from .email_utils import send_result_email

# routes_bp = Blueprint('routes', __name__)

# # ✅ Correct Gemini model
# genai.configure(api_key=os.getenv("AIzaSyAJlbXwlsKB-u2WWP14NLt4TvAK6DRFbuc"))
# model = genai.GenerativeModel("gemini-1.5-flash")



# def get_resume_feedback(resume, jd):
#     prompt = f"""
#     Analyze the following resume against the job description and give 3 improvement suggestions.

#     Job Description:
#     {jd}

#     Resume:
#     {resume}
#     """
#     response = model.generate_content(prompt)
#     return response.text.strip().split('\n')


# def generate_skill_sentences(missing_skills):
#     skills = ", ".join(missing_skills)
#     prompt = f"Write 2 strong resume sentences demonstrating experience with the following skills: {skills}"
#     response = model.generate_content(prompt)
#     return response.text.strip().split('\n')


# @routes_bp.route('/analyze', methods=['POST'])
# @jwt_required()
# def analyze():
#     user_email = get_jwt_identity()

#     resume_file = request.files.get('resume')
#     jd_text = request.form.get('job_description')

#     if resume_file is None or jd_text is None:
#         return jsonify({"error": "Missing resume file or job description"}), 400

#     resume_text = extract_text_from_pdf(resume_file)
#     score, missing_skills = analyze_resume(resume_text, jd_text)

#     feedback = get_resume_feedback(resume_text, jd_text)
#     filler_sentences = generate_skill_sentences(missing_skills)

#     send_result_email(user_email, score, feedback, filler_sentences)

#     return jsonify({
#         "score": round(score * 100, 2),
#         "missing_skills": list(missing_skills),
#         "suggestions": feedback,
#         "generated_lines": filler_sentences
#     })
from flask import current_app
import os
import re
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .pdf_parser import extract_text_from_pdf
from .nlp_engine import analyze_resume
from .email_utils import send_result_email

from .db_utils import save_analysis
try:
    save_analysis(user_email, score, list(missing_skills), feedback, filler_sentences)
except Exception as e:
    print(f"Error saving analysis to DB: {e}")
    
routes_bp = Blueprint('routes', __name__)

# ✅ Secure Gemini key configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Store in .env safely
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_skills_from_text(text):
    # Keywords list can be extended
    keywords = ['python', 'java', 'nodejs', 'react', 'express', 'mongodb', 'docker', 'aws', 'flask', 'sql']
    found = []
    text_lower = text.lower()
    for kw in keywords:
        if re.search(rf'\b{kw}\b', text_lower):
            found.append(kw)
    return list(set(found))


def get_resume_feedback(resume, jd):
    prompt = f"""
    Analyze the following resume against the job description and give 3 improvement suggestions.

    Job Description:
    {jd}

    Resume:
    {resume}
    """
    response = model.generate_content(prompt)
    return response.text.strip().split('\n')


def generate_skill_sentences(missing_skills):
    if not missing_skills:
        return ["No missing skills detected."]
    skills = ", ".join(missing_skills)
    prompt = f"Write 2 strong resume sentences demonstrating experience with the following skills: {skills}"
    response = model.generate_content(prompt)
    return response.text.strip().split('\n')


@routes_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    user_email = get_jwt_identity()

    resume_file = request.files.get('resume')
    jd_text = request.form.get('job_description')

    if resume_file is None or jd_text is None:
        return jsonify({"error": "Missing resume file or job description"}), 400

    # Extract text from resume
    resume_text = extract_text_from_pdf(resume_file)

    # Basic cleanup if someone sends just "python java" as job description
    if len(jd_text.split()) <= 5:
        extracted_skills = extract_skills_from_text(jd_text)
        jd_text = "We are looking for candidates with experience in: " + ", ".join(extracted_skills)

    # Analyze and score
    score, missing_skills = analyze_resume(resume_text, jd_text)

    try:
        feedback = get_resume_feedback(resume_text, jd_text)
    except Exception as e:
        feedback = [f"Gemini feedback generation failed: {str(e)}"]

    try:
        filler_sentences = generate_skill_sentences(missing_skills)
    except Exception as e:
        filler_sentences = [f"Gemini sentence generation failed: {str(e)}"]

    # Email results
    try:
        send_result_email(user_email, score, feedback, filler_sentences)
    except Exception as e:
        print(f"Email failed to send: {e}")

    return jsonify({
        "score": round(score * 100, 2),
        "missing_skills": list(missing_skills),
        "suggestions": feedback,
        "generated_lines": filler_sentences
    })
