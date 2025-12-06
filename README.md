# FastAPI + Next.js Monorepo

A modern monorepo template combining a FastAPI backend service with a Next.js frontend application.

## Project Structure

```
├── backend/              # FastAPI backend service
│   ├── app/             # Application code
│   ├── tests/           # Test suite
│   ├── pyproject.toml   # Poetry configuration
│   ├── Dockerfile       # Backend container
│   └── README.md        # Backend documentation
├── frontend/            # Next.js frontend application
│   ├── src/             # Frontend source code
│   ├── public/          # Static assets
│   ├── package.json     # NPM configuration
│   ├── Dockerfile       # Frontend container
│   ├── next.config.js   # Next.js configuration
│   └── README.md        # Frontend documentation
├── shared/              # Shared configuration
│   ├── docker-compose.yml
│   └── .env.example
├── .github/             # GitHub Actions workflows
├── Makefile             # Task runner
└── README.md           # This file
```

## Prerequisites

- **Python 3.11+** - For backend development
- **Node.js 18+** - For frontend development
- **Docker & Docker Compose** - For containerized development
- **Poetry** - For Python dependency management
- **npm or yarn** - For Node.js package management

## Local Development

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-name>
   ```

2. **Using Docker Compose (Recommended)**
   ```bash
   make docker-up
   ```

3. **Manual Setup**

   **Backend:**
   ```bash
   cd backend
   poetry install
   poetry run python -m app.main
   ```

   **Frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Available Make Commands

```bash
# Docker commands
make docker-up       # Start all services with Docker Compose
make docker-down     # Stop all services
make docker-rebuild  # Rebuild Docker images
make docker-logs     # View logs from all services

# Backend commands
make backend-install # Install backend dependencies
make backend-lint    # Run linting on backend
make backend-format  # Format backend code
make backend-test    # Run backend tests
make backend-dev     # Run backend in development mode

# Frontend commands
make frontend-install # Install frontend dependencies
make frontend-lint    # Run linting on frontend
make frontend-format  # Format frontend code
make frontend-build   # Build frontend for production
make frontend-dev     # Run frontend in development mode

# Full workflow
make install         # Install all dependencies
make lint           # Lint both stacks
make format         # Format both stacks
make test           # Run all tests
make build          # Build for production
```

## Architecture

### Backend (FastAPI)

- **Framework**: FastAPI with async/await support
- **Database**: SQLAlchemy ORM ready
- **Package Manager**: Poetry
- **Linting**: Pylint
- **Formatting**: Black, isort
- **Testing**: pytest with coverage
- **API Documentation**: Auto-generated OpenAPI/Swagger at `/docs`

**Run backend**:
```bash
make backend-dev
# or manually:
cd backend && poetry run uvicorn app.main:app --reload
```

Backend API runs on `http://localhost:8000` by default.

### Frontend (Next.js)

- **Framework**: Next.js 14+ with App Router
- **Language**: TypeScript
- **Styling**: CSS/Tailwind CSS ready
- **Package Manager**: npm
- **Linting**: ESLint
- **Formatting**: Prettier
- **API Client**: Ready to consume backend API

**Run frontend**:
```bash
make frontend-dev
# or manually:
cd frontend && npm run dev
```

Frontend runs on `http://localhost:3000` by default.

### Shared Infrastructure

- **Docker Compose**: Orchestrates backend, frontend, and any services
- **Environment Configuration**: `.env.example` for reference
- **Makefile**: Unified command interface for common tasks

## Environment Configuration

Copy `.env.example` to `.env` in the root directory:

```bash
cp shared/.env.example .env
```

Key environment variables:
- `BACKEND_URL` - Backend API URL (used by frontend)
- `DATABASE_URL` - Database connection string (backend only)
- `DEBUG` - Enable debug mode
- `NODE_ENV` - Node environment (development/production)

## Deployment

### Backend Deployment

The backend can be deployed to any platform supporting Python/Docker:
- **Heroku**: `git push heroku main`
- **Railway**: Connect repository and deploy
- **AWS/GCP/Azure**: Use Docker image with container services
- **DigitalOcean**: App Platform or Droplets

See `backend/README.md` for detailed backend deployment instructions.

### Frontend Deployment

The frontend is configured for Vercel and Netlify:

**Vercel** (Recommended for Next.js):
1. Connect repository to Vercel
2. Configure build settings:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

**Netlify**:
1. Connect repository to Netlify
2. Configure build settings:
   - Base Directory: `frontend`
   - Build Command: `npm run build`
   - Publish Directory: `out` (after configuring Next.js export)

See `frontend/README.md` for detailed frontend deployment instructions.

## CI/CD

GitHub Actions workflows are configured for:
- **Linting**: ESLint (frontend), Pylint (backend)
- **Type Checking**: TypeScript (frontend), mypy (backend)
- **Testing**: Jest (frontend), pytest (backend)
- **Building**: Production builds for both stacks

Workflows run on:
- Push to `main` and `develop` branches
- Pull requests to `main`

See `.github/workflows/` for detailed workflow configurations.

## Development Guidelines

- **Backend**: See `backend/README.md` for coding standards
- **Frontend**: See `frontend/README.md` for coding standards
- **API**: Keep API contracts documented in OpenAPI/Swagger
- **Versioning**: Use semantic versioning for releases

## Contributing

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes and commit: `git commit -m "feat: your feature"`
3. Push to the branch: `git push origin feat/your-feature`
4. Open a pull request

All checks must pass before merging:
- Linting
- Type checking
- Tests
- Build verification

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check existing GitHub issues
2. Create a new issue with detailed reproduction steps
3. Join our community discussions

## Related Documentation

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Docker Setup](./shared/docker-compose.yml)
- [Environment Configuration](./shared/.env.example)
