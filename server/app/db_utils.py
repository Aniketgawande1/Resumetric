from flask import current_app

def save_analysis(email, score, skills, suggestions, sentences):
    """Save analysis to MongoDB if available, otherwise skip"""
    try:
        if hasattr(current_app, 'mongo') and current_app.mongo is not None:
            return current_app.mongo['analysis_results'].insert_one({
                "user_email": email,
                "score": score,
                "missing_skills": skills,
                "suggestions": suggestions,
                "generated_lines": sentences
            })
        else:
            print("MongoDB not available, skipping database save")
            return None
    except Exception as e:
        print(f"Error saving to database: {e}")
        return None
