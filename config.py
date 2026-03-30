"""App-wide constants: colors, branding, stage thresholds."""

import os
from dotenv import load_dotenv

load_dotenv()

# ESG axes
AXES: list[str] = ["governance", "environmental", "social", "reporting", "economic"]

# Maturity stage score thresholds (upper bound inclusive)
STAGE_THRESHOLDS: dict[int, float] = {
    1: 1.8,
    2: 2.4,
    3: 3.0,
    4: 3.6,
    5: 4.0,
}

# Maturity stage names in both languages
STAGE_NAMES: dict[int, dict[str, str]] = {
    1: {"es": "Sensibilización", "en": "Awareness"},
    2: {"es": "Adopción", "en": "Adoption"},
    3: {"es": "Especialización", "en": "Specialization"},
    4: {"es": "Gobernanza", "en": "Governance"},
    5: {"es": "Comunicación Estratégica", "en": "Strategic Communication"},
}

# Brand colors
BRAND_COLORS: dict[str, str] = {
    "primary": "#2E7D32",
    "secondary": "#1565C0",
    "accent": "#FF8F00",
    "background": "#FAFAFA",
    "text": "#212121",
}

# Language settings
SUPPORTED_LANGUAGES: list[str] = ["es", "en"]
DEFAULT_LANGUAGE: str = os.getenv("APP_LANG_DEFAULT", "es")
