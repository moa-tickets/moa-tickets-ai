from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field

class ReviewItem(BaseModel):
    id: int
    concert_review: str
    user_id: int | None = None
    concert_id: int | None = None

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
    id: int = Field(alias="reviewId")
    concert_review: str = Field(alias="content")
    user_id: int = Field(alias="userId")
    concert_id: int = Field(alias="concertId")

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
