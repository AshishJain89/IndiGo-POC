# Refactor & Optimization Plan

This document logs phases, progress, and decisions as we evolve the codebase from POC to production-ready.

## Phase 1: Resilience, Configuration, Observability (In Progress)
- Completed
  - Centralized settings via `backend/infrastructure/settings.py` with validated env and defaults.
  - RAG service uses settings; added idempotent upserts (content hashes) to avoid duplicate vectors.
  - Scraper aligned with centralized timeouts; PDF/HTML handling; resilient fetch.
  - Embedding fallback: OpenAI → sentence-transformers.
  - Extraction fallback: OpenAI → Perplexity; CLI continues on failures and writes empty rules.
  - Logging: correlation IDs (`X-Request-ID`) and request timing in `logging_middleware`.
- Next
  - Add minimal metrics counters and expose a `/metrics` endpoint (Prometheus format).
  - Integration tests for index + extract with a temporary Chroma dir.

## Phase 2: Retrieval & Extraction Quality (Planned)
- Domain-aware chunking (headings/sections), provenance (url, page/section), and collection versioning.
- Hybrid retrieval (BM25 + vectors) and optional reranker.
- Deterministic JSON extraction with evidence and schema validation.

## Phase 3: API & Frontend (Planned)
- Normalize API responses; pagination; DTOs.
- Frontend data layer with TanStack Query; component-level error boundaries and skeletons.
- Accessibility pass and route-based code-splitting.

## Changelog
- 2025-09-12: Created plan doc; centralized settings; idempotent vector upserts; improved scraper; logging with correlation IDs; added extraction/embedding fallbacks; docs updated.
- 2025-09-12: Added `scripts/simulate_issues.py` to seed conflicting rosters and disruptions. Fixed Windows async DB error by setting `WindowsSelectorEventLoopPolicy` before `asyncio.run()`.

## 2025-09-12: Fix Pydantic BaseSettings Import Error

- **Problem:**  
  Uvicorn server failed to start due to:
  ```
  pydantic.errors.PydanticImportError: `BaseSettings` has been moved to the `pydantic-settings` package.
  ```
  This is caused by importing `BaseSettings` from `pydantic` in Pydantic v2+.

- **Solution:**  
  1. Install the new package:
     ```
     pip install pydantic-settings
     ```
  2. Update `backend/infrastructure/settings.py`:
     ```python
     # OLD:
     from pydantic import BaseSettings, Field

     # NEW:
     from pydantic_settings import BaseSettings
     from pydantic import Field
     ```

- **Reference:**  
  [Pydantic v2 Migration Guide](https://docs.pydantic.dev/2.11/migration/#basesettings-has-moved-to-pydantic-settings)

## 2025-09-12: Fix Pydantic Settings ValidationError for Extra Inputs

- **Problem:**  
  After migrating to Pydantic v2 and using `pydantic-settings`, the app failed with:
  ```
  pydantic_core._pydantic_core.ValidationError: ... Extra inputs are not permitted ...
  ```
  This is because Pydantic v2 now forbids extra fields by default, so any environment variable not defined in the `Settings` class causes an error.

- **Solution:**  
  1. Ensure all expected environment variables are defined as fields in the `Settings` class in `backend/infrastructure/settings.py`.
  2. Optionally, set `extra = "ignore"` in the `Config` class if you want to ignore extra environment variables.

  Example:
  ```python
  class Settings(BaseSettings):
      postgres_host: str = Field(..., env="POSTGRES_HOST")
      postgres_port: int = Field(..., env="POSTGRES_PORT")
      postgres_db: str = Field(..., env="POSTGRES_DB")
      postgres_user: str = Field(..., env="POSTGRES_USER")
      postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
      groq_api_key: str = Field(..., env="GROQ_API_KEY")
      cursor_api_key: str = Field(..., env="CURSOR_API_KEY")

      class Config:
          extra = "ignore"
  ```

- **Reference:**  
  [Pydantic v2 Migration Guide: Extra fields](https://docs.pydantic.dev/2.11/migration/#extra-fields)
