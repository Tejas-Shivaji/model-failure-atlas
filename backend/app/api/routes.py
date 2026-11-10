import json
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.config import MAX_UPLOAD_BYTES
from app.database import get_db
from app.models import Investigation
from app.schemas.analysis import AnalyzeRequest, SaveInvestigationRequest
from app.services.dataset_store import put_dataset, get_dataset
from app.services.validation import read_and_validate_csv, DatasetValidationError
from app.services.analysis import run_analysis

router = APIRouter(prefix="/api")

@router.post("/datasets")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail=f"File exceeds the {MAX_UPLOAD_BYTES // (1024 * 1024)} MB upload limit.")
    try:
        frame = read_and_validate_csv(content)
    except DatasetValidationError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    dataset_id = put_dataset(file.filename, frame)
    preview_frame = frame.head(8).astype(object).where(frame.head(8).notna(), None)
    preview = preview_frame.to_dict(orient="records")
    return {
        "dataset_id": dataset_id,
        "filename": file.filename,
        "row_count": len(frame),
        "column_count": len(frame.columns),
        "columns": [str(c) for c in frame.columns],
        "preview": preview,
        "missing_values": {str(c): int(frame[c].isna().sum()) for c in frame.columns if frame[c].isna().any()},
    }

@router.post("/analyze")
def analyze(request: AnalyzeRequest):
    item = get_dataset(request.dataset_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Dataset session expired. Please upload the CSV again.")
    try:
        result = run_analysis(
            item["frame"], request.actual_column, request.predicted_column,
            request.comparison_column, request.slice_column
        )
    except (DatasetValidationError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    return {"dataset_id": request.dataset_id, "dataset_name": item["name"], **result}

@router.post("/investigations")
def save_investigation(request: SaveInvestigationRequest, db: Session = Depends(get_db)):
    record = Investigation(
        name=request.name.strip(),
        dataset_name=request.dataset_name,
        summary_json=json.dumps(request.summary, ensure_ascii=False),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"id": record.id, "name": record.name, "dataset_name": record.dataset_name,
            "created_at": record.created_at.isoformat() if record.created_at else None}

@router.get("/investigations")
def list_investigations(db: Session = Depends(get_db)):
    records = db.query(Investigation).order_by(Investigation.id.desc()).limit(100).all()
    return [{"id": r.id, "name": r.name, "dataset_name": r.dataset_name,
             "created_at": r.created_at.isoformat() if r.created_at else None,
             "summary": json.loads(r.summary_json)} for r in records]

@router.get("/investigations/{investigation_id}")
def get_investigation(investigation_id: int, db: Session = Depends(get_db)):
    record = db.query(Investigation).filter(Investigation.id == investigation_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    return {"id": record.id, "name": record.name, "dataset_name": record.dataset_name,
            "created_at": record.created_at.isoformat() if record.created_at else None,
            "summary": json.loads(record.summary_json)}
