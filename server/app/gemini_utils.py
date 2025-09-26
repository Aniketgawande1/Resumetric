import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-1.5-flash-latest")

try:
    model = genai.GenerativeModel(GEMINI_MODEL_NAME)
except Exception as init_error:
    model = None
    print(f"Failed to initialize Gemini model '{GEMINI_MODEL_NAME}': {init_error}")


DEFAULT_FEEDBACK = [
    "Quantify recent achievements to highlight the impact you delivered.",
    "Align your skills section with the core requirements from the job description.",
    "Reorder or refine content so the most relevant experience appears near the top."
]


def _default_skill_sentences(missing_skills):
    if not missing_skills:
        return [
            "Collaborated across teams to deliver production-ready solutions that met business goals.",
            "Implemented modern development practices to keep releases reliable and on schedule."
        ]

    sentences = []
    for skill in missing_skills[:2]:
        sentences.append(
            f"Showcased hands-on experience with {skill} by applying it to high-impact projects."
        )

    while len(sentences) < 2:
        sentences.append(
            "Partnered with stakeholders to translate requirements into measurable outcomes."
        )

    return sentences


def _generate_with_fallback(prompt, fallback_lines):
    if not model:
        return fallback_lines

    try:
        response = model.generate_content(prompt)
        if not response or not getattr(response, "text", None):
            return fallback_lines
        lines = [line.strip() for line in response.text.split('\n') if line.strip()]
        return lines or fallback_lines
    except Exception as gen_error:
        print(f"Gemini generation failed: {gen_error}")
        return fallback_lines


def get_resume_feedback(resume, jd):
    prompt = f"""
    Analyze the following resume against the job description and provide exactly 3 concise improvement suggestions.

    Job Description:
    {jd}

    Resume:
    {resume}
    """
    return _generate_with_fallback(prompt, DEFAULT_FEEDBACK)


def generate_skill_sentences(missing_skills):
    skills = ", ".join(missing_skills)
    fallback = _default_skill_sentences(missing_skills)

    if not skills:
        return fallback

    prompt = (
        "Write 2 resume bullet sentences (no numbering) that demonstrate strong, real-world experience with the "
        f"following skills: {skills}. Focus on measurable impact."
    )

    return _generate_with_fallback(prompt, fallback)
