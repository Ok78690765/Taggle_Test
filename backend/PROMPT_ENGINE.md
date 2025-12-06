# Prompt Edit Engine Documentation

## Overview

The Prompt Edit Engine is a backend module that transforms natural language prompts into actionable code edits. It provides a complete workflow for AI-assisted code modification with built-in safeguards, validation, formatting, and testing capabilities.

## Architecture

### Core Components

1. **LLM Provider Interface** (`app/services/llm_provider.py`)
   - Abstract provider interface for multiple LLM backends
   - OpenAI provider (GPT-4, GPT-3.5)
   - Anthropic provider (Claude)
   - Mock provider for testing
   - Extensible factory pattern for adding new providers

2. **Edit Planner Service** (`app/services/edit_planner.py`)
   - Converts user prompts into structured edit plans
   - Integrates with LLM providers to generate intelligent edits
   - Manages edit sessions and tracks state
   - Stores repo context for better understanding

3. **Diff Generation** (`app/utils/diff_utils.py`)
   - Unified diff generation for preview
   - Diff statistics (additions/deletions)
   - Line number tracking for changes

4. **Formatting Service** (`app/services/formatting_service.py`)
   - Automatic code formatting with Black, Ruff, Prettier
   - Language-specific formatter selection
   - Validates formatter availability

5. **Validation Service** (`app/services/validation_service.py`)
   - Syntax validation (Python AST, Node.js)
   - Linting (pylint, ESLint)
   - Type checking (mypy, TypeScript)

6. **Test Runner Service** (`app/services/test_runner.py`)
   - Executes test suites post-edit
   - Captures test results and coverage
   - Supports custom test commands

### Data Models

**EditSession**: Tracks the entire editing session
- `session_id`: Unique identifier
- `user_prompt`: Original user request
- `repo_context`: Repository context (files, language, etc.)
- `status`: Current status (pending, plan_generated, applied, etc.)
- `llm_provider` / `llm_model`: LLM configuration
- `dry_run`: Whether to only plan without applying
- Timestamps: created_at, updated_at

**CodeEdit**: Individual file edit plan
- `session_id`: Parent session
- `file_path`: Target file path
- `edit_type`: create, modify, delete, rename
- `description`: Human-readable description
- `original_content` / `modified_content`: File contents
- `applied`, `validated`, `formatted`: Status flags

**EditValidation**: Validation results
- `session_id`: Parent session
- `validation_type`: syntax, lint, type
- `status`: pass, fail, warning
- `message`: Validation details

## REST API Endpoints

### 1. Submit Prompt

**POST** `/api/prompt/submit`

Submit a prompt to generate code edit plans.

**Request Body:**
```json
{
  "prompt": "Add error handling to the user authentication function",
  "repo_context": {
    "repo_path": "/home/engine/project",
    "files": ["backend/app/auth.py", "backend/app/models/user.py"],
    "file_contents": {
      "backend/app/auth.py": "def authenticate(username, password):\n    ..."
    },
    "language": "python",
    "framework": "FastAPI"
  },
  "target_files": ["backend/app/auth.py"],
  "dry_run": true,
  "llm_provider": "openai",
  "llm_model": "gpt-4"
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "plan_generated",
  "message": "Edit plan generated successfully with 1 file(s)",
  "edit_plans": [
    {
      "file_path": "backend/app/auth.py",
      "edit_type": "modify",
      "description": "Add try-except blocks for error handling",
      "original_content": "...",
      "modified_content": "...",
      "line_range": [10, 30]
    }
  ],
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Preview Diffs

**GET** `/api/prompt/{session_id}/preview`

Get unified diffs for all planned edits.

**Path Parameter:**
- `session_id`: Session identifier

**Response:**
```json
{
  "session_id": "uuid-here",
  "diffs": [
    {
      "file_path": "backend/app/auth.py",
      "diff": "--- original/backend/app/auth.py\n+++ modified/backend/app/auth.py\n@@ -10,5 +10,10 @@\n...",
      "additions": 5,
      "deletions": 2,
      "edit_type": "modify"
    }
  ],
  "total_files": 1,
  "total_additions": 5,
  "total_deletions": 2
}
```

### 3. Validate Edits

**POST** `/api/prompt/{session_id}/validate`

Run validation checks on planned edits.

**Path Parameter:**
- `session_id`: Session identifier

**Request Body:**
```json
{
  "validation_types": ["syntax", "lint", "type"]
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "results": [
    {
      "validation_type": "syntax",
      "status": "pass",
      "file_path": "backend/app/auth.py",
      "message": "Python syntax is valid",
      "details": null
    },
    {
      "validation_type": "lint",
      "status": "warning",
      "file_path": "backend/app/auth.py",
      "message": "Line too long (92/88)",
      "details": {"line": 15}
    }
  ],
  "overall_status": "passed",
  "passed": 2,
  "failed": 0,
  "warnings": 1
}
```

### 4. Format Files

**POST** `/api/prompt/{session_id}/format`

Format files using appropriate formatters.

**Path Parameter:**
- `session_id`: Session identifier

**Request Body:**
```json
{
  "file_paths": ["backend/app/auth.py"],
  "formatters": ["black", "ruff"]
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "results": [
    {
      "file_path": "backend/app/auth.py",
      "formatter": "black",
      "status": "success",
      "message": null,
      "formatted_content": "...",
      "changes_made": true
    }
  ],
  "total_formatted": 1,
  "total_changed": 1
}
```

### 5. Apply Edits

**POST** `/api/prompt/{session_id}/apply`

Apply the planned edits to the filesystem.

**Path Parameter:**
- `session_id`: Session identifier

**Request Body:**
```json
{
  "file_paths": null,
  "skip_validation": false,
  "auto_format": true
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "applied_files": ["backend/app/auth.py"],
  "failed_files": [],
  "status": "success",
  "message": "Applied 1 file(s), 0 failed",
  "errors": null
}
```

### 6. Run Tests

**POST** `/api/prompt/{session_id}/test`

Execute tests after applying edits.

**Path Parameter:**
- `session_id`: Session identifier

**Request Body:**
```json
{
  "test_command": "pytest tests/",
  "test_paths": ["tests/test_auth.py"],
  "coverage": true
}
```

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "passed",
  "passed": 15,
  "failed": 0,
  "skipped": 2,
  "duration": 2.45,
  "output": "===== test session starts =====\n...",
  "coverage_percent": 87.5
}
```

### 7. Get Session Status

**GET** `/api/prompt/{session_id}/status`

Get the current status of an edit session.

**Path Parameter:**
- `session_id`: Session identifier

**Response:**
```json
{
  "session_id": "uuid-here",
  "status": "applied",
  "prompt": "Add error handling to the user authentication function",
  "edit_count": 1,
  "applied_count": 1,
  "validated": true,
  "formatted": true,
  "tests_run": true,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:00"
}
```

## Workflow

### Typical Usage Flow

1. **Submit Prompt**: Send a natural language prompt with context
2. **Preview Diffs**: Review the generated changes
3. **Validate**: Run syntax, lint, and type checks
4. **Format**: Apply code formatters for consistency
5. **Apply**: Write changes to the filesystem
6. **Test**: Run tests to ensure nothing broke
7. **Monitor**: Check session status

### Dry Run Mode

Set `dry_run: true` in the submit request to:
- Generate edit plans without applying
- Preview and validate changes
- Review and iterate before applying

### Safeguards

The engine includes multiple safeguards:

1. **Syntax Validation**: Ensures code is syntactically correct before applying
2. **Lint Checks**: Identifies style and quality issues
3. **Type Checking**: Validates type annotations (Python, TypeScript)
4. **Formatting**: Automatic code formatting to maintain consistency
5. **Test Execution**: Runs test suite to catch regressions
6. **Dry Run**: Preview mode to review before applying
7. **Session Tracking**: Full audit trail of all changes

## Prompt Instruction Schema

### Writing Effective Prompts

**Good prompts are:**
- Specific about what to change
- Clear about the desired outcome
- Include relevant context
- Specify file locations when possible

**Examples:**

```
"Add input validation to the create_user function in backend/app/api/users.py.
Validate that email is a valid format and username is at least 3 characters."
```

```
"Refactor the authentication middleware to use async/await syntax.
Ensure backward compatibility with existing route handlers."
```

```
"Add comprehensive error handling to all database operations in
backend/app/models/. Use try-except blocks and log errors appropriately."
```

### Providing Context

Include relevant context in `repo_context`:

```json
{
  "repo_context": {
    "repo_path": "/path/to/repo",
    "files": ["list", "of", "relevant", "files.py"],
    "file_contents": {
      "file.py": "actual file content here"
    },
    "language": "python",
    "framework": "FastAPI",
    "additional_context": {
      "coding_style": "Google style guide",
      "dependencies": ["fastapi", "sqlalchemy", "pydantic"]
    }
  }
}
```

## LLM Provider Configuration

### OpenAI

Set environment variable:
```bash
export OPENAI_API_KEY="sk-..."
```

Use in request:
```json
{
  "llm_provider": "openai",
  "llm_model": "gpt-4"
}
```

### Anthropic

Set environment variable:
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Use in request:
```json
{
  "llm_provider": "anthropic",
  "llm_model": "claude-3-sonnet-20240229"
}
```

### Mock Provider (Testing)

No configuration needed:
```json
{
  "llm_provider": "mock"
}
```

## Code Quality Standards

The engine enforces Google-level code quality through:

1. **Black** (Python): 88 character lines, consistent formatting
2. **Ruff** (Python): Fast linting and auto-fixes
3. **Prettier** (JS/TS): Consistent formatting across JavaScript/TypeScript
4. **Pylint** (Python): Code quality checks
5. **ESLint** (JS/TS): JavaScript/TypeScript linting
6. **Mypy** (Python): Type checking
7. **TSC** (TypeScript): Type checking

## Integration Examples

### Python Client

```python
import requests

API_BASE = "http://localhost:8000"

# Submit prompt
response = requests.post(f"{API_BASE}/api/prompt/submit", json={
    "prompt": "Add error handling to auth.py",
    "repo_context": {
        "repo_path": "/home/engine/project",
        "language": "python"
    },
    "dry_run": True,
    "llm_provider": "openai"
})
session_id = response.json()["session_id"]

# Preview diffs
diffs = requests.get(f"{API_BASE}/api/prompt/{session_id}/preview")
print(diffs.json())

# Validate
validation = requests.post(f"{API_BASE}/api/prompt/{session_id}/validate", json={
    "validation_types": ["syntax", "lint"]
})

# Apply
apply_result = requests.post(f"{API_BASE}/api/prompt/{session_id}/apply", json={
    "skip_validation": False,
    "auto_format": True
})
```

### JavaScript Client

```javascript
const API_BASE = 'http://localhost:8000';

async function editCode(prompt) {
  // Submit prompt
  const submitRes = await fetch(`${API_BASE}/api/prompt/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      dry_run: true,
      llm_provider: 'openai'
    })
  });
  const { session_id } = await submitRes.json();

  // Preview diffs
  const diffsRes = await fetch(`${API_BASE}/api/prompt/${session_id}/preview`);
  const diffs = await diffsRes.json();
  console.log(diffs);

  // Apply edits
  const applyRes = await fetch(`${API_BASE}/api/prompt/${session_id}/apply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      auto_format: true
    })
  });
  return await applyRes.json();
}
```

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `404`: Session not found
- `500`: Internal server error

Error responses include:
```json
{
  "detail": "Error message here"
}
```

## Performance Considerations

- LLM calls typically take 2-10 seconds
- Formatting is fast (<1 second per file)
- Validation depends on file size and tool
- Test execution time varies by test suite
- Use `dry_run: true` for faster iteration

## Limitations

- LLM responses quality depends on prompt clarity
- Large files (>10K lines) may need chunking
- Test execution has 30-minute timeout
- Formatters must be installed separately
- No real-time streaming of LLM responses yet

## Future Enhancements

- Streaming LLM responses
- Multi-file refactoring coordination
- Integration with version control (git)
- Automatic rollback on test failures
- Code review suggestions
- Performance profiling
- Security vulnerability scanning
