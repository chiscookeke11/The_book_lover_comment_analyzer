import os
import requests
from datetime import datetime, timezone


SUPABASE_URL = os.getenv("SUPASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

def publish_scheduled_articles():
    now = datetime.now(timezone.utc).isoformat()

# Fetched scheduled articles
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/articles",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        },

        params={
             "select": "id",
            "status": "eq.scheduled",
            "scheduled_at": f"lte.{now}"
        }
    )


    data = response.json()

    if not data:
        print("NOW:", now)
        return {"message": "Nothing to publish"}

    ids = [item["id"] for item in data]

    # Update articles
    update_response = requests.patch(
        f"{SUPABASE_URL}/rest/v1/articles?id=in.({','.join(map(str, ids))})",
        headers={
            "apikey": SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "status": "published"
        }
    )

    print("NOW:", now)

    if update_response.status_code >= 400:
        return {"error": update_response.text}

    return {
        "message": "Published successfully",
        "ids": ids
    }