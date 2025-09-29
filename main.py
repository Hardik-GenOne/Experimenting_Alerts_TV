from fastapi import FastAPI, Query
import requests

app = FastAPI()

# Your Telegram bot token and chat_id
TELEGRAM_TOKEN = "8021458974:AAH_U6vWbr877Cv669Ig88MFqWVUWZtf5Mk"
CHAT_ID = "5609562789"  # Your Telegram user ID or group ID

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/alerts")
def receive_alert(alert: str = Query(..., description="Alert message from TV")):
    # Send alert to Telegram
    telegram_response = send_telegram_message(alert)
    return {"status": "sent", "telegram_response": telegram_response}
