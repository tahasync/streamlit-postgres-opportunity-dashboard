"""Page 5: Analytics dashboard with KPIs and interactive Plotly charts.

Displays summary metrics and distribution visualizations for all opportunities.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login
from db import get_engine
from queries import (
    get_analytics_summary,
    get_category_distribution,
    get_city_distribution,
    get_work_mode_distribution,
    get_status_distribution,
    get_salary_by_category,
    get_top_companies,
    get_skills_frequency,
)

require_login()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>📊 Analytics Dashboard</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

col_refresh = st.columns([4, 1])
with col_refresh[1]:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()


@st.cache_data(ttl=120)
def load_analytics_data(_engine):
    summary = get_analytics_summary(_engine)
    category_dist = get_category_distribution(_engine)
    city_dist = get_city_distribution(_engine)
    work_mode_dist = get_work_mode_distribution(_engine)
    status_dist = get_status_distribution(_engine)
    salary_by_cat = get_salary_by_category(_engine)
    top_companies = get_top_companies(_engine)
    skills_freq = get_skills_frequency(_engine)
    return summary, category_dist, city_dist, work_mode_dist, status_dist, salary_by_cat, top_companies, skills_freq


with st.spinner("Loading analytics..."):
    (summary, category_dist, city_dist, work_mode_dist,
     status_dist, salary_by_cat, top_companies, skills_freq) = load_analytics_data(engine)

st.markdown("### 📈 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1:
    st.metric("Total", summary["total_count"])
with kpi2:
    st.metric("Open", summary["open_count"])
with kpi3:
    st.metric("Closed", summary["closed_count"])
with kpi4:
    st.metric("Expired", summary["expired_count"])
with kpi5:
    st.metric("Shortlisted", summary["shortlisted_count"])
with kpi6:
    st.metric("Avg Salary Min", f"PKR {summary['avg_salary_min']:,.0f}")

st.markdown("---")
st.markdown("### 📊 Distributions")

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig_pie = px.pie(
        category_dist,
        names="category",
        values="count",
        title="Category Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_pie, use_container_width=True)

with row2_col2:
    fig_city = px.bar(
        city_dist,
        x="count",
        y="city",
        title="City Distribution",
        orientation="h",
        color="count",
        color_continuous_scale="Blues",
    )
    fig_city.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_city, use_container_width=True)

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    fig_workmode = px.pie(
        work_mode_dist,
        names="work_mode",
        values="count",
        title="Work Mode Distribution",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig_workmode.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig_workmode, use_container_width=True)

with row3_col2:
    fig_status = px.bar(
        status_dist,
        x="status",
        y="count",
        title="Status Distribution",
        color="status",
        color_discrete_map={
            "Open": "#28a745",
            "Closed": "#dc3545",
            "Expired": "#6c757d",
            "Shortlisted": "#007bff",
        },
    )
    st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")
st.markdown("### 💰 Salary Analysis")

fig_salary = go.Figure()
fig_salary.add_trace(go.Bar(
    x=salary_by_cat["category"],
    y=salary_by_cat["avg_salary_min"],
    name="Avg Salary Min",
    marker_color="#007bff",
))
fig_salary.add_trace(go.Bar(
    x=salary_by_cat["category"],
    y=salary_by_cat["avg_salary_max"],
    name="Avg Salary Max",
    marker_color="#28a745",
))
fig_salary.update_layout(
    title="Average Salary Range by Category",
    xaxis_title="Category",
    yaxis_title="Avg Salary (PKR)",
    barmode="group",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)
st.plotly_chart(fig_salary, use_container_width=True)

st.markdown("---")
st.markdown("### 🏢 Companies & Skills")

row5_col1, row5_col2 = st.columns(2)

with row5_col1:
    top10 = top_companies.head(10)
    fig_companies = px.bar(
        top10,
        x="count",
        y="company_name",
        title="Top 10 Companies by Listing Count",
        orientation="h",
        color="count",
        color_continuous_scale="Viridis",
    )
    fig_companies.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_companies, use_container_width=True)

with row5_col2:
    top_skills = skills_freq.head(15)
    if not top_skills.empty and top_skills.columns[0] != "skill":
        top_skills.columns = ["skill", "count"]
    top_skills = top_skills.head(15)
    fig_skills = px.bar(
        top_skills,
        x="count",
        y="skill",
        title="Top 15 Most Required Skills",
        orientation="h",
        color="count",
        color_continuous_scale="Plasma",
    )
    fig_skills.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_skills, use_container_width=True)


