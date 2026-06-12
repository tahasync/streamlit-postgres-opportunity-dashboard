"""Page 4: Delete an opportunity record with two-step confirmation.

Admin-only page that requires explicit checkbox confirmation before deletion.
"""

import streamlit as st

st.set_page_config(page_title="Delete Opportunity", page_icon="🗑️", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login, require_admin
from db import get_engine
from queries import get_all_opportunities, get_opportunity_by_id, delete_opportunity

require_login()
require_admin()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>🗑️ Delete Opportunity</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

all_opps = get_all_opportunities(engine)

if all_opps.empty:
    st.info("No opportunities available to delete.")
    st.stop()

opp_options = {
    f"ID {row['opportunity_id']} — {row['company_name']} — {row['job_title']}": row["opportunity_id"]
    for _, row in all_opps.iterrows()
}

selected_label = st.selectbox("Select Opportunity to Delete", list(opp_options.keys()))
selected_id = opp_options[selected_label]

st.subheader("📄 Record Preview")
current = get_opportunity_by_id(engine, selected_id)
if not current.empty:
    st.dataframe(current, use_container_width=True, hide_index=True)

st.divider()

st.warning(
    "⚠️ This action cannot be undone. Please review the record above before proceeding."
)

confirm = st.checkbox("I confirm I want to delete this record permanently")

if confirm:
    if st.button("🗑️ Delete Record", type="primary", use_container_width=True):
        try:
            rows = delete_opportunity(engine, selected_id)
            if rows > 0:
                st.success(f"Opportunity ID {selected_id} deleted successfully!")
                st.rerun()
            else:
                st.error("Record not found. It may have already been deleted.")
        except Exception as e:
            st.error(f"Failed to delete opportunity: {e}")
else:
    st.info("Please check the confirmation box to enable deletion.")


