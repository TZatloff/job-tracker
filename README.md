# Job Application Tracker API

A REST API for tracking job applications, built with FastAPI and PostgreSQL.

I built this project to organize my own job search and to practice building a production-style backend. It allows me to
manage companies, track every application from submission to final decision, and keep a history of all status changes.

The project focuses on backend fundamentals such as authentication, request validation, middleware, background tasks,
database relationships, and automated testing.

---

## Features

- CRUD operations for companies and job applications
- Foreign key relationships between companies and applications
- Status workflow (`applied → screening → interview → offer / rejected`)
- Bearer token authentication
- Protected admin endpoints
- Background tasks for audit logging
- Request logging middleware
- CORS configuration for local frontend development
- Input validation with Pydantic
- Consistent API error handling
- Automated tests using pytest and TestClient

---

## Tech Stack

| Layer           | Technology          |
|-----------------|---------------------|
| Framework       | FastAPI             |
| Language        | Python 3            |
| Database        | PostgreSQL 16       |
| Database Driver | psycopg2            |
| Validation      | Pydantic            |
| Testing         | pytest + TestClient |
| Configuration   | python-dotenv       |

---

## Project Structure

job_tracker/
├── main.py # Application setup
├── config.py # Environment configuration
├── database.py # Database connection helper
├── auth.py # Authentication and token verification
├── schemas.py # Pydantic models
├── routers/
│ ├── companies.py
│ ├── applications.py
│ └── admin.py
├── services/
│ └── audit.py # Background audit logging
└── tests/
└── test_api.py---

## Getting Started

### 1. Clone the repository

git clone https://github.com/<your-username>/job_tracker.git
cd job_tracker

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt### 2. Create the database
CREATE TABLE companies (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL UNIQUE,
website TEXT,
created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE applications (
id SERIAL PRIMARY KEY,
company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
position TEXT NOT NULL,
status TEXT NOT NULL DEFAULT 'applied'
CHECK (status IN ('applied','screening','interview','offer','rejected')),
applied_date DATE NOT NULL DEFAULT CURRENT_DATE,
notes TEXT
);

CREATE TABLE audit_log (
id SERIAL PRIMARY KEY,
application_id INTEGER REFERENCES applications(id) ON DELETE SET NULL,
action TEXT NOT NULL,
old_status TEXT,
new_status TEXT,
created_at TIMESTAMP DEFAULT now()
);### 3. Create a .env file
DATABASE_PASSWORD=your_postgres_password
API_TOKEN=your_long_random_token
ADMIN_USER=your_username
ADMIN_PASSWORD=your_password### 4. Run the application
uvicorn main:app --reload---

## API Highlights

- Authentication with Bearer tokens
- CRUD endpoints for companies and applications
- Status updates with audit logging
- Request validation using Pydantic
- Background tasks for non-blocking audit writes
- Middleware for request timing and logging

---

## Testing

Run the test suite with:
pytestThe tests cover:

- Authentication
- Validation errors
- Foreign key constraints
- Duplicate resources
- Common API error responses

---

## Future Improvements

- Docker & Docker Compose
- Alembic migrations
- JWT authentication
- SQLAlchemy
- CI/CD with GitHub Actions
- Deployment to Render or Railway