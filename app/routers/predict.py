from fastapi import APIRouter
from app.core.state import state
from app.models.schemas import KeywordTopRequest

from app.models.schemas import SpringReviewRequest
from app.services.sentiment import predict_one
from app.services.keyword_extractor import extract_keywords_kor

router = APIRouter(prefix="/predict", tags=["predict"])

# Spring API에서 리뷰 데이터를 받아서 예측 및 키워드 추출 후 반환
@router.post("/predict-from-spring")
async def predict_from_spring(req: SpringReviewRequest):
    # 1. 감정 분석
    label, sentiment, score = predict_one(req.review_text)
    
    # 2. 키워드 추출
    keywords = extract_keywords_kor(req.review_text)
    
    # 3. 상태 업데이트
    if label == 1:
        state.pos_counter.update(keywords)
    else:
        state.neg_counter.update(keywords)
    
    return {
        "concert_id": req.concert_id,
        "user_id": req.user_id,
        "prediction": {
            "label": label,
            "sentiment": sentiment,
            "score": score,
            "keywords": keywords
        }
    }