# shiny-waffle

FastAPI application for RAG (Retrieval-Augmented Generation) with vector search, structured logging, and multi-provider LLM support.

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Starlette |
| Vector DB | Qdrant 1.12 |
| Relational DB | PostgreSQL 16 |
| Cache | Redis 7 |
| LLM inference | Ollama (local) + Anthropic / OpenAI / Cohere |
| Embeddings | OpenAI `text-embedding-3-small` |
| Logging | structlog (JSON + correlation ID) |
| Settings | pydantic-settings |
| Package manager | uv |

## Prerequisites

- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- Docker + Docker Compose

## Getting started

```bash
# 1. start infrastructure
docker compose up -d

# 2. install dependencies (includes dev + eval extras)
uv sync --all-extras

# 3. install pre-commit hooks
uv run pre-commit install

# 4. copy and fill in the required environment variables
cp .env.example .env
```

### Required environment variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Required |
| `OPENAI_API_KEY` | Optional — needed for embeddings and OpenAI models |
| `COHERE_API_KEY` | Optional |
| `POSTGRES_PASSWORD` | Defaults to `dev_only` in Docker Compose |

All other settings (DB URLs, chunking params, log level) have sensible defaults. See `src/shared/config.py` for the full list.

## Development

```bash
# lint
uv run ruff check .

# format
uv run ruff format .

# type check
uv run mypy src/

# tests
uv run pytest -v

# run all pre-commit checks manually
uv run pre-commit run --all-files
```

Pre-commit hooks run automatically on every `git commit`: ruff lint, ruff format, mypy, trailing whitespace, secret detection, and large-file checks.

## Project structure

```
src/
  api/          # HTTP layer (middleware, routes)
  shared/       # Cross-cutting concerns (config, logging)
  infra/        # Database clients and external service adapters
  ingestion/    # Document chunking and embedding pipelines
  eval/         # RAG evaluation (RAGAS, DeepEval)
  notebooks/    # Exploratory notebooks (output stripped by pre-commit)
tests/
  unit/
  integration/
infra/
  sql/          # PostgreSQL init scripts
```

## CI

Every pull request and push to `main` runs:

1. **lint** — `ruff check` + `ruff format --check`
2. **typecheck** — `mypy src/` (strict)
3. **test** — pytest with live Qdrant and PostgreSQL containers
4. **security** — Trufflehog secret scanning (verified credentials only)
