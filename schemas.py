from pydantic import BaseModel
from typing import List, Optional

# Pydantic models
class SurveyCreate(BaseModel):
    name: str
    questions: List[str]

class ResponseSubmit(BaseModel):
    candidate_name: str
    response: List[Optional[int]]
