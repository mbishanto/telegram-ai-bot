from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq
import random
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

keys = os.getenv("GROQ_KEYS", "")
GROQ_KEYS = keys.split(",") if keys else []

def get_client():
    return Groq(api_key=random.choice(GROQ_KEYS))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    client = get_client()
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": user_text}]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
