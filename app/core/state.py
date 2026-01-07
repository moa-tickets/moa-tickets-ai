from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd
from collections import Counter

@dataclass
class AppState:
    df_reviews: Optional[pd.DataFrame] = None
    cursor: int = 0
    reviews_cache: List[dict] = field(default_factory=list)

    pos_counter: Counter = field(default_factory=Counter)
    neg_counter: Counter = field(default_factory=Counter)

    tokenizer: object = None
    model: object = None

state = AppState()
