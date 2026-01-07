from __future__ import annotations
from fastapi import APIRouter
from app.core.state import state

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    return {"status": "ok", "count": len(state.reviews_cache)}
