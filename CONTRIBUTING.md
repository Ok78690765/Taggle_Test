# Contributing

We welcome contributions to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/repo.git`
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Set up your environment:
   ```bash
   make install
   ```

## Development Workflow

### Before You Start

- Check existing issues and pull requests
- Create an issue to discuss large changes
- Keep commits focused and atomic

### Making Changes

1. **Backend changes** (Python/FastAPI):
   ```bash
   cd backend
   poetry install  # Install dependencies
   poetry run uvicorn app.main:app --reload  # Run server
   ```

2. **Frontend changes** (Next.js/TypeScript):
   ```bash
   cd frontend
   npm install  # Install dependencies
   npm run dev  # Run dev server
   ```

### Code Quality

All code must pass checks before merging:

```bash
# Backend
make backend-lint
make backend-format
make backend-test

# Frontend
make frontend-lint
make frontend-format
make frontend-test

# Or all at once
make lint
make format
make test
```

### Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: fix a bug
docs: update documentation
style: formatting changes
refactor: code refactoring
test: add or update tests
chore: maintenance tasks
```

Example:
```
feat(backend): add user authentication
- Implement JWT token generation
- Add login endpoint
- Add middleware for protected routes
```

## Pull Request Process

1. **Before submitting**:
   - Run all tests and checks locally
   - Update documentation
   - Add tests for new features
   - Keep PRs focused on a single feature/fix

2. **PR description** should include:
   - What changes were made
   - Why these changes were needed
   - Any relevant issue numbers
   - Screenshots (if UI changes)

3. **Review process**:
   - Automated checks must pass
   - At least one approval required
   - Address feedback and update PR
   - Squash commits before merge (optional)

## Testing

### Backend Testing

```bash
cd backend
poetry run pytest tests/ -v --cov=app
```

### Frontend Testing

```bash
cd frontend
npm run test:coverage
```

New features should include tests. Test coverage should not decrease.

## Documentation

- Update README.md for new features
- Add docstrings to functions
- Document API endpoints in code
- Keep configuration documented

## Branching Strategy

- `main` - Production ready code
- `develop` - Development branch
- `feat/*` - Feature branches
- `fix/*` - Bug fix branches
- `docs/*` - Documentation branches

## Issues

### Reporting Bugs

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment info (Python/Node version, OS, etc.)
- Error messages/logs

### Feature Requests

Include:
- Clear use case
- Why it's needed
- Proposed implementation (optional)
- Examples/mockups (if applicable)

## Performance

- Consider performance implications of changes
- Avoid unnecessary dependencies
- Profile code for bottlenecks
- Use caching where appropriate

## Security

- Don't commit secrets or credentials
- Use environment variables for config
- Follow security best practices
- Report security issues privately

## Questions?

- Open an issue with `[QUESTION]` prefix
- Check existing documentation
- Contact maintainers

Thank you for contributing! 🎉
