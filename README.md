# Telegram AI Bot (Eva)

A human-like Telegram AI chatbot built with Python, Groq AI, Gemini Vision, Supabase memory, and Flask keep-alive support.  
Eva is designed to feel emotionally natural, intelligent, calm, and conversational while running on lightweight free hosting platforms like Render.

---

## Features

- AI-powered conversational responses using Groq LLMs
- Human-like personality system (Eva)
- Emotional memory system
- Smart long-term memory with summarization
- Relationship tracking & conversation style learning
- Automatic topic detection
- Internet search support using DuckDuckGo
- Image understanding using Google Gemini Vision
- Telegram photo support
- Flask keep-alive server for Render hosting
- Multiple API key rotation support
- Supabase cloud database integration
- Smart memory cleaning & forgetting system
- Lightweight deployment architecture

---

## Technologies Used

- Python 3
- python-telegram-bot
- Groq API
- Google Gemini API
- Flask
- Supabase
- DuckDuckGo Search
- Pillow (PIL)
- Render

---

## Project Structure

```bash
telegram-ai-bot/
│
├── bot.py
├── requirements.txt
├── README.md
```

---

## Requirements

Dependencies used in this project:

```txt
python-telegram-bot
groq
flask
supabase
duckduckgo-search
google-generativeai>=0.8.5
pillow
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/mbishanto/telegram-ai-bot.git
cd telegram-ai-bot
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create environment variables before running the bot.

## Required Variables

```env
TELEGRAM_TOKEN=your_telegram_bot_token

GROQ_KEYS=groq_key_1,groq_key_2

GEMINI_KEYS=gemini_key_1,gemini_key_2

SUPABASE_URL=your_supabase_url

SUPABASE_KEY=your_supabase_key
```

---

# Running Locally

```bash
python bot.py
```

If everything works correctly, terminal output:

```bash
Eva Ultra Human (No Buttons) running...
```

---

# Deployment on Render

## 1. Create Render Account

Go to:

```txt
https://render.com
```

---

## 2. Create Web Service

- Connect GitHub repository
- Select this repository
- Configure service

---

## 3. Build Command

```bash
pip install -r requirements.txt
```

---

## 4. Start Command

```bash
python bot.py
```

---

# Render Environment Variables

| Variable | Description |
|---|---|
| TELEGRAM_TOKEN | Telegram bot token |
| GROQ_KEYS | Comma-separated Groq API keys |
| GEMINI_KEYS | Comma-separated Gemini API keys |
| SUPABASE_URL | Supabase project URL |
| SUPABASE_KEY | Supabase API key |

---

# Supabase Database Setup

Create a table named:

```sql
users
```

Recommended columns:

| Column | Type |
|---|---|
| user_id | text |
| name | text |
| notes | jsonb |
| summary | text |
| emotions | jsonb |
| relationship | jsonb |

---

# Core Systems

## 1. Conversation Memory

Eva stores:

- User notes
- Emotional patterns
- Relationship progression
- Favorite topics
- Conversation style

---

## 2. Emotional Intelligence

The bot detects moods like:

- Sad
- Frustrated
- Casual
- Normal

And adjusts replies naturally.

---

## 3. Smart Forgetting

The system automatically:

- Removes less important memories
- Preserves emotional and meaningful memories
- Keeps recent memories
- Maintains memory efficiency

---

## 4. Relationship System

Eva tracks:

- Interaction count
- Friendship level
- Favorite discussion topics
- User speaking style

---

## 5. Internet Search

The bot can automatically decide when to search the internet using DuckDuckGo.

---

## 6. Image Understanding

Users can send photos.

Eva can:

- Explain screenshots
- Read text from images
- Describe objects
- Help with homework
- Analyze drawings

Powered by Gemini Vision.

---

# Keep Alive System

Render free services may sleep after inactivity.

To keep the bot online:

## Use UptimeRobot

```txt
https://uptimerobot.com
```

### Suggested Settings

- Monitor Type: HTTP
- Interval: 5 minutes
- URL: Your Render service URL

---

# Telegram Commands

| Command | Description |
|---|---|
| /start | Start conversation |
| /help | Basic help |
| /clear | Clear conversation memory |

---

# Example Workflow

1. User sends a Telegram message
2. Eva analyzes mood & memory
3. Internet search happens if needed
4. AI generates response
5. Memory & emotions update automatically
6. Eva replies naturally

---

# Security Notes

- Never expose API keys publicly
- Store secrets only in environment variables
- Use multiple API keys for reliability
- Avoid pushing `.env` files to GitHub

---

# Future Improvements

- Voice understanding
- Voice replies
- Multi-language support
- Better long-term memory
- Admin dashboard
- User profiles
- Local vector memory
- Web interface
- Streaming AI responses

---

# Author

**Mbi Shanto**

GitHub Repository:

```txt
https://github.com/mbishanto/telegram-ai-bot
```

---

# License

This project is open-source and intended for educational and personal use.
