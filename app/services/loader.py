from __future__ import annotations

from app.core.state import state

def load_reviews() -> None:
    """
    Spring 서버에서 리뷰 데이터를 받을 때까지 대기
    Spring API가 /api/spring/reviews 엔드포인트로 리뷰 데이터를 보내면
    해당 라우터에서 state.reviews_cache를 업데이트합니다.
    """
    state.reviews_cache.clear()
    state.cursor = 0
    print("✅ Spring API 리뷰 수신 대기 중...")