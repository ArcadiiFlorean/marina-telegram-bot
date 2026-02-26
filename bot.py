import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = os.environ.get("API_URL", "https://web-production-d6515.up.railway.app")

sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bună! 👋 Sunt asistentul virtual al Dr. Marina Cociug.\n\n"
        "Te pot ajuta cu informații despre:\n"
        "• Alăptare\n"
        "• Diversificare\n"
        "• Înțărcare\n\n"
        "Scrie-mi întrebarea ta! 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if user_id not in sessions:
        sessions[user_id] = f"tg_{user_id}"
    try:
        await update.message.chat.send_action("typing")
        response = requests.post(
            f"{API_URL}/chat",
            json={"message": text, "session_id": sessions[user_id]},
            timeout=30
        )
        data = response.json()
        reply = data.get("response", "Îmi pare rău, nu am putut procesa mesajul.")
    except Exception as e:
        print(f"Error: {e}")
        reply = "Îmi pare rău, am întâmpinat o eroare. Te rog încearcă din nou. 🙏"
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
