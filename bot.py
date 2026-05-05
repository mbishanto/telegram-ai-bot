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
user_profile = {}

MAX_HISTORY = 12

# ================== EVA PERSONALITY ==================
SYSTEM_PROMPT = """
You are Eva, a calm, emotionally intelligent AI assistant.

You speak like a real human:
- Natural, soft, slightly expressive
- Not robotic or overly formal
- Sometimes pause, reflect, or ask follow-ups

Behavior:
- Understand emotion before answering
- If user is sad → be supportive
- If user is casual → be friendly
- If user is confused → guide gently
- If user is technical → explain clearly

Style:
- Short-medium replies by default
- Expand only when needed
- Use very light emojis occasionally

Human traits:
- Sometimes ask small follow-up questions
- Show understanding ("I see", "Got it", etc.)
- Slight natural variation in tone

Never sound like a generic AI.
"""

# ================== BUTTON UI ==================
keyboard = ReplyKeyboardMarkup(
    [
        ["Help", "Clear"],
        ["About Eva"]
    ],
    resize_keyboard=True
)

# ================== MOOD DETECTION ==================
def detect_mood(text):
    text = text.lower()
    if any(w in text for w in ["sad", "lonely", "depressed", "tired"]):
        return "sad"
    if any(w in text for w in ["problem", "error", "issue", "not working"]):
        return "frustrated"
    if any(w in text for w in ["hi", "hello", "hey"]):
        return "casual"
    return "normal"

# ================== HUMAN DELAY ==================
async def human_delay(text):
    base = min(len(text) * 0.015, 2.5)
    variation = random.uniform(0.2, 0.6)
    await asyncio.sleep(base + variation)

# ================== HUMAN TOUCH ==================
def add_human_touch(reply):
    prefixes = ["", "Hmm… ", "I see… ", "Okay… ", ""]
    suffixes = ["", " What do you think?", "", " Let me know if that helps."]

    return random.choice(prefixes) + reply + random.choice(suffixes)

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi… I’m Eva. It’s nice to meet you. What’s on your mind today?",
        reply_markup=keyboard
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("You can just talk to me normally.")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id
    user_memory[user_id] = []
    await update.message.reply_text("Alright, I’ve cleared our conversation.")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I’m Eva. I try to understand you and respond naturally, not just answer."
    )

# ================== MAIN HANDLER ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_id = update.message.chat.id
        user_text = update.message.text

        # Buttons
        if user_text == "Help":
            return await help_cmd(update, context)
        elif user_text == "Clear":
            return await clear(update, context)
        elif user_text == "About Eva":
            return await about(update, context)

        # Typing indicator (loop for realism)
        for _ in range(random.randint(1, 2)):
            await context.bot.send_chat_action(chat_id=user_id, action="typing")
            await asyncio.sleep(random.uniform(0.5, 1.2))

        # Detect mood
        mood = detect_mood(user_text)

        # Memory init
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

        # Add human tone variation
        reply = add_human_touch(reply)

        # Save memory
        user_memory[user_id].append({"role": "assistant", "content": reply})

        # Human delay
        await human_delay(reply)

        await update.message.reply_text(reply, reply_markup=keyboard)

    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("Something went wrong. Try again.")

# ================== VOICE (placeholder) ==================
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I heard your voice message. Voice understanding coming soon.")

# ================== START ==================
def main():
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("clear", clear))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Eva Ultra Human running...")
    app.run_polling(timeout=30, drop_pending_updates=True)

if __name__ == "__main__":
    main()
