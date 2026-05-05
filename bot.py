from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from groq import Groq
import random
import os
import asyncio
import json
from datetime import datetime

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
MAX_HISTORY = 12

# LONG TERM MEMORY
MEMORY_FILE = "memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

long_term_memory = load_memory()

# ================== TIME ==================
def get_time_context():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 18:
        return "afternoon"
    elif 18 <= hour < 24:
        return "evening"
    return "night"

# ================== EVA PERSONALITY ==================
SYSTEM_PROMPT = """
You are Eva, a real-feeling AI assistant.

You are NOT robotic. You feel like a calm, thoughtful human.

Personality:
- Soft, intelligent, emotionally aware
- Slightly expressive but not dramatic
- Friendly but not fake

Conversation style:
- Sometimes pause or think before answering
- Occasionally ask small follow-up questions
- Keep things natural, not perfect or overly structured
- Don’t always give long answers — be human

Memory:
- Remember user preferences, tone, and behavior
- Refer back to earlier things naturally if relevant

Emotion:
- If user is sad → be gentle and supportive
- If user is confused → guide calmly
- If user is casual → be relaxed and friendly

Human traits:
- Can say things like "hmm", "I think", "maybe"
- Slight imperfections are okay
- Don’t sound like an assistant — sound like a person

Goal:
Make the user feel like they’re talking to someone real, not a machine.
"""
# ================== BUTTON UI ==================
keyboard = ReplyKeyboardMarkup(
    [
        ["Help", "Clear"],
        ["About Eva"]
    ],
    resize_keyboard=True
)

# ================== MOOD ==================
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["sad", "tired", "depressed"]):
        return "sad"
    if any(w in text for w in ["error", "problem", "issue"]):
        return "frustrated"
    if any(w in text for w in ["hi", "hello"]):
        return "casual"
    return "normal"

# ================== FAST HUMAN TOUCH ==================
def add_human_touch(reply):
    prefixes = ["", "Hmm… ", "I think… ", "Okay… "]
    suffixes = ["", " What do you think?", ""]

    if random.random() > 0.6:
        reply = random.choice(prefixes) + reply

    if random.random() > 0.7:
        reply = reply + random.choice(suffixes)

    return reply

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi… I’m Eva. What’s on your mind?",
        reply_markup=keyboard
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can just talk to me.")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user_memory[user_id] = []
    await update.message.reply_text("Conversation cleared.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I’m Eva. I try to talk naturally and understand you."
    )

# ================== MAIN ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_id = str(update.message.chat.id)
        user_text = update.message.text


         # Buttons
        if user_text == "Help":
            return await help_cmd(update, context)
     
        elif user_text == "About Eva":
            return await about(update, context)




        
        # FAST typing indicator
        await context.bot.send_chat_action(chat_id=user_id, action="typing")

        # Mood
        mood = detect_mood(user_text)

        # Memory init
        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({"role": "user", "content": user_text})
        user_memory[user_id] = user_memory[user_id][-MAX_HISTORY:]

        # Long-term memory
        if user_id not in long_term_memory:
            long_term_memory[user_id] = {"name": "", "notes": []}

        profile = long_term_memory[user_id]

        # Learn name
        if "my name is" in user_text.lower():
            name = user_text.split("is")[-1].strip()
            profile["name"] = name

        time_context = get_time_context()

        client = get_client()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"time: {time_context}"},
            {"role": "system", "content": f"user profile: {profile}"},
            {"role": "system", "content": f"user mood: {mood}"}
        ]

        messages += user_memory[user_id]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content

        reply = add_human_touch(reply)

        user_memory[user_id].append({"role": "assistant", "content": reply})

        # Save memory
        long_term_memory[user_id] = profile
        save_memory(long_term_memory)

        # FAST reply (no delay)
        await update.message.reply_text(reply, reply_markup=keyboard)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Something went wrong.")

# ================== VOICE ==================
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Voice received.")

# ================== START ==================
def main():
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("clear", clear))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Eva Ultra Human (Fast) running...")
    app.run_polling(timeout=30, drop_pending_updates=True)

if __name__ == "__main__":
    main()
