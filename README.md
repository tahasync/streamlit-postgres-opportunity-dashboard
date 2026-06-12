# 🎓 UCP Internship & Job Opportunity Dashboard

A Dockerized, multi-page **Streamlit** web application for university faculty to manage internship and job opportunities — with full CRUD, advanced analytics, CSV import/export, duplicate detection, deadline alerts, and database health monitoring — all running on **PostgreSQL** via **Docker Compose**.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-D71F00?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly&logoColor=white)

Built for the **Tools & Techniques for DS** course at **University of Central Punjab (UCP)**, Assignment 4.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
│                                                             │
│  ┌──────────────────┐      ┌──────────────────┐            │
│  │    Streamlit App  │      │     pgAdmin       │            │
│  │   (Port 8501)     │      │    (Port 5050)    │            │
│  └────────┬───────────┘      └────────┬──────────┘            │
│           │                           │                       │
│           └──────────┬────────────────┘                       │
│                      ▼                                       │
│  ┌─────────────────────────────────────────────────┐         │
│  │         PostgreSQL 16 (Port 5432)                │         │
│  │         Volume: postgres_data                    │         │
│  └─────────────────────────────────────────────────┘         │
│                                                             │
│  All services communicate via Docker internal network        │
│  using service names (postgres_db, pgadmin, streamlit_app)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Python 3.11** | Core programming language |
| **Streamlit** | Web application framework |
| **PostgreSQL 16** | Relational database |
| **SQLAlchemy** | ORM & database connectivity |
| **Plotly** | Interactive data visualizations |
| **Pandas** | Data manipulation & analysis |
| **Docker Compose** | Container orchestration |
| **pgAdmin** | Database administration GUI |

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed & running
- Git
- VS Code (recommended)

### Setup

```bash
# Clone the repository
git clone https://github.com/mtahanaeem/streamlit-postgres-opportunity-dashboard.git
cd streamlit-postgres-opportunity-dashboard

# Start all services
docker compose up -d

# Wait ~30s for PostgreSQL to initialize
# Open in browser:
#   Streamlit → http://localhost:8501
#   pgAdmin   → http://localhost:5050
```

### Default Credentials

| Login Type | Username / Email | Password |
|-----------|-----------------|----------|
| Streamlit (Admin) | `admin` | `admin123` |
| Streamlit (Viewer) | `viewer` | `viewer123` |
| pgAdmin | `admin@example.com` | `admin123` |
| PostgreSQL | `app_user` | `app_password` |

---

## 📱 App Pages

| Page | File | Access |
|------|------|--------|
| **📝 Add Opportunity** | `1_Add_Opportunity.py` | Admin |
| **🔍 View & Search** | `2_View_Search.py` | All |
| **✏️ Update Opportunity** | `3_Update_Opportunity.py` | Admin |
| **🗑️ Delete Opportunity** | `4_Delete_Opportunity.py` | Admin |
| **📊 Analytics Dashboard** | `5_Analytics_Dashboard.py` | All |
| **📂 CSV Upload & Export** | `6_CSV_Upload_Export.py` | Upload: Admin / Export: All |
| **🔁 Duplicate Detection** | `7_Duplicate_Detection.py` | All |
| **⏰ Deadline Alerts** | `8_Deadline_Alerts.py` | All |
| **🩺 Database Health Check** | `9_Database_Health_Check.py` | All |

---

## 🐳 Docker Services

| Service | Image | Port | Purpose |
|---------|-------|------|---------|
| `postgres_db` | postgres:16 | 5432 | Relational database |
| `pgadmin` | dpage/pgadmin4:latest | 5050 | Database administration |
| `streamlit_app` | Custom build | 8501 | Streamlit web application |

---

## 📁 Project Structure

```
streamlit-postgres-opportunity-dashboard/
├── app/
│   ├── main.py              # Entry point & Home page
│   ├── db.py                # Database connection module
│   ├── queries.py           # SQL query functions
│   ├── auth.py              # Authentication module
│   ├── utils.py             # Utility functions
│   ├── theme.py             # Light/dark theme manager
│   └── pages/               # 9 Streamlit pages
├── database/
│   ├── init.sql             # Schema definition
│   └── seed_data.sql        # 215 sample records
├── screenshots/             # Screenshots folder
├── docker-compose.yml       # Docker Compose config
├── Dockerfile               # Streamlit app build
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md
```

---

## 🐳 Docker Compose Concepts

| Concept | Description |
|---------|-------------|
| **Service** | Each container defined in `docker-compose.yml` |
| **Image** | Pre-built package (e.g., `postgres:16`) |
| **Build** | Custom image built from `Dockerfile` |
| **Container Name** | Custom name via `container_name` |
| **Ports** | Host-to-container port mapping (`"8501:8501"`) |
| **Environment** | Variables passed to containers |
| **Volumes** | Persistent data (`postgres_data`) & init scripts |
| **depends_on** | Startup order (pgAdmin depends on PostgreSQL) |
| **Restart Policy** | `unless-stopped` for auto-recovery |
| **Network** | Containers communicate via service-named DNS |

---

## 🔗 pgAdmin Connection Guide

1. Open `http://localhost:5050`
2. Login: `admin@example.com` / `admin123`
3. Right-click **Servers** → **Register** → **Server**
4. **General** tab → Name: `Opportunity DB`
5. **Connection** tab:
   - Host: `postgres_db` (not `localhost`)
   - Port: `5432`
   - Database: `student_opportunities_db`
   - Username: `app_user`
   - Password: `app_password`
6. Click **Save**

---

## 📊 Database

The `opportunities` table has **16 columns** with CHECK constraints, defaults, and a SERIAL primary key. The `seed_data.sql` file inserts **215 records** with realistic Pakistani tech industry data — including deliberate duplicates, a mix of statuses, multiple currencies, and deadline dates (past, present, and future).

**6 Required SQL Queries:**

```sql
-- 1. All open opportunities
SELECT * FROM opportunities WHERE status = 'Open' ORDER BY created_at DESC;

-- 2. Count by category
SELECT category, COUNT(*) FROM opportunities GROUP BY category ORDER BY count DESC;

-- 3. Salary > 100,000
SELECT company_name, job_title, salary_min, salary_max, currency
FROM opportunities WHERE salary_min > 100000 OR salary_max > 100000 ORDER BY salary_max DESC;

-- 4. Unique cities
SELECT DISTINCT city FROM opportunities WHERE city IS NOT NULL ORDER BY city;

-- 5. Expiring within 7 days
SELECT company_name, job_title, application_deadline FROM opportunities
WHERE application_deadline BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days'
ORDER BY application_deadline;

-- 6. Duplicate records
SELECT company_name, job_title, city, COUNT(*)
FROM opportunities GROUP BY company_name, job_title, city HAVING COUNT(*) > 1
ORDER BY COUNT(*) DESC;
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change host port in `docker-compose.yml` |
| PostgreSQL connection refused | Wait 30s for init, then restart Streamlit |
| pgAdmin can't connect | Use `postgres_db` (not `localhost`) as host |
| Docker Compose not found | Ensure Docker Desktop is running |
| Table not found | Check `docker compose logs postgres_db` |
| Seed data missing | Run `docker compose down -v && docker compose up -d` |
| Container exits immediately | `docker compose logs streamlit_app` to diagnose |

---

## 👥 Team

- Muhammad Taha
- Abdur Rehman
- Adil Hayat Khan

---

**University of Central Punjab, Lahore** — Tools and Techniques for Data Science — Assignment 4
