# Development Quick Start Guide

## Prerequisites

- Docker & Docker Compose (recommended)
- OR: Python 3.11+, Node.js 18+, Poetry

## Option 1: Using Docker Compose (Recommended)

```bash
# Start all services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

Services will be available at:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:3000

## Option 2: Manual Setup

### Backend Setup

```bash
cd backend

# Install dependencies
poetry install

# Run development server
poetry run uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs at `http://localhost:3000`

## Common Development Tasks

### Linting & Formatting

```bash
# Lint both stacks
make lint

# Format both stacks
make format

# Or specific stack
make backend-lint
make backend-format
make frontend-lint
make frontend-format
```

### Testing

```bash
# Run all tests
make test

# Backend tests
cd backend
poetry run pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test:coverage
```

### Building for Production

```bash
# Build frontend
make frontend-build

# Or manually
cd frontend
npm run build

# Build Docker images
docker build -t myapp-backend backend/
docker build -t myapp-frontend frontend/
```

## Troubleshooting

### Ports Already in Use

**Port 8000 (Backend):**
```bash
lsof -ti:8000 | xargs kill -9
```

**Port 3000 (Frontend):**
```bash
lsof -ti:3000 | xargs kill -9
```

### Python Dependencies Issues

```bash
cd backend
poetry install --no-cache
poetry run pip install --upgrade pip
```

### Node Dependencies Issues

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker Issues

```bash
# Rebuild images
make docker-rebuild

# Clean everything
docker-compose -f shared/docker-compose.yml down -v
make docker-up
```

## API Integration

The frontend is already configured to connect to the backend.

**Environment Variables** (see `shared/.env.example`):
- `NEXT_PUBLIC_API_URL` - Backend API URL (set in `.env.local`)

**Example Usage:**
```typescript
import { api } from '@/lib/api';

const response = await api.get('/api/items');
```

## Database Management

### SQLite (Default)

Database file is at `backend/test.db` for development.

To reset:
```bash
cd backend
rm test.db
poetry run python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### PostgreSQL (Optional)

Update `DATABASE_URL` in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/myapp
```

## IDE Setup

### VSCode

1. Install extensions:
   - Python
   - Pylance
   - Black Formatter
   - ESLint
   - Prettier
   - Tailwind CSS IntelliSense

2. Settings (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

### PyCharm

1. Set project interpreter to `backend/.venv/bin/python`
2. Enable Pytest as default test runner
3. Configure code style: Python → Black (line length 88)

### Dev Container

Uses `.devcontainer/devcontainer.json` for full VS Code dev environment:
```bash
# Open in container
Remote-Containers: Open Folder in Container
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feat/your-feature

# Make changes and commit
git add .
git commit -m "feat: your feature description"

# Push and create PR
git push origin feat/your-feature
```

## Documentation

- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`
- Architecture: `README.md`
- Contributing: `CONTRIBUTING.md`

## CI/CD

All checks run automatically on push/PR:
- Backend: Linting, type checking, tests
- Frontend: Linting, type checking, tests, build
- Docker: Image builds
- Security: Vulnerability scanning

See `.github/workflows/` for configurations.

## Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Poetry Docs](https://python-poetry.org/docs/)
- [Docker Docs](https://docs.docker.com/)

## Getting Help

1. Check relevant README files
2. Review CONTRIBUTING.md
3. Check GitHub Issues
4. Ask in discussions

Happy coding! 🚀
