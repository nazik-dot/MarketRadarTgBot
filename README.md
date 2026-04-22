# 📊 MarketRadar Bot

A Telegram bot for tracking cryptocurrency, stocks, and precious metals using the Alpha Vantage API.

The bot lets you search market prices, view asset data, and manage your personal watchlist.

---

## ⚙️ Technical stack

![Python](https://img.shields.io/badge/Python-3.11+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Aiogram](https://img.shields.io/badge/Aiogram-v3.1-4ba94b?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Telegram-Bot2.0-2CA5E0?style=for-the-badge&logo=telegram&logoColor=ffffff)
![API](https://img.shields.io/badge/Alpha_Vantage-API-orange?style=for-the-badge)

---

## 📄 Requirements

> - ⚙️ Python 3.11+
> - 📊 Alpha Vantage API key
> - 🤖 Telegram Bot token

---

## 🚀 How to install

1. Clone the repository 
```bash
git clone https://github.com/nazik-dot/MarketRadarTgBot.git

cd MarketRadarTgBot
```
2. Create virtual environment 
```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```
3. Create `.env` file with next variables:
```dotenv
TOKEN=your_telegram_token
ALPHA_VANTAGE_KEY=your_api_key
```
4. Run `python main.py`

---
## 👥 Team
- [Nazar](https://github.com/nazik-dot) — Team Lead, responsible for the overall direction of the project
- [Serafym](https://github.com/serafymba-alt) — Developer, focused on documentation and interface part
- [Denys](https://github.com/denysbilykgit) — Developer, responsible for backend logic and services
- [Zomif](https://github.com/zomif) — Developer, involved in backend development

-  Team — collaborative development of `handlers` module
---
## 📌 Notes
- Project completed as a team assignment.
- Core functionality implemented and tested.
- Bot is fully functional for market tracking and watchlist management.