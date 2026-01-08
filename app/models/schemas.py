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
    review: str

# Spring 서버에서 보낼 리뷰 데이터
class SpringReviewItem(BaseModel):
    """Spring에서 보낼 리뷰 데이터 항목"""
    id: int
    concert_review: str

class SpringReviewsPayload(BaseModel):
    """Spring에서 보낼 리뷰 리스트"""
    reviews: List[SpringReviewItem]

# 단일 리뷰 예측 요청
class SpringReviewRequest(BaseModel):
    """Spring API에서 받을 개별 리뷰 데이터"""
    review_text: str
    concert_id: int
    user_id: int

class PredictionResult(BaseModel):
    """모델 처리 결과"""
    label: int
    sentiment: str
    score: float
    keywords: List[str]
