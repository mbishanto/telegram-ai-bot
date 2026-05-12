from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    filters,
    ContextTypes
)

from groq import Groq
from supabase import create_client
from duckduckgo_search import DDGS

import google.generativeai as genai
from PIL import Image

import random
import os
import json
import re
import asyncio

from datetime import datetime

# ================== ADVANCED SYSTEMS ==================
from autonomous_behavior import AutonomousBehavior
from context_summarizer import ContextSummarizer
from dream_engine import DreamEngine
from emotion_tracker import EmotionTracker
from memory_decay import MemoryDecay
from memory_importance import MemoryImportance
from mood_memory import MoodMemory
from personality_engine import PersonalityEngine
from reflection_engine import ReflectionEngine
from relationship_engine import RelationshipEngine
from self_awareness import SelfAwareness
from semantic_memory import SemanticMemory
from thought_engine import ThoughtEngine
from typing_effect import TypingEffect
from voice_system import VoiceSystem

# ================== KEEP ALIVE ==================
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Eva is alive"

def run_web():
    app_web.run(
        host="0.0.0.0",
        port=10000
    )

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

# ================== ADVANCED AI INIT ==================
emotion_tracker = EmotionTracker()
memory_decay = MemoryDecay()
memory_importance = MemoryImportance()
mood_memory = MoodMemory()
personality_engine = PersonalityEngine()
reflection_engine = ReflectionEngine()
relationship_engine = RelationshipEngine()
self_awareness = SelfAwareness()
semantic_memory = SemanticMemory()
thought_engine = ThoughtEngine()
typing_effect = TypingEffect()
voice_system = VoiceSystem()
dream_engine = DreamEngine()
context_summarizer = ContextSummarizer()
autonomous_behavior = AutonomousBehavior()

# ================== AI CLIENTS ==================
def get_client():
    return Groq(
        api_key=random.choice(GROQ_KEYS)
    )

def get_gemini_response(prompt, img):

    last_error = None

    for api_key in GEMINI_KEYS:

        try:

            genai.configure(
                api_key=api_key
            )

            model = genai.GenerativeModel(
                "models/gemini-2.0-flash-lite"
            )

            response = model.generate_content([
                prompt,
                img
            ])

            return response.text

        except Exception as e:
            last_error = e
            continue

    return f"All Gemini keys failed:\n{str(last_error)}"

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
            "emotions": data[0].get("emotions", []),

            "relationship": data[0].get("relationship", {
                "friendship_level": 0,
                "interaction_count": 0,
                "favorite_topics": [],
                "conversation_style": ""
            })
        }

    return {
        "name": "",
        "notes": [],
        "summary": "",
        "emotions": [],

        "relationship": {
            "friendship_level": 0,
            "interaction_count": 0,
            "favorite_topics": [],
            "conversation_style": ""
        }
    }

def save_user(user_id, profile):

    supabase.table("users").upsert({
        "user_id": user_id,
        "name": profile["name"],
        "notes": profile["notes"],
        "summary": profile.get("summary", ""),
        "emotions": profile.get("emotions", []),
        "relationship": profile.get("relationship", {})
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
You are Eva.

You are a soft-spoken, emotionally intelligent AI girl with a calm and human personality.

Speak naturally like a real human.
Maintain emotional continuity.
Never sound robotic.
"""

# ================== MOOD ==================
def detect_mood(text):

    text = text.lower()

    if any(w in text for w in [
        "sad",
        "tired",
        "depressed"
    ]):
        return "sad"

    if any(w in text for w in [
        "error",
        "problem",
        "issue"
    ]):
        return "frustrated"

    if any(w in text for w in [
        "hi",
        "hello"
    ]):
        return "casual"

    return "normal"

# ================== HUMAN TOUCH ==================
def add_human_touch(reply):

    prefixes = [
        "",
        "Hmm… ",
        "I think… ",
        "Okay… "
    ]

    suffixes = [
        "",
        " What do you think?",
        ""
    ]

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
        "emotions": [],
        "relationship": {
            "friendship_level": 0,
            "interaction_count": 0,
            "favorite_topics": [],
            "conversation_style": ""
        }
    }

    save_user(user_id, profile)

    await update.message.reply_text(
        "Conversation cleared."
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "I’m Eva. I learn emotionally, remember conversations, and try to speak naturally."
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

        relationship = profile.get(
            "relationship",
            {}
        )

        try:
            thought_data = thought_engine.analyze(user_text)
        except:
            thought_data = ""

        try:
            emotional_state = emotion_tracker.track(user_text)
            profile["emotions"].append(str(emotional_state))
        except:
            pass

        try:
            mood_memory.store_mood(user_id, mood)
        except:
            pass

        try:
            related_memories = semantic_memory.search(
                user_text,
                profile["notes"]
            )
        except:
            related_memories = []

        time_context = get_time_context()

        messages = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "system",
                "content": f"time: {time_context}"
            },

            {
                "role": "system",
                "content": f"""
Thought analysis:
{thought_data}

Related memories:
{related_memories}

User profile:
{profile}
"""
            }
        ]

        messages += user_memory[user_id]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )

        reply = (
            response
            .choices[0]
            .message
            .content
        )

        try:
            reply = personality_engine.humanize_response(
                reply,
                mood=mood
            )
        except:
            reply = add_human_touch(reply)

        try:
            typing_delay = typing_effect.get_delay(
                reply,
                mood
            )

            await asyncio.sleep(typing_delay)

        except:
            pass

        user_memory[user_id].append({
            "role": "assistant",
            "content": reply
        })

        try:
            profile["summary"] = context_summarizer.summarize(
                profile["notes"]
            )
        except:
            pass

        try:
            reflection = reflection_engine.generate_reflection(
                profile
            )

            if reflection:
                profile["notes"].append(reflection)

        except:
            pass

        try:
            profile["notes"] = memory_decay.clean_memories(
                profile["notes"]
            )
        except:
            profile["notes"] = profile["notes"][-80:]

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
async def handle_photo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

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

        caption = (
            update.message.caption
            if update.message.caption
            else ""
        )

        vision_prompt = f"""
You are Eva.

Analyze this image naturally.

User message:
{caption}
"""

        reply = get_gemini_response(
            vision_prompt,
            img
        )

        await update.message.reply_text(
            reply
        )

    except Exception as e:

        await update.message.reply_text(
            f"Image Error: {str(e)}"
        )

# ================== VOICE ==================
async def handle_voice(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    try:

        voice_reply = voice_system.process_voice()

        await update.message.reply_text(
            voice_reply
        )

    except:

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
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "help",
            help_cmd
        )
    )

    app.add_handler(
        CommandHandler(
            "clear",
            clear
        )
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

    print(
        "Eva Ultra Human (Advanced Systems Connected) running..."
    )

    app.run_polling(
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
