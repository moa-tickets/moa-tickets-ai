from __future__ import annotations

from fastapi import APIRouter
from app.core.state import state
from app.models.schemas import KeywordTopRequest

router = APIRouter(prefix="/keywords", tags=["keywords"])

@router.post("/top")
async def analyze_top_keywords(req: KeywordTopRequest):
    k = req.k
    
    return {
        "positive_top": [{"keyword": w, "count": c} for w, c in state.pos_counter.most_common(k)],
        "negative_top": [{"keyword": w, "count": c} for w, c in state.neg_counter.most_common(k)],
        "total_unique_keywords": {
            "positive": len(state.pos_counter),
            "negative": len(state.neg_counter),
        },
    }
