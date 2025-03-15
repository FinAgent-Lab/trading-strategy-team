# Trading Strategy Team

## How to Play

### Local Play

---

1. install poetry

- 구글에 poetry 설치 방법을 검색하셔서 poetry를 설치해주세요.

2. 환경변수 설정

- 최상위 폴더에 `.env` 파일을 생성하고 다음과 같은 환경변수들을 설정해주세요.

```
POSTGRES_USER=uni
POSTGRES_PASSWORD=1234
POSTGRES_DB=trading
POSTGRES_PORT=5454
DATABASE_URL=postgresql://uni:1234@postgres:5454/trading

# OpenAI
OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# KIS
KIS_APP_KEY=aa
KIS_SECRET_KEY=a
```

3. 서버 실행

### Local Play

- `run.sh` 파일을 이용해서 서버 실행 시, Fastapi 서버"만" 실행이 되며, DB는 따로 실행되지 않습니다.
- port는 8000번을 사용합니다.
- API Docs는 `http://localhost:8000/api-docs` 링크를 통해 들어가실 수 있습니다.

```bash
./run.sh
```

### Docker Play

---

1. Compose up

```bash
docker-compose up -d

# 혹은
docker compose up -d
```
