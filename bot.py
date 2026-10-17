import os, requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def kitob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    await update.message.reply_text(f"🔍 {q}")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        # Тожик кутубхона - kitob.ws
        r = requests.get(f"https://kitob.ws/?s={q}", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            link = a['href']
            if 'kitob' in link.lower():
                if not link.startswith('http'):
                    link = "https://kitob.ws" + (link if link.startswith('/') else f"/{link}")
                try:
                    p = requests.get(link, headers=headers, timeout=15).text
                    s2 = BeautifulSoup(p, 'html.parser')
                    for x in s2.find_all('a', href=True):
                        pdf = x['href']
                        if '.pdf' in pdf:
                            if not pdf.startswith('http'):
                                pdf = "https://kitob.ws" + (pdf if pdf.startswith('/') else f"/{pdf}")
                            data = requests.get(pdf, timeout=30).content
                            if len(data) > 20000:
                                await update.message.reply_document(document=data, filename=f"{q}.pdf")
                                return
                except:
                    continue
        await update.message.reply_text("❌ Топилмади")
    except:
        await update.message.reply_text("❌ Хато")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kitob))
app.run_polling()
