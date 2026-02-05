from pathlib import Path
from app.core.init_model import ensure_model_loaded
from app.services.sentiment import predict_sentiment

ensure_model_loaded()

BASE_DIR = Path(__file__).resolve().parent
data_path = BASE_DIR / "ratings.txt"

BATCH_SIZE = 32  # 맥이면 16~64 사이 권장. 죽으면 16으로 더 줄여.

tp = fp = fn = tn = 0

def update_confusion(y_true_batch, y_pred_batch):
    global tp, fp, fn, tn
    for yt, yp in zip(y_true_batch, y_pred_batch):
        if yt == 1 and yp == 1: tp += 1
        elif yt == 0 and yp == 1: fp += 1
        elif yt == 1 and yp == 0: fn += 1
        elif yt == 0 and yp == 0: tn += 1

texts, labels = [], []

with open(data_path, encoding="utf-8") as f:
    header = next(f, None)  # header skip (없어도 안전)
    for line in f:
        line = line.strip()
        if not line:
            continue
        # NSMC 스타일: id \t document \t label
        _, text, label = line.split("\t")
        texts.append(text)
        labels.append(int(label))

        if len(texts) >= BATCH_SIZE:
            preds = predict_sentiment(texts)

            # ✅ predict_sentiment가 logits/torch tensor를 반환하는 경우 대비
            # (리스트[int]가 아니면 여기서 정규화)
            try:
                import torch
                if isinstance(preds, torch.Tensor):
                    preds = torch.argmax(preds, dim=1).tolist()
            except Exception:
                pass

            update_confusion(labels, preds)
            texts, labels = [], []

# 마지막 찌꺼기 배치 처리
if texts:
    preds = predict_sentiment(texts)
    try:
        import torch
        if isinstance(preds, torch.Tensor):
            preds = torch.argmax(preds, dim=1).tolist()
    except Exception:
        pass
    update_confusion(labels, preds)

# F1 계산 (binary, positive=1 기준)
precision = tp / (tp + fp) if (tp + fp) else 0.0
recall = tp / (tp + fn) if (tp + fn) else 0.0
f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

print(f"TP={tp}, FP={fp}, FN={fn}, TN={tn}")
print(f"precision={precision:.4f}, recall={recall:.4f}, f1={f1:.4f}")
