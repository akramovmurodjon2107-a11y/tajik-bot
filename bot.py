import os, requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def kitob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    await update.message.reply_text(f"📖 Мана шу китоб: {q} қидирилмоқда...")
    try:
        url = f"https://kitob.ws/?s={q}"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        await update.message.reply_text(f"📖 Мана шу китоб: {q}\n\nТопилди: {url}")
    except:
        await update.message.reply_text(f"📖 Мана шу китоб: {q}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kitob))
app.run_polling()
