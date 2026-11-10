import pandas as pd
from app.services.metrics import calculate_metrics, calculate_slices
from app.services.validation import validate_prediction_columns

def run_analysis(frame: pd.DataFrame, actual_col: str, predicted_col: str,
                 comparison_col: str | None = None, slice_col: str | None = None):
    validate_prediction_columns(frame, actual_col, predicted_col)
    metrics = calculate_metrics(frame[actual_col], frame[predicted_col])

    actual = frame[actual_col].astype(str)
    predicted = frame[predicted_col].astype(str)
    wrong = frame.loc[actual != predicted].copy()
    errors = []
    for index, row in wrong.head(200).iterrows():
        errors.append({
            "row_number": int(index) + 2,
            "actual": str(row[actual_col]),
            "predicted": str(row[predicted_col]),
            "features": {
                str(col): (None if pd.isna(row[col]) else str(row[col]))
                for col in frame.columns if col not in (actual_col, predicted_col, comparison_col)
            }
        })

    slices = calculate_slices(frame, actual_col, predicted_col, slice_col) if slice_col else []
    comparison = None
    if comparison_col:
        validate_prediction_columns(frame, actual_col, comparison_col)
        comparison = {
            "primary_name": predicted_col,
            "comparison_name": comparison_col,
            "primary": calculate_metrics(frame[actual_col], frame[predicted_col]),
            "comparison": calculate_metrics(frame[actual_col], frame[comparison_col]),
        }

    missing_features = {
        str(col): int(frame[col].isna().sum())
        for col in frame.columns
        if col not in (actual_col, predicted_col, comparison_col) and frame[col].isna().any()
    }
    return {
        "metrics": metrics,
        "errors": errors,
        "error_count": len(wrong),
        "error_display_limit": 200,
        "slices": slices,
        "comparison": comparison,
        "missing_feature_values": missing_features,
        "columns": [str(c) for c in frame.columns],
        "interpretation_note": (
            "Slice results are descriptive, not proof of causation. "
            "Small groups can produce unstable estimates; inspect sample counts before drawing conclusions."
        ),
    }
