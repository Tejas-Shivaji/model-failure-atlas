import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

def calculate_metrics(actual, predicted):
    actual = [str(v) for v in actual]
    predicted = [str(v) for v in predicted]
    labels = sorted(set(actual) | set(predicted))
    precision, recall, f1, _ = precision_recall_fscore_support(
        actual, predicted, labels=labels, average="weighted", zero_division=0
    )
    matrix = confusion_matrix(actual, predicted, labels=labels)
    return {
        "sample_count": len(actual),
        "accuracy": round(float(accuracy_score(actual, predicted)), 4),
        "precision_weighted": round(float(precision), 4),
        "recall_weighted": round(float(recall), 4),
        "f1_weighted": round(float(f1), 4),
        "labels": labels,
        "confusion_matrix": matrix.astype(int).tolist(),
    }

def calculate_slices(frame, actual_col, predicted_col, feature_col):
    if feature_col not in frame.columns:
        raise ValueError(f"Feature column '{feature_col}' was not found.")
    series = frame[feature_col]
    if series.isna().all():
        raise ValueError(f"Feature column '{feature_col}' contains no usable values.")

    working = frame.loc[series.notna()].copy()
    values = working[feature_col]
    groups = []

    if values.dtype.kind in "biufc" and values.nunique() > 5:
        try:
            bins = min(5, int(values.nunique()))
            working["_atlas_slice"] = pd.qcut(values, q=bins, duplicates="drop").astype(str)
            grouping = working.groupby("_atlas_slice", observed=True, sort=True)
        except Exception:
            working["_atlas_slice"] = values.astype(str)
            grouping = working.groupby("_atlas_slice", observed=True, sort=True)
    else:
        working["_atlas_slice"] = values.astype(str)
        grouping = working.groupby("_atlas_slice", observed=True, sort=True)

    for group_value, subset in grouping:
        metrics = calculate_metrics(subset[actual_col], subset[predicted_col])
        groups.append({
            "slice": str(group_value),
            "sample_count": metrics["sample_count"],
            "accuracy": metrics["accuracy"],
            "precision_weighted": metrics["precision_weighted"],
            "recall_weighted": metrics["recall_weighted"],
            "f1_weighted": metrics["f1_weighted"],
            "error_count": int((subset[actual_col].astype(str) != subset[predicted_col].astype(str)).sum()),
        })
    return sorted(groups, key=lambda row: (row["accuracy"], -row["sample_count"]))
