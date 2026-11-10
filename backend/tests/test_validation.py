import pytest
from app.services.validation import read_and_validate_csv, validate_prediction_columns, DatasetValidationError

def test_reads_valid_csv():
    frame = read_and_validate_csv(b"id,actual,predicted\n1,A,A\n2,B,A\n")
    assert list(frame.columns) == ["id", "actual", "predicted"]
    assert len(frame) == 2

def test_rejects_empty_file():
    with pytest.raises(DatasetValidationError):
        read_and_validate_csv(b"")

def test_rejects_duplicate_headers():
    with pytest.raises(DatasetValidationError):
        read_and_validate_csv(b"id,actual,actual\n1,A,A\n")

def test_rejects_missing_prediction_labels():
    frame = read_and_validate_csv(b"actual,predicted\nA,A\nB,\n")
    with pytest.raises(DatasetValidationError):
        validate_prediction_columns(frame, "actual", "predicted")

def test_rejects_unknown_column():
    frame = read_and_validate_csv(b"actual,predicted\nA,A\n")
    with pytest.raises(DatasetValidationError):
        validate_prediction_columns(frame, "truth", "predicted")
