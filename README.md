# Notification Challenge API

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/CWmkDVcqPMWbHCRX9eAqhf/KnkpvY4fatgoPVuuFtHwf3/tree/master.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/CWmkDVcqPMWbHCRX9eAqhf/KnkpvY4fatgoPVuuFtHwf3/tree/master)
[![Coverage Status](https://coveralls.io/repos/github/Cainabel1910/notification-challenge/badge.svg?branch=master)](https://coveralls.io/github/Cainabel1910/notification-challenge?branch=master)

FastAPI REST API for user and notification management, with JWT authentication, business validations, and channel-based notification strategies.

## Requirements

- Python 3.11+
- Docker Desktop or Docker Engine
- PostgreSQL configured through Docker Compose
- Git

## Local installation

1. Clone the repository and enter the project directory:

```bash
cd challenge-setup
```

2. Go to the backend folder:

```bash
cd backend
```

3. Create and activate a virtual environment:

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

4. Install the project dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest httpx
```

## Environment configuration

The project uses a `.env` file inside `backend/` with the required variables. You can reuse the default configuration or adjust it to your local environment:

```env
POSTGRES_DB=notification_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/notification_db

PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_NUMBER=true
PASSWORD_REQUIRE_SYMBOL=true

JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30

SMS_MAX_LENGTH=160
```

## Run with Docker Compose

Create `backend/.env` from `backend/.env.example` and set the database credentials and application secrets. Then, from the `backend/` directory, start the database and API:

```bash
docker compose up --build
```

Compose waits for PostgreSQL's healthcheck before starting the API. The API applies Alembic migrations before serving requests and is available at:

- http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Stop the services with `docker compose down`. The PostgreSQL data remains in the `postgres_data` volume.

## Run locally without Docker

```bash
docker compose up -d db
```

Apply migrations:

```bash
alembic upgrade head
```

## Running the backend

Start the API with Uvicorn:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:

- http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running tests

```bash
pytest
```

## Technical decisions

- FastAPI as the main framework to build the REST API with automatic validation and OpenAPI documentation.
- SQLAlchemy + PostgreSQL for persisting users, notifications, and deliveries, with Alembic for sustainable migrations.
- Layered architecture: controllers, services, repositories, and models to separate responsibilities and make maintenance easier.
- Strategy pattern for notification channels (`email`, `sms`, `push`), allowing new delivery methods to be added without changing the core logic.
- JWT-based authentication to protect endpoints and validate user identity.
- Centralized exception handling to return consistent and clearer responses to the client.
- Docker Compose for the API and PostgreSQL, with a database healthcheck that gates API startup.

## Areas for improvement

- Integrate email, SMS, and push providers. The current strategies validate and format notifications, but simulate delivery by printing messages.
- Expand automated test coverage to include authentication, user management, delivery outcomes, and failure scenarios.
- Add retry policies and background processing for transient provider or network failures.
- Improve operational visibility with structured logging, metrics, and delivery status tracking.
- Pin dependency versions and add automated dependency and security checks.

## Diagrams

See [the database and class diagrams](docs/diagrams.md), including the notification Strategy pattern.

## Main structure

```text
backend/
├── app/
│   ├── auth/
│   ├── notifications/
│   ├── security/
│   ├── users/
│   └── main.py
├── core/
├── database/
├── tests/
├── alembic/
├── docker-compose.yml
├── .env
└── alembic.ini
```

## Notes

- The project can run fully in Docker Compose or locally with PostgreSQL in Docker and the API in a Python virtual environment.
- If you change the database credentials, make sure the same values are kept in both `DATABASE_URL` and the Docker Compose configuration.
