from __future__ import annotations
from typing import List
from pydantic import BaseModel

class ReviewItem(BaseModel):
    id: int
    concert_review: str

class ReviewListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[ReviewItem]

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    label: int
    sentiment: str
    score: float

class KeywordTopRequest(BaseModel):
    k: int = 7