from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .pdf_parser import extract_text_from_pdf
from .nlp_engine import analyze_resume
from .email_utils import send_result_email
import google.generativeai as genai
import os

# ✅ Define blueprint BEFORE using it
routes_bp = Blueprint('routes', __name__)

# ✅ Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

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

@routes_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    user_email = get_jwt_identity()
    resume_file = request.files.get('resume')
    jd_text = request.form.get('job_description')

    if not resume_file or not jd_text:
        return jsonify({"error": "Missing resume or job description"}), 400

    resume_text = extract_text_from_pdf(resume_file)
    score, missing_skills = analyze_resume(resume_text, jd_text)
    feedback = get_resume_feedback(resume_text, jd_text)
    filler_sentences = generate_skill_sentences(missing_skills)

    send_result_email(user_email, score, feedback, filler_sentences)

    return jsonify({
        'score': round(score * 100, 2),
        'missing_skills': list(missing_skills),
        'suggestions': feedback,
        'generated_lines': filler_sentences
    })
