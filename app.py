"""
CleanSlate — Data Validation & Cleansing Utility
Vintage Garage Edition.

Uses the existing validator.py:
    REQUIRED_FIELDS
    process_records(records) -> (cleaned_records, errors)

CSV files are processed in memory. No database or permanent upload storage.
"""

from __future__ import annotations

import io
from typing import Any

import pandas as pd
import streamlit as st
import validator


# ---------------------------------------------------------------------------
# PAGE CONFIGURATION AND PROJECT CONTRACT
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="CleanSlate | Vintage Garage",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

REQUIRED_FIELDS = list(validator.REQUIRED_FIELDS)


# ---------------------------------------------------------------------------
# VINTAGE GARAGE THEME
# ---------------------------------------------------------------------------

C = {
    "cream": "#E9E1D0",
    "ivory": "#F4EBDD",
    "charcoal": "#242321",
    "black": "#171717",
    "green": "#294C3B",
    "olive": "#74775A",
    "orange": "#B7653D",
    "brass": "#B08A52",
    "soft": "#5B574F",
    "faint": "#8A8478",
}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;1,600&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

.stApp {{
    background: radial-gradient(circle at 12% 8%, {C['ivory']} 0%, transparent 42%),
                radial-gradient(circle at 88% 85%, {C['ivory']} 0%, transparent 40%),
                {C['cream']};
    color: {C['charcoal']};
    font-family: 'Inter', sans-serif;
}}
.block-container {{max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}}
#MainMenu, footer {{visibility: hidden;}}
h1, h2, h3 {{color: {C['charcoal']};}}
.cs-header {{
    display:flex; justify-content:space-between; align-items:flex-end;
    border-bottom:2px solid {C['charcoal']}; padding-bottom:1rem; margin-bottom:1.5rem;
    position:relative;
}}
.cs-header:after {{
    content:''; position:absolute; bottom:-6px; left:0; right:0;
    height:1px; background:{C['brass']};
}}
.cs-brand {{font-family:'Oswald',sans-serif; font-size:1.8rem; font-weight:700;
    letter-spacing:.08em; text-transform:uppercase; display:flex; align-items:center; gap:.7rem;}}
.cs-mark {{width:25px;height:25px;background:{C['green']};border:2px solid {C['charcoal']};}}
.cs-sub {{font-family:'Playfair Display',serif;font-style:italic;color:{C['soft']};}}
.cs-meta {{font-family:'IBM Plex Mono',monospace;font-size:.68rem;text-align:right;
    color:{C['faint']};letter-spacing:.1em;text-transform:uppercase;}}
.cs-status {{color:{C['green']};border:1px solid {C['green']};padding:.2rem .5rem;display:inline-block;margin-top:.4rem;}}
.cs-hero {{padding:1.7rem 0 2rem;border-bottom:1px dashed {C['soft']};margin-bottom:1.6rem;}}
.cs-eyebrow {{font-family:'IBM Plex Mono',monospace;color:{C['orange']};font-size:.72rem;
    letter-spacing:.18em;text-transform:uppercase;margin-bottom:.6rem;}}
.cs-title {{font-family:'Oswald',sans-serif;font-size:3.3rem;line-height:1.02;
    text-transform:uppercase;font-weight:600;margin:0;color:{C['charcoal']};}}
.cs-title em {{font-family:'Playfair Display',serif;color:{C['green']};text-transform:none;}}
.cs-lede {{max-width:700px;color:{C['soft']};line-height:1.65;margin-top:.8rem;}}
.cs-steps {{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid {C['charcoal']};
    border-bottom:1px solid {C['charcoal']};margin:1.5rem 0 2rem;}}
.cs-step {{padding:1rem;border-right:1px solid {C['soft']};}}
.cs-step:last-child {{border-right:0;}}
.cs-num {{font-family:'IBM Plex Mono',monospace;color:{C['brass']};font-size:.75rem;}}
.cs-step strong {{display:block;font-family:'Oswald',sans-serif;letter-spacing:.1em;margin:.3rem 0;text-transform:uppercase;}}
.cs-step span {{font-size:.8rem;color:{C['soft']};}}
.cs-card {{background:{C['ivory']};border:1px solid {C['soft']};padding:1.2rem 1.3rem;margin:.5rem 0 1rem;}}
.cs-card-title {{font-family:'Oswald',sans-serif;text-transform:uppercase;letter-spacing:.12em;
    border-bottom:1px solid {C['soft']};padding-bottom:.6rem;margin-bottom:.8rem;}}
.cs-rule {{display:flex;align-items:center;gap:.8rem;margin:1.7rem 0 .8rem;
    font-family:'IBM Plex Mono',monospace;font-size:.68rem;letter-spacing:.16em;
    color:{C['faint']};text-transform:uppercase;}}
.cs-rule:after {{content:'';height:1px;background:{C['brass']};flex:1;}}
.cs-stats {{display:grid;grid-template-columns:repeat(5,1fr);border:1px solid {C['charcoal']};margin:1rem 0;}}
.cs-stat {{padding:1rem;background:{C['ivory']};border-right:1px solid {C['soft']};}}
.cs-stat:last-child {{border-right:0;}}
.cs-stat small {{display:block;font-family:'IBM Plex Mono',monospace;font-size:.62rem;
    letter-spacing:.12em;color:{C['faint']};text-transform:uppercase;}}
.cs-stat b {{display:block;font-family:'Oswald',sans-serif;font-size:2rem;margin-top:.3rem;}}
.cs-stat.issue b {{color:{C['orange']};}}
.cs-stat.good b {{color:{C['green']};}}
.stButton>button,.stDownloadButton>button {{
    background:{C['charcoal']}!important;color:{C['ivory']}!important;border:1px solid {C['charcoal']}!important;
    border-radius:0!important;font-family:'Oswald',sans-serif!important;letter-spacing:.12em!important;
    text-transform:uppercase!important;padding:.55rem 1rem!important;
}}
.stButton>button:hover,.stDownloadButton>button:hover {{
    background:{C['green']}!important;border-color:{C['green']}!important;
}}
[data-testid="stFileUploaderDropzone"] {{background:{C['ivory']};border:1px dashed {C['charcoal']};border-radius:0;}}
.stTabs [data-baseweb="tab-list"] {{gap:0;border-bottom:1px solid {C['charcoal']};}}
.stTabs [data-baseweb="tab"] {{font-family:'IBM Plex Mono',monospace;text-transform:uppercase;
    letter-spacing:.08em;border-radius:0;}}
.stTabs [aria-selected="true"] {{background:{C['ivory']}!important;color:{C['charcoal']}!important;}}
[data-testid="stDataFrame"] {{border:1px solid {C['charcoal']};border-radius:0;}}
.cs-footer {{border-top:1px solid {C['soft']};margin-top:2.5rem;padding-top:1rem;
    display:flex;justify-content:space-between;gap:.5rem;flex-wrap:wrap;
    font-family:'IBM Plex Mono',monospace;font-size:.65rem;letter-spacing:.1em;color:{C['faint']};}}
@media(max-width:800px) {{
    .cs-steps {{grid-template-columns:repeat(2,1fr);}}
    .cs-stats {{grid-template-columns:repeat(2,1fr);}}
    .cs-title {{font-size:2.4rem;}}
}}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def section_rule(label: str) -> None:
    st.markdown(
        f'<div class="cs-rule">{label}</div>',
        unsafe_allow_html=True,
    )


def read_csv(uploaded_file: Any) -> pd.DataFrame:
    raw = uploaded_file.getvalue()

    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return pd.read_csv(
                io.BytesIO(raw),
                encoding=encoding,
                dtype=str,
                keep_default_na=False,
                skip_blank_lines=True,
            )

        except UnicodeDecodeError:
            continue

        except pd.errors.EmptyDataError as exc:
            raise ValueError("The uploaded CSV is empty.") from exc

        except pd.errors.ParserError as exc:
            raise ValueError(f"Could not read this CSV: {exc}") from exc

    raise ValueError("The CSV encoding could not be recognised.")


def normalise_errors(raw_errors: Any) -> list[dict]:
    if raw_errors is None:
        return []

    if isinstance(raw_errors, dict):
        raw_errors = [raw_errors]

    result = []

    for item in raw_errors:
        if isinstance(item, dict):
            result.append({
                "row": item.get(
                    "row",
                    item.get("row_number", item.get("row_index"))
                ),
                "field": item.get("field", item.get("column", "")),
                "problem": item.get(
                    "problem",
                    item.get("message", item.get("error", ""))
                ),
            })

        else:
            result.append({
                "row": None,
                "field": "",
                "problem": str(item),
            })

    return result


def make_clean_dataframe(
    cleaned_records: Any,
    original: pd.DataFrame
) -> pd.DataFrame:

    if isinstance(cleaned_records, pd.DataFrame):
        cleaned = cleaned_records.copy()
    else:
        cleaned = pd.DataFrame(cleaned_records or [])

    # Retain extra source columns when the validator returns the same row count.
    if len(cleaned) == len(original):
        for column in original.columns:
            if column not in cleaned.columns:
                cleaned[column] = original[column].values

    if not cleaned.empty:
        ordered = [
            column for column in original.columns
            if column in cleaned.columns
        ]

        extras = [
            column for column in cleaned.columns
            if column not in ordered
        ]

        cleaned = cleaned[ordered + extras]

    return cleaned


def calculate_metrics(total: int, errors: list[dict]) -> dict:
    affected_rows = set()

    for error in errors:
        try:
            if error["row"] is not None:
                affected_rows.add(int(error["row"]))

        except (TypeError, ValueError):
            pass

    rows_with_issues = len(affected_rows)
    valid = max(total - rows_with_issues, 0)

    duplicates = [
        error for error in errors
        if "duplicate" in str(error.get("problem", "")).lower()
    ]

    score = (valid / total * 100) if total else 0

    return {
        "total": total,
        "valid": valid,
        "with_issues": rows_with_issues,
        "total_issues": len(errors),
        "duplicates": len(duplicates),
        "score": score,
    }


def csv_bytes(dataframe: pd.DataFrame) -> bytes:
    return dataframe.to_csv(index=False).encode("utf-8")


def show_metric(label: str, value: str, css_class: str = "") -> str:
    return (
        f'<div class="cs-stat {css_class}">'
        f'<small>{label}</small><b>{value}</b></div>'
    )


# ---------------------------------------------------------------------------
# HEADER AND HERO
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="cs-header">
      <div>
        <div class="cs-brand"><span class="cs-mark"></span> CleanSlate</div>
        <div class="cs-sub">Data Validation &amp; Cleansing Utility</div>
      </div>
      <div class="cs-meta">BUILD 2.0 · VINTAGE GARAGE<br>
        <span class="cs-status">● SYSTEM READY</span>
      </div>
    </div>

    <div class="cs-hero">
      <div class="cs-eyebrow">Workshop No. 01 · Data Quality Line</div>
      <h1 class="cs-title">Clean data.<br><em>Clear</em> decisions.</h1>
      <p class="cs-lede">
      An intelligent data validation and cleansing workspace designed to
      identify inconsistencies, standardise records, and improve data reliability,
      one upload at a time.</p>
    </div>

    <div class="cs-steps">
      <div class="cs-step">
        <div class="cs-num">01</div>
        <strong>Source</strong>
        <span>Upload CSV data</span>
      </div>

      <div class="cs-step">
        <div class="cs-num">02</div>
        <strong>Inspect</strong>
        <span>Review structure</span>
      </div>

      <div class="cs-step">
        <div class="cs-num">03</div>
        <strong>Clean</strong>
        <span>Validate records</span>
      </div>

      <div class="cs-step">
        <div class="cs-num">04</div>
        <strong>Export</strong>
        <span>Download results</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# UPLOAD AND INSPECT
# ---------------------------------------------------------------------------

section_rule("Stage 01 · Source your dataset")

uploaded = st.file_uploader(
    "Choose a CSV file",
    type=["csv"],
    help="CSV only. Uploaded data is processed in memory.",
)

if uploaded is None:
    st.markdown(
        f'<div class="cs-card">'
        f'<div class="cs-card-title">Awaiting input</div>'
        f'<p style="color:{C["soft"]};margin:0">'
        f'Upload a CSV file to begin. '
        f'The project includes sample_data.csv for a quick demonstration.'
        f'</p></div>',
        unsafe_allow_html=True,
    )

    st.stop()


try:
    raw_df = read_csv(uploaded)

except ValueError as error:
    st.error(str(error))
    st.stop()


missing_columns = [
    field for field in REQUIRED_FIELDS
    if field not in raw_df.columns
]

if missing_columns:
    st.error("Missing required column(s): " + ", ".join(missing_columns))
    st.caption("Columns found: " + ", ".join(map(str, raw_df.columns)))
    st.stop()


if raw_df.empty:
    st.warning("This CSV contains column headings but no data rows.")
    st.stop()


st.success(
    f"Loaded **{uploaded.name}** · "
    f"{len(raw_df):,} records · "
    f"{len(raw_df.columns)} columns"
)


# ---------------------------------------------------------------------------
# DATASET PREVIEW
# ---------------------------------------------------------------------------

section_rule("Stage 02 · Inspect the records")

st.markdown(
    '<div class="cs-card">'
    '<div class="cs-card-title">Dataset preview</div>',
    unsafe_allow_html=True,
)

a, b, c = st.columns(3)

a.metric("Rows", f"{len(raw_df):,}")
b.metric("Columns", f"{len(raw_df.columns):,}")
c.metric("File", uploaded.name)

st.dataframe(
    raw_df.head(25),
    use_container_width=True,
    hide_index=True,
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------

section_rule("Stage 03 · Clean and validate")

analyse = st.button(
    "RUN DATA INSPECTION",
    type="primary",
    use_container_width=True,
)


if "analysis_cache" not in st.session_state:
    st.session_state.analysis_cache = None


if analyse:
    try:
        with st.spinner("Inspecting records in the workshop..."):

            records = raw_df.to_dict(orient="records")

            cleaned_records, raw_errors = validator.process_records(records)

            errors = normalise_errors(raw_errors)

            cleaned_df = make_clean_dataframe(
                cleaned_records,
                raw_df,
            )

            metrics = calculate_metrics(
                len(raw_df),
                errors,
            )

            st.session_state.analysis_cache = {
                "filename": uploaded.name,
                "cleaned": cleaned_df,
                "errors": errors,
                "metrics": metrics,
                "original": raw_df.copy(),
            }

    except Exception as error:
        st.session_state.analysis_cache = None
        st.error(f"Analysis could not be completed: {error}")


result = st.session_state.analysis_cache


# Clear stale results when a different upload is selected.
if result is not None and result["filename"] != uploaded.name:
    st.session_state.analysis_cache = None
    result = None


if result is None:
    st.info(
        "Upload your dataset and select **Run Data Inspection** "
        "to see the analysis."
    )
    st.stop()


# ---------------------------------------------------------------------------
# RESULTS DASHBOARD
# ---------------------------------------------------------------------------

metrics = result["metrics"]
errors = result["errors"]
cleaned_df = result["cleaned"]

issues_df = pd.DataFrame(
    errors,
    columns=["row", "field", "problem"],
)

duplicate_df = issues_df[
    issues_df["problem"].astype(str).str.contains(
        "duplicate",
        case=False,
        na=False,
    )
].copy()


section_rule("Workshop report · Quality overview")


st.markdown(
    '<div class="cs-stats">'
    + show_metric("Total records", f'{metrics["total"]:,}')
    + show_metric("Valid records", f'{metrics["valid"]:,}', "good")
    + show_metric("Records with issues", f'{metrics["with_issues"]:,}', "issue")
    + show_metric("Total issues", f'{metrics["total_issues"]:,}', "issue")
    + show_metric(
        "Quality score",
        f'{metrics["score"]:.1f}%',
        "good" if metrics["score"] >= 70 else "issue"
    )
    + '</div>',
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# CHARTS
# ---------------------------------------------------------------------------

left, right = st.columns(2)


with left:
    st.markdown("**Record quality**")

    quality_chart = pd.DataFrame(
        {
            "Records": [
                metrics["valid"],
                metrics["with_issues"],
            ],
        },
        index=["Valid", "With issues"],
    )

    st.bar_chart(quality_chart)


with right:
    st.markdown("**Issues by field**")

    if issues_df.empty:
        st.success("No validation issues found.")

    else:
        issue_counts = (
            issues_df["field"]
            .replace("", "Unspecified")
            .value_counts()
            .rename_axis("Field")
            .to_frame("Issues")
        )

        st.bar_chart(issue_counts)


# ---------------------------------------------------------------------------
# RESULTS TABS
# ---------------------------------------------------------------------------

section_rule("Stage 04 · Review and export")

tab_original, tab_cleaned, tab_issues, tab_duplicates = st.tabs([
    "Original dataset",
    "Cleaned dataset",
    "Validation issues",
    "Duplicate records",
])


with tab_original:
    st.markdown("**Source data**")

    st.dataframe(
        result["original"],
        use_container_width=True,
        hide_index=True,
    )


with tab_cleaned:
    st.markdown("**Standardised output**")

    st.caption(
        "Safe formatting changes are applied by your existing validator. "
        "Invalid records are not silently deleted."
    )

    st.dataframe(
        cleaned_df,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "DOWNLOAD CLEANED CSV",
        data=csv_bytes(cleaned_df),
        file_name="cleaned_data.csv",
        mime="text/csv",
        use_container_width=True,
    )


with tab_issues:
    st.markdown("**Validation error report**")

    if issues_df.empty:
        st.success("No validation issues were found.")

    else:
        st.dataframe(
            issues_df,
            use_container_width=True,
            hide_index=True,
        )

    st.download_button(
        "DOWNLOAD ERROR REPORT",
        data=csv_bytes(issues_df),
        file_name="error_report.csv",
        mime="text/csv",
        use_container_width=True,
    )


with tab_duplicates:
    st.markdown("**Duplicate email findings**")

    if duplicate_df.empty:
        st.success("No duplicate email findings.")

    else:
        st.dataframe(
            duplicate_df,
            use_container_width=True,
            hide_index=True,
        )


# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------

st.markdown(
    """
    <div class="cs-footer">
      <span><strong>CleanSlate</strong> · Vintage Garage Edition</span>
      <span>Data validation &amp; cleansing utility</span>
      <span>Processed in memory · CSV export</span>
    </div>
    """,
    unsafe_allow_html=True,
)