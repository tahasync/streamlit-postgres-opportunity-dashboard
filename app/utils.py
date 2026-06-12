"""Utility functions for the UCP Internship & Job Opportunity Dashboard.

Provides validation, formatting, parsing, and data transformation helpers.
"""

import io
from datetime import datetime, date

import pandas as pd
import streamlit as st


def validate_opportunity_form(data_dict):
    """Validate opportunity form data.

    Args:
        data_dict: dict with form field values

    Returns:
        tuple: (True, None) if valid, (False, error_message_string) if invalid
    """
    if not data_dict.get("company_name") or not data_dict["company_name"].strip():
        return False, "Company name is required."
    if not data_dict.get("job_title") or not data_dict["job_title"].strip():
        return False, "Job title is required."
    if not data_dict.get("category"):
        return False, "Category is required."
    if not data_dict.get("required_skills") or not data_dict["required_skills"].strip():
        return False, "Required skills are required."
    valid_statuses = ["Open", "Closed", "Expired", "Shortlisted"]
    if data_dict.get("status") not in valid_statuses:
        return False, f"Status must be one of: {', '.join(valid_statuses)}"
    valid_modes = ["Remote", "Onsite", "Hybrid"]
    if data_dict.get("work_mode") and data_dict["work_mode"] not in valid_modes:
        return False, f"Work mode must be one of: {', '.join(valid_modes)}"
    s_min = data_dict.get("salary_min")
    s_max = data_dict.get("salary_max")
    if s_min is not None and s_max is not None:
        try:
            if float(s_min) > float(s_max):
                return False, "Salary minimum cannot exceed salary maximum."
        except (ValueError, TypeError):
            return False, "Invalid salary values."
    return True, None


def format_currency(amount, currency="PKR"):
    """Format a number as a currency string.

    Args:
        amount: numeric value
        currency: currency code (PKR, USD, EUR)

    Returns:
        str: Formatted currency string, e.g. "PKR 50,000"
    """
    if amount is None:
        return f"{currency} 0"
    try:
        formatted = f"{float(amount):,.0f}"
        return f"{currency} {formatted}"
    except (ValueError, TypeError):
        return f"{currency} 0"


def days_until_deadline(deadline_date):
    """Calculate the number of days until a deadline.

    Args:
        deadline_date: a date or datetime object (or string)

    Returns:
        int: days remaining (negative if past, 0 if today)
    """
    if deadline_date is None:
        return None
    if isinstance(deadline_date, str):
        try:
            deadline_date = datetime.strptime(deadline_date, "%Y-%m-%d").date()
        except ValueError:
            return None
    if isinstance(deadline_date, datetime):
        deadline_date = deadline_date.date()

    today = date.today()
    delta = deadline_date - today
    return delta.days


def parse_skills_list(skills_string):
    """Split a comma-separated skills string into a cleaned list.

    Args:
        skills_string: comma-separated string of skills

    Returns:
        list: cleaned skill names
    """
    if not skills_string or not skills_string.strip():
        return []
    return [skill.strip() for skill in skills_string.split(",") if skill.strip()]


def dataframe_to_csv_bytes(df):
    """Convert a DataFrame to CSV bytes for download.

    Returns:
        bytes: UTF-8 encoded CSV
    """
    return df.to_csv(index=False).encode("utf-8")


def get_status_color(status):
    """Return a hex color string for a given opportunity status.

    Args:
        status: string status value

    Returns:
        str: hex color code
    """
    color_map = {
        "Open": "#28a745",
        "Closed": "#dc3545",
        "Expired": "#6c757d",
        "Shortlisted": "#007bff",
    }
    return color_map.get(status, "#000000")


def sanitize_csv_upload(df):
    """Validate and clean a DataFrame uploaded from CSV.

    Checks that all required columns are present, renames if close match found.

    Args:
        df: pandas DataFrame from uploaded CSV

    Returns:
        tuple: (cleaned_df, warnings_list)
    """
    required_columns = [
        "company_name", "job_title", "category", "city", "country",
        "work_mode", "required_skills", "salary_min", "salary_max",
        "currency", "experience_level", "application_deadline", "status", "source_link"
    ]
    warnings = []
    column_mapping = {}

    for col in df.columns:
        col_lower = col.strip().lower().replace(" ", "_")
        if col_lower in required_columns:
            if col != col_lower:
                column_mapping[col] = col_lower
                warnings.append(f"Renamed column '{col}' to '{col_lower}'")
        elif col_lower not in required_columns:
            warnings.append(f"Unexpected column '{col}' will be ignored")

    df = df.rename(columns=column_mapping)
    missing = [c for c in required_columns if c not in df.columns]
    if missing:
        warnings.append(f"Missing columns: {', '.join(missing)}")
        for col in missing:
            df[col] = None

    return df, warnings
