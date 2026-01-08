from __future__ import annotations

import asyncio
from typing import List

from app.core.config import settings
from app.core.state import state
from app.services.sentiment import predict_sentiment
from app.services.keyword_extractor import extract_keywords_kor

async def fetch_new_reviews(batch_size: int) -> List[str]:
    if state.reviews_cache is None or len(state.reviews_cache) == 0:
        return []

    if state.cursor >= len(state.reviews_cache):
        return []

    end = min(state.cursor + batch_size, len(state.reviews_cache))
    batch = state.reviews_cache[state.cursor:end]
    state.cursor = end

    # reviews_cache는 딕셔너리 리스트 구조
    return [item.get("concert_review", "") for item in batch if isinstance(item, dict)]

async def stream_loop() -> None:
    while True:
        reviews = await fetch_new_reviews(batch_size=settings.stream_batch_size)

        if reviews:
            labels = predict_sentiment(reviews)

            for text, y in zip(reviews, labels):
                kws = extract_keywords_kor(text)
                if not kws:
                    continue

                if y == 1:
                    state.pos_counter.update(kws)
                else:
                    state.neg_counter.update(kws)

        await asyncio.sleep(settings.stream_interval_sec)
