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

DATA_PATH = Path(__file__).parent / "results.parquet"
MAX_DEGREE = 320


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------
def inject_css():
    st.markdown("""
<style>
.stApp {
    background-color: #F2FBF6;
}

/* ---------- Header ---------- */
.brand-header {
    text-align: center;
    padding: 8px 0 24px 0;
}
.brand-eyebrow {
    color: #B08A2E;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 6px;
}
.brand-title {
    color: #063B26 !important;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1.3;
    margin: 4px 0 10px 0;
}
.brand-sub {
    color: #1F3D33;
    font-size: 1.05rem;
    font-weight: 500;
}

/* ---------- Lookup form card ---------- */
.lookup-card {
    background: #FFFFFF;
    border: 1px solid #D7EDE1;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 4px 14px rgba(6, 59, 38, 0.06);
    margin-bottom: 18px;
}
.stTextInput>div>div>input {
    border: 2px solid #0B6E4F !important;
    border-radius: 10px !important;
    color: #063B26 !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    text-align: center;
    padding: 10px !important;
}
.stButton>button, .stFormSubmitButton>button {
    background-color: #0B6E4F !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    width: 100%;
    transition: background-color 0.15s ease;
}
.stButton>button:hover, .stFormSubmitButton>button:hover {
    background-color: #094F39 !important;
}

/* ---------- Result card ---------- */
.result-wrap {
    margin-top: 8px;
}
.result-card {
    background: #FFFFFF;
    border-radius: 18px;
    padding: 26px 28px;
    box-shadow: 0 6px 20px rgba(6, 59, 38, 0.10);
    border-top: 6px solid #0B6E4F;
}
.result-card.result-second {
    border-top-color: #B08A2E;
}
.result-card.result-fail {
    border-top-color: #B03A2E;
}

.seat-no {
    display: block;
    text-align: left;
    direction: ltr;
    color: #6B7D74;
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 14px;
}

.result-status {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.95rem;
    margin-bottom: 16px;
}
.status-pass {
    background-color: #DFF3E7;
    color: #0B3D2D;
}
.status-second {
    background-color: #FBEFD4;
    color: #7A5A0C;
}
.status-fail {
    background-color: #FBE0DD;
    color: #7A1F1F;
}

.student-name {
    color: #0F2A20 !important;
    font-size: 1.5rem;
    font-weight: 800;
    margin-bottom: 22px;
    line-height: 1.4;
}

.degree-row {
    display: flex;
    align-items: baseline;
    justify-content: flex-end;
    gap: 8px;
    margin-bottom: 12px;
    direction: ltr;
}
.degree-num {
    color: #0B6E4F;
    font-size: 2.4rem;
    font-weight: 800;
}
.degree-den {
    color: #6B7D74;
    font-size: 1.2rem;
    font-weight: 600;
}
.degree-pct {
    color: #0F2A20;
    font-size: 1.1rem;
    font-weight: 700;
    margin-left: auto;
}

.progress-track {
    width: 100%;
    height: 10px;
    background-color: #E4EFE9;
    border-radius: 999px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease;
}

/* ---------- Disclaimer / footer ---------- */
.disclaimer {
    text-align: center;
    color: #6B7D74;
    font-size: 0.85rem;
    margin-top: 22px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


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
            <div class="brand-sub"> أدخل رقم الجلوس لعرض نتيجتك </div>
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
            placeholder="2001970",
            max_chars=7,
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

st.markdown("""
<div style="text-align:center; margin-top:40px; padding:12px; color:#0B6E4F; font-weight:600;">
    Made By: Ahmed Essam
</div>
""", unsafe_allow_html=True)
