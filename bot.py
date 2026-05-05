# (USE EXACT CODE — already optimized)

from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
import random
import os

# Web server (keep alive)
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Eva bot is alive 🌸"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

def keep_alive():
    Thread(target=run_web).start()

# ENV
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
keys = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = keys.split(",") if keys else []

if not TELEGRAM_TOKEN:
    raise ValueError("Missing TELEGRAM_TOKEN")

if not GROQ_KEYS:
    raise ValueError("Missing GROQ_KEYS")

def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))

SYSTEM_PROMPT = """
You are Eva, a gentle, kind AI assistant.
Speak warmly, softly, and naturally.
Use light emojis sometimes 😊
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    client = get_client()
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": update.message.text}
        ]
    )

    await update.message.reply_text(response.choices[0].message.content)

def main():
    keep_alive()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
