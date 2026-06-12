"""Page 1: Add a new internship or job opportunity.

Admin-only page with a comprehensive form including duplicate checking.
"""

import streamlit as st
from datetime import date

st.set_page_config(page_title="Add Opportunity", page_icon="📝", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login, require_admin
from db import get_engine
from queries import insert_opportunity, search_opportunities
from utils import validate_opportunity_form

require_login()
require_admin()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>📝 Add New Opportunity</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

with st.form("add_opportunity_form"):
    st.subheader("Opportunity Details")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input("Company Name *", placeholder="e.g. Systems Limited")
        job_title = st.text_input("Job Title *", placeholder="e.g. Data Analyst")
        category = st.selectbox(
            "Category *",
            ["Data Science", "AI/ML", "Web Development", "Cyber Security", "Software Engineering"],
        )
        city = st.text_input("City", placeholder="e.g. Lahore")
        country = st.text_input("Country", placeholder="e.g. Pakistan")
        work_mode = st.selectbox("Work Mode", ["Onsite", "Remote", "Hybrid"])
        experience_level = st.selectbox(
            "Experience Level", ["Fresher", "1-2 Years", "3-5 Years", "Senior"]
        )

    with col2:
        currency = st.selectbox("Currency", ["PKR", "USD", "EUR"])
        salary_min = st.number_input("Salary Min", min_value=0.0, step=10000.0, format="%.2f")
        salary_max = st.number_input("Salary Max", min_value=0.0, step=10000.0, format="%.2f")
        status = st.selectbox("Status", ["Open", "Closed", "Expired", "Shortlisted"])
        application_deadline = st.date_input(
            "Application Deadline", value=date.today()
        )
        source_link = st.text_input("Source Link (URL)", placeholder="https://...")

    required_skills = st.text_area(
        "Required Skills * (comma-separated)",
        placeholder="e.g. Python, SQL, Tableau, Excel",
    )

    submitted = st.form_submit_button("Add Opportunity", use_container_width=True)

    if submitted:
        data = {
            "company_name": company_name.strip(),
            "job_title": job_title.strip(),
            "category": category,
            "city": city.strip(),
            "country": country.strip(),
            "work_mode": work_mode,
            "required_skills": required_skills.strip(),
            "salary_min": salary_min if salary_min > 0 else None,
            "salary_max": salary_max if salary_max > 0 else None,
            "currency": currency,
            "experience_level": experience_level,
            "application_deadline": application_deadline,
            "status": status,
            "source_link": source_link.strip(),
        }

        is_valid, error_msg = validate_opportunity_form(data)
        if not is_valid:
            st.error(error_msg)
        else:
            try:
                existing = search_opportunities(
                    engine,
                    company_name=company_name.strip(),
                    city=city.strip(),
                )
                if not existing.empty:
                    match = existing[
                        existing["job_title"].str.lower() == job_title.strip().lower()
                    ]
                    if not match.empty:
                        st.warning(
                            "⚠️ A similar record already exists: "
                            f"**{company_name} - {job_title} - {city}**. "
                            "You can still add this record if it is distinct."
                        )

                new_id = insert_opportunity(engine, data)
                st.success(f"Opportunity added successfully! ID: {new_id}")
            except Exception as e:
                st.error(f"Failed to add opportunity: {e}")


