from pydantic import BaseModel, Field
from typing import Dict, Optional

class RequestCreate(BaseModel):
    model: str = Field(..., example="gpt-3.5-turbo")
    prompt: str = Field(..., example="Write a short story about a cat.")
    parameters: Optional[Dict[str, float]] = Field(default_factory=dict, example={"temperature": 0.7})

class RequestOut(BaseModel):
    status: str
    result: str
    request_id: int

class ErrorResponse(BaseModel):
    detail: str