from __future__ import annotations
import re
from typing import Dict, List, Optional, Tuple

AspectDict = Dict[str, List[str]]

DEFAULT_ASPECT_DICT: AspectDict = {
    "음향": ["음향", "사운드", "스피커", "웅장", "마이크", "성량"],
    "시야": ["시야", "좌석", "자리", "단차", "거리감"],
    "시설": ["화장실", "주차", "로비", "물품보관소", "편의시설", "시설"],
    "연출": ["조명", "무대", "장치", "효과", "분위기", "영화", "느낌", "연출"],
    "연기": ["배우", "발성", "대사", "연기"],
}

def normalize_kw(s: str) -> str:
    s = s.strip()
    s = re.sub(r"\s+", " ", s)
    # 자주 나오는 변형만 최소로 통일 (필요시 추가)
    replacements = {
        "웅장함": "웅장",
        "거리": "거리감",
    }
    return replacements.get(s, s)

class AspectMapper:
    def __init__(self, aspect_dict: AspectDict, priority: Optional[List[str]] = None):
        self.aspect_dict = aspect_dict
        self.priority = priority or list(aspect_dict.keys())

        # contains 매칭을 위해 토큰을 길이 내림차순 정렬(긴 단어 우선)
        self._tokens: List[Tuple[str, str]] = []
        for aspect, toks in aspect_dict.items():
            for t in toks:
                self._tokens.append((aspect, t))
        self._tokens.sort(key=lambda x: len(x[1]), reverse=True)

    def map_keyword(self, kw: str) -> str:
        kw_n = normalize_kw(kw)

        # 1) exact match 우선
        for aspect in self.priority:
            if kw_n in self.aspect_dict.get(aspect, []):
                return aspect

        # 2) contains match
        hits = []
        for aspect, token in self._tokens:
            if token and token in kw_n:
                hits.append(aspect)

        if hits:
            # priority 순서대로 첫 번째 선택
            for p in self.priority:
                if p in hits:
                    return p

        return "기타"
