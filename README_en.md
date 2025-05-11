# 📈 FinAgent Trading Strategy Team

[English](./README_en.md) | [한국어](./README.md)

---

## 📋 Overview

FinAgent Trading Strategy Team is a platform that automates trading strategies using AI, supporting backtesting and execution.  
The backend is built with Nest.js, PostgreSQL, and Prisma, and the strategy execution server is implemented with FastAPI.  
OpenAI API and KIS API are used to automate the creation and execution of strategies.

---

## ✨ Key Features

- 🤖 AI-based strategy generation using OpenAI  
- 📊 Real-time data collection and order execution via KIS API  
- 🧪 Backtesting and performance analysis of strategies  
- 🧱 Modular execution structure (based on FastAPI)  
- 🗂️ Data management via Prisma ORM  

---

## 🗂️ Project Structure

```
trading-strategy-team/
├── src/                  # Nest.js backend code
├── prisma/               # Prisma schema and migrations
├── static/charts/        # Strategy result chart images
├── tests/                # Test code
├── .env                  # Environment variable config
├── Dockerfile            # Docker config
├── docker-compose.yml    # Docker Compose config
├── run.sh                # Server run script
└── README.md             # README file
```

---

## ⚙️ Setup

### 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Create `.env` file

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

### 3. Install dependencies

```bash
poetry install
```

---

## ▶️ Running the Project

### 1. Start database and server

```bash
docker-compose up -d
```

### 2. Run FastAPI server

```bash
bash run.sh
```

By default, the server runs at `http://localhost:8000`.  
You can view the Swagger docs at `http://localhost:8000/docs`.

---

## 💬 Example Interaction

> **User**: Create a strategy based on RSI  
> **System**: Created a strategy that buys when RSI is below 30 and sells when above 70. Here are the backtest results:  
> ![Chart](./static/charts/sample_result.png)

---

## 🛠 Tech Stack

| Component   | Stack                  |
|------------|------------------------|
| Backend     | Nest.js, FastAPI       |
| Database    | PostgreSQL, Prisma     |
| AI          | OpenAI API             |
| External API| KIS API                |
| Infra       | Docker, Docker Compose |

---

## 🚀 Roadmap

- [ ] Strategy performance visualization dashboard  
- [ ] Personalized strategy recommendation  
- [ ] Strategy templates based on various indicators  
- [ ] Integration with real-time alert system  

---

## 🤝 Contributing

1. Report bugs or request features via issues.  
2. Fork the repo and create a feature branch.  
3. Submit a Pull Request — we’ll review and merge it.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE).
