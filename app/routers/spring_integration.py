from __future__ import annotations

from fastapi import APIRouter
from app.core.state import state
from app.models.schemas import SpringReviewsPayload
from app.services.sentiment import predict_sentiment
from app.services.keyword_extractor import extract_keywords_kor

import redis, os

router = APIRouter(prefix="/api", tags=["spring-integration"])
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)
r.ping()

@router.post("/reviews")
async def receive_reviews_from_spring(payload: SpringReviewsPayload):
    
    print("✅ Spring API로부터 리뷰 데이터 수신 완료")
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
    
    texts = []
    # 받은 리뷰 저장
    for review in payload.reviews:
        state.reviews_cache.append({
            "id": review.id,
            "concert_review": review.concert_review,
            "user_id": review.user_id,
            "concert_id": review.concert_id
        })
        texts.append(review.concert_review)

    labels = predict_sentiment(texts)

    for text, y in zip(texts, labels):
        kws = extract_keywords_kor(text)
        if not kws:
            continue

        if y == 1:
            for kw in kws:
                r.zincrby('positive_keywords', 1, kw)
        else:
            for kw in kws:
                r.zincrby('negative_keywords', 1, kw)

    
    return {
        "status": "success",
        "message": f"{len(payload.reviews)}개의 리뷰를 저장했습니다.",
        "totalReviews": len(state.reviews_cache),
        "positiveKeywords": r.zrevrange('positive_keywords', 0, 6, withscores=True),
        "negativeKeywords": r.zrevrange('negative_keywords', 0, 6, withscores=True)
    }

@router.get("/status")
async def spring_integration_status():
    """현재 저장된 리뷰 상태 조회"""
    return {
        "total_reviews": len(state.reviews_cache),
        "positive_keywords": dict(state.pos_counter.most_common(10)),
        "negative_keywords": dict(state.neg_counter.most_common(10))
    }
