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
    st.markdown(
        """
        <style>

        /* =========================
           Global
        ========================= */

        .stApp {
            background: #F6FAF8;
        }

        .main .block-container {
            max-width: 720px;
            padding-top: 45px;
            padding-bottom: 30px;
        }

        /* Hide Streamlit branding */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            visibility: hidden;
        }


        /* =========================
           Header
        ========================= */

        .brand-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .brand-icon {
            width: 62px;
            height: 62px;
            margin: 0 auto 18px auto;
            border-radius: 18px;

            display: flex;
            align-items: center;
            justify-content: center;

            background: #E4F3EC;
            color: #087F5B;

            font-size: 30px;

            box-shadow: 0 5px 20px rgba(8, 127, 91, 0.08);
        }

        .brand-eyebrow {
            color: #087F5B;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 8px;
        }

        .brand-title {
            color: #063B26 !important;
            font-size: 34px !important;
            line-height: 1.35 !important;
            font-weight: 800 !important;
            margin: 0 !important;
        }

        .brand-sub {
            color: #64746D;
            font-size: 16px;
            margin-top: 12px;
        }


        /* =========================
           Search Card
        ========================= */

        .lookup-card {
            background: white;
            border: 1px solid #E0EAE5;
            border-radius: 22px;

            padding: 26px 28px 18px 28px;

            box-shadow:
                0 10px 35px rgba(0, 50, 30, 0.06);

            margin-bottom: 18px;
        }

        .stTextInput label {
            color: #17372A !important;
            font-weight: 700 !important;
            font-size: 15px !important;
        }

        .stTextInput input {
            height: 52px !important;

            border-radius: 13px !important;
            border: 1.5px solid #C9DAD2 !important;

            background: #FBFDFC !important;

            color: #063B26 !important;

            font-size: 17px !important;
            font-weight: 600 !important;

            text-align: center;
        }

        .stTextInput input:focus {
            border-color: #0B6E4F !important;
            box-shadow: 0 0 0 3px rgba(11, 110, 79, 0.10) !important;
        }

        .stTextInput input::placeholder {
            color: #A5B3AD !important;
        }


        /* =========================
           Search Button
        ========================= */

        .stFormSubmitButton button {
            width: 100%;

            height: 52px;

            border-radius: 13px;

            background: #0B6E4F !important;
            color: white !important;

            border: none !important;

            font-size: 16px !important;
            font-weight: 700 !important;

            transition: 0.2s ease;
        }

        .stFormSubmitButton button:hover {
            background: #095C42 !important;
            transform: translateY(-1px);
        }


        /* =========================
           Result Container
        ========================= */

        .result-wrap {
            display: flex;
            justify-content: center;

            margin-top: 28px;
            margin-bottom: 25px;
        }

        .result-card {
            width: 100%;

            background: white;

            border-radius: 26px;

            padding: 30px 32px 32px 32px;

            text-align: center;

            border: 1px solid #DDE9E3;

            box-shadow:
                0 15px 45px rgba(0, 50, 30, 0.08);

            position: relative;
            overflow: hidden;
        }

        /* Small green top line instead of black seat bar */
        .result-card::before {
            content: "";
            position: absolute;

            top: 0;
            left: 50%;

            transform: translateX(-50%);

            width: 70px;
            height: 4px;

            background: #0B6E4F;

            border-radius: 0 0 10px 10px;
        }


        /* =========================
           Seat Number
        ========================= */

        .seat-no {
            display: inline-block;

            margin-top: 5px;
            margin-bottom: 20px;

            padding: 7px 15px;

            background: #F1F7F4;

            border: 1px solid #DCEBE4;

            border-radius: 30px;

            color: #477064;

            font-size: 13px;
            font-weight: 600;
        }


        /* =========================
           Status
        ========================= */

        .result-status {
            display: inline-flex;

            align-items: center;
            justify-content: center;

            padding: 7px 16px;

            border-radius: 30px;

            font-size: 14px;
            font-weight: 700;

            margin-bottom: 18px;
        }

        .status-pass {
            background: #E8F7EF;
            color: #087F5B;
        }

        .status-second {
            background: #FFF6DD;
            color: #946C00;
        }

        .status-fail {
            background: #FDECEC;
            color: #A33A3A;
        }


        /* =========================
           Student Name
        ========================= */

        .student-name {
            color: #063B26;

            font-size: 27px;

            font-weight: 800;

            margin: 4px 0 22px 0;

            line-height: 1.5;
        }


        /* =========================
           Score
        ========================= */

        .degree-row {
            display: flex;

            align-items: baseline;
            justify-content: center;

            gap: 6px;

            margin-bottom: 18px;
        }

        .degree-num {
            color: #063B26;

            font-size: 52px;

            font-weight: 800;

            line-height: 1;
        }

        .degree-den {
            color: #7C8D86;

            font-size: 19px;

            font-weight: 600;
        }

        .degree-pct {
            color: #0B6E4F;

            font-size: 16px;

            font-weight: 700;

            margin-right: 8px;
        }


        /* =========================
           Progress
        ========================= */

        .progress-track {
            width: 100%;

            height: 9px;

            background: #EAF1ED;

            border-radius: 20px;

            overflow: hidden;

            margin-top: 5px;
        }

        .progress-fill {
            height: 100%;

            border-radius: 20px;

            transition: width 0.5s ease;
        }


        /* =========================
           Disclaimer
        ========================= */

        .disclaimer {
            text-align: center;

            color: #7A8983;

            font-size: 13px;

            line-height: 1.7;

            margin-top: 15px;
        }


        /* =========================
           Mobile
        ========================= */

        @media (max-width: 600px) {

            .main .block-container {
                padding-left: 18px;
                padding-right: 18px;
                padding-top: 30px;
            }

            .brand-title {
                font-size: 27px !important;
            }

            .brand-sub {
                font-size: 14px;
            }

            .lookup-card {
                padding: 22px 18px 14px 18px;
                border-radius: 18px;
            }

            .result-card {
                padding: 27px 20px 28px 20px;
                border-radius: 22px;
            }

            .student-name {
                font-size: 23px;
            }

            .degree-num {
                font-size: 45px;
            }
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

    # ------------------------------------------------------------
    # Header
    # ------------------------------------------------------------

    st.markdown(
        """
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
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    # Load database
    # ------------------------------------------------------------

    try:
        df = load_data()

    except FileNotFoundError:

        st.error(
            "تعذر تحميل قاعدة بيانات النتيجة. "
            "تأكد من وجود ملف results.parquet."
        )

        return

    # ------------------------------------------------------------
    # Search card
    # ------------------------------------------------------------

    st.markdown(
        '<div class="lookup-card">',
        unsafe_allow_html=True,
    )

    with st.form(
        key="lookup_form",
        clear_on_submit=False,
    ):

        seat_input = st.text_input(
            "رقم الجلوس",
            placeholder="مثال: 2001970",
            max_chars=7,
            label_visibility="visible",
        )

        submitted = st.form_submit_button(
            "استعلام عن النتيجة"
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    # Initial state
    # ------------------------------------------------------------

    if not submitted:

        st.markdown(
            f"""
            <div class="disclaimer">
                قاعدة البيانات تضم نتائج
                <strong>{len(df):,}</strong>
                طالبًا وطالبة
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    # ------------------------------------------------------------
    # Validate input
    # ------------------------------------------------------------

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

    # ------------------------------------------------------------
    # Find result
    # ------------------------------------------------------------

    if seat_no not in df.index:

        st.error(
            "لم يتم العثور على نتيجة بهذا الرقم. "
            "برجاء التأكد من رقم الجلوس والمحاولة مرة أخرى."
        )

        return

    # ------------------------------------------------------------
    # Get student data
    # ------------------------------------------------------------

    row = df.loc[seat_no]

    name = row["arabic_name"]

    degree = row["total_degree"]

    status = str(
        row["student_case_desc"]
    ).strip()

    cls = status_class(status)

    meta = STATUS_META[cls]

    pct = (
        degree / MAX_DEGREE * 100
        if pd.notna(degree)
        else 0
    )

    # ------------------------------------------------------------
    # Result card
    # ------------------------------------------------------------

    st.markdown(
        f"""
        <div class="result-wrap">

            <div class="result-card">

                <div class="seat-no">
                    رقم الجلوس · {seat_no}
                </div>

                <div class="result-status {meta['badge']}">
                    {meta['icon']}&nbsp;&nbsp;{status}
                </div>

                <div class="student-name">
                    {name}
                </div>

                <div class="degree-row">

                    <span class="degree-num">
                        {int(degree) if pd.notna(degree) else '—'}
                    </span>

                    <span class="degree-den">
                        / {MAX_DEGREE}
                    </span>

                    <span class="degree-pct">
                        {pct:.1f}%
                    </span>

                </div>

                <div class="progress-track">

                    <div
                        class="progress-fill"
                        style="
                            width:{min(pct, 100):.1f}%;
                            background:{meta['bar']};
                        "
                    >
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # ------------------------------------------------------------
    # Disclaimer
    # ------------------------------------------------------------

    st.markdown(
        """
        <div class="disclaimer">
            هذه الخدمة للاستعلام الإلكتروني فقط،
            ولا تُغني عن الشهادة الرسمية
            الصادرة من وزارة التربية والتعليم.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    main()

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:35px;
        padding:12px;
        color:#7A8983;
        font-size:12px;
    ">
        Made by <strong style="color:#0B6E4F;">Ahmed Essam</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
