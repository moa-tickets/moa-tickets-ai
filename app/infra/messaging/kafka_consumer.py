from app.services.sentiment import predict_sentiment
from app.services.keyword_extractor import extract_keywords_kor
from app.infra.messaging.topics import REVIEW_TOPIC
from kafka import KafkaConsumer
import json
import redis
from app.core.init_model import ensure_model_loaded
from app.services.aspect_mapper import AspectMapper, DEFAULT_ASPECT_DICT
import os

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "host.docker.internal:9092")
TOPIC = os.getenv("KAFKA_TOPIC", REVIEW_TOPIC)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)
r.ping()

# ✅ 매퍼 1회 생성 (루프 밖)
aspect_mapper = AspectMapper(
    DEFAULT_ASPECT_DICT,
    # priority=["연출", "음향", "시야", "시설"]  # 겹치면 이 순서로 결정
)

def main():
    ensure_model_loaded()
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[s.strip() for s in BOOTSTRAP.split(",")],
        group_id=os.getenv("KAFKA_CONSUMER_GROUP", "review-consumer-group"),
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    )

    print("[consumer] started")

    for message in consumer:
        payload = message.value.get("reviews", [])[0]
        content = payload.get("content", "")
        concert_id = payload.get("concertId", "")
        print(f"Received message: {content}")

        labels = predict_sentiment([content])
        label = labels[0]
        kws = extract_keywords_kor(content)
        print(kws)

        sentiment = "pos" if label == 1 else "neg"

        pipe = r.pipeline()

        # 전체 키워드 저장
        total_key = f"concert:{concert_id}:{sentiment}:keywords_total"
        for kw in kws:
            pipe.zincrby(total_key, 1, kw)

        # aspect별로 저장
        for kw in kws:
            aspect = aspect_mapper.map_keyword(kw)
            aspect_key = f"concert:{concert_id}:{sentiment}:aspect:{aspect}"
            pipe.zincrby(aspect_key, 1, kw)

        pipe.execute()

        # (디버그)
        debug_key = f"concert:{concert_id}:{sentiment}:keywords_total"
        top7 = r.zrevrange(debug_key, 0, 6, withscores=True)
        print(f"[redis] debug_key={debug_key}")
        print(f"[redis] top7={top7}")

    print("[consumer] ended")
    

if __name__ == "__main__":
    main()