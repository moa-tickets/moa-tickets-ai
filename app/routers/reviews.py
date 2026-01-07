from __future__ import annotations

from typing import Optional
from fastapi import APIRouter, Query

from app.core.config import settings
from app.core.state import state
from app.models.schemas import ReviewListResponse, ReviewItem

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.get("", response_model=ReviewListResponse)
async def list_reviews(
    page: int = Query(1, ge=1),
    size: int = Query(settings.default_page_size, ge=1, le=settings.max_page_size),
    q: Optional[str] = Query(None),
):
    items = state.reviews_cache

    if q:
        q_lower = q.lower()
        items = [r for r in items if q_lower in r["concert_review"].lower()]

    total = len(items)
    start = (page - 1) * size
    end = start + size

    return {"total": total, "page": page, "size": size, "items": items[start:end]}

@router.get("/{review_id}", response_model=ReviewItem)
async def get_review(review_id: int):
    # 단순 검색(필요하면 dict 인덱싱으로 개선 가능)
    for r in state.reviews_cache:
        if r["id"] == review_id:
            return r
    return {"detail": "Review not found"}
