import csv
from io import BytesIO, StringIO
import pandas as pd
from app.core.config import MAX_ROWS, MAX_COLUMNS

class DatasetValidationError(ValueError):
    pass

def read_and_validate_csv(content: bytes) -> pd.DataFrame:
    if not content:
        raise DatasetValidationError("The uploaded file is empty.")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise DatasetValidationError("CSV must use UTF-8 encoding. Save it as CSV UTF-8 and retry.") from exc

    try:
        header = next(csv.reader(StringIO(text)))
    except StopIteration:
        raise DatasetValidationError("The CSV does not contain a header row.")
    if not header or all(not str(col).strip() for col in header):
        raise DatasetValidationError("The CSV header row is empty.")
    cleaned = [str(col).strip() for col in header]
    if len(set(cleaned)) != len(cleaned):
        raise DatasetValidationError("Duplicate column names were found. Rename duplicate columns and retry.")
    if len(cleaned) > MAX_COLUMNS:
        raise DatasetValidationError(f"Too many columns. The limit is {MAX_COLUMNS}.")

    try:
        frame = pd.read_csv(BytesIO(content))
    except Exception as exc:
        raise DatasetValidationError(f"Could not parse CSV: {exc}") from exc

    if frame.empty:
        raise DatasetValidationError("The CSV has a header but no data rows.")
    if len(frame) > MAX_ROWS:
        raise DatasetValidationError(f"Too many rows. The limit is {MAX_ROWS:,}.")
    frame.columns = cleaned
    return frame

def validate_prediction_columns(frame: pd.DataFrame, actual: str, predicted: str):
    for col in (actual, predicted):
        if col not in frame.columns:
            raise DatasetValidationError(f"Column '{col}' was not found in the uploaded dataset.")
        if frame[col].isna().any():
            count = int(frame[col].isna().sum())
            raise DatasetValidationError(f"Column '{col}' contains {count} missing value(s). Fix these labels before evaluation.")
    if frame[actual].astype(str).str.strip().eq("").any():
        raise DatasetValidationError(f"Column '{actual}' contains blank labels.")
    if frame[predicted].astype(str).str.strip().eq("").any():
        raise DatasetValidationError(f"Column '{predicted}' contains blank labels.")
