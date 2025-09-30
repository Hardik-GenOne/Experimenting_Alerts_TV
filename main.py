from fastapi import FastAPI, Request
import requests

app = FastAPI()

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
def home():
    return {"message": "Hello, World!"}

@app.get("/ping")
def ping():
    return {"status": "OK"}

@app.post("/alerts")
async def receive_alert(request: Request):
    try:
        data = await request.json()  # try parse JSON
    except:
        body = await request.body()  # fallback to raw text
        data = {"raw": body.decode("utf-8")}

    # Pick message safely
    if isinstance(data, dict):
        alert_message = data.get("alert") or str(data)
    else:
        alert_message = str(data)

    telegram_response = send_telegram_message(alert_message)
    return {"status": "sent", "alert": alert_message, "telegram_response": telegram_response}
