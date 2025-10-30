## DevOps Report (short)

### Technologies used

- Python 3.8+ / Flask
- PostgreSQL (tests use a service in CI)
- Docker (image build & push)
- GitHub Actions (CI/CD)
- Pipenv for dependency management
- flake8 (lint), Bandit (security), pytest (tests)
- Optional deploy targets: Railway / Render

### Pipeline design 


- Stages: build → lint & security → test (with Postgres) → docker-build → deploy

ASCII diagram:

    push -> Build -> Lint/Bandit -> Test (+Postgres) -> Docker Build -> Deploy

Logs from lint/test/deploy steps are printed to the Actions job output; deploy can trigger provider APIs and poll status.

### Secret management

- Keep secrets in GitHub repo Settings → Secrets → Actions (DO NOT commit keys).
- Examples used: `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `RAILWAY_TOKEN`, `RENDER_API_KEY`, `RENDER_SERVICE_ID`.
- Principle: least privilege, rotate regularly, and restrict repo access.

### Testing process

- Unit tests run via `pytest` in CI with a PostgreSQL service container.
- Local development: use `.env` and Pipenv to install deps; tests can run against a local Postgres or use lightweight SQLite for isolated tests.
- Fast feedback: run `flake8` and `pytest` locally before pushing.

### Lessons learned (short)

- Exclude local `.venv` from security scans to avoid vendor noise; scan dependencies separately with `pip-audit`.
- Make runtime config resilient (e.g., `DATABASE_URL`, sensible DB defaults) to avoid test-time crashes.
- Use provider integrations (Railway/Render) for simpler deploys; Actions can trigger deploys and surface logs in pipeline output.

---

Generated: concise DevOps summary for repo CI/CD.
