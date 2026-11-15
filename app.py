
import streamlit as st
import pandas as pd
import csv
import io

from validator import REQUIRED_FIELDS, process_records

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CleanSlate | Data Quality",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0B1120;
    color: #E8EEF6;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #101A2B;
    border-right: 1px solid #26364B;
}

.hero {
    background: linear-gradient(120deg, #142B40, #123C3A);
    border: 1px solid #28534E;
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 28px;
}

.hero h1 {
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    margin: 0;
}

.hero p {
    color: #B8D0CE;
    font-size: 15px;
}

.eyebrow {
    color: #65D6A5;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.metric-card {
    background: linear-gradient(145deg, #172438, #111C2D);
    border: 1px solid #293A50;
    border-radius: 15px;
    padding: 19px;
    min-height: 125px;
}

.metric-label {
    color: #9EADC2;
    font-size: 12px;
    font-weight: 600;
}

.metric-value {
    color: #F4F7FB;
    font-size: 30px;
    font-weight: 800;
    margin-top: 9px;
}

.metric-note {
    color: #8293A9;
    font-size: 11px;
    margin-top: 5px;
}

.green { color: #65D6A5; }
.red { color: #FF8791; }
.orange { color: #FFC36A; }

.section-title {
    color: #F0F4F8;
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 5px;
}

div.stButton > button {
    background: #168B68;
    color: white;
    border: 1px solid #168B68;
    border-radius: 10px;
    min-height: 44px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #20A47D;
    border-color: #20A47D;
    color: white;
}

div.stDownloadButton > button {
    background: #172B40;
    color: #E5EEF8;
    border: 1px solid #38516A;
    border-radius: 10px;
    font-weight: 600;
}

[data-testid="stMetric"] {
    background: #172438;
    border: 1px solid #293A50;
    border-radius: 14px;
    padding: 15px;
}

hr {
    border-color: #293A50;
}

#MainMenu, footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def make_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")


def make_error_csv(errors):
    output = io.StringIO()

    writer = csv.DictWriter(
        output,
        fieldnames=["row", "field", "problem"]
    )

    writer.writeheader()
    writer.writerows(errors)

    return output.getvalue().encode("utf-8")


def metric_card(label, value, note, color=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color}">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "results" not in st.session_state:
    st.session_state.results = None

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding:12px 0 22px 0;">
        <div style="font-size:25px;font-weight:800;color:white;">
            🧹 CleanSlate
        </div>
        <div style="font-size:10px;letter-spacing:2px;color:#65D6A5;">
            DATA QUALITY PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Dashboard", "About Project"]
    )

    st.divider()

    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        '<span style="color:#65D6A5;">●</span> Ready to process',
        unsafe_allow_html=True
    )

    st.caption("CleanSlate · CP-099")


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="eyebrow">DATA QUALITY MANAGEMENT</div>
    <h1>Clean your data. Trust your insights.</h1>
    <p>
        Validate, analyse and standardise your CSV datasets
        in one simple workspace.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

if page == "About Project":

    st.markdown(
        '<div class="section-title">About CleanSlate</div>',
        unsafe_allow_html=True
    )

    st.write("""
    CleanSlate is a Python-based Data Validation and Cleansing Utility.

    It identifies missing values, invalid information, inconsistent
    formatting and duplicate email addresses in CSV datasets.

    It also standardises safe formatting issues and generates
    cleaned datasets and error reports.
    """)

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Data validation")
        st.write("""
        - Missing field detection
        - Email validation
        - Indian mobile number validation
        - Date of birth validation
        - Duplicate email detection
        """)

    with right:
        st.subheader("Data cleansing")
        st.write("""
        - Remove unnecessary spaces
        - Standardise names
        - Standardise cities
        - Convert emails to lowercase
        - Export cleaned datasets
        """)

    st.divider()
    st.subheader("Technology stack")
    st.write("Python · Streamlit · Pandas · CSV · Regular Expressions")

    st.info(
        "The original uploaded file is preserved. "
        "Invalid and duplicate records are reported, not deleted."
    )


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

else:

    st.markdown(
        '<div class="section-title">Workspace Overview</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Upload your dataset to begin quality analysis."
    )

    uploaded_file = st.file_uploader(
        "Drop your CSV file here or browse files",
        type=["csv"],
        help="Required columns: name, email, phone, date_of_birth, city"
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()

        import hashlib
        current_hash = hashlib.sha256(file_bytes).hexdigest()

        if current_hash != st.session_state.file_hash:
            st.session_state.file_hash = current_hash
            st.session_state.results = None

        try:

            df = pd.read_csv(
                io.BytesIO(file_bytes),
                dtype=str,
                keep_default_na=False
            )

            df.columns = [str(c).strip() for c in df.columns]

            if len(df.columns) != len(set(df.columns)):
                st.error("Duplicate column names found in CSV.")

            elif df.empty:
                st.warning("The uploaded CSV has no records.")

            else:

                missing = [
                    field for field in REQUIRED_FIELDS
                    if field not in df.columns
                ]

                if missing:

                    st.error(
                        "Missing required columns: "
                        + ", ".join(missing)
                    )

                    st.caption(
                        "Required: " + ", ".join(REQUIRED_FIELDS)
                    )

                else:

                    st.success(
                        f"File uploaded successfully: {uploaded_file.name}"
                    )

                    st.caption(
                        f"{len(df):,} records · {len(df.columns)} columns"
                    )

                    with st.expander("Preview original dataset"):
                        st.dataframe(
                            df,
                            use_container_width=True,
                            hide_index=True
                        )

                    if st.button(
                        "✦ Run Data Validation",
                        type="primary",
                        use_container_width=True
                    ):

                        with st.spinner("Analysing your dataset..."):

                            records = df[REQUIRED_FIELDS].to_dict(
                                orient="records"
                            )

                            cleaned_records, errors = process_records(
                                records
                            )

                            cleaned_df = pd.DataFrame(
                                cleaned_records,
                                columns=REQUIRED_FIELDS
                            )

                            error_df = pd.DataFrame(
                                errors,
                                columns=["row", "field", "problem"]
                            )

                            total = len(records)

                            issue_rows = {
                                error["row"] for error in errors
                            }

                            issue_count = len(issue_rows)
                            valid_count = total - issue_count

                            duplicate_count = sum(
                                "Duplicate email" in error["problem"]
                                for error in errors
                            )

                            score = (
                                round(valid_count / total * 100, 1)
                                if total else 0
                            )

                            st.session_state.results = {
                                "original": df,
                                "cleaned": cleaned_df,
                                "errors": errors,
                                "error_df": error_df,
                                "total": total,
                                "valid": valid_count,
                                "issues": issue_count,
                                "duplicates": duplicate_count,
                                "score": score
                            }

                    # ------------------------------------------
                    # RESULTS
                    # ------------------------------------------

                    result = st.session_state.results

                    if result is not None:

                        st.divider()

                        st.markdown(
                            '<div class="section-title">Quality Overview</div>',
                            unsafe_allow_html=True
                        )

                        st.caption(
                            "Live statistics calculated from your dataset."
                        )

                        c1, c2, c3, c4 = st.columns(4)

                        with c1:
                            metric_card(
                                "TOTAL RECORDS",
                                f"{result['total']:,}",
                                "Records analysed"
                            )

                        with c2:
                            metric_card(
                                "VALID RECORDS",
                                f"{result['valid']:,}",
                                "No detected issues",
                                "green"
                            )

                        with c3:
                            metric_card(
                                "RECORDS WITH ISSUES",
                                f"{result['issues']:,}",
                                "Need attention",
                                "red"
                            )

                        with c4:
                            metric_card(
                                "DUPLICATE EMAILS",
                                f"{result['duplicates']:,}",
                                "Repeated email entries",
                                "orange"
                            )

                        st.write("")
                        left, right = st.columns(2)

                        with left:
                            st.markdown("**Overall data quality**")
                            st.markdown(
                                f"""
                                <div class="metric-card">
                                    <div class="metric-value green">
                                        {result['score']}%
                                    </div>
                                    <div class="metric-note">
                                        Records without detected issues
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.progress(result["score"] / 100)

                        with right:
                            st.markdown("**Validation summary**")
                            st.metric(
                                "Total issues detected",
                                len(result["errors"])
                            )
                            st.metric(
                                "Fields with errors",
                                result["error_df"]["field"].nunique()
                                if not result["error_df"].empty else 0
                            )

                        st.divider()

                        st.markdown(
                            '<div class="section-title">Error Analytics</div>',
                            unsafe_allow_html=True
                        )

                        if result["errors"]:

                            chart1, chart2 = st.columns(2)

                            with chart1:
                                st.markdown("**Issues by field**")
                                st.bar_chart(
                                    result["error_df"]["field"].value_counts(),
                                    color="#20A47D"
                                )

                            with chart2:
                                st.markdown("**Issue categories**")
                                st.bar_chart(
                                    result["error_df"]["problem"].value_counts(),
                                    color="#4B91C5"
                                )

                        else:
                            st.success(
                                "No validation issues detected."
                            )

                        st.divider()

                        st.markdown(
                            '<div class="section-title">Dataset Explorer</div>',
                            unsafe_allow_html=True
                        )

                        tab1, tab2, tab3 = st.tabs([
                            "Original Data",
                            "Cleaned Data",
                            "Error Report"
                        ])

                        with tab1:

                            st.caption("Original uploaded records.")

                            st.dataframe(
                                result["original"],
                                use_container_width=True,
                                hide_index=True
                            )

                        with tab2:

                            st.caption("Standardised dataset.")

                            st.dataframe(
                                result["cleaned"],
                                use_container_width=True,
                                hide_index=True
                            )

                            st.download_button(
                                "↓ Download Cleaned CSV",
                                data=make_csv(result["cleaned"]),
                                file_name="cleaned_data.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                        with tab3:

                            st.caption(
                                "Detected problems by row and field."
                            )

                            if result["errors"]:

                                st.dataframe(
                                    result["error_df"],
                                    use_container_width=True,
                                    hide_index=True
                                )

                                st.download_button(
                                    "↓ Download Error Report",
                                    data=make_error_csv(result["errors"]),
                                    file_name="error_report.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )

                            else:
                                st.success("No errors to report.")

                        st.success(
                            "Analysis completed. Original data remains unchanged."
                        )

        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV is empty or has no header.")

        except pd.errors.ParserError:
            st.error("The CSV format is invalid.")

        except UnicodeDecodeError:
            st.error("Please upload a UTF-8 encoded CSV file.")

        except Exception as error:
            st.error(f"Processing error: {error}")

    else:

        st.markdown("""
        <div style="
            background:#121E30;
            border:1px dashed #426078;
            border-radius:16px;
            padding:30px;
            margin-top:15px;
            text-align:center;">
            <div style="font-size:38px;">📂</div>
            <div style="color:white;font-size:19px;font-weight:700;">
                Your data workspace is ready
            </div>
            <div style="color:#93A6BB;font-size:13px;margin-top:8px;">
                Upload a CSV dataset to discover data quality issues.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        f1, f2, f3 = st.columns(3)

        with f1:
            st.markdown("### 🔍 Validate")
            st.caption(
                "Find missing fields, invalid emails, phone numbers and dates."
            )

        with f2:
            st.markdown("### ✨ Clean")
            st.caption(
                "Standardise spaces, names, cities and email formatting."
            )

        with f3:
            st.markdown("### 📊 Analyse")
            st.caption(
                "Explore quality metrics, errors and downloadable reports."
            )

        st.info(
            "Required columns: name, email, phone, date_of_birth, city"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#71839A;
    font-size:11px;
    padding:10px;">
    <strong style="color:#9AADC2;">CleanSlate</strong>
    · Data Validation & Cleansing Utility
    <br>
    Built with Python and Streamlit
</div>
""", unsafe_allow_html=True)
