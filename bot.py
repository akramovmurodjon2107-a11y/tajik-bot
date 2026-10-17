import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг - легал кутубхонадан қидириб бераман!")

async def kitob_qidir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    if len(q) < 2:
        return
    await update.message.reply_text(f"🔍 '{q}' қидирилмоқда...")
    try:
        # Легал API - Open Library
        r = requests.get(f"https://openlibrary.org/search.json?q={q}&limit=5", timeout=15).json()
        docs = r.get('docs', [])
        if not docs:
            await update.message.reply_text("❌ Топилмади, бошқа ном ёзиб кўр")
            return
        
        for doc in docs[:3]:
            title = doc.get('title', 'Номсиз')
            author = ', '.join(doc.get('author_name', [])[:2])
            year = doc.get('first_publish_year', '')
            key = doc.get('key', '')
            link = f"https://openlibrary.org{key}" if key else ""
            
            text = f"📖 **{title}**\n✍️ {author}\n📅 {year}\n🔗 {link}\n\n"
            # Агар public domain бўлса PDF боради
            if doc.get('public_scan_b'):
                text += "✅ Бу китобни легал PDF да ўқиш мумкин!"
            await update.message.reply_text(text)
    except Exception as e:
        await update.message.reply_text(f"Хато: {e}")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kitob_qidir))
app.run_polling()
