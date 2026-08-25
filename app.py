import streamlit as st
import pandas as pd
from pathlib import Path
from textwrap import dedent
from html import escape

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

    st.markdown(
        dedent("""
        <style>

        /* =========================================================
           PAGE
        ========================================================= */

        .stApp {
            background-color: #F4FBF7;
        }

        .main .block-container {
            max-width: 680px;
            padding-top: 45px;
            padding-bottom: 25px;
        }

        /* Hide Streamlit chrome */
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
        .stApp {
            direction: rtl;
        }


        /* =========================================================
           HEADER
        ========================================================= */

        .brand-header {
            text-align: center;
            margin-bottom: 28px;
        }

        .brand-eyebrow {
            color: #0B6E4F;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 7px;
        }

        .brand-title {
            color: #063B26 !important;
            font-size: 34px !important;
            line-height: 1.4 !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }

        .brand-sub {
            color: #71817A;
            font-size: 15px;
            margin-top: 9px;
        }


        /* =========================================================
           SEARCH FORM
           
           IMPORTANT:
           We style Streamlit's native form instead of opening
           an HTML div before the form and closing it afterwards.
           This prevents the broken/empty-card problem.
        ========================================================= */

        div[data-testid="stForm"] {
            background: #FFFFFF;

            border: 1px solid #DDE9E3;

            border-radius: 20px;

            padding: 24px 26px 22px 26px;

            box-shadow:
                0 8px 28px rgba(0, 50, 30, 0.055);

            margin-bottom: 16px;
        }

        .lookup-label {
            color: #17372A;

            font-size: 15px;

            font-weight: 700;

            margin-bottom: 8px;

            text-align: right;
        }


        /* =========================================================
           INPUT
        ========================================================= */

        .stTextInput {
            margin-bottom: 12px;
        }

        .stTextInput label {
            display: none !important;
        }

        .stTextInput input {
            height: 52px !important;

            box-sizing: border-box !important;

            border: 1.5px solid #C8D9D1 !important;

            border-radius: 12px !important;

            background: #FCFDFC !important;

            color: #063B26 !important;

            font-size: 18px !important;

            font-weight: 700 !important;

            text-align: center !important;

            direction: ltr !important;

            transition:
                border-color 0.2s ease,
                box-shadow 0.2s ease;
        }

        .stTextInput input:focus {
            border-color: #0B6E4F !important;

            box-shadow:
                0 0 0 3px rgba(11, 110, 79, 0.09) !important;
        }

        .stTextInput input::placeholder {
            color: #A2B0AA !important;
            font-weight: 500 !important;
        }


        /* =========================================================
           BUTTON
        ========================================================= */

        div[data-testid="stFormSubmitButton"] button,
        .stFormSubmitButton button {

            width: 100% !important;

            height: 50px !important;

            border: none !important;

            border-radius: 12px !important;

            background-color: #0B6E4F !important;

            color: #FFFFFF !important;

            font-size: 16px !important;

            font-weight: 700 !important;

            transition:
                background-color 0.2s ease,
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        div[data-testid="stFormSubmitButton"] button:hover,
        .stFormSubmitButton button:hover {

            background-color: #095E44 !important;

            transform: translateY(-1px);

            box-shadow:
                0 5px 15px rgba(11, 110, 79, 0.16);
        }


        /* =========================================================
           DATABASE NOTE
        ========================================================= */

        .disclaimer {
            text-align: center;

            color: #7B8983;

            font-size: 13px;

            line-height: 1.7;

            margin: 12px 0 20px 0;
        }

        .database-count {
            color: #0B6E4F;
            font-weight: 700;
        }


        /* =========================================================
           RESULT WRAPPER
        ========================================================= */

        .result-wrap {
            width: 100%;

            display: flex;

            justify-content: center;

            margin-top: 24px;

            margin-bottom: 20px;
        }


        /* =========================================================
           RESULT CARD
        ========================================================= */

        .result-card {

            width: 100%;

            box-sizing: border-box;

            background: #FFFFFF;

            border: 1px solid #DCE8E2;

            border-radius: 22px;

            padding: 27px 30px 30px 30px;

            text-align: center;

            box-shadow:
                0 10px 32px rgba(0, 50, 30, 0.065);

            position: relative;

            overflow: hidden;
        }

        /* Small accent instead of a black bar */
        .result-card::before {

            content: "";

            position: absolute;

            top: 0;
            left: 50%;

            transform: translateX(-50%);

            width: 60px;

            height: 4px;

            background: #0B6E4F;

            border-radius: 0 0 8px 8px;
        }


        /* =========================================================
           SEAT NUMBER
        ========================================================= */

        .seat-no {

            display: inline-block;

            margin-top: 2px;

            margin-bottom: 17px;

            padding: 6px 14px;

            background: #F1F7F4;

            border: 1px solid #DCE9E3;

            border-radius: 50px;

            color: #61776D;

            font-size: 13px;

            font-weight: 600;
        }

        .seat-number-value {
            color: #31594B;
            font-weight: 700;
        }


        /* =========================================================
           STATUS
        ========================================================= */

        .result-status {

            display: inline-flex;

            align-items: center;

            justify-content: center;

            padding: 7px 15px;

            border-radius: 50px;

            font-size: 14px;

            font-weight: 700;

            margin-bottom: 15px;
        }

        .status-pass {
            background: #E8F7EF;
            color: #087F5B;
        }

        .status-second {
            background: #FFF5DB;
            color: #946C00;
        }

        .status-fail {
            background: #FDECEC;
            color: #A33A3A;
        }


        /* =========================================================
           STUDENT NAME
        ========================================================= */

        .student-name {

            color: #063B26;

            font-size: 27px;

            line-height: 1.5;

            font-weight: 800;

            margin: 2px 0 21px 0;
        }


        /* =========================================================
           DEGREE
        ========================================================= */

        .degree-row {

            display: flex;

            align-items: baseline;

            justify-content: center;

            direction: ltr;

            gap: 5px;

            margin-bottom: 17px;
        }

        .degree-num {

            color: #063B26;

            font-size: 52px;

            line-height: 1;

            font-weight: 800;
        }

        .degree-den {

            color: #7D8D86;

            font-size: 18px;

            font-weight: 600;
        }

        .degree-pct {

            color: #0B6E4F;

            font-size: 15px;

            font-weight: 700;

            margin-left: 7px;
        }


        /* =========================================================
           PROGRESS BAR
        ========================================================= */

        .progress-track {

            width: 100%;

            height: 8px;

            background: #E9F1ED;

            border-radius: 20px;

            overflow: hidden;
        }

        .progress-fill {

            height: 100%;

            border-radius: 20px;
        }


        /* =========================================================
           MOBILE
        ========================================================= */

        @media (max-width: 600px) {

            .main .block-container {
                max-width: 100%;

                padding-left: 16px;
                padding-right: 16px;

                padding-top: 30px;
            }

            .brand-title {
                font-size: 27px !important;
            }

            .brand-sub {
                font-size: 14px;
            }

            div[data-testid="stForm"] {
                padding: 21px 18px 19px 18px;
                border-radius: 18px;
            }

            .result-card {
                padding: 25px 19px 27px 19px;
                border-radius: 20px;
            }

            .student-name {
                font-size: 23px;
            }

            .degree-num {
                font-size: 46px;
            }

            .degree-den {
                font-size: 16px;
            }
        }

        </style>
        """),
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------

@st.cache_data(show_spinner="جاري تحميل قاعدة بيانات النتيجة...")
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
        "badge": "status-pass",
        "bar": "#0B6E4F",
        "icon": "✓",
    },

    "second": {
        "badge": "status-second",
        "bar": "#B08A2E",
        "icon": "⏳",
    },

    "fail": {
        "badge": "status-fail",
        "bar": "#A33A3A",
        "icon": "!",
    },
}


# ----------------------------------------------------------------------------
# App
# ----------------------------------------------------------------------------

def main():

    inject_css()

    # ============================================================
    # HEADER
    # ============================================================

    st.markdown(
        dedent("""
        <div class="brand-header">

            <div class="brand-eyebrow">
                بوابة الاستعلام الإلكتروني
            </div>

            <h1 class="brand-title">
                نتيجة الثانوية العامة
                <br>
                ٢٠٢٦ — الدور الأول
            </h1>

            <div class="brand-sub">
                أدخل رقم الجلوس لعرض نتيجتك
            </div>

        </div>
        """),
        unsafe_allow_html=True,
    )

    # ============================================================
    # LOAD DATA
    # ============================================================

    try:

        df = load_data()

    except FileNotFoundError:

        st.error(
            "تعذر تحميل قاعدة بيانات النتيجة. "
            "تأكد من وجود ملف results.parquet"
        )

        return

    # ============================================================
    # SEARCH
    # ============================================================

    with st.form(
        key="lookup_form",
        clear_on_submit=False,
    ):

        st.markdown(
            '<div class="lookup-label">رقم الجلوس</div>',
            unsafe_allow_html=True,
        )

        seat_input = st.text_input(
            "رقم الجلوس",
            placeholder="2001970",
            max_chars=7,
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "استعلام عن النتيجة"
        )

    # ============================================================
    # BEFORE SEARCH
    # ============================================================

    if not submitted:

        st.markdown(
            dedent(
                f"""
                <div class="disclaimer">
                    قاعدة البيانات تضم نتائج
                    <span class="database-count">
                        {len(df):,}
                    </span>
                    طالبًا وطالبة
                </div>
                """
            ),
            unsafe_allow_html=True,
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
    # FIND RESULT
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

    name = escape(
        str(row["arabic_name"]).strip()
    )

    degree = row["total_degree"]

    status = escape(
        str(row["student_case_desc"]).strip()
    )

    cls = status_class(
        str(row["student_case_desc"]).strip()
    )

    meta = STATUS_META[cls]

    # ============================================================
    # SCORE
    # ============================================================

    if pd.notna(degree):

        degree_value = int(degree)

        pct = (
            degree_value / MAX_DEGREE
        ) * 100

    else:

        degree_value = None

        pct = 0

    # Prevent progress bar from going beyond 100%
    progress_pct = min(
        max(pct, 0),
        100
    )

    # ============================================================
    # RESULT CARD
    # ============================================================

    result_html = dedent(
        f"""
        <div class="result-wrap">

            <div class="result-card">

                <div class="seat-no">
                    رقم الجلوس:
                    <span class="seat-number-value">
                        {seat_no}
                    </span>
                </div>

                <div class="result-status {meta['badge']}">
                    {meta['icon']}
                    &nbsp;
                    {status}
                </div>

                <div class="student-name">
                    {name}
                </div>

                <div class="degree-row">

                    <span class="degree-pct">
                        {pct:.1f}%
                    </span>

                    <span class="degree-num">
                        {degree_value if degree_value is not None else "—"}
                    </span>

                    <span class="degree-den">
                        / {MAX_DEGREE}
                    </span>

                </div>

                <div class="progress-track">

                    <div
                        class="progress-fill"
                        style="
                            width: {progress_pct:.1f}%;
                            background: {meta['bar']};
                        "
                    ></div>

                </div>

            </div>

        </div>
        """
    )

    st.markdown(
        result_html,
        unsafe_allow_html=True,
    )

    # ============================================================
    # OFFICIAL DISCLAIMER
    # ============================================================

    st.markdown(
        dedent("""
        <div class="disclaimer">
            هذه الخدمة للاستعلام الإلكتروني فقط
            ولا تُغني عن الشهادة الرسمية الصادرة
            من وزارة التربية والتعليم.
        </div>
        """),
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Run
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

    st.markdown(
        dedent("""
        <div style="
            text-align:center;
            margin-top:35px;
            padding:10px;
            color:#7A8983;
            font-size:12px;
            direction:ltr;
        ">
            Made By:
            <strong style="color:#0B6E4F;">
                Ahmed Essam
            </strong>
        </div>
        """),
        unsafe_allow_html=True,
    )
