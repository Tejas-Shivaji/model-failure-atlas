from pydantic import BaseModel, Field
from typing import Optional

class AnalyzeRequest(BaseModel):
    dataset_id: str
    actual_column: str
    predicted_column: str
    comparison_column: Optional[str] = None
    slice_column: Optional[str] = None
    slice_value: Optional[str] = None

class SaveInvestigationRequest(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    dataset_name: str = Field(min_length=1, max_length=255)
    summary: dict
