from __future__ import annotations
from pydantic import BaseModel

class Settings(BaseModel):
    csv_path: str = "kr3_concert_reviews.csv"
    text_col: str = "concert_review"
    model_dir: str = "./kc_electra_sentiment/final"

    stream_interval_sec: float = 2.0
    stream_batch_size: int = 20

    default_page_size: int = 20
    max_page_size: int = 200

settings = Settings()
