import pandas as pd
from app.services.analysis import run_analysis

def test_analysis_reports_errors_and_slices():
    frame = pd.DataFrame({
        "age_group": ["young", "young", "older", "older"],
        "actual": ["yes", "no", "yes", "no"],
        "predicted": ["yes", "yes", "no", "no"],
    })
    result = run_analysis(frame, "actual", "predicted", slice_col="age_group")
    assert result["metrics"]["sample_count"] == 4
    assert result["error_count"] == 2
    assert len(result["errors"]) == 2
    assert len(result["slices"]) == 2
    assert "not proof of causation" in result["interpretation_note"]

def test_model_comparison_returns_both_metrics():
    frame = pd.DataFrame({
        "actual": ["A", "B", "A"],
        "model_one": ["A", "A", "A"],
        "model_two": ["A", "B", "B"],
    })
    result = run_analysis(frame, "actual", "model_one", comparison_col="model_two")
    assert result["comparison"]["primary"]["accuracy"] == round(2 / 3, 4)
    assert result["comparison"]["comparison"]["accuracy"] == round(2 / 3, 4)
