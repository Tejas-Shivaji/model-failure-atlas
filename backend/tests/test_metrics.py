from app.services.metrics import calculate_metrics

def test_metrics_for_perfect_predictions():
    result = calculate_metrics(["yes", "no", "yes"], ["yes", "no", "yes"])
    assert result["accuracy"] == 1.0
    assert result["f1_weighted"] == 1.0
    assert result["sample_count"] == 3

def test_metrics_for_mixed_predictions():
    result = calculate_metrics(["A", "A", "B", "B"], ["A", "B", "B", "B"])
    assert result["accuracy"] == 0.75
    assert result["sample_count"] == 4
    assert result["confusion_matrix"] == [[1, 1], [0, 2]]

def test_zero_division_is_handled():
    result = calculate_metrics(["cat", "cat"], ["dog", "dog"])
    assert result["accuracy"] == 0.0
    assert result["precision_weighted"] == 0.0
