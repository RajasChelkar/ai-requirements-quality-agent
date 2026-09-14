import json
from pathlib import Path

import streamlit as st
import pandas as pd

from src.scoring import calculate_quality_score


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

CACHE_FILE = PROJECT_ROOT / "Data" / "analysis_cache.json"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Requirements Quality Agent",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("AI Requirements Quality Agent")

st.write(
    "AI-assisted requirements quality and traceability analysis"
)

st.divider()


# --------------------------------------------------
# Upload
# --------------------------------------------------

st.subheader("Upload Requirements")

uploaded_file = st.file_uploader(
    "Upload an Excel requirements file",
    type=["xlsx"]
)


# Everything below depends on an uploaded file
if uploaded_file is not None:

    # --------------------------------------------------
    # Load requirements
    # --------------------------------------------------

    requirements = pd.read_excel(uploaded_file)

    st.success(
        f"Loaded {len(requirements)} requirements."
    )

    # --------------------------------------------------
    # Display requirements
    # --------------------------------------------------

    st.subheader("Requirements")

    st.dataframe(
        requirements,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # Load cache
    # --------------------------------------------------

    if CACHE_FILE.exists():

        with open(
            CACHE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            cache = json.load(file)

    else:

        cache = {}

    # --------------------------------------------------
    # Find completed AI analyses
    # --------------------------------------------------

    analyzed_ids = [
        requirement_id
        for requirement_id in requirements["Requirement_ID"]
        if requirement_id in cache
        and "status" not in cache[requirement_id]
    ]

    # --------------------------------------------------
    # AI Analysis section
    # --------------------------------------------------

    st.subheader("AI Analysis")

    st.info(
        f"AI analysis available for "
        f"{len(analyzed_ids)} of "
        f"{len(requirements)} requirements."
    )

    # --------------------------------------------------
    # Overall dashboard summary
    # --------------------------------------------------

    scores = []
    ambiguous_count = 0
    traceability_issue_count = 0

    for requirement_id in analyzed_ids:

        ai_result = cache[requirement_id]

        requirement_row = requirements[
            requirements["Requirement_ID"] == requirement_id
        ].iloc[0]

        parent_id = str(
            requirement_row["Parent_ID"]
        ).strip()

        verification_method = str(
            requirement_row["Verification_Method"]
        ).strip()

        traceability_issues = []

        if parent_id in ["", "-", "—"]:
            traceability_issues.append(
                "Missing Parent_ID"
            )

        if verification_method in ["", "-", "—"]:
            traceability_issues.append(
                "Missing Verification_Method"
            )

        traceability = {
            "traceability_issues": traceability_issues
        }

        score = calculate_quality_score(
            ai_result,
            traceability
        )

        scores.append(score)

        if ai_result.get("ambiguous", False):
            ambiguous_count += 1

        if traceability_issues:
            traceability_issue_count += 1

    # Average score
    if scores:

        average_score = round(
            sum(scores) / len(scores)
        )

    else:

        average_score = None

    # --------------------------------------------------
    # Summary metrics
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Requirements",
            len(requirements)
        )

    with col2:

        st.metric(
            "AI Analyzed",
            len(analyzed_ids)
        )

    with col3:

        st.metric(
            "Average Quality Score",
            f"{average_score}/100"
            if average_score is not None
            else "—"
        )

    col4, col5 = st.columns(2)

    with col4:

        st.metric(
            "Ambiguous Requirements",
            ambiguous_count
        )

    with col5:

        st.metric(
            "Traceability Issues",
            traceability_issue_count
        )

    st.divider()

    # --------------------------------------------------
    # Requirements quality overview
    # --------------------------------------------------

    st.subheader("Requirements Quality Overview")

    overview_rows = []

    for _, requirement in requirements.iterrows():

        requirement_id = requirement["Requirement_ID"]

        score = None
        classification = "—"
        ambiguous = "—"
        traceability_status = "—"
        status = "AI Analysis Pending"

        # ----------------------------------------------
        # Completed AI analysis
        # ----------------------------------------------

        if requirement_id in analyzed_ids:

            ai_result = cache[requirement_id]

            parent_id = str(
                requirement["Parent_ID"]
            ).strip()

            verification_method = str(
                requirement["Verification_Method"]
            ).strip()

            traceability_issues = []

            if parent_id in ["", "-", "—"]:
                traceability_issues.append(
                    "Missing Parent_ID"
                )

            if verification_method in ["", "-", "—"]:
                traceability_issues.append(
                    "Missing Verification_Method"
                )

            traceability = {
                "traceability_issues": traceability_issues
            }

            score = calculate_quality_score(
                ai_result,
                traceability
            )

            classification = ai_result[
                "classification"
            ]

            ambiguous = (
                "Yes"
                if ai_result["ambiguous"]
                else "No"
            )

            traceability_status = (
                "Issue"
                if traceability_issues
                else "OK"
            )

            status = "Analyzed"

        # ----------------------------------------------
        # Add row
        # ----------------------------------------------

        overview_rows.append({
            "Requirement ID": requirement_id,
            "Quality Score": (
                score
                if score is not None
                else "—"
            ),
            "Classification": classification,
            "Ambiguous": ambiguous,
            "Traceability": traceability_status,
            "Status": status
        })

    overview_df = pd.DataFrame(
        overview_rows
    )

    st.dataframe(
        overview_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # Individual requirement analysis
    # --------------------------------------------------

    if analyzed_ids:

        selected_id = st.selectbox(
            "Select a requirement",
            analyzed_ids
        )

        selected_row = requirements[
            requirements["Requirement_ID"] == selected_id
        ].iloc[0]

        ai_result = cache[selected_id]

        # Traceability
        parent_id = str(
            selected_row["Parent_ID"]
        ).strip()

        verification_method = str(
            selected_row["Verification_Method"]
        ).strip()

        traceability_issues = []

        if parent_id in ["", "-", "—"]:
            traceability_issues.append(
                "Missing Parent_ID"
            )

        if verification_method in ["", "-", "—"]:
            traceability_issues.append(
                "Missing Verification_Method"
            )

        traceability = {
            "traceability_issues": traceability_issues
        }

        # Score
        quality_score = calculate_quality_score(
            ai_result,
            traceability
        )

        st.subheader(selected_id)

        st.write(
            selected_row["Requirement_Text"]
        )

        # Metrics
        detail_col1, detail_col2, detail_col3 = st.columns(3)

        with detail_col1:

            st.metric(
                "Quality Score",
                f"{quality_score}/100"
            )

        with detail_col2:

            st.metric(
                "Classification",
                ai_result["classification"]
            )

        with detail_col3:

            st.metric(
                "Ambiguous",
                "Yes"
                if ai_result["ambiguous"]
                else "No"
            )

        # Ambiguous terms
        st.subheader("Ambiguous Terms")

        if ai_result["ambiguous_terms"]:

            for term in ai_result["ambiguous_terms"]:

                st.warning(term)

        else:

            st.success(
                "No ambiguous terms identified."
            )

        # Quality issues
        st.subheader("Quality Issues")

        if ai_result["quality_issues"]:

            for issue in ai_result["quality_issues"]:

                st.write(f"• {issue}")

        else:

            st.success(
                "No quality issues identified."
            )

        # Suggested improvement
        st.subheader("Suggested Improvement")

        st.info(
            ai_result["suggested_improvement"]
        )

        # Traceability
        st.subheader("Traceability")

        trace_col1, trace_col2 = st.columns(2)

        with trace_col1:

            if parent_id in ["", "-", "—"]:

                st.error(
                    "✗ Parent ID missing"
                )

            else:

                st.success(
                    f"✓ Parent ID: {parent_id}"
                )

        with trace_col2:

            if verification_method in ["", "-", "—"]:

                st.error(
                    "✗ Verification method missing"
                )

            else:

                st.success(
                    f"✓ Verification: "
                    f"{verification_method}"
                )

    else:

        st.warning(
            "No completed AI analysis is available yet."
        )