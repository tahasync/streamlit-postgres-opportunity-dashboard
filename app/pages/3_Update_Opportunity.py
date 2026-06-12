"""Page 3: Update an existing opportunity record.

Admin-only page that loads current values and allows selective updates.
"""

import streamlit as st
from datetime import date

st.set_page_config(page_title="Update Opportunity", page_icon="✏️", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login, require_admin
from db import get_engine
from queries import get_all_opportunities, get_opportunity_by_id, update_opportunity

require_login()
require_admin()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>✏️ Update Opportunity</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

all_opps = get_all_opportunities(engine)

if all_opps.empty:
    st.info("No opportunities available to update.")
    st.stop()

opp_options = {
    f"ID {row['opportunity_id']} — {row['company_name']} — {row['job_title']}": row["opportunity_id"]
    for _, row in all_opps.iterrows()
}

selected_label = st.selectbox("Select Opportunity to Update", list(opp_options.keys()))
selected_id = opp_options[selected_label]

with st.expander("📄 Current Record Details", expanded=True):
    current = get_opportunity_by_id(engine, selected_id)
    if not current.empty:
        st.dataframe(current, use_container_width=True, hide_index=True)

st.divider()
st.subheader("Update Fields")

with st.form("update_opportunity_form"):
    col1, col2 = st.columns(2)

    with col1:
        new_status = st.selectbox(
            "Status",
            ["Open", "Closed", "Expired", "Shortlisted"],
            index=["Open", "Closed", "Expired", "Shortlisted"].index(
                current.iloc[0]["status"] if not current.empty else "Open"
            ),
        )
        new_work_mode = st.selectbox(
            "Work Mode",
            ["Remote", "Onsite", "Hybrid"],
            index=["Remote", "Onsite", "Hybrid"].index(
                current.iloc[0]["work_mode"] if not current.empty else "Onsite"
            ),
        )
        new_city = st.text_input(
            "City",
            value=current.iloc[0]["city"] if not current.empty else "",
        )
        new_experience_level = st.selectbox(
            "Experience Level",
            ["Fresher", "1-2 Years", "3-5 Years", "Senior"],
            index=["Fresher", "1-2 Years", "3-5 Years", "Senior"].index(
                current.iloc[0]["experience_level"] if not current.empty else "Fresher"
            ),
        )

    with col2:
        new_salary_min = st.number_input(
            "Salary Min",
            min_value=0.0,
            value=float(current.iloc[0]["salary_min"]) if not current.empty and current.iloc[0]["salary_min"] else 0.0,
            step=10000.0,
            format="%.2f",
        )
        new_salary_max = st.number_input(
            "Salary Max",
            min_value=0.0,
            value=float(current.iloc[0]["salary_max"]) if not current.empty and current.iloc[0]["salary_max"] else 0.0,
            step=10000.0,
            format="%.2f",
        )
        new_skills = st.text_area(
            "Required Skills",
            value=current.iloc[0]["required_skills"] if not current.empty else "",
        )
        new_deadline = st.date_input(
            "Application Deadline",
            value=(
                current.iloc[0]["application_deadline"]
                if not current.empty and current.iloc[0]["application_deadline"]
                else date.today()
            ),
        )

    submitted = st.form_submit_button("Update Opportunity", use_container_width=True)

    if submitted:
        updates = {
            "status": new_status,
            "work_mode": new_work_mode,
            "city": new_city.strip(),
            "experience_level": new_experience_level,
            "salary_min": new_salary_min if new_salary_min > 0 else None,
            "salary_max": new_salary_max if new_salary_max > 0 else None,
            "required_skills": new_skills.strip(),
            "application_deadline": new_deadline,
        }
        try:
            rows = update_opportunity(engine, selected_id, updates)
            if rows > 0:
                st.success(f"Opportunity ID {selected_id} updated successfully!")
            else:
                st.warning("No changes were made.")
        except Exception as e:
            st.error(f"Failed to update opportunity: {e}")


