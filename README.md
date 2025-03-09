# Trading Strategy Team

## How to Play

### Local Play

---

1. install poetry

- 구글에 poetry 설치 방법을 검색하셔서 poetry를 설치해주세요.

2. 환경변수 설정

- 최상위 폴더에 `.env` 파일을 생성하고 다음과 같은 환경변수들을 설정해주세요.

```
DATABASE_URL=a
```

3. 서버 실행

```bash
./run.sh
```

### Docker Play

---

1. Docker Run

```Dockerfile
docker run -dp 8000:8000 -t trading-server:latest .
```
