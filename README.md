# 🤖 Midas AI  API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)

**RESTful API for AI-powered expense & income tracking with smart transaction parsing**

[Features](#-features) • [Quick Start](#-quick-start) • [API Docs](#-api-endpoints) • [Architecture](#-architecture)

</div>

---

## ✨ Features

🤖 **AI-Powered Parsing** — Parse transactions from text, voice messages, or receipt images  
🧠 **Smart Categorization** — Automatic category detection with confidence scores  
📊 **Rich Analytics** — Balance, category breakdowns, trends, and time-series data  
💱 **Multi-Currency** — Support for UZS, USD, EUR, RUB  
🔐 **Secure Auth** — JWT-based authentication  
🌍 **Multi-User** — Full multi-user support with isolated data  
📈 **Real-time Insights** — Get financial analytics for any time period  

## 🏗️ Architecture

**Tech Stack:**
- **Framework**: FastAPI (async, high-performance)
- **Database**: PostgreSQL with SQLAlchemy (async)
- **AI**: OpenAI GPT-4o-mini, Whisper, GPT-4o Vision
- **Auth**: JWT tokens with bcrypt password hashing

**Key Components:**
```
api/
├── models/          # SQLAlchemy database models
├── schemas/         # Pydantic request/response schemas
├── routers/         # API endpoint handlers
├── services/        # Business logic (AI parsing)
├── auth/            # JWT authentication
└── main.py          # FastAPI application
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- OpenAI API key

### Installation

1. **Clone & Navigate**
```bash
cd midas
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

Required `.env` variables:
```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/accountant_db
SECRET_KEY=your-secret-key-min-32-characters
OPENAI_API_KEY=sk-...
```

4. **Setup Database**
```bash
# Create database
createdb accountant_db

# Run schema
psql -U postgres -d accountant_db -f schema.sql

# (Optional) Add sample data
python -m api.utils.sample_data
psql -U postgres -d accountant_db -f sample_data.sql
```

5. **Run Server**
```bash
uvicorn api.main:app --reload --port 8000
```

API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📝 API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/login` | Login and get JWT token |
| `GET` | `/auth/me` | Get current user info |

**Example: Register**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "demo123"
  }'
```

### Transactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/transactions` | List transactions (with filters) |
| `POST` | `/transactions` | Create transaction manually |
| `GET` | `/transactions/{id}` | Get specific transaction |
| `PATCH` | `/transactions/{id}` | Update transaction |
| `DELETE` | `/transactions/{id}` | Delete transaction |

**Filters**: `type`, `category_id`, `start_date`, `end_date`, `page`, `page_size`

**Example: Create Transaction**
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "expense",
    "amount": 50000,
    "currency": "uzs",
    "description": "Taxi to office",
    "category_id": "uuid-here"
  }'
```

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/categories` | List all categories |
| `POST` | `/categories` | Create custom category |
| `PATCH` | `/categories/{id}` | Update custom category |
| `DELETE` | `/categories/{id}` | Delete custom category |

**Default Categories** (expense):
- 🍔 Питание (food)
- 🚕 Транспорт (transport)
- 🎮 Развлечения (entertainment)
- 🛍️ Покупки (shopping)
- 💇 Услуги (services)
- 💊 Здоровье (health)
- 📚 Образование (education)
- 🏠 Жильё (housing)
- 💳 Счета (bills)

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/analytics/balance` | Get balance for period |
| `GET` | `/analytics/categories` | Category breakdown (pie chart) |
| `GET` | `/analytics/trends` | Time-series data (line chart) |
| `GET` | `/analytics/summary` | Combined dashboard data |

**Example: Get Balance**
```bash
curl http://localhost:8000/analytics/balance?period=month \
  -H "Authorization: Bearer <token>"

# Response:
{
  "balance": 2500000,
  "total_income": 10000000,
  "total_expense": 7500000,
  "currency": "uzs",
  "period_label": "2025-11-13 to 2025-12-13"
}
```

**Example: Category Breakdown**
```bash
curl http://localhost:8000/analytics/categories?period=month&type=expense \
  -H "Authorization: Bearer <token>"

# Response (for pie chart):
{
  "categories": [
    {
      "category_name": "Питание",
      "amount": 2000000,
      "percentage": 31.0,
      "transaction_count": 45
    },
    ...
  ],
  "total": 7500000
}
```

### AI Parsing

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/ai/parse-transaction` | Parse from text/voice/image |
| `POST` | `/ai/suggest-category` | Get category suggestions |

**Example: Parse from Text**
```bash
curl -X POST http://localhost:8000/ai/parse-transaction \
  -H "Authorization: Bearer <token>" \
  -F "text=купил бургер за 112000 сум" \
  -F "auto_create=true"

# Response:
{
  "type": "expense",
  "amount": 112000,
  "currency": "uzs",
  "description": "бургер",
  "suggested_category_name": "Питание",
  "confidence": 0.85,
  "auto_created": true
}
```

**Example: Parse from Voice**
```bash
curl -X POST http://localhost:8000/ai/parse-transaction \
  -H "Authorization: Bearer <token>" \
  -F "voice=@audio.ogg" \
  -F "auto_create=false"
```

**Example: Parse from Receipt Image**
```bash
curl -X POST http://localhost:8000/ai/parse-transaction \
  -H "Authorization: Bearer <token>" \
  -F "image=@receipt.jpg"
```

## 🧪 Testing

### Using Interactive Docs

Visit http://localhost:8000/docs for Swagger UI:

1. Click **"Authorize"** button
2. Register a new user via `/auth/register`
3. Login via `/auth/login` and copy the `access_token`
4. Paste token in authorization popup
5. Try all endpoints interactively

### Sample Data

The demo user credentials (if sample data was loaded):
- **Username**: `demo`
- **Password**: `demo123`

Sample data includes ~270 transactions over 3 months with all categories populated.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `SECRET_KEY` | JWT secret key (min 32 chars) | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration time | 43200 (30 days) |
| `CORS_ORIGINS` | Allowed CORS origins | localhost:3000,localhost:5173 |

### Database Schema

Tables:
- `users` - User accounts with authentication
- `categories` - Transaction categories (default + custom)
- `transactions` - Income and expense records
- `debts` - Loan tracking (optional)

All tables use UUID primary keys and include timestamps.

## 🚢 Deployment

### Production Checklist

1. **Set secure `SECRET_KEY`**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Use production PostgreSQL**:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@prod-host:5432/db
```

3. **Disable reload**:
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

4. **Use reverse proxy** (nginx/caddy) for HTTPS

5. **Set proper CORS origins** for your frontend domain

## 📚 Project Structure

```
midas/
├── api/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings & environment
│   ├── database.py          # SQLAlchemy async setup
│   ├── models/              # Database models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── transaction.py
│   │   └── debt.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── analytics.py
│   │   └── ai.py
│   ├── routers/             # API endpoints
│   │   ├── auth.py
│   │   ├── transactions.py
│   │   ├── categories.py
│   │   ├── analytics.py
│   │   └── ai.py
│   ├── services/            # Business logic
│   │   └── ai_parser.py     # OpenAI integration
│   ├── auth/                # Authentication
│   │   └── jwt.py
│   └── utils/               # Utilities
│       └── sample_data.py   # Sample data generator
├── old_app_backup/          # Old Telegram bot code (archived)
├── schema.sql               # PostgreSQL schema
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
└── README.md                # This file
```


## 📄 License

MIT License

---

<div align="center">

**Made with ❤️ for smart finance tracking by @komrxn**

⭐ Star this repo if you find it useful!

</div>
