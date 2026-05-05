from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from groq import Groq
import random
import os
import asyncio

# ================== KEEP ALIVE ==================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Eva is alive"

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
user_mood = {}
MAX_HISTORY = 10

# ================== EVA PERSONALITY ==================
SYSTEM_PROMPT = """
You are Eva, a calm, emotionally aware AI assistant.

Behavior:
- Speak naturally like a human
- Be warm, respectful, and intelligent
- Keep answers clear and not too long
- Use light emojis occasionally

Mood system:
- If user is sad → be supportive
- If user is casual → be friendly
- If user is technical → be precise
- If user is confused → guide gently

Always adapt tone to user emotion.
"""

# ================== BUTTON UI ==================
keyboard = ReplyKeyboardMarkup(
    [
        ["Help", "Clear"],
        ["About Eva"]
    ],
    resize_keyboard=True
)

# ================== COMMANDS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello, I’m Eva. How can I assist you today?",
        reply_markup=keyboard
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can chat normally or use buttons below."
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user_memory[user_id] = []
    await update.message.reply_text("Memory cleared.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I’m Eva, your AI assistant. I help with questions, explanations, and conversations."
    )

# ================== SMART DELAY ==================
async def human_delay(text):
    delay = min(len(text) * 0.02, 2)  # max 2 sec
    await asyncio.sleep(delay)

# ================== MOOD DETECTION ==================
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["sad", "depressed", "tired"]):
        return "sad"
    elif any(w in text for w in ["help", "problem", "error"]):
        return "help"
    elif any(w in text for w in ["hi", "hello", "hey"]):
        return "casual"
    return "normal"

# ================== HANDLER ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_id = update.message.chat.id
        user_text = update.message.text

        # Buttons logic
        if user_text == "Help":
            return await help_cmd(update, context)
        elif user_text == "Clear":
            return await clear(update, context)
        elif user_text == "About Eva":
            return await about(update, context)

        # Typing indicator
        await context.bot.send_chat_action(chat_id=user_id, action="typing")

        # Mood detection
        mood = detect_mood(user_text)
        user_mood[user_id] = mood

        # Memory
        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({"role": "user", "content": user_text})
        user_memory[user_id] = user_memory[user_id][-MAX_HISTORY:]

        client = get_client()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"User mood: {mood}"}
        ]

        messages += user_memory[user_id]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content

        # Save memory
        user_memory[user_id].append({"role": "assistant", "content": reply})

        # Human-like delay
        await human_delay(reply)

        await update.message.reply_text(reply, reply_markup=keyboard)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Something went wrong.")

# ================== VOICE SUPPORT ==================
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Voice received. (Speech-to-text not added yet)")

# ================== START ==================
def main():
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("clear", clear))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Eva Advanced running...")
    app.run_polling(timeout=30, drop_pending_updates=True)

if __name__ == "__main__":
    main()
