from flask import current_app

def save_analysis(email, score, skills, suggestions, sentences):
    return current_app.mongo['analysis_results'].insert_one({
        "user_email": email,
        "score": score,
        "missing_skills": skills,
        "suggestions": suggestions,
        "generated_lines": sentences
    })
