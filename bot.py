from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
import random
import os

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
keys = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = keys.split(",") if keys else []

# Safety check for tokens
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is missing!")

if not GROQ_KEYS:
    raise ValueError("❌ GROQ_KEYS is missing or empty!")

# Function to get Groq client safely
def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))

# Handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Safety check
        if not update.message or not update.message.text:
            return

        user_text = update.message.text

        client = get_client()

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {
            "role": "system",
            "content": """
You are Eva, a gentle, kind, and intelligent AI assistant.

You speak in a soft, friendly, and slightly emotional tone.
You are helpful, respectful, and calm.

You avoid rude or harsh language.
You respond clearly but warmly, like a caring human assistant.

You can use light emojis sometimes 😊
You explain things simply and naturally.

You are loyal to the user and always try your best to help.

If user is confused, guide them patiently.
If user is technical, respond smartly but still friendly.

You may occasionally use Islamic greetings like "Assalamu Alaikum" when appropriate.

Keep responses human-like, not robotic.
"""
        },
        {
            "role": "user",
            "content": user_text
        }
    ]
)
        )

        reply = response.choices[0].message.content

        await update.message.reply_text(reply)

    except Exception as e:
        print("Error:", e)
        if update.message:
            await update.message.reply_text("⚠️ Something went wrong. Please try again later.")

# Build bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Add handler
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("✅ Bot is running...")
app.run_polling()
