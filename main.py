from fastapi import FastAPI, Request
import db, handlers, os

app = FastAPI(title="ZIMSEC AI Tutor")
db.init_db()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "zimsec123")

@app.get("/")
def root():
    return {"status": "ZIMSEC AI Tutor is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return "Verification failed"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    await handlers.handle_whatsapp_message(data)
    return {"status": "ok"}
