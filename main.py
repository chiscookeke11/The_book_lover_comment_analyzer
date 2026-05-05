from fastapi import FastAPI, Request
from sentiment import analyze_sentiment
from scheduler import publish_scheduled_articles
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
CRON_SECRET = os.getenv("CRON_SECRET")



@app.get("/")
def home():
    return {"status": "API running"}


@app.post("/analyze")
async def analyze(data: dict):
    # Supabase sends data like this
    comment = data["record"]
    text = comment["content"]
    comment_id = comment["id"]

    result = analyze_sentiment(text)

    # Update Supabase
    response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/comments?id=eq.{comment_id}",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "sentiment": result["label"],
            "score": result["score"]
        }
    )

    print("Supabase response:", response.text)

    print("Incoming:", data)
    print("Result:", result)

    return {"status": "processed"}


@app.post("/publish-scheduled")
async def publish_scheduled(request: Request):
    auth_header = request.headers.get("authorization")

    if auth_header != f"Bearer {CRON_SECRET}":
        return {"error": "Unauthorized"}

    result = publish_scheduled_articles()
    return result