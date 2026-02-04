# app/core/init_model.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.state import state
from app.core.config import settings

def ensure_model_loaded():
    if state.tokenizer is not None and state.model is not None:
        return
    state.tokenizer = AutoTokenizer.from_pretrained(settings.model_dir)
    state.model = AutoModelForSequenceClassification.from_pretrained(settings.model_dir)
    state.model.eval()
