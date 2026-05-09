from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS
import google.generativeai as genai
from PIL import Image
import random
import os
import json
import re
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

gemini_keys = os.getenv("GEMINI_KEYS", "")
GEMINI_KEYS = gemini_keys.split(",") if gemini_keys else []

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("Missing TELEGRAM_TOKEN")

if not GROQ_KEYS:
    raise ValueError("Missing GROQ_KEYS")

if not GEMINI_KEYS:
    raise ValueError("Missing GEMINI_KEYS")

def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))

def get_gemini_model():

    api_key = random.choice(GEMINI_KEYS)

    genai.configure(
        api_key=api_key
    )

    return genai.GenerativeModel(
        "gemini-1.5-flash-latest"
    )

# ================== MEMORY ==================
user_memory = {}
MAX_HISTORY = 1000

# ================== DATABASE ==================
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

def get_user(user_id):

    response = supabase.table("users") \
        .select("*") \
        .eq("user_id", user_id) \
        .execute()

    data = response.data

    if data:
        return {
            "name": data[0].get("name", ""),
            "notes": data[0].get("notes", []),
            "summary": data[0].get("summary", ""),
            "emotions": data[0].get("emotions", [])
        }

    return {
        "name": "",
        "notes": [],
        "summary": "",
        "emotions": []
    }

def save_user(user_id, profile):

    supabase.table("users").upsert({
        "user_id": user_id,
        "name": profile["name"],
        "notes": profile["notes"],
        "summary": profile.get("summary", ""),
        "emotions": profile.get("emotions", [])
    }).execute()

# ================== WEB SEARCH ==================

def web_search(query):

    results_text = ""

    try:

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

        for r in results:

            title = r.get("title", "")
            body = r.get("body", "")

            results_text += f"""
Title: {title}

Snippet: {body}

"""

    except Exception as e:

        results_text = f"Search failed: {str(e)}"

    return results_text

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

Internet:
- If internet search results are available,
use them naturally and accurately.

Goal:
Make the user feel like they’re talking to someone real, not a machine.
"""

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

# ================== HUMAN TOUCH ==================
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
        "Hi… I’m Eva. What’s on your mind?"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You can just talk to me."
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.chat.id)

    user_memory[user_id] = []

    profile = {
        "name": "",
        "notes": [],
        "summary": "",
        "emotions": []
    }

    save_user(user_id, profile)

    await update.message.reply_text(
        "Conversation cleared."
    )

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

        await context.bot.send_chat_action(
            chat_id=user_id,
            action="typing"
        )

        mood = detect_mood(user_text)

        if user_id not in user_memory:
            user_memory[user_id] = []

        user_memory[user_id].append({
            "role": "user",
            "content": user_text
        })

        user_memory[user_id] = user_memory[user_id][-MAX_HISTORY:]

        profile = get_user(user_id)

        client = get_client()

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        messages += user_memory[user_id]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = response.choices[0].message.content

        reply = add_human_touch(reply)

        user_memory[user_id].append({
            "role": "assistant",
            "content": reply
        })

        save_user(user_id, profile)

        await update.message.reply_text(
            reply
        )

    except Exception as e:
        import traceback
        traceback.print_exc()

        await update.message.reply_text(
            f"Error: {str(e)}"
        )

# ================== IMAGE UNDERSTANDING ==================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        user_id = str(update.message.chat.id)

        photo = update.message.photo[-1]

        await context.bot.send_chat_action(
            chat_id=user_id,
            action="typing"
        )

        file = await context.bot.get_file(
            photo.file_id
        )

        image_path = f"{user_id}.jpg"

        await file.download_to_drive(
            image_path
        )

        img = Image.open(image_path)

        model = get_gemini_model()

        caption = (
            update.message.caption
            if update.message.caption
            else ""
        )

        vision_prompt = f"""
You are Eva, a warm and intelligent AI assistant.

Analyze this image naturally.

If it contains:
- homework → solve it
- screenshot → explain it
- text → read it
- drawing → describe it
- object → identify it

User message:
{caption}

Be conversational and human-like.
"""

        response = model.generate_content([
            vision_prompt,
            img
        ])

        reply = response.text

        await update.message.reply_text(
            reply
        )

    except Exception as e:

        await update.message.reply_text(
            f"Image Error: {str(e)}"
        )

# ================== VOICE ==================
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Voice received."
    )

# ================== START ==================
def main():
    keep_alive()

    app = ApplicationBuilder().token(
        TELEGRAM_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_cmd)
    )

    app.add_handler(
        CommandHandler("clear", clear)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    app.add_handler(
        MessageHandler(
            filters.VOICE,
            handle_voice
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            handle_photo
        )
    )

    print("Eva Ultra Human (No Buttons) running...")

    app.run_polling(
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
