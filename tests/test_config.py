"""Tests for config.py — app-wide constants and branding."""

import pytest


class TestConfigConstants:
    """Verify all required constants exist in config module."""

    def test_stage_thresholds_exist(self):
        from config import STAGE_THRESHOLDS
        assert isinstance(STAGE_THRESHOLDS, dict)
        assert len(STAGE_THRESHOLDS) == 5

    def test_stage_thresholds_values(self):
        from config import STAGE_THRESHOLDS
        assert STAGE_THRESHOLDS[1] == 1.8
        assert STAGE_THRESHOLDS[2] == 2.4
        assert STAGE_THRESHOLDS[3] == 3.0
        assert STAGE_THRESHOLDS[4] == 3.6
        assert STAGE_THRESHOLDS[5] == 4.0

    def test_stage_names_exist(self):
        from config import STAGE_NAMES
        assert isinstance(STAGE_NAMES, dict)
        for stage in range(1, 6):
            assert stage in STAGE_NAMES
            assert "es" in STAGE_NAMES[stage]
            assert "en" in STAGE_NAMES[stage]

    def test_brand_colors_exist(self):
        from config import BRAND_COLORS
        assert isinstance(BRAND_COLORS, dict)
        assert "primary" in BRAND_COLORS
        assert "secondary" in BRAND_COLORS

    def test_axes_list(self):
        from config import AXES
        assert AXES == ["governance", "environmental", "social", "reporting", "economic"]

    def test_supported_languages(self):
        from config import SUPPORTED_LANGUAGES
        assert "es" in SUPPORTED_LANGUAGES
        assert "en" in SUPPORTED_LANGUAGES

    def test_default_language(self):
        from config import DEFAULT_LANGUAGE
        assert DEFAULT_LANGUAGE in ("es", "en")
