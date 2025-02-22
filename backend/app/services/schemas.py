from pydantic import BaseModel
from typing import List, Optional

class ROIResponse(BaseModel):
    labels: List[str]
    values: List[float]
