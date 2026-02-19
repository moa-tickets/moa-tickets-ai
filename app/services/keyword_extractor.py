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
    "제 해 진짜 줄 으웩 왜 못 폰 몇 년 동안 거 알 직접 건 또 달라 모든 속 그대로 것 비주 얼 디테 일도 고요 폰 층 안보 여요 때문 \
    뭘 덜햇 조금 차라리 낫 쏙쏙 걸 또한 차땜 좀 안 오히려 커튼 콜 제대로 하나 하루 시간 저 별로 세 모양 갑자기 주의 주시 눈 내내 줄줄 \
    직거려 듣기 등 내 정말 정도"
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
