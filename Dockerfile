# Python 3.12 slim 이미지를 베이스로 사용
FROM python:3.12-slim

# 필요한 패키지 설치 (curl과 다른 기본 도구들)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -

# poetry를 PATH에 추가
ENV PATH="/root/.local/bin:$PATH"

# 로컬의 poetry.lock과 pyproject.toml을 컨테이너로 복사
COPY pyproject.toml poetry.lock /app/

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치
RUN poetry install --no-root

# 로컬의 src 디렉토리를 컨테이너의 /app/src로 복사
COPY src /app/src

# uvicorn을 사용하여 main.py를 실행
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
