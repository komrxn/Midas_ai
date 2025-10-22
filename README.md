# 🤖 Accountant Bot

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**AI-powered expense tracker for Telegram with voice input, smart parsing, and intelligent reports**

[Features](#-features) • [Quick Start](#-quick-start) • [Commands](#-commands) • [Deploy](#-deploy) • [Demo](#-demo)

</div>

---

## ✨ Features

🎤 **Voice & Text Input** — Just speak or type naturally, AI handles the rest  
🧠 **Smart Parsing** — Automatically extracts amount, currency, category, and description  
⚡ **Instant Corrections** — Fix details inline with simple commands like `категория: такси` or `amount: 15.5`  
🌍 **Multi-language** — Full support for Russian and English  
💱 **Multi-currency** — Track expenses in UZS, USD, EUR, RUB with per-user defaults  
📊 **AI Reports** — Generate custom summaries with `/report <your question>`  
🔍 **Smart Memory** — AI remembers context and provides intelligent insights  
🏥 **Health Monitoring** — Built-in system checks with `/health`  

## 🏗️ Tech Stack

- **Bot Framework**: Python 3.11+ with aiogram
- **AI**: OpenAI GPT-4 for parsing and reports
- **Database**: Supabase (PostgreSQL)
- **Cache**: Redis
- **Deployment**: Systemd service on Ubuntu/Debian

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Telegram Bot Token ([get it from @BotFather](https://t.me/botfather))
- OpenAI API Key ([get it here](https://platform.openai.com/api-keys))
- Supabase account ([create free](https://supabase.com))
- Redis instance (local or managed)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/accountant-bot.git
cd accountant-bot
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize database**

Run this SQL in your Supabase SQL Editor:
```sql
-- expenses table
create table if not exists public.expenses (
  id bigint generated always as identity primary key,
  user_id text not null,
  amount numeric(18,2) not null check (amount > 0),
  currency text not null default 'uzs',
  category text not null,
  description text,
  expense_date timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists expenses_user_date_idx on public.expenses (user_id, expense_date desc);
create index if not exists expenses_category_idx on public.expenses (category);

-- user_settings table
create table if not exists public.user_settings (
  user_id text primary key,
  language text not null default 'ru',
  currency text not null default 'uzs',
  updated_at timestamptz not null default now()
);

alter table public.expenses disable row level security;
alter table public.user_settings disable row level security;
```

5. **Run the bot**
```bash
python -m app.main
```

## ⚙️ Configuration

Create a `.env` file with the following variables:
```dotenv
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
REDIS_URL=redis://127.0.0.1:6379/0
DEFAULT_CURRENCY=uzs
```

## 💬 Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize bot, choose language and default currency |
| `/setlang` | Change interface language (ru/en) |
| `/setcurrency` | Change default currency (uzs/usd/eur/rub) |
| `/report <question>` | Generate AI-powered expense report (default: last 30 days) |
| `/health` | Check system status (OpenAI, Redis, Supabase) |

## 📝 Usage Examples

**Adding expense (text):**
```
50000 taxi to airport
```

**Adding expense (voice):**
🎤 *"Пятьдесят тысяч сум на такси до аэропорта"*

**Quick corrections:**
```
категория: транспорт
amount: 55000
description: taxi + tip
```

**Smart reports:**
```
/report show me food expenses for last week
/report what did I spend most on this month?
/report compare this month to last month
```

## 🚀 Deploy

Detailed deployment guide for production: **[docs/deploy.md](docs/deploy.md)**

Quick deploy on Ubuntu/Debian:
```bash
# Clone and setup
cd /opt
git clone https://github.com/yourusername/accountant-bot.git
cd accountant-bot

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure systemd service
sudo cp accountant-bot.service /etc/systemd/system/
sudo systemctl enable accountant-bot
sudo systemctl start accountant-bot
```

## 🎬 Demo

> 🎥 *Coming soon: video demo and screenshots*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [aiogram](https://github.com/aiogram/aiogram)
- Powered by [OpenAI GPT-4](https://openai.com)
- Database by [Supabase](https://supabase.com)

---

<div align="center">

**Made with ❤️ for smart expense tracking**

⭐ Star this repo if you find it useful!

</div>