import os
import smtplib
from email.mime.text import MIMEText

def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

_load_env()

def send_email(to_email, stats):
    sender = os.environ.get('EMAIL_ADDRESS')
    password = os.environ.get('EMAIL_APP_PASSWORD')

    if not sender or not password:
        print("Email credentials not found in .env")
        return

    winner = "You won!" if stats['winner'] == 'player' else "You lost!"
    score = f"{stats['player_score']} - {stats['opponent_score']}"
    mins = stats['duration_seconds'] // 60
    secs = stats['duration_seconds'] % 60

    body = f"""Touchless Pong Results

{winner}

Final score: {score}
Duration: {mins}m {secs}s

Thanks for playing!"""

    msg = MIMEText(body)
    msg['Subject'] = 'Touchless Pong - Game Results'
    msg['From'] = sender
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email error: {e}")