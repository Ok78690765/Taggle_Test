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
- **Code Analysis API**: Comprehensive code quality, complexity, and debugging analysis
  - Code quality scoring with detailed metrics
  - Issue detection (complexity, style, naming)
  - Complexity metrics (cyclomatic, cognitive)
  - Architecture insights (design patterns)
  - Formatting recommendations
  - Debugging insights
  - Multi-language support (Python, JavaScript, TypeScript, Java, C++)

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

#### Code Analysis API

The backend includes a comprehensive Code Analysis API for analyzing source code across multiple languages:

- **Documentation**: See [ANALYSIS_API.md](./ANALYSIS_API.md) for detailed documentation
- **Endpoints**: `/api/analysis/*` - Quality scoring, issue detection, complexity metrics, architecture insights, formatting recommendations, and debugging analysis
- **Supported Languages**: Python, JavaScript, TypeScript, Java, C/C++
- **Features**: Heuristic-based analysis with design pattern detection, code metrics, and actionable insights

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
│   │   ├── base.py
│   │   └── analysis.py      # Analysis models
│   ├── schemas/             # Pydantic schemas/DTOs
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── analysis.py      # Analysis schemas
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── analysis.py      # Code analysis endpoints
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── code_analyzer.py # Analysis service
│   ├── middleware/          # Custom middleware
│   │   └── __init__.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── language_adapter.py  # Language parsers
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── test_main.py
│   ├── test_analysis_api.py        # Analysis API tests
│   ├── test_analysis_service.py    # Analysis service tests
│   ├── api/                 # API endpoint tests
│   │   ├── __init__.py
│   │   └── test_items.py
│   └── services/            # Service tests
│       ├── __init__.py
│       └── test_base.py
├── migrations/              # Alembic database migrations (optional)
├── pyproject.toml           # Poetry configuration
├── poetry.lock              # Locked dependencies
├── ANALYSIS_API.md          # Analysis API documentation
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

### Railway Deployment (Recommended)

Railway is a modern platform that provides seamless deployment with built-in PostgreSQL support and automatic deployments from GitHub.

#### Prerequisites

- A [Railway account](https://railway.app/) (free tier available)
- GitHub repository connected to Railway
- PostgreSQL database (optional, can provision through Railway)

#### Initial Setup

1. **Connect Your GitHub Repository**
   
   - Log in to [Railway](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Authorize Railway to access your repository
   - Select your repository from the list

2. **Configure the Service**

   Railway will automatically detect the `railway.toml` configuration file. The project includes:
   - Automatic Poetry dependency installation
   - Health check monitoring at `/health`
   - Restart policy for reliability
   - Auto-deployment triggers on `main` branch pushes

3. **Provision a PostgreSQL Database**

   - In your Railway project dashboard, click "New" → "Database" → "Add PostgreSQL"
   - Railway will automatically:
     - Create a PostgreSQL instance
     - Generate a `DATABASE_URL` environment variable
     - Link it to your service

   **Note**: If you don't need PostgreSQL yet, you can skip this step. The backend defaults to SQLite for development.

4. **Set Environment Variables**

   Navigate to your service's "Variables" tab and add the following:

   **Required Variables:**
   ```
   ENVIRONMENT=production
   SECRET_KEY=<generate-a-secure-random-key>
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

   **Optional Variables:**
   ```
   DEBUG=false
   LOG_LEVEL=INFO
   ENABLE_API_DOCS=true
   ```

   **How to generate a secure `SECRET_KEY`:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

   **Important**: If you provisioned PostgreSQL, Railway automatically sets `DATABASE_URL`. You don't need to set it manually.

5. **Deploy**

   - Railway will automatically build and deploy your service
   - Monitor the deployment logs in the "Deployments" tab
   - Once deployed, Railway will provide a public URL (e.g., `https://myapp-backend.up.railway.app`)

6. **Capture Your Public API URL**

   - Go to your service's "Settings" tab
   - Under "Domains", you'll see your public Railway URL
   - Copy this URL (e.g., `https://myapp-backend-production.up.railway.app`)
   - **Important**: Add this URL to your frontend's environment variables as `NEXT_PUBLIC_API_URL`

7. **Enable Automatic Deployments**

   The `railway.toml` configuration already enables auto-deployments:
   - Every push to the `main` branch triggers a new deployment
   - Railway rebuilds and redeploys the service automatically
   - You can monitor deployment status in the Railway dashboard

#### Database Migrations

If you're using PostgreSQL with Alembic migrations:

```bash
# Run migrations after deployment via Railway CLI
railway run alembic upgrade head
```

Or set up a migration job in Railway's dashboard.

#### Health Checks & Monitoring

Railway automatically monitors your service using the `/health` endpoint defined in `railway.toml`:
- **Health check path**: `/health`
- **Timeout**: 100 seconds
- **Restart policy**: ON_FAILURE (up to 10 retries)

You can view health status and logs in the Railway dashboard.

#### Connecting Frontend to Backend

After deploying to Railway:

1. Copy your Railway backend URL (e.g., `https://myapp-backend-production.up.railway.app`)
2. In your Vercel frontend project, add this environment variable:
   ```
   NEXT_PUBLIC_API_URL=https://myapp-backend-production.up.railway.app
   ```
3. Update the backend's `CORS_ORIGINS` on Railway to include your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://your-app-preview.vercel.app
   ```

#### Troubleshooting Railway Deployments

**Build Failures:**
- Check the build logs in the "Deployments" tab
- Ensure `pyproject.toml` and `poetry.lock` are committed
- Verify Python version compatibility (3.11+ required)

**Connection Errors:**
- Verify `DATABASE_URL` is set correctly (check "Variables" tab)
- Ensure `CORS_ORIGINS` includes your frontend URL
- Check service logs for detailed error messages

**Health Check Failures:**
- Verify the `/health` endpoint is accessible
- Check that the service is binding to `0.0.0.0` and the `PORT` env var
- Review the service logs for startup errors

**Environment Variables Not Working:**
- Redeploy after adding new variables (Railway requires a redeploy)
- Check variable names are uppercase and match `config.py`
- Ensure no trailing spaces in variable values

#### Railway CLI (Optional)

For advanced usage, install the Railway CLI:

```bash
# Install
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run commands in Railway environment
railway run python manage.py migrate

# View logs
railway logs

# Open dashboard
railway open
```

#### Cost Optimization

- **Free Tier**: Railway provides $5 free credits per month
- **Optimize**: Use the smallest PostgreSQL instance for development
- **Monitor**: Check the "Usage" tab to track resource consumption
- **Scale**: Upgrade to a paid plan when you exceed free tier limits

### Other Cloud Platforms

**Heroku**:
```bash
git push heroku main
```

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
