"""Page 6: CSV upload for bulk insert and filtered CSV export.

Admin-only upload section; export section available to all roles.
"""

import io
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Upload & Export", page_icon="📂", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login, require_admin, get_role
from db import get_engine
from queries import (
    get_all_opportunities,
    search_opportunities,
    bulk_insert_from_dataframe,
)
from utils import sanitize_csv_upload, dataframe_to_csv_bytes

require_login()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>📂 CSV Upload & Export</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

role = get_role()

st.markdown("### 📥 Upload Section (Admin Only)")
if role == "Admin":
    uploaded_file = st.file_uploader(
        "Choose a CSV file", type="csv", help="Upload a CSV file with opportunity data."
    )

    sample_df = pd.DataFrame({
        "company_name": ["Example Corp"],
        "job_title": ["Software Engineer"],
        "category": ["Software Engineering"],
        "city": ["Lahore"],
        "country": ["Pakistan"],
        "work_mode": ["Onsite"],
        "required_skills": ["Python, SQL, Django"],
        "salary_min": [80000],
        "salary_max": [150000],
        "currency": ["PKR"],
        "experience_level": ["1-2 Years"],
        "application_deadline": ["2026-07-01"],
        "status": ["Open"],
        "source_link": ["https://example.com/careers"],
    })
    csv_template = dataframe_to_csv_bytes(sample_df)
    st.download_button(
        label="📄 Download Sample CSV Template",
        data=csv_template,
        file_name="sample_template.csv",
        mime="text/csv",
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.subheader("Uploaded Data Preview")
            st.dataframe(df.head(10), use_container_width=True, hide_index=True)

            cleaned_df, warnings = sanitize_csv_upload(df)

            if warnings:
                with st.expander("⚠️ Warnings", expanded=True):
                    for w in warnings:
                        st.warning(w)

            valid_count = len(cleaned_df)
            st.metric("Total Rows in Upload", valid_count)

            if st.button("Insert Valid Rows", type="primary", use_container_width=True):
                with st.spinner("Inserting records..."):
                    success, errors = bulk_insert_from_dataframe(engine, cleaned_df)
                    st.success(f"✅ {success} records inserted successfully!")
                    if errors:
                        with st.expander(f"❌ {len(errors)} Errors", expanded=True):
                            for err in errors:
                                st.error(f"Row {err['row_index']}: {err['error_message']}")
        except Exception as e:
            st.error(f"Failed to read CSV file: {e}")
else:
    st.info("👤 You are logged in as Viewer. Upload is available for Admin users only.")

st.markdown("---")
st.markdown("### 📤 Export Section")

all_data = get_all_opportunities(engine)
export_categories = st.multiselect(
    "Filter by Category",
    options=sorted(all_data["category"].dropna().unique()) if not all_data.empty else [],
)
export_statuses = st.multiselect(
    "Filter by Status",
    options=sorted(all_data["status"].dropna().unique()) if not all_data.empty else [],
)
export_work_modes = st.multiselect(
    "Filter by Work Mode",
    options=sorted(all_data["work_mode"].dropna().unique()) if not all_data.empty else [],
)

export_filters = {}
if export_categories:
    export_filters["category"] = export_categories
if export_statuses:
    export_filters["status"] = export_statuses
if export_work_modes:
    export_filters["work_mode"] = export_work_modes

if export_filters:
    export_df = search_opportunities(engine, **export_filters)
else:
    export_df = all_data

st.metric("Rows to Export", len(export_df))

if not export_df.empty:
    csv_export = dataframe_to_csv_bytes(export_df)
    st.download_button(
        label="📥 Download Filtered CSV",
        data=csv_export,
        file_name="exported_opportunities.csv",
        mime="text/csv",
        use_container_width=True,
    )


