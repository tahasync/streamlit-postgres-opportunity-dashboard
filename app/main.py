"""Main entry point and Home page for the UCP Internship & Job Opportunity Dashboard.

Initializes the database engine, calls require_login(), and displays the
beautified Home page with team info, architecture, app guide, and theme toggle.
"""

import streamlit as st

st.set_page_config(
    page_title="UCP Internship & Job Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from auth import require_login, logout, get_role
from db import get_engine
from theme import init_theme, inject_theme_css, toggle_theme

init_theme()
inject_theme_css()

require_login()

if "engine" not in st.session_state:
    with st.spinner("Connecting to database..."):
        try:
            st.session_state["engine"] = get_engine()
        except Exception as e:
            st.error(f"Database connection failed: {e}")
            st.stop()

st.markdown(
    """
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 2.8rem; margin-bottom: 0.3rem;
            background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;'>
            🎓 UCP Internship & Job Opportunity Dashboard
        </h1>
        <p style='font-size: 1.2rem; color: var(--text-secondary); margin-top: 0;'>
            University of Central Punjab — Tools & Techniques for DS
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        """
        <div style='background: var(--bg-card); border-radius: var(--radius);
            padding: 2rem; box-shadow: var(--shadow); border: 1px solid var(--border);
            text-align: center;'>
            <h3>📋 Welcome to the Dashboard</h3>
            <p style='color: var(--text-secondary);'>
            Manage internship and job opportunities for UCP students with full CRUD
            operations, advanced analytics, CSV import/export, duplicate detection,
            deadline alerts, and database health monitoring — all in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown(
        """
        <div style='background: var(--bg-card); border-radius: var(--radius);
            padding: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border);
            text-align: center; height: 100%;'>
            <h2>👥</h2>
            <h4>Team Members</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    for name in ["Muhammad Taha", "Abdur Rehman", "Adil Hayat Khan"]:
        st.markdown(
            f"<div style='background: var(--bg-card); border-radius: 8px; "
            f"padding: 0.6rem 1rem; margin: 0.3rem 0; "
            f"box-shadow: var(--shadow); border: 1px solid var(--border);'>"
            f"<strong>{name}</strong></div>",
            unsafe_allow_html=True,
        )

with t2:
    st.markdown(
        """
        <div style='background: var(--bg-card); border-radius: var(--radius);
            padding: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border);
            text-align: center;'>
            <h2>🛠️</h2>
            <h4>Tools Used</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    tools = [
        ("Python 3.11", "Core language"),
        ("Streamlit", "Web framework"),
        ("PostgreSQL", "Database"),
        ("SQLAlchemy", "ORM"),
        ("Plotly", "Charts"),
        ("Pandas", "Data analysis"),
        ("Docker Compose", "Container orchestration"),
        ("pgAdmin", "DB admin"),
    ]
    for tool, desc in tools:
        st.markdown(
            f"<div style='background: var(--bg-card); border-radius: 8px; "
            f"padding: 0.4rem 1rem; margin: 0.2rem 0; font-size: 0.9rem; "
            f"box-shadow: var(--shadow); border: 1px solid var(--border);'>"
            f"<strong>{tool}</strong> — {desc}</div>",
            unsafe_allow_html=True,
        )

with t3:
    st.markdown(
        """
        <div style='background: var(--bg-card); border-radius: var(--radius);
            padding: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border);
            text-align: center;'>
            <h2>🏗️</h2>
            <h4>Architecture</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(
        "**Three-tier Setup:** PostgreSQL (5432) ← pgAdmin (5050) / Streamlit (8501)"
        "\n\nAll services communicate via Docker's internal network using service names."
    )

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown(
    """
    <div style='background: var(--bg-card); border-radius: var(--radius);
        padding: 1.5rem; box-shadow: var(--shadow); border: 1px solid var(--border);'>
        <h3 style='margin-top: 0;'>📖 App Guide</h3>
    </div>
    """,
    unsafe_allow_html=True,
)
pages_guide = [
    ("📝 Add Opportunity", "Insert new internship/job records (Admin only)"),
    ("🔍 View & Search", "Browse and filter opportunities with CSV export"),
    ("✏️ Update Opportunity", "Modify existing records (Admin only)"),
    ("🗑️ Delete Opportunity", "Remove records with confirmation (Admin only)"),
    ("📊 Analytics Dashboard", "Visual KPIs and interactive charts"),
    ("📂 CSV Upload & Export", "Bulk import and filtered data export"),
    ("🔁 Duplicate Detection", "Identify and review duplicate records"),
    ("⏰ Deadline Alerts", "Track closing soon and expired listings"),
    ("🩺 Database Health Check", "Connection testing and schema info"),
]
cols = st.columns(3)
for i, (page, desc) in enumerate(pages_guide):
    with cols[i % 3]:
        st.markdown(
            f"<div style='background: var(--bg-card); border-radius: 8px; "
            f"padding: 0.7rem 1rem; margin: 0.4rem 0; "
            f"box-shadow: var(--shadow); border: 1px solid var(--border);"
            f"border-left: 3px solid var(--accent);'>"
            f"<strong>{page}</strong><br><span style='font-size: 0.85rem; "
            f"color: var(--text-secondary);'>{desc}</span></div>",
            unsafe_allow_html=True,
        )

sidebar = st.sidebar
sidebar.markdown(
    f"<div style='background: var(--bg-card); border-radius: 8px; padding: 0.8rem; "
    f"box-shadow: var(--shadow); border: 1px solid var(--border); text-align: center;'>"
    f"<h4>🎓 UCP Dashboard</h4>"
    f"<p style='font-size: 0.85rem; color: var(--text-secondary);'>"
    f"👤 {st.session_state.get('username', 'Unknown')} | "
    f"🔑 {get_role()}</p></div>",
    unsafe_allow_html=True,
)
sidebar.divider()
sidebar.markdown("### 📌 Navigation")
sidebar.markdown("Select a page from the sidebar menu above.")
theme_col, logout_col = sidebar.columns(2)
current = st.session_state.get("theme", "dark")
icon = "☀️" if current == "dark" else "🌙"
label = " Light" if current == "dark" else " Dark"
if theme_col.button(f"{icon}{label}", key="sidebar_theme_toggle", use_container_width=True):
    toggle_theme()
if logout_col.button("🚪 Logout", use_container_width=True):
    logout()
