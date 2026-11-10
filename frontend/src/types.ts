export type DatasetInfo = {
  dataset_id: string;
  filename: string;
  row_count: number;
  column_count: number;
  columns: string[];
  preview: Record<string, unknown>[];
  missing_values: Record<string, number>;
};

export type Metrics = {
  sample_count: number;
  accuracy: number;
  precision_weighted: number;
  recall_weighted: number;
  f1_weighted: number;
  labels: string[];
  confusion_matrix: number[][];
};

export type SliceResult = {
  slice: string;
  sample_count: number;
  accuracy: number;
  precision_weighted: number;
  recall_weighted: number;
  f1_weighted: number;
  error_count: number;
};

export type AnalysisResult = {
  dataset_id: string;
  dataset_name: string;
  metrics: Metrics;
  errors: { row_number: number; actual: string; predicted: string; features: Record<string, string | null> }[];
  error_count: number;
  error_display_limit: number;
  slices: SliceResult[];
  comparison: null | {
    primary_name: string;
    comparison_name: string;
    primary: Metrics;
    comparison: Metrics;
  };
  missing_feature_values: Record<string, number>;
  columns: string[];
  interpretation_note: string;
};

export type SavedInvestigation = {
  id: number;
  name: string;
  dataset_name: string;
  created_at: string | null;
  summary: AnalysisResult;
};
