# Backend Service (FastAPI)

A modern Python backend service built with FastAPI, SQLAlchemy, and Pydantic.

## Features

- **FastAPI Framework**: High-performance async web framework
- **SQLAlchemy ORM**: Database abstraction and modeling
- **Pydantic**: Data validation and serialization
- **Poetry**: Dependency management and packaging
- **Pytest**: Comprehensive testing framework
- **Black & isort**: Code formatting and import sorting
- **Pylint & mypy**: Linting and type checking
- **Uvicorn**: ASGI server for production deployments

## Setup

### Prerequisites

- Python 3.11 or higher
- Poetry 1.4 or higher

### Installation

1. **Install dependencies**
   ```bash
   poetry install
   ```

2. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

   Or use `poetry run` to execute commands directly.

## Development

### Running the Server

**Development mode** (with auto-reload):
```bash
poetry run uvicorn app.main:app --reload
```

**Production mode**:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

### API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

### File Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── base.py
│   ├── schemas/             # Pydantic schemas/DTOs
│   │   ├── __init__.py
│   │   └── base.py
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Dependency injection
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── items.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── base.py
│   ├── middleware/          # Custom middleware
│   │   └── __init__.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── logging.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_main.py
│   ├── api/                 # API endpoint tests
│   │   ├── __init__.py
│   │   └── test_items.py
│   └── services/            # Service tests
│       ├── __init__.py
│       └── test_base.py
├── migrations/              # Alembic database migrations (optional)
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Locked dependencies
└── Dockerfile               # Container configuration
```

## Code Quality

### Formatting

Format code with Black and isort:

```bash
# Using make
make backend-format

# Or manually
poetry run black app/ tests/
poetry run isort app/ tests/
```

### Linting

Run linters to check for code issues:

```bash
# Using make
make backend-lint

# Or manually
poetry run pylint app/
poetry run mypy app/
```

### Type Checking

Ensure type safety across the codebase:

```bash
poetry run mypy app/
```

## Testing

### Running Tests

Run the test suite with coverage:

```bash
# Using make
make backend-test

# Or manually
poetry run pytest tests/ -v --cov=app
```

### Test Coverage

Generate coverage reports:

```bash
poetry run pytest tests/ --cov=app --cov-report=html
```

Coverage reports will be generated in `htmlcov/index.html`.

### Writing Tests

Create test files in the `tests/` directory following the structure:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_items():
    response = client.get("/api/items")
    assert response.status_code == 200
```

## Database

### Connection

Database connection is configured via environment variable `DATABASE_URL`.

**SQLite** (default for development):
```
DATABASE_URL=sqlite:///./test.db
```

**PostgreSQL**:
```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### Migrations

To set up Alembic for migrations:

```bash
poetry run alembic init migrations
poetry run alembic revision --autogenerate -m "Initial migration"
poetry run alembic upgrade head
```

## Environment Variables

Key environment variables (see `shared/.env.example`):

- `DEBUG` - Enable debug mode (default: false)
- `DATABASE_URL` - Database connection string
- `CORS_ORIGINS` - Allowed CORS origins
- `SECRET_KEY` - Secret key for security
- `LOG_LEVEL` - Logging level (default: INFO)

## Deployment

### Docker

Build the Docker image:

```bash
docker build -t myapp-backend .
```

Run the container:

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  myapp-backend
```

### Cloud Deployment

**Heroku**:
```bash
git push heroku main
```

**Railway**:
Connect your repository and Railway will auto-detect and deploy.

**AWS ECS/Fargate**:
Push image to ECR and create task definition.

**Google Cloud Run**:
```bash
gcloud run deploy --source . --platform managed
```

**Azure Container Instances**:
```bash
az container create --resource-group mygroup --name myapp-backend --image myimage
```

## Dependencies

### Core

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pydantic**: Data validation
- **sqlalchemy**: ORM

### Database

- **psycopg2-binary**: PostgreSQL adapter (optional)

### Development

- **pytest**: Testing framework
- **pytest-cov**: Coverage plugin
- **black**: Code formatter
- **isort**: Import sorter
- **pylint**: Linter
- **mypy**: Type checker
- **python-dotenv**: Environment variables

See `pyproject.toml` for complete dependency list.

## Common Tasks

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "Add user table"

# Run migrations
poetry run alembic upgrade head

# Add a new dependency
poetry add requests

# Add a development dependency
poetry add --group dev pytest-asyncio

# Export requirements
poetry export -f requirements.txt > requirements.txt
```

## Troubleshooting

**Port already in use**:
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Database connection errors**:
- Check `DATABASE_URL` is correct
- Ensure database service is running
- Verify network connectivity

**Import errors**:
- Ensure virtual environment is activated: `poetry shell`
- Reinstall dependencies: `poetry install`

**Tests failing**:
- Check if database is initialized
- Run `poetry run pytest -v` for verbose output
- Use `--pdb` flag to debug: `poetry run pytest --pdb`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Pytest Documentation](https://docs.pytest.org/)
