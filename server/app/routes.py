from flask import current_app
import os
import re
import google.generativeai as genai
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .pdf_parser import extract_text_from_pdf
from .nlp_engine import analyze_resume, get_analysis_summary
from .email_utils import send_result_email

from .db_utils import save_analysis
from .report_genrator import ReportGenerator
    
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

    # Analyze and score - use enhanced analysis
    analysis_result = get_analysis_summary(resume_text, jd_text)
    score = analysis_result["similarity_score"]
    missing_skills = set(analysis_result["missing_keywords"])  # Use keywords instead of tokens
    matched_skills = set(analysis_result["matched_keywords"])
    
    # For backward compatibility with existing code
    missing_skills_list = list(missing_skills)

    try:
        feedback = get_resume_feedback(resume_text, jd_text)
    except Exception as e:
        feedback = [f"Gemini feedback generation failed: {str(e)}"]

    try:
        filler_sentences = generate_skill_sentences(missing_skills_list)
    except Exception as e:
        filler_sentences = [f"Gemini sentence generation failed: {str(e)}"]

    # Email results
    try:
        send_result_email(user_email, score, feedback, filler_sentences)
    except Exception as e:
        print(f"Email failed to send: {e}")

    # Save analysis to database
    try:
        save_analysis(user_email, score, missing_skills_list, feedback, filler_sentences)
        print("Analysis saved to database successfully")
    except Exception as e:
        print(f"Error saving analysis to DB: {e}")
        
        # Fallback: Save to local file using report generator
        try:
            report_generator = ReportGenerator()
            
            # Create a comprehensive report
            report = report_generator.create_analysis_report(
                user_id=user_email.split('@')[0],
                user_email=user_email,
                resume_filename=resume_file.filename if resume_file else "uploaded_resume.pdf",
                job_title="Job Analysis",
                company_name=None,
                similarity_score=score,
                missing_keywords=missing_skills_list,
                matched_keywords=list(matched_skills),
                ai_feedback=feedback
            )
            
            # Save as JSON and HTML reports
            json_path = report_generator.generate_json_report(report)
            html_path = report_generator.generate_html_report(report)
            
            print(f"Fallback: Analysis saved locally - JSON: {json_path}, HTML: {html_path}")
        except Exception as fallback_error:
            print(f"Error saving analysis to local files: {fallback_error}")

    return jsonify({
        "score": round(score * 100, 2),
        "missing_skills": missing_skills_list,
        "matched_skills": list(matched_skills),
        "suggestions": feedback,
        "generated_lines": filler_sentences,
        "analysis_details": {
            "total_keywords_found": len(matched_skills),
            "total_missing_keywords": len(missing_skills),
            "match_percentage": round(analysis_result["match_percentage"], 2)
        }
    })


@routes_bp.route('/generate-report', methods=['POST'])
@jwt_required()
def generate_report():
    """Generate a comprehensive report for the last analysis"""
    user_email = get_jwt_identity()
    
    try:
        # Get the data from the request
        data = request.get_json()
        
        # Extract data from the request or use the analysis result
        score = data.get('score', 0) / 100  # Convert from percentage
        missing_skills = data.get('missing_skills', [])
        matched_skills = data.get('matched_skills', [])
        suggestions = data.get('suggestions', [])
        generated_lines = data.get('generated_lines', [])
        
        # Create report generator
        report_generator = ReportGenerator()
        
        # Create a comprehensive report
        report = report_generator.create_analysis_report(
            user_id=user_email.split('@')[0],
            user_email=user_email,
            resume_filename="latest_resume.pdf",
            job_title="Backend Developer",  # Could be extracted from job description
            company_name=None,
            similarity_score=score,
            missing_keywords=missing_skills,
            matched_keywords=matched_skills,
            ai_feedback=suggestions
        )
        
        # Generate reports in different formats
        json_path = report_generator.generate_json_report(report)
        html_path = report_generator.generate_html_report(report)
        
        return jsonify({
            "success": True,
            "message": "Report generated successfully",
            "files": {
                "json_report": json_path,
                "html_report": html_path
            },
            "download_links": {
                "html": f"/api/download-report/{report.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                "json": f"/api/download-report/{report.user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

@routes_bp.route('/download-report/<filename>')
def download_report(filename):
    """Download a generated report"""
    try:
        from flask import send_file
        import os
        
        reports_dir = os.path.join(os.getcwd(), "reports")
        file_path = os.path.join(reports_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "Report file not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Failed to download report: {str(e)}"}), 500

@routes_bp.route('/list-reports')
@jwt_required()
def list_reports():
    """List all available reports for the current user"""
    user_email = get_jwt_identity()
    user_id = user_email.split('@')[0]
    
    try:
        import os
        reports_dir = os.path.join(os.getcwd(), "reports")
        
        if not os.path.exists(reports_dir):
            return jsonify({"reports": []})
        
        # Filter reports for current user
        all_files = os.listdir(reports_dir)
        user_reports = [f for f in all_files if f.startswith(f"resume_analysis_{user_id}")]
        
        reports = []
        for filename in user_reports:
            file_path = os.path.join(reports_dir, filename)
            stat = os.stat(file_path)
            reports.append({
                "filename": filename,
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "size": stat.st_size,
                "download_url": f"/api/download-report/{filename}"
            })
        
        return jsonify({
            "user_id": user_id,
            "total_reports": len(reports),
            "reports": sorted(reports, key=lambda x: x['created'], reverse=True)
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to list reports: {str(e)}"}), 500
