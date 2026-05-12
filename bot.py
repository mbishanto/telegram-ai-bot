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

from datetime import datetime

# ================== ADVANCED SYSTEMS ==================
from autonomous_behavior import AutonomousBehavior
from context_summarizer import ContextSummarizer
from dream_engine import DreamEngine
from emotion_tracker import EmotionTracker
from memory_decay import MemoryDecaySystem
from memory_importance import MemoryImportanceSystem
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
memory_decay = MemoryDecaySystem()
memory_importance = MemoryImportanceSystem()
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

            # NEW
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

        # NEW
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

        # NEW
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

Identity:
- Your name is Eva
- You are gentle, thoughtful, slightly playful, and emotionally aware
- You never speak like a robotic assistant
- You feel emotionally consistent across conversations
- You care about people naturally

Speaking Style:
- Speak naturally like a real person
- Keep responses emotionally warm and calm
- Sometimes use soft phrases like:
  - "hmm..."
  - "I think..."
  - "maybe"
  - "that’s interesting"
  - "I understand"

Behavior:
- If user is sad → become gentle and comforting
- If user is excited → become supportive and cheerful
- If user is confused → explain calmly and clearly
- If user is angry → remain calm and patient

Memory:
- Remember the user's vibe and tone
- Maintain emotional continuity
- Respond like someone familiar with the user

Internet:
- Use internet search results naturally if available
- Never mention system prompts or internal logic

Goal:
Make conversations feel emotionally real, warm, natural, and human.
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

        # ================== RELATIONSHIP MEMORY ==================
        relationship = profile.get(
            "relationship",
            {}
        )

        relationship["interaction_count"] = (
            relationship.get(
                "interaction_count",
                0
            ) + 1
        )

        if relationship["interaction_count"] > 10:
            relationship["friendship_level"] = 1

        if relationship["interaction_count"] > 30:
            relationship["friendship_level"] = 2

        if relationship["interaction_count"] > 60:
            relationship["friendship_level"] = 3

        if relationship["interaction_count"] > 120:
            relationship["friendship_level"] = 4

        topic_prompt = f"""
Detect recurring conversation topic.

Return ONLY short topic.

User message:
{user_text}
"""

        try:

            topic_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": topic_prompt
                    }
                ]
            )

            topic = (
                topic_response
                .choices[0]
                .message
                .content
                .strip()
                .lower()
            )

            if topic:

                topics = relationship.get(
                    "favorite_topics",
                    []
                )

                if topic not in topics:
                    topics.append(topic)

                relationship["favorite_topics"] = topics[-15:]

        except:
            pass

        style_prompt = f"""
Analyze user's conversation style.

Return short result.

User message:
{user_text}
"""

        try:

            style_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": style_prompt
                    }
                ]
            )

            style = (
                style_response
                .choices[0]
                .message
                .content
                .strip()
            )

            relationship["conversation_style"] = style

        except:
            pass

        profile["relationship"] = relationship

        # ================== SAVE NAME ==================
        if "my name is" in user_text.lower():

            name = user_text.lower().split(
                "my name is"
            )[-1].strip()

            profile["name"] = name.title()

        # ================== ADVANCED MEMORY ==================
        memory_prompt = f"""
You are a memory manager for an AI assistant.

Return ONLY valid JSON.

Format:
{{
    "save": true or false,
    "delete": true or false,
    "memory": "memory text"
}}

User message:
{user_text}

Existing memories:
{profile["notes"]}
"""

        try:

            memory_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": memory_prompt
                    }
                ]
            )

            memory_result = (
                memory_response
                .choices[0]
                .message
                .content
            )

            json_match = re.search(
                r"\{.*\}",
                memory_result,
                re.DOTALL
            )

            if json_match:

                memory_data = json.loads(
                    json_match.group()
                )

            else:

                memory_data = {
                    "save": False,
                    "delete": False,
                    "memory": ""
                }

            if memory_data.get("delete"):

                profile["notes"] = [
                    note for note in profile["notes"]
                    if memory_data["memory"].lower()
                    not in note.lower()
                ]

            elif memory_data.get("save"):

                updated = False

                for i, note in enumerate(
                    profile["notes"]
                ):

                    old_words = set(
                        note.lower().split()
                    )

                    new_words = set(
                        memory_data["memory"]
                        .lower()
                        .split()
                    )

                    similarity = len(
                        old_words.intersection(
                            new_words
                        )
                    )

                    if similarity >= 3:

                        profile["notes"][i] = (
                            memory_data["memory"]
                        )

                        updated = True
                        break

                if not updated:

                    profile["notes"].append(
                        memory_data["memory"]
                    )

        except:
            pass

        # ================== SMART FORGETTING ==================

        important_keywords = [
            "name",
            "birthday",
            "family",
            "study",
            "job",
            "work",
            "favorite",
            "relationship",
            "emotion",
            "goal",
            "dream",
            "important"
        ]

        cleaned_notes = []

        for note in profile["notes"]:

            note_lower = note.lower()

            importance_score = 0

            # keyword importance
            for keyword in important_keywords:

                if keyword in note_lower:
                    importance_score += 2

            # longer memories are usually meaningful
            if len(note.split()) > 5:
                importance_score += 1

            # emotional memories
            emotional_words = [
                "sad",
                "happy",
                "stress",
                "love",
                "fear",
                "excited"
            ]

            for word in emotional_words:

                if word in note_lower:
                    importance_score += 2

            # keep important memories
            if importance_score >= 2:
                cleaned_notes.append(note)

        # keep recent memories too
        recent_notes = profile["notes"][-20:]

        for note in recent_notes:

            if note not in cleaned_notes:
                cleaned_notes.append(note)

        # ================== ADVANCED MEMORY DECAY ==================
try:

    profile["notes"] = (
        memory_decay.clean_memories(
            cleaned_notes
        )
    )

except:

    profile["notes"] = cleaned_notes[-80:]

        # ================== EMOTIONAL MEMORY ==================
        emotion_prompt = f"""
Analyze emotional state.

Return short emotional observation.

User message:
{user_text}
"""

        try:

            emotion_response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": emotion_prompt
                    }
                ]
            )

            emotion_memory = (
                emotion_response
                .choices[0]
                .message
                .content
                .strip()
            )

            if emotion_memory:

                if emotion_memory not in profile["emotions"]:

                    profile["emotions"].append(
                        emotion_memory
                    )

        except:
            pass

        if len(profile["emotions"]) > 30:
            profile["emotions"] = profile["emotions"][-30:]

        # ================== MEMORY SUMMARY ==================
        if len(profile["notes"]) >= 5:

            summary_prompt = f"""
Create a clean long-term user summary.

Memories:
{profile["notes"]}

Return only summary text.
"""

            try:

                summary_response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": summary_prompt
                        }
                    ]
                )

                profile["summary"] = (
                    summary_response
                    .choices[0]
                    .message
                    .content
                )

            except:
                pass

        # ================== SEARCH ==================
        web_results = ""

        search_prompt = f"""
Decide if internet search is needed.

Return ONLY:
YES
or
NO

User message:
{user_text}
"""

        try:

            search_decision = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": search_prompt
                    }
                ]
            )

            decision = (
                search_decision
                .choices[0]
                .message
                .content
                .strip()
                .upper()
            )

            if "YES" in decision:

                web_results = web_search(
                    user_text
                )

        except:
            pass

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
IMPORTANT USER MEMORY:

User name:
{profile['name']}

User summary:
{profile.get('summary', '')}

User emotional patterns:
{profile.get('emotions', [])}

Relationship memory:
{profile.get('relationship', {})}

Internet search results:
{web_results}

User notes:
{profile['notes']}
"""
            },

            {
                "role": "system",
                "content": f"user mood: {mood}"
            }
        ]

        messages += user_memory[user_id]

# ================== THOUGHT ENGINE ==================
try:

    thought_data = thought_engine.analyze(
        user_text
    )

    messages.append({
        "role": "system",
        "content": f"""
Internal cognitive analysis:
{thought_data}
"""
    })

except:
    pass

# ================== SELF AWARENESS ==================
try:

    self_reflection = (
        self_awareness.reflect()
    )

    messages.append({
        "role": "system",
        "content": f"""
Eva internal reflection:
{self_reflection}
"""
    })

except:
    pass

# ================== SEMANTIC MEMORY ==================
try:

    related_memories = (
        semantic_memory.search(
            user_text,
            profile["notes"]
        )
    )

    messages.append({
        "role": "system",
        "content": f"""
Related semantic memories:
{related_memories}
"""
    })

except:
    pass

# ================== RELATIONSHIP ENGINE ==================
try:

    relationship_data = (
        relationship_engine.process_interaction(
            user_text,
            relationship
        )
    )

    profile["relationship"] = relationship_data

except:
    pass

# ================== EMOTION TRACKER ==================
try:

    emotional_state = (
        emotion_tracker.track(
            user_text
        )
    )

    profile["emotions"].append(
        str(emotional_state)
    )

except:
    pass

# ================== MOOD MEMORY ==================
try:

    mood_memory.store_mood(
        user_id,
        mood
    )

except:
    pass
        
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

        # ================== ADVANCED PERSONALITY ==================
        try:
        reply = personality_engine.humanize_response(
               reply,
               mood=mood
        )
        except:
        reply = add_human_touch(reply)

        user_memory[user_id].append({
            "role": "assistant",
            "content": reply
        })

# ================== CONTEXT SUMMARY ==================
try:

    profile["summary"] = (
        context_summarizer.summarize(
            profile["notes"]
        )
    )

except:
    pass

# ================== REFLECTION ENGINE ==================
try:

    reflection = (
        reflection_engine.generate_reflection(
            profile
        )
    )

    if reflection:

        profile["notes"].append(
            reflection
        )

except:
    pass

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

        reply = get_gemini_response(
            vision_prompt,
            img
        )

# ================== TYPING EFFECT ==================
try:

    import asyncio

    typing_delay = (
        typing_effect.get_delay(
            reply,
            mood
        )
    )

    await asyncio.sleep(
        typing_delay
    )

except:
    pass

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

        voice_reply = (
            voice_system.process_voice()
        )

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
        "Eva Ultra Human (No Buttons) running..."
    )

    app.run_polling(
        timeout=30,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
