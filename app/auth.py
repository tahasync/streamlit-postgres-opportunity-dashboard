"""Authentication module for the UCP Internship & Job Opportunity Dashboard.

Implements a session-state-based login system with two roles: Admin and Viewer.
"""

import streamlit as st

USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "viewer": {"password": "viewer123", "role": "Viewer"},
}


def login_page():
    """Render a centered login form and authenticate users.

    Stores logged_in, username, and role in st.session_state on success.
    """
    st.markdown(
        "<h1 style='text-align: center;'>🎓 UCP Internship & Job Opportunity Dashboard</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='text-align: center; color: gray;'>Please log in to continue</h3>",
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            username = st.session_state.login_username.strip().lower()
            password = st.session_state.login_password

            if username in USERS and USERS[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = USERS[username]["role"]
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")


def logout():
    """Clear session state to log out the current user."""
    for key in ["logged_in", "username", "role", "engine"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def require_login():
    """Ensure the user is logged in. Shows login_page and stops execution if not."""
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login_page()
        st.stop()


def require_admin():
    """Ensure the current user has Admin role. Shows error and stops if not."""
    if st.session_state.get("role") != "Admin":
        st.error("⛔ Access denied. This action requires Admin privileges.")
        st.stop()


def get_role():
    """Return the current user's role or None if not logged in."""
    return st.session_state.get("role")
