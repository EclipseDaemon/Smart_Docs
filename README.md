# SmartDocs — Intelligent Document Processing and Search API

A production-grade async REST API for document ingestion, processing, and full-text search.
Built with FastAPI, PostgreSQL, Redis, and Docker.

---

## Project Overview

SmartDocs allows users to securely upload documents (PDF, Word), automatically extract
and process their content, and perform full-text search across all stored documents.
The system is designed with a clean async architecture and is built to be extended
with AI-powered RAG (Retrieval Augmented Generation) capabilities in future phases.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI (async) |
| Database | PostgreSQL + SQLAlchemy (async) + Alembic |
| Cache | Redis |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose) + bcrypt |
| File Processing | pypdf2, python-docx |
| Logging | structlog |
| Testing | PyTest + pytest-asyncio |
| Containerization | Docker + Docker Compose |

---

## Project Structure
```
smart_docs/
├── app/
│   ├── main.py               # FastAPI app, lifespan, middleware
│   ├── config.py             # Pydantic Settings, env management
│   ├── api/
│   │   ├── dependencies.py   # Shared dependencies (auth, db)
│   │   └── routes/
│   │       ├── auth.py       # Register, login endpoints
│   │       ├── documents.py  # Upload, list, delete endpoints
│   │       └── search.py     # Full-text search endpoints
│   ├── core/
│   │   ├── security.py       # JWT creation and validation
│   │   └── exceptions.py     # Custom exception handlers
│   ├── models/
│   │   ├── user.py           # SQLAlchemy User model
│   │   └── document.py       # SQLAlchemy Document model
│   ├── schemas/
│   │   ├── user.py           # Pydantic user schemas
│   │   └── document.py       # Pydantic document schemas
│   ├── services/
│   │   ├── document_service.py  # Document business logic
│   │   ├── search_service.py    # Search business logic
│   │   └── cache_service.py     # Redis caching logic
│   ├── db/
│   │   ├── base.py           # DeclarativeBase + TimeStampMixin
│   │   └── session.py        # Async engine, session factory, get_db
│   └── utils/
│       └── file_processor.py # PDF and Word text extraction
├── tests/
│   ├── test_auth.py
│   └── test_documents.py
├── docker-compose.yml        # Redis container (see setup notes)
├── Dockerfile                # App containerization
├── requirements.txt
├── .env                      # Local env vars (never commit)
├── .env.example              # Template for env vars
└── README.md
```

---

## Local Development Setup

### Prerequisites

- Python 3.13
- PostgreSQL installed locally
- Docker Desktop (for Redis)
- Git

### Step 1 — Clone and create virtual environment
```bash
git clone https://github.com/EclipseDaemon/smart_docs
cd smart_docs
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` with your local values. See `.env.example` for reference.

### Step 4 — Set up local PostgreSQL

Create the database in your local PostgreSQL:
```bash
psql -U postgres
```
```sql
CREATE USER smartdocs_user WITH PASSWORD 'your_password';
CREATE DATABASE smartdocs_db OWNER smartdocs_user;
GRANT ALL PRIVILEGES ON DATABASE smartdocs_db TO smartdocs_user;
\q
```

### Step 5 — Start Redis via Docker
```bash
docker-compose up -d
```

This starts only Redis. PostgreSQL runs locally (see setup notes below).

### Step 6 — Run the application
```bash
uvicorn app.main:app --reload --port 8000
```

### Step 7 — Verify

- Health check: http://localhost:8000/health
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values.
```env
# Application
APP_NAME=SmartDocs
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-minimum-32-chars

# PostgreSQL (local installation)
POSTGRES_USER=smartdocs_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=smartdocs_db
DATABASE_URL=postgresql+asyncpg://smartdocs_user:your_password@localhost:5432/smartdocs_db

# Redis (Docker)
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
MAX_FILE_SIZE_MB=10
UPLOAD_DIR=uploads
```

---

## Docker

Docker Compose runs Redis only for local development.
```bash
# Start Redis
docker-compose up -d

# Stop Redis
docker-compose down

# Check status
docker-compose ps
```

---

## API Endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /health | Health check | No |
| POST | /auth/register | Register new user | No |
| POST | /auth/login | Login, get JWT token | No |
| POST | /documents/upload | Upload document | Yes |
| GET | /documents | List all documents | Yes |
| GET | /documents/{id} | Get document by ID | Yes |
| DELETE | /documents/{id} | Delete document | Yes |
| GET | /search | Full-text search | Yes |

---

## Development Progress

### Completed
- Project structure and architecture
- Virtual environment and dependencies
- Git initialization with .gitignore
- Docker Compose for Redis
- Environment variable management with Pydantic Settings
- FastAPI app with lifespan, CORS, health check
- Async SQLAlchemy engine with connection pooling
- Base model with TimeStampMixin
- Session factory with auto commit and rollback
- Database connection verified on startup
- Structured logging with structlog

### In Progress
- Alembic migrations
- User model and auth system
- Document model and upload pipeline
- Full-text search with PostgreSQL tsvector
- Redis caching layer
- WebSocket for real-time processing status
- PyTest test suites

---

## Known Issues and Setup Notes

### Windows + Python 3.13 + PostgreSQL in Docker

asyncpg 0.31.0 has a scram-sha-256 authentication incompatibility
with PostgreSQL running in Docker on Windows with Python 3.13.

**Symptom:**
```
asyncpg.exceptions.InvalidPasswordError: password authentication 
failed for user
```

**Fix:** Use local PostgreSQL installation for development instead
of Docker PostgreSQL. Docker is used only for Redis in the local
dev environment.

### Environment URLs
```
Local development  →  DATABASE_URL uses localhost
Docker deployment  →  DATABASE_URL uses service name postgres
```

### Windows Bind Mounts

When using bind mounts in Docker on Windows with Git Bash,
use Windows path format:
```
"D:/path/to/project:/container/path"
```

Not Git Bash format (`/d/path/to/project`).

---

## Contributing

This project follows clean architecture principles with separation
of concerns across routes, services, schemas, and models.

Before submitting:
- Run tests: `pytest`
- Check formatting
- Update this README if setup steps change

---

## License

MIT