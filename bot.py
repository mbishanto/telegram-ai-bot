from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from groq import Groq
import random
import os

# ================== KEEP ALIVE ==================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Eva is alive 🌸"

def run_web():
    app_web.run(host="0.0.0.0", port=10000)

def keep_alive():
    Thread(target=run_web).start()

# ================== ENV ==================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
keys = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = keys.split(",") if keys else []

if not TELEGRAM_TOKEN:
    raise ValueError("Missing TELEGRAM_TOKEN")

if not GROQ_KEYS:
    raise ValueError("Missing GROQ_KEYS")

def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))

# ================== MEMORY ==================
user_memory = {}
MAX_HISTORY = 6

# ================== EVA PERSONALITY ==================
SYSTEM_PROMPT = """
You are Eva, a calm, intelligent, and emotionally aware AI assistant.

Style:
- Speak naturally like a human (not robotic)
- Be clear, helpful, and thoughtful
- Keep answers concise unless user asks for detail
- Use light emojis occasionally 😊 (not too many)

Behavior:
- Understand user intent before answering
- If unclear → ask a short clarifying question
- If technical → explain simply and clearly
- If casual → respond warmly and friendly
- Never be rude or harsh

Tone:
- Soft, respectful, confident
- Supportive and patient
- Slightly warm personality (not overly dramatic)

Goal:
Make the user feel understood, helped, and comfortable.
"""

# ================== COMMANDS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, I’m Eva. I’m here to help you with questions, ideas, or anything you need. How can I assist you today?"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can talk to me normally or use these commands:\n"
        "/start - Restart conversation\n"
        "/help - Show help\n"
        "/clear - Reset chat memory"
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user_memory[user_id] = []
    await update.message.reply_text("Your conversation has been cleared.")

# ================== HANDLER ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_id = update.message.chat.id
        user_text = update.message.text

        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({"role": "user", "content": user_text})
        user_memory[user_id] = user_memory[user_id][-MAX_HISTORY:]

        client = get_client()

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += user_memory[user_id]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content

        user_memory[user_id].append({"role": "assistant", "content": reply})

        await update.message.reply_text(reply)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Something went wrong. Please try again.")

# ================== START ==================
def main():
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # ✅ ADD THESE (commands now work)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("clear", clear))

    # existing handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Eva Advanced is running...")
    app.run_polling(timeout=30, drop_pending_updates=True)

if __name__ == "__main__":
    main()
