import os
from datetime import datetime, timezone
from fastapi import APIRouter, Request, HTTPException
from supabase import create_client, Client

router = APIRouter()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")
SCHEDULER_SECRET: str = os.getenv("SCHEDULER_SECRET")   # reuse CRON_SECRET you already have

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.post("/publish-due-posts")
async def publish_due_posts(request: Request):
    # Verify the shared secret sent by Supabase Cron
    if request.headers.get("X-Scheduler-Key") != SCHEDULER_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    now = datetime.now(timezone.utc).isoformat()

    # Find all articles where scheduled_at <= now AND status is "scheduled"
    result = (
        supabase.table("articles")
        .select("id, title, scheduled_at")
        .lte("scheduled_at", now)
        .eq("status", "scheduled")
        .execute()
    )

    articles = result.data or []
    published_ids = []

    for article in articles:
        supabase.table("articles").update({
            "status": "published",
        }).eq("id", article["id"]).execute()

        published_ids.append(article["id"])
        print(f"[scheduler] Published article {article['id']} — '{article.get('title', '')}'")

    return {
        "status": "ok",
        "published_count": len(published_ids),
        "published_ids": published_ids,
    }