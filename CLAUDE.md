# CLAUDE.md — Sustainability Diagnostic Tool

> This file is read automatically by Claude Code at the start of every session.
> It contains the full context, architecture, conventions, and task instructions needed to build and maintain this project.

---

## 🧭 Project Overview

**What this is:** A bilingual (Spanish / English) web application that asks sustainability-related questions, scores the user's ESG maturity, and recommends a personalized learning path from a catalogue of 48 courses.

**Who uses it:** End clients fill it out independently (no consultant present).

**Stack:** Python · Streamlit · Supabase (PostgreSQL)

**Output:** Maturity score per ESG axis + ordered course recommendations + downloadable PDF report.

---

## 📁 Repository Structure

```
sustainability-diagnostic/
├── CLAUDE.md                  ← You are here. Claude Code reads this first.
├── README.md                  ← Public-facing project description
├── .env.example               ← Environment variable template (never commit .env)
├── requirements.txt           ← Python dependencies
├── config.py                  ← App-wide constants: colors, branding, stage thresholds
├── i18n/
│   ├── es.json                ← All Spanish UI strings
│   └── en.json                ← All English UI strings
├── app/
│   ├── main.py                ← Streamlit entry point (st.set_page_config here only)
│   ├── pages/
│   │   ├── 1_questionnaire.py ← Multi-step form: profile → questions → results
│   │   ├── 2_results.py       ← Score display, radar chart, learning path
│   │   └── 3_admin.py         ← Password-protected admin dashboard
│   ├── components/
│   │   ├── language_toggle.py ← ES/EN switcher component
│   │   ├── progress_bar.py    ← Question progress indicator
│   │   ├── radar_chart.py     ← Plotly radar chart for axis scores
│   │   └── course_card.py     ← Single course recommendation card
│   ├── engine/
│   │   ├── scorer.py          ← Scoring logic: answers → axis scores → overall stage
│   │   ├── recommender.py     ← Maps stage + axis weaknesses → ordered course list
│   │   └── pdf_generator.py   ← Generates branded PDF report (ReportLab)
│   └── db/
│       ├── client.py          ← Supabase client singleton
│       ├── questions.py       ← Fetch active questions from Supabase
│       └── responses.py       ← Write completed session to Supabase
├── data/
│   └── seed_questions.sql     ← SQL to seed the initial 25 questions into Supabase
├── tests/
│   ├── test_scorer.py
│   ├── test_recommender.py
│   └── test_db.py
└── docs/
    └── technical_brief.docx   ← Full technical brief (reference only)
```

---

## ⚙️ Environment Setup

### 1. Clone and install

```bash
git clone https://github.com/YOUR_ORG/sustainability-diagnostic.git
cd sustainability-diagnostic
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

`.env.example` contents:
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
ADMIN_PASSWORD=choose-a-secure-password
APP_LANG_DEFAULT=es
```

> ⚠️ **Never commit `.env` to the repository.** It is in `.gitignore`.

### 3. Seed the database

```bash
# Run the seed SQL in your Supabase project's SQL editor,
# or use the Supabase CLI:
supabase db push
# or manually paste contents of data/seed_questions.sql
```

### 4. Run locally

```bash
streamlit run app/main.py
```

---

## 🗄️ Supabase Schema

### Table: `questions`

```sql
create table questions (
  id           uuid primary key default gen_random_uuid(),
  order_num    int not null,
  axis         text not null check (axis in ('governance','environmental','social','reporting','economic')),
  block        text not null,          -- 'A' through 'E'
  text_es      text not null,
  text_en      text not null,
  option_a_es  text not null,
  option_a_en  text not null,
  option_b_es  text not null,
  option_b_en  text not null,
  option_c_es  text not null,
  option_c_en  text not null,
  option_d_es  text not null,
  option_d_en  text not null,
  score_a      int not null default 1,
  score_b      int not null default 2,
  score_c      int not null default 3,
  score_d      int not null default 4,
  weight       float not null default 1.0,
  is_active    boolean not null default true
);
```

### Table: `responses`

```sql
create table responses (
  id                    uuid primary key default gen_random_uuid(),
  created_at            timestamptz default now(),
  language              text,
  company_name          text,
  sector                text,
  company_size          text,
  respondent_name       text,
  respondent_role       text,
  answers               jsonb,          -- { "question_uuid": "a"|"b"|"c"|"d" }
  score_governance      float,
  score_environmental   float,
  score_social          float,
  score_reporting       float,
  score_economic        float,
  overall_score         float,
  maturity_stage        int,            -- 1 to 5
  recommended_courses   jsonb,          -- ordered array of course names
  pdf_generated         boolean default false
);
```

### Table: `course_rules` *(optional for v1, required for v2)*

```sql
create table course_rules (
  id           uuid primary key default gen_random_uuid(),
  stage        int not null,            -- 1 to 5
  axis         text,                    -- null means applies to all axes
  course_name  text not null,
  priority     int not null,            -- lower = shown first
  is_active    boolean default true
);
```

---

## 🧠 Scoring & Recommendation Engine

### How scoring works (`engine/scorer.py`)

```python
# Pseudocode — implement exactly this logic
def score_session(answers: dict, questions: list) -> dict:
    axis_scores = defaultdict(list)

    for question in questions:
        selected_option = answers.get(str(question["id"]))  # "a", "b", "c", or "d"
        raw_score = question[f"score_{selected_option}"]    # 1–4
        weighted = raw_score * question["weight"]
        axis_scores[question["axis"]].append(weighted)

    result = {}
    for axis, scores in axis_scores.items():
        result[axis] = round(sum(scores) / len(scores), 2)

    result["overall"] = round(sum(result.values()) / len(result), 2)
    result["stage"] = map_to_stage(result["overall"])
    return result


def map_to_stage(score: float) -> int:
    if score <= 1.8:  return 1   # Sensibilización
    if score <= 2.4:  return 2   # Adopción
    if score <= 3.0:  return 3   # Especialización
    if score <= 3.6:  return 4   # Gobernanza
    return 5                     # Comunicación Estratégica
```

### How recommendations work (`engine/recommender.py`)

```python
# Core logic — do not change stage → course mappings without updating course_rules in Supabase
STAGE_COURSES = {
    1: [
        "Introducción a la Sostenibilidad Organizacional",
        "Marco Normativo de la Sostenibilidad: lo que las empresas deben conocer antes de 2027",
        "Gobernanza", "Ambiental", "Económica", "Social", "Financiera",
        "Diagnóstico: punto de partida para el cumplimiento",
    ],
    2: [
        "Diseño y Adopción de la Política de Sostenibilidad",
        "De la Política al Programa de Sostenibilidad",
        "Doble Materialidad & Asuntos Estratégicos",
        "Gestión de Riesgos (básica)",
        "Introducción a las Certificaciones en Sostenibilidad",
    ],
    3: {
        "environmental": ["Medición de Huella de Carbono y Estrategias de Descarbonización",
                          "Descarbonizacion Corporativa", "Mercados de Carbono"],
        "reporting":     ["Reporte Estratégico de Sostenibilidad", "GHG - Greenhouse Protocol",
                          "GRI", "IFRS", "EU: SFDR, CSRD", "Supersociedades"],
        "default":       ["Strategic Sustainability for BusDev", "Creación de Valor a través de la Sostenibilidad",
                          "Sostenibilidad, Influencia y Acceso a Capital"],
    },
    4: [
        "Gobierno Corporativo Sostenible",
        "Gestión Integral de Riesgos ESG",
        "ESG y Compliance: sostenibilidad, transparencia y cumplimiento empresarial",
        "Transparencia & Ética Empresarial",
        "Madurez, Brechas Estratégicas & Hoja de Ruta",
        "Reputación y Valor Empresarial",
    ],
    5: [
        "Divulgación y Marketing de la Sostenibilidad",
        "RRSS & ESG Estratégico",
        "Data Analytics for Marketing",
        "The Architects - Mastering Future-Proof Value",
        "The Drivers - The Pioneer Path: AI-Augmented Leadership",
    ],
}

def get_recommendations(scores: dict) -> list:
    stage = scores["stage"]
    weakest_axis = min(
        ["governance", "environmental", "social", "reporting", "economic"],
        key=lambda a: scores.get(a, 4)
    )
    courses = STAGE_COURSES.get(stage, [])

    # Stage 3: axis-aware routing
    if stage == 3:
        if weakest_axis in ("environmental",):
            courses = STAGE_COURSES[3]["environmental"] + STAGE_COURSES[3]["default"]
        elif weakest_axis == "reporting":
            courses = STAGE_COURSES[3]["reporting"] + STAGE_COURSES[3]["default"]
        else:
            courses = STAGE_COURSES[3]["default"] + STAGE_COURSES[3]["reporting"]

    # Cross-axis correction: if governance is very weak, prepend Stage 2 governance courses
    if scores.get("governance", 4) < 2.0 and stage > 2:
        courses = ["Asuntos de Gobernanza", "Gestión de Riesgos (básica)"] + courses

    return courses
```

---

## 🌐 Internationalisation (i18n)

All user-facing strings live in `i18n/es.json` and `i18n/en.json`. **Never hardcode UI text in Python files.**

```python
# Usage pattern throughout the app
import json, streamlit as st

def t(key: str) -> str:
    lang = st.session_state.get("lang", "es")
    strings = st.session_state.get("i18n_strings", {})
    return strings.get(key, key)   # falls back to key if missing — easy to spot gaps

# Load once at session start in main.py
with open(f"i18n/{lang}.json") as f:
    st.session_state["i18n_strings"] = json.load(f)
```

Example `i18n/es.json` structure:
```json
{
  "app_title": "Diagnóstico de Sostenibilidad",
  "start_button": "Comenzar diagnóstico",
  "profile_company": "Nombre de la empresa",
  "profile_sector": "Sector",
  "profile_size": "Tamaño de la empresa",
  "profile_name": "Nombre completo",
  "profile_role": "Cargo",
  "question_progress": "Pregunta {current} de {total}",
  "results_title": "Tu Ruta de Aprendizaje en Sostenibilidad",
  "results_stage": "Etapa de Madurez",
  "download_pdf": "Descargar reporte en PDF",
  "stage_1_name": "Sensibilización",
  "stage_2_name": "Adopción",
  "stage_3_name": "Especialización",
  "stage_4_name": "Gobernanza",
  "stage_5_name": "Comunicación Estratégica"
}
```

---

## 📋 Streamlit Session State Contract

Use these keys consistently across all pages. Do not invent new keys without adding them here.

| Key | Type | Set in | Description |
|-----|------|--------|-------------|
| `lang` | `str` | `main.py` | `"es"` or `"en"` |
| `i18n_strings` | `dict` | `main.py` | Loaded translation dict |
| `profile` | `dict` | `1_questionnaire.py` | `{company_name, sector, size, name, role}` |
| `answers` | `dict` | `1_questionnaire.py` | `{question_id: "a"\|"b"\|"c"\|"d"}` |
| `current_question` | `int` | `1_questionnaire.py` | Index of current question (0-based) |
| `questions` | `list` | `1_questionnaire.py` | Fetched from Supabase at session start |
| `scores` | `dict` | `engine/scorer.py` | Axis scores + overall + stage |
| `recommendations` | `list` | `engine/recommender.py` | Ordered list of course names |
| `session_id` | `str` | `db/responses.py` | UUID written to Supabase |
| `pdf_ready` | `bool` | `2_results.py` | Whether PDF bytes are ready to serve |

---

## 📄 PDF Report (`engine/pdf_generator.py`)

Use **ReportLab** (`pip install reportlab`). Generate in-memory and return `BytesIO`.

```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from io import BytesIO

def generate_pdf(profile: dict, scores: dict, recommendations: list, lang: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    # ... build story elements ...
    doc.build(story)
    buffer.seek(0)
    return buffer
```

Serve it in Streamlit:
```python
pdf_bytes = generate_pdf(profile, scores, recommendations, lang)
st.download_button(
    label=t("download_pdf"),
    data=pdf_bytes,
    file_name=f"sustainability_report_{profile['company_name']}.pdf",
    mime="application/pdf"
)
```

PDF sections (in order):
1. Cover — company name, respondent, date, maturity stage badge
2. Profile summary — sector, size, role
3. Scores table — one row per axis, plus overall score and stage name
4. Learning path — numbered list of recommended courses with one-line descriptions
5. Next steps paragraph
6. Footer with branding and generated date

---

## 🔐 Admin Dashboard (`pages/3_admin.py`)

```python
import streamlit as st
from app.db.client import supabase

def check_auth():
    pwd = st.text_input("Admin password", type="password")
    if pwd != st.secrets["ADMIN_PASSWORD"]:
        st.stop()

check_auth()

# Load all responses
data = supabase.table("responses").select("*").order("created_at", desc=True).execute()
df = pd.DataFrame(data.data)
st.dataframe(df)
st.download_button("Export CSV", df.to_csv(index=False), "responses.csv", "text/csv")
```

Admin capabilities to implement:
- Filterable responses table (by date range, sector, maturity stage)
- Aggregated KPIs: total completions, avg score by sector, most recommended courses
- Question editor: toggle `is_active`, update text, reorder (edit Supabase rows directly)
- Re-generate PDF for any past `session_id`

---

## 📦 `requirements.txt`

```
streamlit>=1.35.0
supabase>=2.4.0
plotly>=5.20.0
pandas>=2.0.0
reportlab>=4.2.0
python-dotenv>=1.0.0
```

---

## 🚀 Deployment

### Option A — Streamlit Community Cloud (simplest)

1. Push repo to GitHub (public or private).
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select repo.
3. Set `app/main.py` as the entry point.
4. Add secrets in the Streamlit Cloud dashboard (same keys as `.env`).

### Option B — Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t sustainability-diagnostic .
docker run -p 8501:8501 --env-file .env sustainability-diagnostic
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term-missing
```

Key things to test:
- `test_scorer.py` — edge cases: all A's → stage 1, all D's → stage 5, mixed answers
- `test_recommender.py` — verify weak-axis routing, cross-axis governance correction
- `test_db.py` — mock Supabase client, verify correct table/column writes

---

## 📐 Code Conventions

- **Formatting:** `black` + `isort` (run before every commit)
- **Type hints:** required on all function signatures in `engine/` and `db/`
- **Docstrings:** required on all public functions — one-line summary minimum
- **No hardcoded strings:** all UI text goes through `t()` (see i18n section)
- **No hardcoded credentials:** always use `os.getenv()` or `st.secrets`
- **Streamlit reruns:** use `st.session_state` to persist data across reruns — never rely on global variables

```python
# ✅ Correct
def score_session(answers: dict, questions: list) -> dict:
    """Calculate per-axis and overall ESG maturity scores from raw answers."""
    ...

# ❌ Avoid
def score(a, q):
    ...
```

---

## 🗺️ Implementation Roadmap

### Phase 1 — Foundation *(~3–5 days)*
- [ ] Create Supabase project, run schema SQL, seed 25 questions
- [ ] Set up repo structure as defined above
- [ ] Configure `.env`, `config.py`, `requirements.txt`
- [ ] Implement `db/client.py` (Supabase singleton)
- [ ] Implement `db/questions.py` (fetch active questions)
- [ ] Create `i18n/es.json` and `i18n/en.json` with all UI strings
- [ ] Scaffold `app/main.py` with language toggle and session state init

### Phase 2 — Questionnaire *(~5–7 days)*
- [ ] Company profile form (company name, sector, size, name, role)
- [ ] Multi-step question display — one question per screen with progress bar
- [ ] Answer storage in `st.session_state["answers"]`
- [ ] Back / Next navigation without losing answers
- [ ] Final submit → triggers scoring engine

### Phase 3 — Scoring Engine *(~3–5 days)*
- [ ] Implement `engine/scorer.py` exactly per the pseudocode above
- [ ] Implement `engine/recommender.py` with stage + axis routing
- [ ] Unit tests for both modules covering all 5 stages and edge cases
- [ ] Write completed session to Supabase via `db/responses.py`

### Phase 4 — Results & PDF *(~5–7 days)*
- [ ] Results page: maturity stage badge, score per axis
- [ ] Plotly radar chart (`components/radar_chart.py`)
- [ ] Ordered learning path list with course cards
- [ ] `engine/pdf_generator.py` — ReportLab branded PDF
- [ ] `st.download_button` wired to PDF generator
- [ ] Mark `pdf_generated = true` in Supabase on download

### Phase 5 — Admin Dashboard *(~4–6 days)*
- [ ] Password-protected admin page (`pages/3_admin.py`)
- [ ] Filterable responses table
- [ ] CSV export
- [ ] Aggregated KPI cards (total completions, avg score by sector)
- [ ] Question editor: toggle active, edit text directly in UI

### Phase 6 — QA & Deploy *(~3–5 days)*
- [ ] Full bilingual review (ES + EN) — every screen, every question
- [ ] Mobile responsiveness check
- [ ] End-to-end test: profile → questions → results → PDF download → Supabase record
- [ ] Deploy to Streamlit Community Cloud or Docker
- [ ] Set up custom domain (if applicable)

---

## ❓ Open Items

These must be resolved before or during Phase 1:

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| 1 | Brand colors, logo, and fonts for PDF and Streamlit theme | Client | ⏳ Pending |
| 2 | Final sector list for dropdown | Client | ⏳ Pending |
| 3 | Company size bands (e.g. 1–10, 11–50, 51–200, 200+) | Client | ⏳ Pending |
| 4 | Should course cards link to an external LMS or product page? | Client | ⏳ Pending |
| 5 | Admin user(s): email/password or SSO? | Client | ⏳ Pending |
| 6 | Privacy/consent notice required before questionnaire? | Client | ⏳ Pending |
| 7 | Custom domain (e.g. diagnostico.yourcompany.com)? | Client | ⏳ Pending |
| 8 | Should any ESG axis carry a higher scoring weight? | Client | ⏳ Pending |

---

## 🤖 Notes for Claude Code

- **Always read this file first.** It is the single source of truth for this project.
- **Follow the repo structure exactly.** Do not create files outside the defined structure without updating this file.
- **Use the session state contract.** Do not invent new `st.session_state` keys without adding them to the table above.
- **Run tests after every engine change.** `pytest tests/` must pass before any commit to `main`.
- **Check i18n coverage.** Every new UI string needs a key in both `es.json` and `en.json`.
- **Do not hardcode course names in the UI.** They must come from `recommendations` in session state, which is populated by `engine/recommender.py`.
- **Supabase writes are fire-and-forget in v1.** Wrap all `supabase.table(...).insert(...)` calls in try/except — a DB failure must never crash the user's session.

```python
# Always wrap Supabase writes like this
try:
    supabase.table("responses").insert(payload).execute()
    st.session_state["session_id"] = payload["id"]
except Exception as e:
    st.warning("Could not save your session. Your results are still shown below.")
    # log e but do not re-raise
```
