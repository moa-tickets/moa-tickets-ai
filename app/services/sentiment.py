from __future__ import annotations

from typing import List
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from app.core.config import settings
from app.core.state import state

def load_model() -> None:
    state.tokenizer = AutoTokenizer.from_pretrained(settings.model_dir)
    state.model = AutoModelForSequenceClassification.from_pretrained(settings.model_dir)
    state.model.eval()

def predict_sentiment(texts: List[str]) -> List[int]:
    """
    return: 1 (positive) / 0 (negative)
    """
    labels: List[int] = []

    # 성능: 1개씩 돌리는 대신, 가능한 한 배치로 처리
    enc = state.tokenizer(
        texts,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="pt"
    )

    with torch.no_grad():
        out = state.model(**enc)
        probs = torch.softmax(out.logits, dim=-1).cpu().numpy()
    # print(f"Accuracy score: {float(probs.max())}")
    for p in probs:
        labels.append(int(p.argmax()))
    # print(f"Sentiment: {"positive" if labels[0] == 1 else "negative"}")
    return labels

def predict_one(text: str) -> tuple[int, str, float]:
    enc = state.tokenizer([text], truncation=True, padding=True, max_length=128, return_tensors="pt")
    with torch.no_grad():
        out = state.model(**enc)
        probs = torch.softmax(out.logits, dim=-1)[0].cpu().numpy()
    label = int(probs.argmax())
    sentiment = "positive" if label == 1 else "negative"
    score = float(probs.max())
    return label, sentiment, score
