# Model-Failure Atlas

### An Explainable Machine Learning Failure Investigation Workbench

Model-Failure Atlas is a full-stack application for investigating classification model performance beyond a single aggregate score. Upload a labelled CSV, evaluate predictions, inspect data slices, explore incorrect predictions, compare two prediction columns, and save investigation summaries.

## What Works in This Release

- CSV upload with file-size, row-count, header and encoding checks
- Required actual/prediction label validation
- Accuracy, weighted precision, weighted recall and weighted F1
- Confusion matrix returned by the API
- Categorical slices and quantile-based numeric slices
- Incorrect-prediction explorer (first 200 rows displayed)
- Same-dataset comparison of two prediction columns
- Saved investigation summaries using SQLite by default
- React + TypeScript dashboard with Plotly visualization
- Pytest coverage for core metrics, validation and analysis

## Quick Start (Windows)

**Requirements:** Python 3.11 or 3.12, Node.js 20 or newer, and Git.

### 1. Start the Backend

Open PowerShell in the project root:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Interactive API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 2. Start the Frontend

Open a second terminal at the project root:

```powershell
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (normally [http://127.0.0.1:5173](http://127.0.0.1:5173)).

### 3. Try the Sample Dataset

Upload `sample-data/sample_classification.csv`.

- Actual label: `actual`
- Prediction: `predicted`
- Compare with: `second_model_prediction`
- Slice by: `age_group` or `monthly_income`

The sample is synthetic and exists only to demonstrate the workflow. Its results are not evidence about real-world populations or models.

## Run Tests

From the project root:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
pytest -q
```

## Architecture

- `frontend/`: React + TypeScript user interface and Plotly chart
- `backend/app/api/`: FastAPI endpoints
- `backend/app/services/`: CSV validation, metrics and analysis logic
- `backend/app/models.py`: saved investigation database model
- `backend/app/database.py`: SQLAlchemy database configuration
- `sample-data/`: synthetic demonstration CSV
- `docs/`: architecture and dataset contract

Uploaded datasets are stored in bounded process memory (up to 8 datasets) and are lost when the backend restarts. Run one backend worker for this release.

Saved investigation summaries are persisted in SQLite by default. PostgreSQL can be configured with `DATABASE_URL`; do not use SQLite or in-memory dataset storage for a multi-user production deployment without replacing the storage layer.

## Important Interpretation Limits

Slice comparisons are descriptive, not causal. Small groups can have unstable estimates.

The application does not currently provide confidence intervals, statistical significance testing, multiple-comparison correction, fairness certification, model explainability methods such as SHAP, authentication, or multi-user isolation.

Weighted classification metrics can conceal minority-class performance; inspect class-level metrics and confusion matrices before making high-stakes decisions.

This tool is an investigation aid, not a model approval system.

## Security and Privacy

Use only datasets you are authorized to process. Do not upload sensitive personal data to an internet-hosted demo.

The local demo has no authentication. Upload limits and bounded in-memory storage are guardrails, not a complete production security boundary.

## Development Status

**Version 1.0.0 — First Functional MVP**

Deployment hardening, persistent dataset storage, authentication, class-wise metric views, confidence intervals, and production observability remain future work.

## License

MIT License. See `LICENSE`.