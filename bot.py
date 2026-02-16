import os
from flask import Flask
import threading
import os

app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Isse bot ke saath ek dummy server chalu ho jayega
threading.Thread(target=run).start()

import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- KEYS (Replace these) ---
TELEGRAM_TOKEN = '8414276375:AAHvTA7x1ueZSutA1yds-YGqg6nRiHY9oVw'
GEMINI_API_KEY = 'AIzaSyAtGCC6uOFgozWU7efJmiFHXL4CL7ZBM84'

# Gemini Setup
genai.configure(api_key="AiZaSyAtGCC6uDFgozwU7efJmiFHXL4CL7ZBM84")
model = genai.GenerativeModel('gemini-1.5-flash')

# Updated System Prompt for Friendly & Expert Knowledge
SYSTEM_PROMPT = (
    "You are zimo21_bot, a friendly and extremely smart AI teacher. "
    "1. Be a friend to the user but provide 100% accurate, NCERT-based answers. "
    "2. If someone chats normally, reply in a friendly, cool, and supportive way. "
    "3. For studies (Class 1-10), give perfect, textbook-style answers in points. "
    "4. Language: Use a mix of Hindi and English (Hinglish) to keep it natural."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    msg = (
        f"Hey {user_name}! Main hoon **zimo21_bot** 🥰\n\n"
        "Main aapka best friend aur teacher dono hoon! Aap mujhse Class 1 se 10 tak ke "
        "sabhi questions puch sakte hain, ya phir bas dosti waali baatein bhi kar sakte hain.\n\n"
        "**Main kya kar sakta hoon?**\n"
        "✅ NCERT ke 100% sahi answers\n"
        "✅ English Grammar tips\n"
        "✅ General Knowledge aur Out-of-box facts\n"
        "✅ Friendly chatting\n\n"
        "Pucho, kya janna chahte ho?"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        # Sending context + user query to AI
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nUser: {user_input}")
        await update.message.reply_text(response.text, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text("Arre yaar, lagta hai signal thoda weak hai. Ek baar fir se pucho?")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_chat))
    print("zimo21_bot is live and friendly!")
    app.run_polling()

if __name__ == '__main__':
    main()
