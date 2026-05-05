# Telegram AI Bot (Eva)

A Telegram AI chatbot built using Python, Groq API, and deployed on Render.
The bot provides natural, human-like responses with a lightweight architecture and free hosting.

---

## Features

* AI-powered responses using Groq language models
* Short-term conversation memory for better context
* Custom personality (Eva: calm, clear, human-like assistant)
* Multiple API key rotation for reliability
* Free deployment using Render
* Keep-alive system using Flask to prevent service sleep

---

## Tech Stack

* Python 3
* python-telegram-bot
* Groq API
* Flask
* Render (cloud hosting)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/mbishanto/telegram-ai-bot.git
cd telegram-ai-bot
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Environment variables

Set the following environment variables:

```
TELEGRAM_TOKEN=your_telegram_bot_token
GROQ_KEYS=key1,key2,key3
```

---

### 4. Run the bot locally

```bash
python bot.py
```

---

## Deployment (Render)

1. Go to https://render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Use the following settings:

**Build Command**

```
pip install -r requirements.txt
```

**Start Command**

```
python bot.py
```

---

### Environment Variables (Render)

| Key            | Value                         |
| -------------- | ----------------------------- |
| TELEGRAM_TOKEN | Your Telegram bot token       |
| GROQ_KEYS      | Comma-separated Groq API keys |

---

## Keep Service Active

Render free services may sleep after inactivity.

To prevent this:

* Use https://uptimerobot.com
* Create an HTTP monitor
* Set interval to 5 minutes
* Use your Render service URL

---

## How It Works

1. User sends a message in Telegram
2. Bot receives the message
3. Message is sent to Groq AI model
4. AI generates a response
5. Bot replies to the user

---

## Notes

* Keep your API keys and tokens private
* Use multiple Groq keys to avoid rate limits
* Free hosting may require uptime monitoring

---

## Future Improvements

* Long-term memory with database
* Command support (/start, /help)
* Multi-language support
* Voice input/output

---

## Author

Mbi Shanto

---

## License

This project is open source and available for personal and educational use.
