from flask_mail import Message
from . import mail

def send_result_email(user_email, score, feedback, lines):
    msg = Message("Your Resume Ranking Result",
                  sender="your_email@gmail.com",
                  recipients=[user_email])
    msg.body = f"""
Your resume score: {round(score*100, 2)}%

Suggestions:
- {feedback[0]}
- {feedback[1]}
- {feedback[2]}

Skill Additions:
- {lines[0]}
- {lines[1]}
"""
    mail.send(msg)