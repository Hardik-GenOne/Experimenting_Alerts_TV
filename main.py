from fastapi import FastAPI, Request
import requests

app = FastAPI()

TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

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

@app.post("/alerts")
async def receive_alert(request: Request):
    data = await request.json()
    alert_message = data.get("alert", "No message received")
    telegram_response = send_telegram_message(alert_message)
    return {"status": "sent", "alert": alert_message, "telegram_response": telegram_response}
