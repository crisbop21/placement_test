# 🌿 Sustainability Diagnostic Tool

A bilingual **(Spanish / English)** self-service web application that helps organizations assess their ESG maturity and receive a personalized sustainability learning path — built with **Streamlit · Python · Supabase**.

---

## ✨ What it does

1. **Company profile** — the client enters their name, company, sector, and role
2. **25-question diagnostic** — covers Governance, Environmental, Social, Reporting, and Economic axes
3. **Maturity score** — each axis is scored 1–4 and mapped to one of 5 maturity stages
4. **Learning path** — an ordered sequence of courses from a catalogue of 48 sustainability programs
5. **PDF report** — a branded, downloadable report with scores and recommended courses
6. **Admin dashboard** — back-office view of all submissions with CSV export and question editor

---

## 🗺️ Maturity Stages

| Stage | Name | Score Range | Focus |
|-------|------|-------------|-------|
| 1 | Sensibilización | 1.0 – 1.8 | Awareness & foundational knowledge |
| 2 | Adopción | 1.9 – 2.4 | Policy design & institutional alignment |
| 3 | Especialización | 2.5 – 3.0 | Operational implementation by ESG axis |
| 4 | Gobernanza | 3.1 – 3.6 | Accountability, risk & corporate governance |
| 5 | Comunicación Estratégica | 3.7 – 4.0 | Strategic communication & market positioning |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | [Streamlit](https://streamlit.io) |
| Backend | Python 3.11+ |
| Database | [Supabase](https://supabase.com) (PostgreSQL) |
| Charts | Plotly |
| PDF | ReportLab |
| i18n | JSON-based (ES / EN) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A [Supabase](https://supabase.com) project (free tier works)
- Git

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_ORG/sustainability-diagnostic.git
cd sustainability-diagnostic
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
ADMIN_PASSWORD=choose-a-secure-password
APP_LANG_DEFAULT=es
```

### 4. Set up the database

Run the contents of `data/seed_questions.sql` in your Supabase project's **SQL Editor**. This creates the schema and seeds the initial 25 questions.

### 5. Run locally

```bash
streamlit run app/main.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
sustainability-diagnostic/
├── CLAUDE.md                  ← Claude Code implementation guide
├── README.md                  ← This file
├── .env.example               ← Environment variable template
├── requirements.txt
├── config.py                  ← Colors, branding, stage thresholds
├── i18n/
│   ├── es.json                ← Spanish UI strings
│   └── en.json                ← English UI strings
├── app/
│   ├── main.py                ← Streamlit entry point
│   ├── pages/
│   │   ├── 1_questionnaire.py
│   │   ├── 2_results.py
│   │   └── 3_admin.py
│   ├── components/
│   │   ├── language_toggle.py
│   │   ├── progress_bar.py
│   │   ├── radar_chart.py
│   │   └── course_card.py
│   ├── engine/
│   │   ├── scorer.py
│   │   ├── recommender.py
│   │   └── pdf_generator.py
│   └── db/
│       ├── client.py
│       ├── questions.py
│       └── responses.py
├── data/
│   └── seed_questions.sql
├── tests/
│   ├── test_scorer.py
│   ├── test_recommender.py
│   └── test_db.py
└── docs/
    └── technical_brief.docx
```

---

## 🌐 Deployment

### Streamlit Community Cloud *(recommended for v1)*

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select this repo and set the entry point to `app/main.py`
4. Add your secrets in the Streamlit Cloud dashboard under **Settings → Secrets**

### Docker

```bash
docker build -t sustainability-diagnostic .
docker run -p 8501:8501 --env-file .env sustainability-diagnostic
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
# with coverage
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 🔐 Admin Dashboard

Access the admin panel at `/3_admin` (Streamlit page routing). You will be prompted for the `ADMIN_PASSWORD` set in your environment.

**Admin capabilities:**
- View and filter all diagnostic submissions
- Export data as CSV
- Edit, activate, or deactivate questions without code changes
- View aggregate stats by sector and maturity stage

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Follow the conventions in `CLAUDE.md`
3. Run `black .` and `isort .` before committing
4. Run `pytest tests/` — all tests must pass
5. Open a pull request against `main`

---

## 📄 License

Private / proprietary. All rights reserved.

---

## 📬 Contact

For questions about this project, reach out to the project maintainer or open an issue in this repository.
