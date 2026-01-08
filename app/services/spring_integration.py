from app.services.sentiment import predict_one
from app.services.keyword_extractor import extract_keywords_kor

# services/spring_integration.py
async def process_spring_review(review_text: str):
    """Spring API 데이터 처리"""
    label, sentiment, score = predict_one(review_text)
    keywords = extract_keywords_kor(review_text)
    return {
        "label": label,
        "sentiment": sentiment,
        "score": score,
        "keywords": keywords
    }