from __future__ import annotations

import re
from typing import List

# --- 형태소 기반 (가능하면) ---
try:
    from konlpy.tag import Okt
    _okt = Okt()
except Exception:
    _okt = None

_STOPWORDS_RAW = (
    "제 "
)
STOPWORDS = set(_STOPWORDS_RAW.split())

def extract_keywords_kor(text: str) -> List[str]:
    text = re.sub(r"[^가-힣0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    if _okt:
        tokens: List[str] = []
        for w, pos in _okt.pos(text, stem=True):
            if pos in ("Noun",) and w not in STOPWORDS:
                tokens.append(w)
        return tokens

    # fallback
    return [t for t in text.split() if t not in STOPWORDS]
