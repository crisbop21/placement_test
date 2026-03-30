"""Tests for db/ modules — client singleton and question fetching."""

import importlib
import sys
import pytest
from unittest.mock import patch, MagicMock


class TestSupabaseClient:
    """Test the Supabase client singleton."""

    def _reload_client_module(self):
        """Force reimport of the client module with clean state."""
        if "app.db.client" in sys.modules:
            del sys.modules["app.db.client"]
        import app.db.client as client_module
        return client_module

    def test_get_client_returns_client(self):
        """get_client should return a Supabase client object."""
        client_module = self._reload_client_module()
        mock_client = MagicMock()

        with patch.dict("sys.modules", {"supabase": MagicMock()}):
            # Mock the lazy import inside get_client
            import supabase
            supabase.create_client = MagicMock(return_value=mock_client)

            # Patch the internal import
            original_import = __builtins__.__import__ if hasattr(__builtins__, '__import__') else __import__

            def mock_import(name, *args, **kwargs):
                if name == "supabase":
                    mod = MagicMock()
                    mod.create_client = MagicMock(return_value=mock_client)
                    return mod
                return original_import(name, *args, **kwargs)

            with patch("builtins.__import__", side_effect=mock_import):
                client_module._client = None
                result = client_module.get_client()

            assert result is mock_client

    def test_get_client_is_singleton(self):
        """Calling get_client twice should return the same instance."""
        client_module = self._reload_client_module()
        mock_client = MagicMock()
        # Directly set the singleton to test caching behavior
        client_module._client = mock_client

        first = client_module.get_client()
        second = client_module.get_client()
        assert first is second
        assert first is mock_client


class TestFetchQuestions:
    """Test db/questions.py — fetching active questions."""

    def _get_questions_module(self, mock_client):
        """Import questions module with mocked client."""
        # Ensure clean import
        for mod_name in ["app.db.questions", "app.db.client"]:
            if mod_name in sys.modules:
                del sys.modules[mod_name]

        # Pre-set the client singleton so it doesn't try to import supabase
        import app.db.client as client_module
        client_module._client = mock_client

        import app.db.questions as questions_module
        return questions_module

    def test_fetch_active_questions_returns_list(self, sample_questions):
        """fetch_active_questions should return a list of question dicts."""
        mock_response = MagicMock()
        mock_response.data = sample_questions

        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.return_value = mock_response

        questions_module = self._get_questions_module(mock_client)
        result = questions_module.fetch_active_questions()

        assert isinstance(result, list)
        assert len(result) == 5

    def test_fetch_active_questions_filters_active(self, sample_questions):
        """Should query for is_active=True."""
        mock_response = MagicMock()
        mock_response.data = sample_questions

        mock_client = MagicMock()
        mock_table = mock_client.table.return_value
        mock_select = mock_table.select.return_value
        mock_eq = mock_select.eq.return_value
        mock_eq.order.return_value.execute.return_value = mock_response

        questions_module = self._get_questions_module(mock_client)
        questions_module.fetch_active_questions()

        mock_client.table.assert_called_with("questions")
        mock_select.eq.assert_called_with("is_active", True)

    def test_fetch_active_questions_orders_by_order_num(self, sample_questions):
        """Should order results by order_num."""
        mock_response = MagicMock()
        mock_response.data = sample_questions

        mock_client = MagicMock()
        mock_table = mock_client.table.return_value
        mock_select = mock_table.select.return_value
        mock_eq = mock_select.eq.return_value
        mock_order = mock_eq.order.return_value
        mock_order.execute.return_value = mock_response

        questions_module = self._get_questions_module(mock_client)
        questions_module.fetch_active_questions()

        mock_eq.order.assert_called_with("order_num")

    def test_fetch_active_questions_handles_db_error(self):
        """Should return empty list on database error, not crash."""
        mock_client = MagicMock()
        mock_client.table.return_value.select.return_value.eq.return_value.order.return_value.execute.side_effect = Exception("DB error")

        questions_module = self._get_questions_module(mock_client)
        result = questions_module.fetch_active_questions()

        assert result == []
