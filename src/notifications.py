import os
import clicksend_client
from clicksend_client import SmsMessage
from clicksend_client.rest import ApiException

import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def _load_env():
    """Read .env file from project root."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

_load_env()

def send_sms(phone, stats):
    username = os.environ.get('CLICKSEND_USERNAME')
    api_key = os.environ.get('CLICKSEND_API_KEY')

    if not username or not api_key:
        print("ClickSend credentials not found in .env")
        return

    configuration = clicksend_client.Configuration()
    configuration.username = username
    configuration.password = api_key

    api_instance = clicksend_client.SMSApi(
        clicksend_client.ApiClient(configuration)
    )

    winner = "You won!" if stats['winner'] == 'player' else "You lost!"
    score = f"{stats['player_score']} - {stats['opponent_score']}"
    mins = stats['duration_seconds'] // 60
    secs = stats['duration_seconds'] % 60

    body = f"Touchless Pong Results: {winner} Final score: {score}. Duration: {mins}m {secs}s."

    message = SmsMessage(
        source="TouchlessPong",
        body=body,
        to=phone
    )
    sms_collection = clicksend_client.SmsMessageCollection(messages=[message])

    try:
        response = api_instance.sms_send_post(sms_collection)
        status = response['data']['messages'][0]['status']
        if status == 'SUCCESS':
            print(f"SMS sent to {phone}")
        else:
            print(f"Failed to send SMS: {status}")
    except ApiException as e:
        print(f"ClickSend error: {e}")