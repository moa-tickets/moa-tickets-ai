from __future__ import annotations
from pydantic import BaseModel
import os

MODEL_DIR = os.getenv("MODEL_DIR", "/moaticket/kc_electra_sentiment/final")

class Settings(BaseModel):
    csv_path: str = "kr3_concert_reviews.csv"
    text_col: str = "concert_review"
    model_dir: str = MODEL_DIR

    stream_interval_sec: float = 2.0
    stream_batch_size: int = 20

    default_page_size: int = 20
    max_page_size: int = 200

settings = Settings()