# نتيجة الثانوية العامة 2026 — بوابة الاستعلام الإلكتروني

A simple Streamlit web app for looking up Egyptian **Thanaweya Amma (الثانوية العامة)** exam results for the **2026 — First Round (الدور الأول)** by seat number.

🔗 **Live demo:** https://thanaweyaresults2026-ahmadessam.streamlit.app

---

## What it does

Students enter their **7-digit seat number (رقم الجلوس)** and instantly get:

- ✅ Their **pass/fail/second-round status** (ناجح / دور ثانٍ / راسب)
- 🧑‍🎓 Full name
- 📊 Total degree out of 320, with percentage and a visual progress bar

The result is displayed in a clean card, color-coded by outcome:
- 🟢 Green — passed
- 🟡 Gold — second round
- 🔴 Red — failed / absent

## Tech stack

- **[Streamlit](https://streamlit.io/)** — web UI framework
- **Pandas** — data loading and lookup
- **Parquet** — result data storage format (fast to load, compact)

## Project structure

```
.
├── app.py               # Main Streamlit application
├── results.parquet      # Student results dataset (seating_no, arabic_name, total_degree, student_case_desc)
├── requirements.txt     # Python dependencies
├── config.toml           # Streamlit configuration
└── README.md
```

## How it works

1. On load, the app reads `results.parquet` into a Pandas DataFrame, indexed by seat number (`seating_no`), and caches it with `@st.cache_resource` so it's only loaded once per session.
2. The user submits a seat number through a form.
3. The app validates the input (must be digits only, must exist in the dataset).
4. If found, it looks up the student's name, total degree, and status, calculates the percentage (`degree / 320`), and renders a styled result card.

## Running locally

```bash
# Clone the repo
git clone https://github.com/eng-ahmad-essam/thanaweya_results_2026.git
cd thanaweya_results_2026

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## Data requirements

`results.parquet` must contain at least these columns:

| Column               | Description                              |
|----------------------|-------------------------------------------|
| `seating_no`          | Student seat number (used as lookup key) |
| `arabic_name`          | Student's full name in Arabic            |
| `total_degree`         | Total score out of 320                   |
| `student_case_desc`    | Result status text (e.g. "ناجح دور أول") |

## Disclaimer

This tool is for **electronic inquiry purposes only** and does not substitute for the official certificate issued by the Ministry of Education (وزارة التربية والتعليم).

---

**Made By: Ahmed Essam**
