"""Supabase client singleton."""

import os

_client = None


def get_client():
    """Return a singleton Supabase client instance."""
    global _client
    if _client is None:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_ANON_KEY", "")
        _client = create_client(url, key)
    return _client
