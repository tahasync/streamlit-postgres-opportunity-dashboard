# UCP Internship & Job Opportunity Dashboard

A Dockerized Streamlit + PostgreSQL web app for University of Central Punjab faculty to manage internship and job opportunities — with full CRUD, analytics, CSV import/export, duplicate detection, deadline alerts, and database health monitoring.

## What it does

Nine Streamlit pages: Add (form with validation + duplicate check), View/Search (filters by type, status, department, deadline), Update (ID-based), Delete (confirmation dialog), Analytics (6 KPIs + 5 Plotly charts), CSV Upload (validation + bulk insert), Duplicate Detection (SQL GROUP BY), Deadline Alerts (BETWEEN query), and Database Health Check (connection test + table info). Auth module supports two roles (admin/viewer) with simple hardcoded credentials. SQLite-like simplicity via PostgreSQL with 16-column schema, CHECK constraints, and 215 seed records. Everything runs via Docker Compose (Streamlit + PostgreSQL 16 + pgAdmin).

## Tech stack

- **App:** Python 3.11, Streamlit, Pandas, Plotly, SQLAlchemy, psycopg2-binary, python-dotenv
- **Database:** PostgreSQL 16
- **Infrastructure:** Docker Compose (3 services: streamlit, postgres_db, pgadmin)

## Setup

```bash
docker compose up --build -d
# Streamlit: http://localhost:8501
# pgAdmin: http://localhost:5050
```

Default credentials: `admin` / `admin123` (viewer: `viewer` / `viewer123`).

## Status

**Complete — academic project.** All 9 pages functional with real SQL queries and Plotly visualizations. Docker Compose orchestration works. Built for UCP faculty use. No automated tests.