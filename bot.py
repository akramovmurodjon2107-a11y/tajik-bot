import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def search_book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 '{query}' қидирилмоқда...")
    try:
        url = f"https://openlibrary.org/search.json?q={query}&limit=1"
        data = requests.get(url, timeout=15).json()
        if data.get('docs'):
            book = data['docs'][0]
            title = book.get('title', 'Номсиз')
            author = book.get('author_name', ['Номалум'])[0]
            await update.message.reply_text(f"Топилди:\n📖 {title}\n✍️ {author}")
        else:
            await update.message.reply_text("❌ Топилмади")
    except Exception as e:
        await update.message.reply_text(f"Хато: {e}")

# МУҲИМ: Бу ерда Updater йўқ!
app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_book))

print("Bot started...")
app.run_polling()
