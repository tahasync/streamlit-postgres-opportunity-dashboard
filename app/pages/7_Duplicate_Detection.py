"""Page 7: Detect and review duplicate opportunity records.

Groups duplicates by company_name + job_title + city and displays them
in expandable sections.
"""

import streamlit as st

st.set_page_config(page_title="Duplicate Detection", page_icon="🔁", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login
from db import get_engine
from queries import detect_duplicates

require_login()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>🔁 Duplicate Detection</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

if st.button("🔄 Refresh", use_container_width=True):
    st.rerun()

with st.spinner("Scanning for duplicates..."):
    duplicates = detect_duplicates(engine)

if duplicates.empty:
    st.success("✅ No duplicates detected in the database.")
    st.stop()

group_count = duplicates["duplicate_count"].nunique()
st.metric("Duplicate Groups Found", duplicates["opportunity_id"].nunique())

for (company, title, city), group_df in duplicates.groupby(
    ["company_name", "job_title", "city"]
):
    count = len(group_df)
    expander_label = f"🏢 {company} | 📋 {title} | 📍 {city} ({count} duplicates)"
    with st.expander(expander_label, expanded=False):
        st.dataframe(group_df, use_container_width=True, hide_index=True)


