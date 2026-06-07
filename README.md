# ALYA — Professional Sassy AI Chatbot

**Production-grade Telegram bot** built with Pyrogram + SQLite.

Owner: @yorichiiprime  
Support Channel: @YoriFederation

---

## ✨ Features

### Core Features
- **Sassy AI Chat** — Bestie personality with mood system (8 moods)
- **Image Generation** — Custom API with styles, sizes, steps, SFW/NSFW toggle
- **Premium Plans** — Free / Weekly / Monthly / Yearly with daily limits & expiry
- **Language Choice** — Users can switch between **English** and **Hinglish**
- **Force Join System** — Multi-channel verification
- **Broadcast System** — Media + text with preview
- **Media Vault** — Random pics & stickers on request
- **Anti-Jailbreak + Rate Limit** — Professional protection
- **Group Support** — Mention `@Yourr_alyabot` anywhere
- **Telegram Stars Payments** — All payments go to owner account

### Professional Touches
- Thinking simulation (`💭 Thinking...`)
- Natural typing effect before replies
- Clean branded responses
- Full SQLite database with export/import (perfect for Render)
- Owner dashboard with inline keyboards
- Analytics & payment tracking

---

## 🚀 Quick Start

### 1. Setup Environment

Copy `.env.example` to `.env` and fill in your values:

```env
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
OWNER_ID=7728424218

GROQ_KEY_1=...
GROQ_KEY_2=...
GROQ_KEY_3=...

OPENROUTER_KEY_1=...
OPENROUTER_KEY_2=...
OPENROUTER_KEY_3=...
```

### 2. Install Dependencies

```bash
cd bot
pip install -r requirements.txt
```

### 3. Run the Bot

```bash
python main.py
```

---

## 📁 File Structure

```
bot/
├── main.py          # Main bot logic + handlers
├── config.py        # Configuration & constants
├── database.py      # SQLite + export/import
├── services.py      # AI, Image, Mood logic
├── keyboards.py     # All keyboards
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🛠️ Important Commands

### User Commands
- `/start` — Welcome + main menu
- `/help` — Command list
- `/profile` — User stats
- `/myplan` — Current plan usage
- `/language` — Switch between English / Hinglish

### Owner Commands (Admin Keyboard)
- `📤 Export Users` — Download all users as .txt
- `📥 Import Users` — Restore users after restart
- `📢 Broadcast` — Send to all users
- `💎 Give Plan` — Grant premium plans

---

## 💎 Payment System

All **Telegram Stars** payments go directly to your account (`@yorichiiprime`).

Users can support via the `/support` command or inline buttons.

---

## 🔄 Render / Hosting Notes

SQLite database resets on Render restart.

**Solution built-in:**
- Use `/export` to download user list
- Use `/import` to restore users from .txt file

---

## 📝 License

Private production bot for @yorichiiprime

---

**Made with ❤️ for a professional Telegram contest experience.**