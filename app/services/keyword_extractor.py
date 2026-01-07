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
    "정말 수 맛 곳 것 매우 제공 방문 더 이 조금 아주 다른 점 중 꼭 정도 다만 때 사람 전체 준비 간식 꽤 그 고기 생각 다소 번 전혀 한 두 다시 있는 맛이 공연을 맛은 않았다 "
    "국물 서서 비해 특히 잘 있었다 없이 많은 있어서 냄새가 나서 했는데 내 1시간을 차가 많아 있었습니다 있어 않은 여러 오히려 국물이 주차하는 데 어려움이 있었고 줄을 음식을 받아야 "
    "기대에 거의 게다가 너무 보러 온 생각이 아 없는 역시 진짜 그냥 왜 다 완전 이건 본 없고 없다 듯"
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
