"""Page 9: Database health check page for monitoring connection and schema.

Tests database connectivity, shows metadata, and provides diagnostic info.
"""

import os
import streamlit as st

st.set_page_config(page_title="Database Health Check", page_icon="🩺", layout="wide")

from theme import init_theme, inject_theme_css

init_theme()
inject_theme_css()

from auth import require_login
from db import get_engine, test_connection
from queries import get_all_opportunities, get_table_info

require_login()

engine = st.session_state.get("engine") or get_engine()

st.markdown(
    "<h1 style='text-align: center;'>🩺 Database Health Check</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### 🔌 Connection Test")

if st.button("Run Health Check", use_container_width=True):
    st.rerun()

success, result = test_connection()

if success:
    st.success(f"✅ PostgreSQL Connection Successful!")
    st.code(result, language="text")
else:
    st.error(f"❌ Connection Failed: {result}")

st.markdown("---")
st.markdown("### 📊 Database Overview")

with st.spinner("Loading database info..."):
    try:
        all_data = get_all_opportunities(engine)
        st.metric("Total Records in opportunities table", len(all_data))

        if not all_data.empty:
            latest = all_data["created_at"].max()
            st.metric("Latest Record Created At", str(latest)[:19])
        else:
            st.info("No records in the opportunities table.")
    except Exception as e:
        st.error(f"Failed to load database info: {e}")

st.markdown("---")
st.markdown("### 📋 Table Schema")

with st.spinner("Loading schema..."):
    try:
        schema_df = get_table_info(engine)
        st.dataframe(schema_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Failed to load schema: {e}")

st.markdown("---")
st.markdown("### ⚙️ Environment Configuration")

db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", "5432")
db_name = os.environ.get("DB_NAME", "student_opportunities_db")
db_user = os.environ.get("DB_USER", "app_user")

env_info = {
    "DB_HOST": db_host,
    "DB_PORT": db_port,
    "DB_NAME": db_name,
    "DB_USER": db_user,
    "DB_PASSWORD": "******** (hidden)",
}
env_df = st.dataframe(
    [{"Variable": k, "Value": v} for k, v in env_info.items()],
    use_container_width=True,
    hide_index=True,
)

st.info(
    "🔗 Connected to **postgres_db** container via Docker internal network. "
    "The Streamlit app communicates with PostgreSQL using the service name "
    "as the hostname, which Docker DNS resolves automatically."
)


