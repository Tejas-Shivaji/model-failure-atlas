import type { AnalysisResult, DatasetInfo, SavedInvestigation } from "./types";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function readError(response: Response): Promise<never> {
  let message = `Request failed (${response.status})`;
  try {
    const body = await response.json();
    message = body.detail || message;
  } catch { /* keep fallback */ }
  throw new Error(message);
}

export async function uploadCsv(file: File): Promise<DatasetInfo> {
  const body = new FormData();
  body.append("file", file);
  const response = await fetch(`${API_BASE}/api/datasets`, { method: "POST", body });
  if (!response.ok) return readError(response);
  return response.json();
}

export async function analyzeDataset(payload: {
  dataset_id: string; actual_column: string; predicted_column: string;
  comparison_column?: string; slice_column?: string;
}): Promise<AnalysisResult> {
  const response = await fetch(`${API_BASE}/api/analyze`, {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
  if (!response.ok) return readError(response);
  return response.json();
}

export async function saveInvestigation(name: string, result: AnalysisResult) {
  const response = await fetch(`${API_BASE}/api/investigations`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, dataset_name: result.dataset_name, summary: result }),
  });
  if (!response.ok) return readError(response);
  return response.json();
}

export async function fetchInvestigations(): Promise<SavedInvestigation[]> {
  const response = await fetch(`${API_BASE}/api/investigations`);
  if (!response.ok) return readError(response);
  return response.json();
}
