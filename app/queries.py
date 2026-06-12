"""SQL query functions for the UCP Internship & Job Opportunity Dashboard.

All functions accept a SQLAlchemy engine and return pandas DataFrames or scalars.
"""

import pandas as pd
from sqlalchemy import text


def get_all_opportunities(engine):
    """Return all opportunities ordered by created_at descending."""
    query = "SELECT * FROM opportunities ORDER BY created_at DESC"
    return pd.read_sql(query, engine)


def get_opportunity_by_id(engine, opp_id):
    """Return a single opportunity row as a DataFrame by its ID."""
    query = "SELECT * FROM opportunities WHERE opportunity_id = %(id)s"
    return pd.read_sql(query, engine, params={"id": opp_id})


def insert_opportunity(engine, data_dict):
    """Insert a new opportunity record and return the new opportunity_id.

    Args:
        engine: SQLAlchemy engine
        data_dict: dict with keys matching column names

    Returns:
        int: The newly created opportunity_id
    """
    columns = list(data_dict.keys())
    placeholders = [f":{col}" for col in columns]
    sql = f"""
        INSERT INTO opportunities ({', '.join(columns)})
        VALUES ({', '.join(placeholders)})
        RETURNING opportunity_id
    """
    with engine.connect() as conn:
        result = conn.execute(text(sql), data_dict)
        conn.commit()
        row = result.fetchone()
        return row[0]


def update_opportunity(engine, opp_id, updates_dict):
    """Update specified columns for an opportunity record.

    Args:
        engine: SQLAlchemy engine
        opp_id: ID of the record to update
        updates_dict: dict of column -> new value

    Returns:
        int: number of rows affected
    """
    set_clause = ", ".join([f"{col} = :{col}" for col in updates_dict])
    sql = f"UPDATE opportunities SET {set_clause} WHERE opportunity_id = :opportunity_id"
    params = {**updates_dict, "opportunity_id": opp_id}
    with engine.connect() as conn:
        result = conn.execute(text(sql), params)
        conn.commit()
        return result.rowcount


def delete_opportunity(engine, opp_id):
    """Delete an opportunity record by its ID.

    Returns:
        int: number of rows deleted
    """
    sql = "DELETE FROM opportunities WHERE opportunity_id = :id"
    with engine.connect() as conn:
        result = conn.execute(text(sql), {"id": opp_id})
        conn.commit()
        return result.rowcount


def search_opportunities(
    engine,
    keyword=None,
    company_name=None,
    category=None,
    city=None,
    work_mode=None,
    status=None,
    salary_min=None,
    salary_max=None,
    experience_level=None,
):
    """Search opportunities with optional filters.

    All filter parameters are optional. Only non-None/non-empty filters
    are applied to the SQL query.

    Returns:
        DataFrame of filtered results
    """
    conditions = []
    params = {}

    if keyword:
        conditions.append(
            "(company_name ILIKE %(keyword)s OR job_title ILIKE %(keyword)s "
            "OR required_skills ILIKE %(keyword)s)"
        )
        params["keyword"] = f"%{keyword}%"

    if company_name:
        conditions.append("company_name ILIKE %(company_name)s")
        params["company_name"] = f"%{company_name}%"

    if category:
        conditions.append("category = ANY(%(category)s)")
        params["category"] = category if isinstance(category, list) else [category]

    if city:
        conditions.append("city = ANY(%(city)s)")
        params["city"] = city if isinstance(city, list) else [city]

    if work_mode:
        conditions.append("work_mode = ANY(%(work_mode)s)")
        params["work_mode"] = work_mode if isinstance(work_mode, list) else [work_mode]

    if status:
        conditions.append("status = ANY(%(status)s)")
        params["status"] = status if isinstance(status, list) else [status]

    if salary_min is not None:
        conditions.append("salary_max >= %(salary_min)s")
        params["salary_min"] = salary_min

    if salary_max is not None:
        conditions.append("salary_min <= %(salary_max)s")
        params["salary_max"] = salary_max

    if experience_level:
        conditions.append("experience_level = ANY(%(experience_level)s)")
        params["experience_level"] = experience_level if isinstance(experience_level, list) else [experience_level]

    where_clause = " AND ".join(conditions) if conditions else "TRUE"
    query = f"SELECT * FROM opportunities WHERE {where_clause} ORDER BY created_at DESC"
    return pd.read_sql(query, engine, params=params)


def get_analytics_summary(engine):
    """Return a dictionary of aggregate analytics counts and averages."""
    query = """
        SELECT
            COUNT(*) AS total_count,
            COUNT(*) FILTER (WHERE status = 'Open') AS open_count,
            COUNT(*) FILTER (WHERE status = 'Closed') AS closed_count,
            COUNT(*) FILTER (WHERE status = 'Expired') AS expired_count,
            COUNT(*) FILTER (WHERE status = 'Shortlisted') AS shortlisted_count,
            COALESCE(AVG(salary_min), 0) AS avg_salary_min,
            COALESCE(AVG(salary_max), 0) AS avg_salary_max
        FROM opportunities
    """
    row = pd.read_sql(query, engine).iloc[0]
    return {
        "total_count": int(row["total_count"]),
        "open_count": int(row["open_count"]),
        "closed_count": int(row["closed_count"]),
        "expired_count": int(row["expired_count"]),
        "shortlisted_count": int(row["shortlisted_count"]),
        "avg_salary_min": float(row["avg_salary_min"]),
        "avg_salary_max": float(row["avg_salary_max"]),
    }


def get_category_distribution(engine):
    """Return DataFrame with category and count of opportunities."""
    query = """
        SELECT category, COUNT(*) AS count
        FROM opportunities
        GROUP BY category
        ORDER BY count DESC
    """
    return pd.read_sql(query, engine)


def get_city_distribution(engine):
    """Return DataFrame with city and count of opportunities."""
    query = """
        SELECT city, COUNT(*) AS count
        FROM opportunities
        GROUP BY city
        ORDER BY count DESC
    """
    return pd.read_sql(query, engine)


def get_work_mode_distribution(engine):
    """Return DataFrame with work_mode and count of opportunities."""
    query = """
        SELECT work_mode, COUNT(*) AS count
        FROM opportunities
        GROUP BY work_mode
        ORDER BY count DESC
    """
    return pd.read_sql(query, engine)


def get_status_distribution(engine):
    """Return DataFrame with status and count of opportunities."""
    query = """
        SELECT status, COUNT(*) AS count
        FROM opportunities
        GROUP BY status
        ORDER BY count DESC
    """
    return pd.read_sql(query, engine)


def get_salary_by_category(engine):
    """Return DataFrame with category, avg_salary_min, avg_salary_max."""
    query = """
        SELECT category,
               COALESCE(AVG(salary_min), 0) AS avg_salary_min,
               COALESCE(AVG(salary_max), 0) AS avg_salary_max
        FROM opportunities
        GROUP BY category
        ORDER BY category
    """
    return pd.read_sql(query, engine)


def get_top_companies(engine):
    """Return DataFrame with company_name and count, ordered descending."""
    query = """
        SELECT company_name, COUNT(*) AS count
        FROM opportunities
        GROUP BY company_name
        ORDER BY count DESC
    """
    return pd.read_sql(query, engine)


def get_skills_frequency(engine):
    """Return DataFrame with skill and count parsed from required_skills.

    Splits the required_skills column by comma, strips whitespace, and counts
    occurrences of each skill across all records.
    """
    query = "SELECT required_skills FROM opportunities"
    df = pd.read_sql(query, engine)
    skills_series = df["required_skills"].str.split(",").explode().str.strip()
    skills_series = skills_series[skills_series != ""]
    result = skills_series.value_counts().reset_index()
    result.columns = ["skill", "count"]
    return result


def get_deadline_alerts(engine):
    """Return DataFrame of opportunities with deadline within the next 7 days."""
    query = """
        SELECT *
        FROM opportunities
        WHERE application_deadline BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
        ORDER BY application_deadline ASC
    """
    return pd.read_sql(query, engine)


def get_expired_opportunities(engine):
    """Return DataFrame of opportunities where deadline has passed and status is not Closed."""
    query = """
        SELECT *
        FROM opportunities
        WHERE application_deadline < CURRENT_DATE
          AND status != 'Closed'
        ORDER BY application_deadline DESC
    """
    return pd.read_sql(query, engine)


def detect_duplicates(engine):
    """Return DataFrame of duplicate groups based on company_name + job_title + city.

    Only returns records where the combination appears more than once.
    """
    query = """
        WITH duplicate_groups AS (
            SELECT company_name, job_title, city,
                   COUNT(*) AS duplicate_count
            FROM opportunities
            GROUP BY company_name, job_title, city
            HAVING COUNT(*) > 1
        )
        SELECT o.*, dg.duplicate_count
        FROM opportunities o
        INNER JOIN duplicate_groups dg
            ON o.company_name = dg.company_name
            AND o.job_title = dg.job_title
            AND o.city = dg.city
        ORDER BY dg.duplicate_count DESC, o.company_name, o.job_title, o.city
    """
    return pd.read_sql(query, engine)


def bulk_insert_from_dataframe(engine, df):
    """Validate and insert multiple rows from a DataFrame.

    Args:
        engine: SQLAlchemy engine
        df: DataFrame with columns matching the opportunities table

    Returns:
        tuple: (success_count, error_list) where error_list contains
               dicts with row_index and error_message
    """
    expected_columns = [
        "company_name", "job_title", "category", "city", "country",
        "work_mode", "required_skills", "salary_min", "salary_max",
        "currency", "experience_level", "application_deadline", "status", "source_link"
    ]
    success_count = 0
    error_list = []

    for idx, row in df.iterrows():
        try:
            record = {}
            for col in expected_columns:
                val = row.get(col)
                if pd.isna(val):
                    val = None
                record[col] = val

            if not record["company_name"] or not record["job_title"]:
                error_list.append({
                    "row_index": idx,
                    "error_message": "Missing required fields: company_name or job_title"
                })
                continue

            insert_opportunity(engine, record)
            success_count += 1
        except Exception as e:
            error_list.append({
                "row_index": idx,
                "error_message": str(e)
            })

    return success_count, error_list


def get_table_info(engine):
    """Return DataFrame with column metadata from information_schema."""
    query = """
        SELECT
            column_name AS "Column Name",
            data_type AS "Data Type",
            is_nullable AS "Nullable"
        FROM information_schema.columns
        WHERE table_name = 'opportunities'
        ORDER BY ordinal_position
    """
    return pd.read_sql(query, engine)
