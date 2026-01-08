from __future__ import annotations

from fastapi import APIRouter
from app.core.state import state
from app.models.schemas import KeywordTopRequest

router = APIRouter(prefix="/keywords", tags=["keywords"])

#http post를 통해서 데이터를 받는다
@router.post("/top")
async def analyze_top_keywords(req: KeywordTopRequest):
    k = 7 # 상위 k개 키워드 추출
    
    return {
        "positive_top": [{"keyword": w, "count": c} for w, c in state.pos_counter.most_common(k)],
        "negative_top": [{"keyword": w, "count": c} for w, c in state.neg_counter.most_common(k)],
        "total_unique_keywords": {
            "positive": len(state.pos_counter),
            "negative": len(state.neg_counter),
        },
    }
