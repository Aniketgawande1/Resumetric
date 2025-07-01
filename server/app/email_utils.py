

from flask_mail import Message
from flask import current_app
from . import mail  # Make sure this import is correct

def send_result_email(user_email, score, feedback, lines):
    # Format feedback as readable text
    if isinstance(feedback, list):
        formatted_feedback = "\n".join(feedback)
    else:
        formatted_feedback = feedback

    # Format lines (resume bullet points)
    formatted_lines = ""
    if lines:
        formatted_lines += f"  - {lines[0]}\n"
        if len(lines) > 1:
            formatted_lines += f"  - {lines[1]}"
    else:
        formatted_lines = "  - No key points found."

    msg = Message(
        "Your Resume Feedback",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[user_email]
    )

    msg.body = f"""Hello,

Here's your resume analysis:

- Score: {round(score * 100, 2)}%

- Feedback:
{formatted_feedback}

- Key Suggestions:
{formatted_lines}

Regards,
Resumetric Bot
"""

    mail.send(msg)
