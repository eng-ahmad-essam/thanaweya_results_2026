import streamlit as st
import pandas as pd
from pathlib import Path
from textwrap import dedent

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
# CSS
# ----------------------------------------------------------------------------

def inject_css():

    css = """
    <style>

    /* =========================================================
       PAGE
    ========================================================= */

    .stApp {
        background: #F5F9F7;
    }

    .main .block-container {
        max-width: 680px;
        padding-top: 55px;
        padding-bottom: 30px;
    }

    /* Hide Streamlit default elements */
    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Arabic direction */
    .stApp,
    .stMarkdown,
    .stTextInput,
    .stButton,
    .stForm {
        direction: rtl;
    }


    /* =========================================================
       HEADER
    ========================================================= */

    .brand-header {
        text-align: center;
        margin-bottom: 32px;
        direction: rtl;
    }

    .brand-icon {
        width: 64px;
        height: 64px;

        margin: 0 auto 18px auto;

        display: flex;
        align-items: center;
        justify-content: center;

        background: #E5F3EC;

        border-radius: 18px;

        font-size: 30px;

        box-shadow:
            0 8px 25px rgba(11, 110, 79, 0.08);
    }

    .brand-eyebrow {
        color: #0B6E4F;

        font-size: 14px;
        font-weight: 700;

        margin-bottom: 8px;
    }

    .brand-title {
        color: #063B26 !important;

        font-size: 34px !important;
        line-height: 1.45 !important;

        font-weight: 800 !important;

        margin: 0 !important;
    }

    .brand-sub {
        color: #71817A;

        font-size: 15px;

        margin-top: 10px;
    }


    /* =========================================================
       SEARCH AREA
    ========================================================= */

    .search-card {
        background: #FFFFFF;

        border: 1px solid #DFEAE4;

        border-radius: 22px;

        padding: 25px 26px 24px 26px;

        box-shadow:
            0 12px 35px rgba(0, 50, 30, 0.06);

        margin-bottom: 18px;

        direction: rtl;
    }

    .search-label {
        display: block;

        color: #18382C;

        font-size: 15px;
        font-weight: 700;

        margin-bottom: 9px;

        text-align: right;
    }


    /* =========================================================
       TEXT INPUT
    ========================================================= */

    .stTextInput {
        margin-bottom: 12px;
    }

    .stTextInput label {
        display: none !important;
    }

    .stTextInput > div {
        width: 100%;
    }

    .stTextInput > div > div {
        width: 100%;
    }

    .stTextInput input {

        height: 54px !important;

        width: 100% !important;

        box-sizing: border-box !important;

        border: 1.5px solid #CBDAD3 !important;

        border-radius: 13px !important;

        background: #FCFDFC !important;

        color: #063B26 !important;

        font-size: 18px !important;

        font-weight: 700 !important;

        text-align: center !important;

        direction: ltr !important;

        transition: all 0.2s ease;
    }

    .stTextInput input:focus {

        border-color: #0B6E4F !important;

        box-shadow:
            0 0 0 3px rgba(11, 110, 79, 0.09) !important;
    }

    .stTextInput input::placeholder {
        color: #A5B2AC !important;
        font-weight: 500 !important;
    }


    /* =========================================================
       SEARCH BUTTON
    ========================================================= */

    .stFormSubmitButton {
        width: 100%;
    }

    .stFormSubmitButton button {

        width: 100% !important;

        height: 52px !important;

        border: none !important;

        border-radius: 13px !important;

        background: #0B6E4F !important;

        color: #FFFFFF !important;

        font-size: 16px !important;

        font-weight: 700 !important;

        transition: all 0.2s ease;
    }

    .stFormSubmitButton button:hover {

        background: #095E44 !important;

        transform: translateY(-1px);

        box-shadow:
            0 6px 18px rgba(11, 110, 79, 0.18);
    }


    /* =========================================================
       DATABASE NOTE
    ========================================================= */

    .database-note {

        text-align: center;

        color: #7A8983;

        font-size: 13px;

        line-height: 1.8;

        margin-top: 8px;

        margin-bottom: 20px;

        direction: rtl;
    }

    .database-number {
        color: #0B6E4F;
        font-weight: 700;
    }


    /* =========================================================
       RESULT CARD
    ========================================================= */

    .result-card {

        width: 100%;

        box-sizing: border-box;

        background: #FFFFFF;

        border: 1px solid #DCE8E2;

        border-radius: 24px;

        padding: 28px 30px 30px 30px;

        text-align: center;

        box-shadow:
            0 14px 40px rgba(0, 50, 30, 0.07);

        position: relative;

        overflow: hidden;

        direction: rtl;
    }

    /* Small elegant accent */
    .result-card::before {

        content: "";

        position: absolute;

        top: 0;
        left: 50%;

        transform: translateX(-50%);

        width: 64px;
        height: 4px;

        background: #0B6E4F;

        border-radius: 0 0 8px 8px;
    }


    /* =========================================================
       SEAT NUMBER
    ========================================================= */

    .seat-number {

        display: inline-block;

        margin-top: 3px;
        margin-bottom: 18px;

        padding: 6px 14px;

        background: #F2F7F4;

        border: 1px solid #DCE9E3;

        border-radius: 50px;

        color: #60766D;

        font-size: 13px;

        font-weight: 600;
    }

    .seat-number strong {
        color: #34584A;
    }


    /* =========================================================
       STATUS
    ========================================================= */

    .status {

        display: inline-flex;

        align-items: center;

        justify-content: center;

        padding: 7px 15px;

        border-radius: 50px;

        font-size: 14px;

        font-weight: 700;

        margin-bottom: 16px;
    }

    .status-pass {
        background: #E8F7EF;
        color: #087F5B;
    }

    .status-second {
        background: #FFF6DE;
        color: #966F00;
    }

    .status-fail {
        background: #FDECEC;
        color: #A43D3D;
    }


    /* =========================================================
       NAME
    ========================================================= */

    .student-name {

        color: #063B26;

        font-size: 27px;

        line-height: 1.5;

        font-weight: 800;

        margin-bottom: 22px;
    }


    /* =========================================================
       SCORE
    ========================================================= */

    .score {

        display: flex;

        align-items: baseline;

        justify-content: center;

        direction: ltr;

        gap: 5px;

        margin-bottom: 19px;
    }

    .score-main {

        color: #063B26;

        font-size: 54px;

        line-height: 1;

        font-weight: 800;
    }

    .score-max {

        color: #82918B;

        font-size: 18px;

        font-weight: 600;
    }

    .score-percent {

        color: #0B6E4F;

        font-size: 15px;

        font-weight: 700;

        margin-left: 7px;
    }


    /* =========================================================
       PROGRESS BAR
    ========================================================= */

    .progress-container {

        width: 100%;

        height: 9px;

        background: #EAF1ED;

        border-radius: 20px;

        overflow: hidden;
    }

    .progress {

        height: 100%;

        border-radius: 20px;

        transition: width 0.4s ease;
    }


    /* =========================================================
       OFFICIAL NOTE
    ========================================================= */

    .official-note {

        text-align: center;

        color: #7B8984;

        font-size: 12px;

        line-height: 1.8;

        margin-top: 18px;

        direction: rtl;
    }


    /* =========================================================
       FOOTER
    ========================================================= */

    .site-footer {

        text-align: center;

        margin-top: 38px;

        color: #87938E;

        font-size: 12px;

        direction: ltr;
    }

    .site-footer strong {
        color: #0B6E4F;
    }


    /* =========================================================
       MOBILE
    ========================================================= */

    @media (max-width: 600px) {

        .main .block-container {

            max-width: 100%;

            padding-left: 17px;
            padding-right: 17px;

            padding-top: 35px;
        }

        .brand-title {
            font-size: 27px !important;
        }

        .brand-sub {
            font-size: 14px;
        }

        .brand-icon {
            width: 58px;
            height: 58px;
            font-size: 27px;
        }

        .search-card {
            padding: 21px 18px 20px 18px;
            border-radius: 19px;
        }

        .result-card {
            padding: 26px 19px 27px 19px;
            border-radius: 21px;
        }

        .student-name {
            font-size: 23px;
        }

        .score-main {
            font-size: 46px;
        }

        .score-max {
            font-size: 16px;
        }
    }

    </style>
    """

    st.markdown(dedent(css), unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------

@st.cache_resource(show_spinner="جاري تحميل قاعدة بيانات النتيجة...")
def load_data() -> pd.DataFrame:

    df = pd.read_parquet(DATA_PATH)

    df = df.set_index(
        "seating_no",
        drop=False
    )

    return df


# ----------------------------------------------------------------------------
# Status
# ----------------------------------------------------------------------------

def status_class(status: str) -> str:

    if "ناجح" in status:
        return "pass"

    if "دور ثان" in status:
        return "second"

    return "fail"


STATUS_META = {

    "pass": {
        "class": "status-pass",
        "icon": "✓",
        "color": "#0B6E4F",
    },

    "second": {
        "class": "status-second",
        "icon": "◷",
        "color": "#B08A2E",
    },

    "fail": {
        "class": "status-fail",
        "icon": "!",
        "color": "#A43D3D",
    },
}


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():

    inject_css()

    # ============================================================
    # HEADER
    # ============================================================

    header_html = """
    <div class="brand-header">

        <div class="brand-icon">
            🎓
        </div>

        <div class="brand-eyebrow">
            بوابة الاستعلام الإلكتروني
        </div>

        <h1 class="brand-title">
            نتيجة الثانوية العامة
            <br>
            ٢٠٢٦ — الدور الأول
        </h1>

        <div class="brand-sub">
            أدخل رقم الجلوس لعرض النتيجة
        </div>

    </div>
    """

    st.markdown(
        dedent(header_html),
        unsafe_allow_html=True
    )

    # ============================================================
    # LOAD DATA
    # ============================================================

    try:

        df = load_data()

    except FileNotFoundError:

        st.error(
            "تعذر تحميل قاعدة بيانات النتيجة. "
            "تأكد من وجود ملف results.parquet."
        )

        return

    # ============================================================
    # SEARCH CARD
    #
    # IMPORTANT:
    # The entire HTML wrapper is inside ONE markdown call.
    # ============================================================

st.markdown(
    """
    <div class="search-label">
        رقم الجلوس
    </div>
    """,
    unsafe_allow_html=True
)

with st.form(
    key="lookup_form",
    clear_on_submit=False
):

    seat_input = st.text_input(
        "رقم الجلوس",
        placeholder="مثال: 2405822",
        max_chars=7,
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "استعلام عن النتيجة"
    )

    # ============================================================
    # INITIAL MESSAGE
    # ============================================================

    if not submitted:

        st.markdown(
            dedent(
                f"""
                <div class="database-note">
                    قاعدة البيانات تضم نتائج
                    <span class="database-number">
                        {len(df):,}
                    </span>
                    طالبًا وطالبة
                </div>
                """
            ),
            unsafe_allow_html=True
        )

        return

    # ============================================================
    # VALIDATION
    # ============================================================

    seat_clean = seat_input.strip()

    if not seat_clean:

        st.warning(
            "من فضلك أدخل رقم الجلوس أولاً."
        )

        return

    if not seat_clean.isdigit():

        st.error(
            "رقم الجلوس يجب أن يتكوّن من أرقام فقط."
        )

        return

    seat_no = int(seat_clean)

    # ============================================================
    # SEARCH
    # ============================================================

    if seat_no not in df.index:

        st.error(
            "لم يتم العثور على نتيجة بهذا الرقم. "
            "برجاء التأكد من رقم الجلوس والمحاولة مرة أخرى."
        )

        return

    # ============================================================
    # STUDENT DATA
    # ============================================================

    row = df.loc[seat_no]

    name = str(
        row["arabic_name"]
    ).strip()

    degree = row["total_degree"]

    status = str(
        row["student_case_desc"]
    ).strip()

    cls = status_class(status)

    meta = STATUS_META[cls]

    if pd.notna(degree):

        degree_int = int(degree)

        percentage = (
            degree_int / MAX_DEGREE
        ) * 100

    else:

        degree_int = None
        percentage = 0

    progress_width = min(
        max(percentage, 0),
        100
    )

    # ============================================================
    # RESULT
    # ============================================================

    result_html = f"""
    <div class="result-card">

        <div class="seat-number">
            رقم الجلوس
            <strong>{seat_no}</strong>
        </div>

        <div class="status {meta['class']}">
            {meta['icon']}
            &nbsp;
            {status}
        </div>

        <div class="student-name">
            {name}
        </div>

        <div class="score">

            <span class="score-percent">
                {percentage:.1f}%
            </span>

            <span class="score-main">
                {degree_int if degree_int is not None else "—"}
            </span>

            <span class="score-max">
                / {MAX_DEGREE}
            </span>

        </div>

        <div class="progress-container">

            <div
                class="progress"
                style="
                    width: {progress_width:.1f}%;
                    background: {meta['color']};
                "
            ></div>

        </div>

    </div>
    """

    st.markdown(
        dedent(result_html),
        unsafe_allow_html=True
    )

    # ============================================================
    # OFFICIAL DISCLAIMER
    # ============================================================

    st.markdown(
        dedent(
            """
            <div class="official-note">
                هذه الخدمة للاستعلام الإلكتروني فقط،
                ولا تُغني عن الشهادة الرسمية
                الصادرة من وزارة التربية والتعليم.
            </div>
            """
        ),
        unsafe_allow_html=True
    )


# ----------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    st.markdown(
        dedent(
            """
            <div class="site-footer">
                Made by <strong>Ahmed Essam</strong>
            </div>
            """
        ),
        unsafe_allow_html=True
    )
