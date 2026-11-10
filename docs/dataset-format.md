# Dataset format

## Required concept

A CSV must contain:
- one ground-truth column (for example `actual`)
- one model prediction column (for example `predicted`)
- zero or more feature columns used to investigate slices and individual failures

An optional second prediction column can be selected to compare model versions on the same labelled rows.

## Example

```csv
record_id,age_group,region,actual,predicted,second_model_prediction
001,18-25,North,Approved,Approved,Approved
002,18-25,South,Rejected,Approved,Rejected
003,26-40,East,Approved,Approved,Approved
```

## Validation rules

- File extension must be `.csv`.
- File encoding must be UTF-8 (UTF-8 with BOM is accepted).
- Header names must be unique and non-empty.
- Dataset must contain at least one data row.
- Defaults: maximum 10 MiB, 100,000 rows, 100 columns.
- Actual and selected prediction columns must exist and contain no missing or blank labels.
- Feature columns may contain missing values. Missing feature counts are reported.
- Actual and prediction labels are compared as strings. Ensure labels are consistently represented (for example, do not mix `1` and `positive` for the same class).

## Alignment

The application assumes each CSV row contains the actual label and prediction(s) for the same observation. It cannot independently verify that predictions are aligned with the correct records. Include a stable record identifier and ensure alignment before upload.

## Privacy

Do not upload personal, confidential, regulated or otherwise sensitive data to a hosted demo unless you have authorization and the deployment has appropriate controls.
