"""Tests for i18n JSON files — ensure both languages have matching keys."""

import json
import os
import pytest


I18N_DIR = os.path.join(os.path.dirname(__file__), "..", "i18n")

REQUIRED_KEYS = [
    "app_title",
    "start_button",
    "profile_company",
    "profile_sector",
    "profile_size",
    "profile_name",
    "profile_role",
    "question_progress",
    "results_title",
    "results_stage",
    "download_pdf",
    "stage_1_name",
    "stage_2_name",
    "stage_3_name",
    "stage_4_name",
    "stage_5_name",
]


class TestI18nFiles:
    """Validate i18n JSON structure and coverage."""

    def test_es_json_loads(self, es_strings):
        assert isinstance(es_strings, dict)
        assert len(es_strings) > 0

    def test_en_json_loads(self, en_strings):
        assert isinstance(en_strings, dict)
        assert len(en_strings) > 0

    def test_es_has_all_required_keys(self, es_strings):
        for key in REQUIRED_KEYS:
            assert key in es_strings, f"Missing key in es.json: {key}"

    def test_en_has_all_required_keys(self, en_strings):
        for key in REQUIRED_KEYS:
            assert key in en_strings, f"Missing key in en.json: {key}"

    def test_both_languages_have_same_keys(self, es_strings, en_strings):
        es_keys = set(es_strings.keys())
        en_keys = set(en_strings.keys())
        missing_in_en = es_keys - en_keys
        missing_in_es = en_keys - es_keys
        assert missing_in_en == set(), f"Keys in ES but not EN: {missing_in_en}"
        assert missing_in_es == set(), f"Keys in EN but not ES: {missing_in_es}"

    def test_no_empty_values_es(self, es_strings):
        for key, value in es_strings.items():
            assert value.strip() != "", f"Empty value in es.json for key: {key}"

    def test_no_empty_values_en(self, en_strings):
        for key, value in en_strings.items():
            assert value.strip() != "", f"Empty value in en.json for key: {key}"
