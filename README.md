# 📈 FinAgent Trading Strategy Team

**AI 기반 트레이딩 전략 자동화 플랫폼**

![FinAgent Banner](https://github.com/user-attachments/assets/f9ab1fec-2f29-421d-9575-1221a6d9810b)


[English](./README_en.md) | [한국어](./README.md)

---

## 📋 개요

FinAgent Trading Strategy Team은 AI 기반 트레이딩 전략을 자동화하고 백테스트 및 실행까지 지원하는 플랫폼입니다.  
Nest.js, PostgreSQL, Prisma 기반의 백엔드에 FastAPI로 전략 실행 서버를 구성했습니다.  
OpenAI API와 KIS API를 활용해 전략 생성과 실행을 자동화하고 있습니다.

---

## ✨ 주요 기능

- 🤖 OpenAI 기반 전략 생성 자동화  
- 📊 KIS API를 통한 실시간 데이터 수집 및 주문 실행  
- 🧪 전략 백테스트 및 성능 분석  
- 🧱 모듈화된 전략 실행 구조 (FastAPI 기반)  
- 🗂️ Prisma ORM을 통한 데이터 관리  

---

## 🗂️ 프로젝트 구조

```
trading-strategy-team/
├── src/                  # Nest.js 백엔드 코드
├── prisma/               # Prisma 스키마 및 마이그레이션
├── static/charts/        # 전략 결과 차트 이미지
├── tests/                # 테스트 코드
├── .env                  # 환경 변수 설정 파일
├── Dockerfile            # 도커 설정
├── docker-compose.yml    # 도커 컴포즈 설정
├── run.sh                # 서버 실행 스크립트
└── README.md             # 리드미 파일
```

---

## ⚙️ 환경 설정

### 1. Poetry 설치

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. `.env` 파일 생성

```env
POSTGRES_USER=uni
POSTGRES_PASSWORD=1234
POSTGRES_DB=trading
POSTGRES_PORT=5454
DATABASE_URL=postgresql://uni:1234@localhost:5454/trading

OPENAI_API_KEY=your_openai_api_key
KIS_APP_KEY=your_kis_app_key
KIS_SECRET_KEY=your_kis_secret_key
```

### 3. 의존성 설치

```bash
poetry install
```

---

## ▶️ 실행 방법

### 1. 데이터베이스 및 서버 실행

```bash
docker-compose up -d
```

### 2. FastAPI 서버 실행

```bash
bash run.sh
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.  
Swagger 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

---

## 💬 예시

> **사용자**: RSI 기반 전략 만들어줘  
> **시스템**: RSI 30 이하에서 매수, 70 이상에서 매도하는 전략을 생성했어요. 백테스트 결과는 다음과 같습니다.  
> ![Chart](./static/charts/sample_result.png)

---

## 🛠 기술 스택

| 구성 요소   | 기술 스택            |
|------------|----------------------|
| 백엔드     | Nest.js, FastAPI     |
| DB         | PostgreSQL, Prisma   |
| AI         | OpenAI API           |
| 외부 API   | KIS API              |
| 인프라     | Docker, Docker Compose |

---

## 🚀 로드맵

- [ ] 전략 성능 시각화 대시보드 개발  
- [ ] 사용자 맞춤형 전략 추천 기능  
- [ ] 다양한 지표 기반 전략 템플릿  
- [ ] 실시간 알림 시스템 연동  

---

## 🤝 기여 방법

1. 이슈를 통해 버그 리포트나 기능 요청을 남겨주세요.
2. 포크 후 브랜치를 생성해서 작업해주세요.
3. Pull Request를 보내주시면 리뷰 후 병합하겠습니다.

---

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](./LICENSE)를 따릅니다.
