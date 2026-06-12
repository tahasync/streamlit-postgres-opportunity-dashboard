"""Page 2: View and search opportunities with filtering and CSV export.

Provides sidebar filters, a sortable data table, and download functionality.
"""

import streamlit as st

st.set_page_config(page_title="View & Search", page_icon="🔍", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login
from db import get_engine
from queries import get_all_opportunities, search_opportunities
from utils import dataframe_to_csv_bytes, get_status_color

require_login()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>🔍 View & Search Opportunities</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

all_data = get_all_opportunities(engine)
st.metric("Total Records", len(all_data))

st.sidebar.header("🔎 Filter Options")

search_keyword = st.sidebar.text_input("Search", placeholder="Company, title, skills...")

categories = st.sidebar.multiselect(
    "Category",
    options=sorted(all_data["category"].dropna().unique()) if not all_data.empty else [],
)
cities = st.sidebar.multiselect(
    "City",
    options=sorted(all_data["city"].dropna().unique()) if not all_data.empty else [],
)
work_modes = st.sidebar.multiselect(
    "Work Mode",
    options=sorted(all_data["work_mode"].dropna().unique()) if not all_data.empty else [],
)
statuses = st.sidebar.multiselect(
    "Status",
    options=sorted(all_data["status"].dropna().unique()) if not all_data.empty else [],
)
experience_levels = st.sidebar.multiselect(
    "Experience Level",
    options=sorted(all_data["experience_level"].dropna().unique()) if not all_data.empty else [],
)

salary_min_val, salary_max_val = st.sidebar.slider(
    "Salary Range (PKR)",
    min_value=0,
    max_value=500000,
    value=(0, 500000),
    step=10000,
)

with st.spinner("Loading results..."):
    filtered = search_opportunities(
        engine,
        keyword=search_keyword if search_keyword else None,
        category=categories if categories else None,
        city=cities if cities else None,
        work_mode=work_modes if work_modes else None,
        status=statuses if statuses else None,
        salary_min=salary_min_val,
        salary_max=salary_max_val,
        experience_level=experience_levels if experience_levels else None,
    )

st.metric("Filtered Results", len(filtered))

if not filtered.empty:
    display_cols = [
        "opportunity_id", "company_name", "job_title", "category", "city",
        "work_mode", "salary_min", "salary_max", "currency",
        "experience_level", "status", "application_deadline"
    ]
    display_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

    csv_bytes = dataframe_to_csv_bytes(filtered)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="filtered_opportunities.csv",
        mime="text/csv",
        use_container_width=True,
    )
else:
    st.info("No opportunities match the current filters.")


