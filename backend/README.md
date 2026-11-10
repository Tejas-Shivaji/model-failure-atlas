# Backend

FastAPI service for CSV ingestion, validation, classification evaluation, slice analysis, error inspection and saved investigation summaries.

## Run locally (Windows PowerShell)

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs: http://127.0.0.1:8000/docs

The default database is local SQLite (`model_failure_atlas.db`). Set `DATABASE_URL` to a PostgreSQL SQLAlchemy URL when deploying. Uploaded CSV data is held in bounded process memory (8 datasets, one worker); saved investigation summaries are stored in the database. This is a single-worker demo architecture, not multi-tenant production storage.
