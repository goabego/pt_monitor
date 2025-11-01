from typing import List
from pydantic import BaseModel, Field

class MetricConfig(BaseModel):
    """
    A Pydantic model for defining a Google Cloud Monitoring metric configuration.
    """
    name: str
    metric_type: str
    value_field: str
    value_name: str
    metric_labels: List[str] = Field(default_factory=list)
    aligner: str = "ALIGN_DELTA"
    reducer: str = "REDUCE_SUM"
