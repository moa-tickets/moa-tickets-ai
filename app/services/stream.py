from __future__ import annotations

import asyncio
from typing import List

from app.core.config import settings
from app.core.state import state
from app.services.sentiment import predict_sentiment
from app.services.keyword_extractor import extract_keywords_kor

async def fetch_new_reviews(batch_size: int) -> List[str]:
    if state.df_reviews is None or state.df_reviews.empty:
        return []

    if state.cursor >= len(state.df_reviews):
        return []

    end = min(state.cursor + batch_size, len(state.df_reviews))
    batch = state.df_reviews.iloc[state.cursor:end]
    state.cursor = end

    col = settings.text_col
    return [str(x) for x in batch[col].fillna("").tolist()]

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
