FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 1) 시스템 의존성 + Java 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    openjdk-21-jre-headless \
 && rm -rf /var/lib/apt/lists/*

# 2) JVM 경로를 명시 (Debian 계열에서 보통 아래 중 하나)
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"
# JPype가 libjvm.so를 못 찾는 경우를 대비
ENV LD_LIBRARY_PATH="${JAVA_HOME}/lib/server:${LD_LIBRARY_PATH}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# torch CPU 전용 설치 (CUDA 패키지 방지)
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.9.1

COPY . .

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker","app.main:app", "-b", "0.0.0.0:8000", "--workers", "1", "--timeout", "120"] 
