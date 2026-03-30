"""Write completed session to Supabase."""

import uuid
from app.db.client import get_client


def save_response(payload: dict) -> str | None:
    """Save a completed diagnostic response to Supabase. Returns session ID or None on error."""
    try:
        if "id" not in payload:
            payload["id"] = str(uuid.uuid4())
        client = get_client()
        client.table("responses").insert(payload).execute()
        return payload["id"]
    except Exception:
        return None
