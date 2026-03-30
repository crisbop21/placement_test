"""Fetch active questions from Supabase."""

from app.db.client import get_client


def fetch_active_questions() -> list[dict]:
    """Fetch all active questions ordered by order_num."""
    try:
        client = get_client()
        response = (
            client.table("questions")
            .select("*")
            .eq("is_active", True)
            .order("order_num")
            .execute()
        )
        return response.data
    except Exception:
        return []
