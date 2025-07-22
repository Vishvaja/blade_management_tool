# 🌀 Blade Management Tool – Full Stack Case Study

A full-stack blade health monitoring platform built for wind farm operations. This project ingests raw CSV data, cleans and stores it in a relational database, exposes clean REST APIs via FastAPI, and provides a maintainable backend structure for CRUD operations, dashboard insights, and technician assignments.

---

## 📁 Folder Structure

```
.
├── app/                      # FastAPI application
│   ├── crud/                # DB operations
│   ├── data/                # Raw + cleaned CSVs
│   ├── models/              # SQLAlchemy ORM models
│   ├── routers/             # API route handlers
│   ├── schemas/             # Pydantic request/response models
│   ├── utils/               # Helpers (ETL, validators, etc.)
│   ├── database.py          # DB session and engine
│   └── main.py              # FastAPI entry point
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
├── run_etl.py               # Data cleaning and ingestion
├── reset_db.py              # Drop and recreate tables
├── display_table.py         # View table contents
├── delete.py                # Delete records
└── README.md
```

---

## 🔧 Features

- **ETL Pipeline**: `run_etl.py` cleans & ingests raw CSVs into PostgreSQL
- **Modular FastAPI Backend**: routers, models, and schemas separated for maintainability
- **RESTful Endpoints**:
  - `/sites`, `/turbines`, `/blades`, `/maintenance`
  - Relationship routes (e.g., `/sites/{site_id}/turbines`)
  - POST/PUT routes for adding/updating blades and maintenance
- **Validation & Error Handling**: Checks for foreign key integrity and input formatting
- **Dockerized Setup**: Run everything with one `docker-compose up` command

---

## 🚀 Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/Vishvaja/blade_management_tool.git
cd blade_management_tool
cp .env.example .env   # Add DB credentials
```

### 2. Start Services
```bash
docker-compose up --build
```

### 3. Run ETL Script
```bash
docker exec -it blade_app python run_etl.py
```

---

## 🛠 Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL (via Docker), validated via Python scripts
- **Deployment**: Docker, Docker Compose
- **Tools**: VS Code, Postman, dotenv

---

## 🧪 API Highlights

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sites` | GET | List all sites |
| `/sites/{site_id}/turbines` | GET | Turbines by site |
| `/turbines/{turbine_id}/blades` | GET | Blades by turbine |
| `/blades/{blade_id}/maintenance` | GET | Maintenance records for blade |
| `/blades` | POST | Add a new blade |
| `/maintenance` | POST | Log a new maintenance event |

All endpoints return JSON responses and include input validation and error handling.

---

## 📌 Assumptions

- CSVs contain duplicate IDs, inconsistent casing, and missing fields
- All input is cleaned and normalized before DB insert
- Blade length and type are editable; maintenance updates include technician/status/issue
- Blades with 3+ recent issues or repeated problems are flagged for review

---

## 📣 GitHub Description Paragraph

> A Dockerized full-stack backend for blade health management in wind farms. Ingests raw CSV data, normalizes it, and exposes clean RESTful APIs using FastAPI. Modular structure (CRUD/models/schemas/routers), PostgreSQL DB, and validation-ready endpoints for real-world turbine and maintenance tracking. Ideal for operations teams managing distributed wind energy assets.
