.PHONY: help install lint format test build docker-up docker-down docker-rebuild docker-logs \
        backend-install backend-lint backend-format backend-test backend-dev \
        frontend-install frontend-lint frontend-format frontend-build frontend-dev

.DEFAULT_GOAL := help

BACKEND_DIR := backend
FRONTEND_DIR := frontend

help:
	@echo "=== FastAPI + Next.js Monorepo ==="
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-up         - Start all services with Docker Compose"
	@echo "  make docker-down       - Stop all services"
	@echo "  make docker-rebuild    - Rebuild Docker images"
	@echo "  make docker-logs       - View logs from all services"
	@echo ""
	@echo "Backend commands:"
	@echo "  make backend-install   - Install backend dependencies"
	@echo "  make backend-lint      - Run linting on backend"
	@echo "  make backend-format    - Format backend code"
	@echo "  make backend-test      - Run backend tests"
	@echo "  make backend-dev       - Run backend in development mode"
	@echo ""
	@echo "Frontend commands:"
	@echo "  make frontend-install  - Install frontend dependencies"
	@echo "  make frontend-lint     - Run linting on frontend"
	@echo "  make frontend-format   - Format frontend code"
	@echo "  make frontend-build    - Build frontend for production"
	@echo "  make frontend-dev      - Run frontend in development mode"
	@echo ""
	@echo "Full workflow commands:"
	@echo "  make install           - Install all dependencies"
	@echo "  make lint              - Lint both stacks"
	@echo "  make format            - Format both stacks"
	@echo "  make test              - Run all tests"
	@echo "  make build             - Build for production"
	@echo ""

# Docker commands
docker-up:
	docker-compose -f shared/docker-compose.yml up -d

docker-down:
	docker-compose -f shared/docker-compose.yml down

docker-rebuild:
	docker-compose -f shared/docker-compose.yml build --no-cache

docker-logs:
	docker-compose -f shared/docker-compose.yml logs -f

# Backend commands
backend-install:
	cd $(BACKEND_DIR) && poetry install

backend-lint:
	cd $(BACKEND_DIR) && poetry run pylint app/ || true
	cd $(BACKEND_DIR) && poetry run mypy app/ || true

backend-format:
	cd $(BACKEND_DIR) && poetry run black app/ tests/
	cd $(BACKEND_DIR) && poetry run isort app/ tests/

backend-test:
	cd $(BACKEND_DIR) && poetry run pytest tests/ -v --cov=app

backend-dev:
	cd $(BACKEND_DIR) && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend commands
frontend-install:
	cd $(FRONTEND_DIR) && npm install

frontend-lint:
	cd $(FRONTEND_DIR) && npm run lint

frontend-format:
	cd $(FRONTEND_DIR) && npm run format

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

frontend-dev:
	cd $(FRONTEND_DIR) && npm run dev

# Full workflow commands
install: backend-install frontend-install

lint: backend-lint frontend-lint

format: backend-format frontend-format

test: backend-test

build: backend-lint frontend-build

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type d -name .pytest_cache -exec rm -rf {} + || true
	find . -type d -name .mypy_cache -exec rm -rf {} + || true
	rm -rf $(BACKEND_DIR)/.coverage
	rm -rf $(FRONTEND_DIR)/.next
	rm -rf $(FRONTEND_DIR)/node_modules
	rm -rf $(BACKEND_DIR)/build
	rm -rf $(BACKEND_DIR)/dist
