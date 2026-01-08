from __future__ import annotations

from fastapi import APIRouter
from app.core.state import state
from app.models.schemas import SpringReviewsPayload

router = APIRouter(prefix="/api", tags=["spring-integration"])

@router.post("/reviews")
async def receive_reviews_from_spring(payload: SpringReviewsPayload):
    """
    Spring 서버에서 리뷰 데이터를 받아서 state에 저장합니다.
    
    요청 예시:
    {
        "reviews": [
            {"id": 1, "concert_review": "공연이 좋았어요", "user_id": 101, "concert_id": 1},
            {"id": 2, "concert_review": "너무 훌륭한 공연", "user_id": 102, "concert_id": 1}
        ]
    }
    """
    # 기존 캐시 초기화
    state.reviews_cache.clear()
    state.cursor = 0
    
    # 받은 리뷰 저장
    for review in payload.reviews:
        state.reviews_cache.append({
            "id": review.id,
            "concert_review": review.concert_review,
            "user_id": review.user_id,
            "concert_id": review.concert_id
        })
    
    return {
        "status": "success",
        "message": f"{len(payload.reviews)}개의 리뷰를 저장했습니다.",
        "total_reviews": len(state.reviews_cache)
    }

@router.get("/status")
async def spring_integration_status():
    """현재 저장된 리뷰 상태 조회"""
    return {
        "total_reviews": len(state.reviews_cache),
        "positive_keywords": dict(state.pos_counter.most_common(10)),
        "negative_keywords": dict(state.neg_counter.most_common(10))
    }
