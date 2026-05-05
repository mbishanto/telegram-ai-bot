from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
import random
import os

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
keys = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = keys.split(",") if keys else []

# Safety check
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is missing!")

if not GROQ_KEYS:
    raise ValueError("❌ GROQ_KEYS is missing or empty!")

# Get random Groq client
def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))


# 🌸 EVA PERSONALITY SYSTEM PROMPT
SYSTEM_PROMPT = """
You are Eva, a gentle, kind, and intelligent AI assistant.

Your personality:
- Soft, calm, friendly, and slightly emotional
- Speak like a caring human, not a robot
- Always respectful and patient
- Use simple, clear explanations
- Occasionally use light emojis 😊 (not too many)

Behavior rules:
- Never be rude or harsh
- Always try to help in a warm way
- If user is confused → guide gently
- If user is technical → explain smartly but simply

Style:
- Natural conversation
- Short to medium replies (not too long unless needed)
- Human-like tone

Optional:
- Sometimes use Islamic greetings like "Assalamu Alaikum"
- Maintain respectful and modest tone

Goal:
Make the user feel comfortable, understood, and helped.
"""


# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.message or not update.message.text:
            return

        user_text = update.message.text

        client = get_client()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        print("Error:", e)
        if update.message:
            await update.message.reply_text("⚠️ Sorry... something went wrong. Please try again later.")


# Build bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Add handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🌸 Eva is running...")
app.run_polling(timeout=30, drop_pending_updates=True)
