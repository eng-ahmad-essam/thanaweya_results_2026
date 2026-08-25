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
 st.markdown("""
<style>
.stApp {
    background-color: #F4FBF7;  /* clean white-green, not gradient */
}
h1, h2, h3 {
    color: #063B26 !important;   /* dark green, strong contrast */
}
p, label, .stMarkdown {
    color: #12251C !important;   /* near-black green-gray for body text */
}
.result-card {
    background-color: #FFFFFF;
    border: 2px solid #0B6E4F;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.stButton>button {
    background-color: #0B6E4F;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
}
.stTextInput>div>div>input {
    border: 2px solid #0B6E4F;
    color: #063B26;
    font-weight: 600;
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
    
