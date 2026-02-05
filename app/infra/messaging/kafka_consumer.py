from app.services.sentiment import predict_sentiment
from app.services.keyword_extractor import extract_keywords_kor
from app.infra.messaging.topics import REVIEW_TOPIC
from kafka import KafkaConsumer
import json
import redis
from app.core.init_model import ensure_model_loaded

# r = redis.Redis(host='redis', port=6379, db=0)
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def main():
    ensure_model_loaded()
    consumer = KafkaConsumer(
        REVIEW_TOPIC,
        bootstrap_servers=['localhost:9092', 'localhost:9093', 'localhost:9094'],
        group_id='review-consumer-group',
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        # value_deserializer=lambda v: v.decode("utf-8", errors="replace")
    )

    print("[consumer] started")

    # ① for 루프 안으로 처리 로직 전체를 이동 (기존: 루프 밖에서 texts 처리)
    for message in consumer:
        # print("topic:", message.topic, "partition:", message.partition, "offset:", message.offset)
        # print("key:", repr(message.key))
        # print("value:", repr(message.value)[:2000])  # 너무 길면 잘라서
        # break
        payload = message.value.get("reviews", [])[0]
        review_id = payload.get("reviewId", -1)
        content = payload.get("content", "")
        print(f"Received message: {content}")

        labels = predict_sentiment([content])
        label = labels[0]
        kws = extract_keywords_kor(content)

        # ③ 키워드별 루프 대신 파이프라인으로 최적화
        target_key = 'positive_keywords' if label == 1 else 'negative_keywords'
        pipe = r.pipeline()
        for kw in kws:
            pipe.zincrby(target_key, 1, kw)
        pipe.execute()  # 한 번에 실행 → Redis 네트워크 왕복 횟수 감소

        print(f"Positive Keywords: {r.zrevrange('positive_keywords', 0, 6, withscores=True)}")
        print(f"Negative Keywords: {r.zrevrange('negative_keywords', 0, 6, withscores=True)}")

    print("[consumer] ended")
    

if __name__ == "__main__":
    main()