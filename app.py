import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="نتيجة الثانوية العامة 2026",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_PATH = Path(__file__).parent  / "results.parquet"
MAX_DEGREE = 320


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Tajawal:wght@400;500;700&display=swap');

        html, body, [class*="css"]  {
            direction: rtl;
            font-family: 'Cairo', 'Tajawal', sans-serif;
        }

        #MainMenu, footer, header {visibility: hidden;}

        .stApp {
            background:
                radial-gradient(1200px 600px at 15% -10%, rgba(11,61,45,0.10), transparent 55%),
                radial-gradient(1000px 500px at 100% 10%, rgba(198,155,73,0.10), transparent 50%),
                #f7f5ef;
        }

        .block-container {
            padding-top: 2.2rem;
            max-width: 760px;
        }

        .brand-header {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            margin-bottom: 1.6rem;
        }
        .brand-eyebrow {
            letter-spacing: .12em;
            font-size: 0.78rem;
            font-weight: 700;
            color: #b08a2e;
            text-transform: uppercase;
            margin-bottom: .35rem;
        }
        .brand-title {
            font-size: 2.05rem;
            font-weight: 800;
            color: #0b3d2d;
            margin: 0;
            line-height: 1.25;
        }
        .brand-sub {
            font-size: 0.98rem;
            color: #55605a;
            margin-top: .5rem;
        }

        .lookup-card {
            background: #ffffff;
            border: 1px solid #e7e2d4;
            border-radius: 18px;
            padding: 1.6rem 1.7rem 1.3rem 1.7rem;
            box-shadow: 0 10px 30px rgba(11,61,45,0.06);
        }

        div[data-testid="stTextInput"] input {
            direction: ltr;
            text-align: center;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: .04em;
            border-radius: 12px;
            border: 1.5px solid #d8d2bf;
            padding: 0.65rem 0.9rem;
            color: #0b3d2d;
        }
        div[data-testid="stTextInput"] input:focus {
            border-color: #0b3d2d;
            box-shadow: 0 0 0 3px rgba(11,61,45,0.12);
        }
        div[data-testid="stTextInput"] label {
            font-weight: 700;
            color: #2b332f;
            font-size: 0.95rem;
        }

        div.stButton > button {
            width: 100%;
            background: #0b3d2d;
            color: #f7f5ef;
            border: none;
            border-radius: 12px;
            padding: 0.65rem 0;
            font-weight: 700;
            font-size: 1.05rem;
            transition: transform .05s ease, background .15s ease;
        }
        div.stButton > button:hover {
            background: #124d38;
        }
        div.stButton > button:active {
            transform: scale(0.99);
        }

        .result-wrap {
            margin-top: 1.4rem;
            animation: rise .35s ease;
        }
        @keyframes rise {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .result-card {
            border-radius: 18px;
            padding: 1.5rem 1.6rem;
            border: 1px solid;
        }
        .result-pass {
            background: linear-gradient(180deg, #eef7ef 0%, #ffffff 65%);
            border-color: #bfe2c4;
        }
        .result-fail {
            background: linear-gradient(180deg, #fbecec 0%, #ffffff 65%);
            border-color: #f0c4c4;
        }
        .result-second {
            background: linear-gradient(180deg, #fdf3e3 0%, #ffffff 65%);
            border-color: #f1d9a8;
        }

        .result-status {
            display: inline-flex;
            align-items: center;
            gap: .4rem;
            font-weight: 800;
            font-size: 1.1rem;
            padding: .3rem .8rem;
            border-radius: 999px;
            margin-bottom: .9rem;
        }
        .status-pass { background: #0b3d2d; color: #eaf4ec; }
        .status-fail { background: #7a1f1f; color: #fbeaea; }
        .status-second { background: #8a5a12; color: #fdf1de; }

        .seat-no {
            color: #6d766f;
            font-size: 0.85rem;
            direction: ltr;
            text-align: right;
            display: block;
            margin-bottom: .15rem;
        }
        .student-name {
            font-size: 1.55rem;
            font-weight: 800;
            color: #1c2420;
            margin: 0 0 1.1rem 0;
        }

        .degree-row {
            display: flex;
            align-items: baseline;
            gap: .5rem;
            margin-bottom: .3rem;
        }
        .degree-num {
            font-size: 2.4rem;
            font-weight: 800;
            color: #0b3d2d;
            direction: ltr;
        }
        .degree-den {
            font-size: 1.1rem;
            color: #6d766f;
            direction: ltr;
        }
        .degree-pct {
            margin-inline-start: auto;
            font-size: 1rem;
            font-weight: 700;
            color: #55605a;
            direction: ltr;
        }

        .progress-track {
            width: 100%;
            height: 10px;
            background: #eceae0;
            border-radius: 999px;
            overflow: hidden;
            margin-top: .5rem;
        }
        .progress-fill {
            height: 100%;
            border-radius: 999px;
        }

        .disclaimer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.8rem;
            color: #8a8f89;
            line-height: 1.7;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_resource(show_spinner="جاري تحميل قاعدة بيانات النتيجة...")
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(DATA_PATH)
    df = df.set_index("seating_no", drop=False)
    return df


def status_class(status: str) -> str:
    if "ناجح" in status:
        return "pass"
    if "دور ثان" in status:
        return "second"
    return "fail"  # راسب / غياب


STATUS_META = {
    "pass": {"card": "result-pass", "badge": "status-pass", "bar": "#0b3d2d", "icon": "✅"},
    "second": {"card": "result-second", "badge": "status-second", "bar": "#b08a2e", "icon": "⏳"},
    "fail": {"card": "result-fail", "badge": "status-fail", "bar": "#7a1f1f", "icon": "❌"},
}


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------
def main():
    inject_css()

    st.markdown(
        """
        <div class="brand-header">
            <div class="brand-eyebrow">بوابة الاستعلام الإلكتروني</div>
            <h1 class="brand-title">نتيجة الثانوية العامة<br>٢٠٢٦ — الدور الأول</h1>
            <div class="brand-sub">أدخل رقم الجلوس لعرض نتيجتك فوراً</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df = load_data()
    except FileNotFoundError:
        st.error("تعذر تحميل قاعدة بيانات النتيجة. تأكد من وجود ملف data/results.parquet")
        return

    st.markdown('<div class="lookup-card">', unsafe_allow_html=True)

    with st.form(key="lookup_form", clear_on_submit=False):
        seat_input = st.text_input(
            "رقم الجلوس",
            placeholder="مثال: 2001970",
            max_chars=10,
        )
        submitted = st.form_submit_button("استعلام عن النتيجة")

    st.markdown("</div>", unsafe_allow_html=True)

    if not submitted:
        st.markdown(
            f'<div class="disclaimer">قاعدة البيانات تضم نتائج {len(df):,} طالبًا وطالبة'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    seat_clean = seat_input.strip()

    if not seat_clean:
        st.warning("من فضلك أدخل رقم الجلوس أولاً.")
        return

    if not seat_clean.isdigit():
        st.error("رقم الجلوس يجب أن يتكوّن من أرقام فقط.")
        return

    seat_no = int(seat_clean)

    if seat_no not in df.index:
        st.error("لم يتم العثور على نتيجة بهذا الرقم. برجاء التأكد من رقم الجلوس والمحاولة مرة أخرى.")
        return

    row = df.loc[seat_no]
    name = row["arabic_name"]
    degree = row["total_degree"]
    status = str(row["student_case_desc"]).strip()

    cls = status_class(status)
    meta = STATUS_META[cls]
    pct = (degree / MAX_DEGREE * 100) if pd.notna(degree) else 0

    st.markdown(
        f"""
        <div class="result-wrap">
            <div class="result-card {meta['card']}">
                <span class="seat-no">رقم الجلوس: {seat_no}</span>
                <div class="result-status {meta['badge']}">{meta['icon']} {status}</div>
                <div class="student-name">{name}</div>
                <div class="degree-row">
                    <span class="degree-num">{int(degree) if pd.notna(degree) else '—'}</span>
                    <span class="degree-den">/ {MAX_DEGREE}</span>
                    <span class="degree-pct">{pct:.1f}%</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width:{pct:.1f}%; background:{meta['bar']};"></div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="disclaimer">هذه الخدمة للاستعلام الإلكتروني فقط ولا تُغني عن الشهادة الرسمية الصادرة من وزارة التربية والتعليم.</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
