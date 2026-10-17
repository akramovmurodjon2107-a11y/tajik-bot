import os, requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def kitob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    await update.message.reply_text(f"🔍 {q} қидирилмоқда...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(f"https://kitob.ws/?s={q}", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'kitob' in href.lower() and len(href) > 10:
                if not href.startswith('http'):
                    href = "https://kitob.ws" + href if href.startswith('/') else f"https://kitob.ws/{href}"
                try:
                    page = requests.get(href, headers=headers, timeout=15).text
                    s2 = BeautifulSoup(page, 'html.parser')
                    for b in s2.find_all('a', href=True):
                        pdf = b['href']
                        if '.pdf' in pdf.lower():
                            if not pdf.startswith('http'):
                                pdf = "https://kitob.ws" + pdf if pdf.startswith('/') else f"https://kitob.ws/{pdf}"
                            data = requests.get(pdf, headers=headers, timeout=30).content
                            if len(data) > 25000:
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
