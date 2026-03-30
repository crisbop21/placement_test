"""Shared fixtures for all tests."""

import json
import os
import pytest


@pytest.fixture
def sample_questions():
    """Return a list of sample question dicts mimicking Supabase rows."""
    return [
        {
            "id": "q1",
            "order_num": 1,
            "axis": "governance",
            "block": "A",
            "text_es": "¿Pregunta de gobernanza?",
            "text_en": "Governance question?",
            "option_a_es": "Opción A", "option_a_en": "Option A",
            "option_b_es": "Opción B", "option_b_en": "Option B",
            "option_c_es": "Opción C", "option_c_en": "Option C",
            "option_d_es": "Opción D", "option_d_en": "Option D",
            "score_a": 1, "score_b": 2, "score_c": 3, "score_d": 4,
            "weight": 1.0,
            "is_active": True,
        },
        {
            "id": "q2",
            "order_num": 2,
            "axis": "environmental",
            "block": "B",
            "text_es": "¿Pregunta ambiental?",
            "text_en": "Environmental question?",
            "option_a_es": "Opción A", "option_a_en": "Option A",
            "option_b_es": "Opción B", "option_b_en": "Option B",
            "option_c_es": "Opción C", "option_c_en": "Option C",
            "option_d_es": "Opción D", "option_d_en": "Option D",
            "score_a": 1, "score_b": 2, "score_c": 3, "score_d": 4,
            "weight": 1.0,
            "is_active": True,
        },
        {
            "id": "q3",
            "order_num": 3,
            "axis": "social",
            "block": "C",
            "text_es": "¿Pregunta social?",
            "text_en": "Social question?",
            "option_a_es": "Opción A", "option_a_en": "Option A",
            "option_b_es": "Opción B", "option_b_en": "Option B",
            "option_c_es": "Opción C", "option_c_en": "Option C",
            "option_d_es": "Opción D", "option_d_en": "Option D",
            "score_a": 1, "score_b": 2, "score_c": 3, "score_d": 4,
            "weight": 1.0,
            "is_active": True,
        },
        {
            "id": "q4",
            "order_num": 4,
            "axis": "reporting",
            "block": "D",
            "text_es": "¿Pregunta de reporte?",
            "text_en": "Reporting question?",
            "option_a_es": "Opción A", "option_a_en": "Option A",
            "option_b_es": "Opción B", "option_b_en": "Option B",
            "option_c_es": "Opción C", "option_c_en": "Option C",
            "option_d_es": "Opción D", "option_d_en": "Option D",
            "score_a": 1, "score_b": 2, "score_c": 3, "score_d": 4,
            "weight": 1.0,
            "is_active": True,
        },
        {
            "id": "q5",
            "order_num": 5,
            "axis": "economic",
            "block": "E",
            "text_es": "¿Pregunta económica?",
            "text_en": "Economic question?",
            "option_a_es": "Opción A", "option_a_en": "Option A",
            "option_b_es": "Opción B", "option_b_en": "Option B",
            "option_c_es": "Opción C", "option_c_en": "Option C",
            "option_d_es": "Opción D", "option_d_en": "Option D",
            "score_a": 1, "score_b": 2, "score_c": 3, "score_d": 4,
            "weight": 1.0,
            "is_active": True,
        },
    ]


@pytest.fixture
def es_strings():
    """Return Spanish i18n strings loaded from file."""
    path = os.path.join(os.path.dirname(__file__), "..", "i18n", "es.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def en_strings():
    """Return English i18n strings loaded from file."""
    path = os.path.join(os.path.dirname(__file__), "..", "i18n", "en.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
