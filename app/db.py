"""Database connection module for the UCP Internship & Job Opportunity Dashboard.

Uses SQLAlchemy with connection pooling to connect to PostgreSQL.
Provides cached engine instance and raw psycopg2 connection fallback.
"""

import os
from contextlib import contextmanager

import streamlit as st
import psycopg2
from sqlalchemy import create_engine, text


@st.cache_resource
def get_engine():
    """Create and return a SQLAlchemy engine with connection pooling.

    Uses st.cache_resource so the engine is reused across Streamlit reruns.
    Reads connection parameters from environment variables with sensible defaults.
    """
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "student_opportunities_db")
    db_user = os.environ.get("DB_USER", "app_user")
    db_password = os.environ.get("DB_PASSWORD", "app_password")

    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    try:
        engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True,
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        raise ConnectionError(
            f"Failed to connect to PostgreSQL at {db_host}:{db_port}/{db_name}. "
            f"Error: {e}. Please ensure the Docker container is running."
        ) from e


@contextmanager
def get_connection():
    """Context manager that yields a raw psycopg2 connection as a fallback.

    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
    """
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "student_opportunities_db")
    db_user = os.environ.get("DB_USER", "app_user")
    db_password = os.environ.get("DB_PASSWORD", "app_password")

    conn = None
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_password,
        )
        yield conn
    except Exception as e:
        raise ConnectionError(
            f"Raw connection failed: {e}"
        ) from e
    finally:
        if conn is not None:
            conn.close()


def test_connection():
    """Test the database connection and return status and version info.

    Returns:
        tuple: (True, version_string) on success, (False, error_message) on failure.
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            return True, version
    except Exception as e:
        return False, str(e)
