from __future__ import annotations

import os
import pandas as pd

from app.core.config import settings
from app.core.state import state

from datasets import load_dataset

def load_reviews() -> None:
    # if not os.path.exists(settings.csv_path):
    #     raise FileNotFoundError(f"CSV not found: {settings.csv_path}")

    # df = pd.read_csv(settings.csv_path)
    ds = load_dataset(
       "e9t/nsmc",
        trust_remote_code=True
    )

    # if settings.text_col not in df.columns:
    #     raise ValueError(f"{settings.text_col} column not found: {df.columns}")

    train = ds["train"]
    df = train.to_pandas()
    if "document" in df.columns and "concert_review" not in df.columns:
        df = df.rename(columns={"document": "concert_review"})
    # 결측 제거
    df = df.dropna(subset=[settings.text_col]).reset_index(drop=True)

    # 전역 state에 저장
    state.df_reviews = df
    state.cursor = 0

    # 캐시(조회 API용) 구성
    state.reviews_cache.clear()
    for idx, text in enumerate(df[settings.text_col].astype(str).tolist()):
        state.reviews_cache.append({"id": idx, "concert_review": text})