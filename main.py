from fastapi import FastAPI
from sentiment import analyze_sentiment
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


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