import os, requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    await update.message.reply_text(f"🔍 {q} қидирилмоқда...")
    try:
        # 1. kitob.ws
        url = f"https://kitob.ws/?s={q}"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            link = a['href']
            if 'kitob' in link and len(link) > 5:
                try:
                    if not link.startswith('http'):
                        link = "https://kitob.ws" + (link if link.startswith('/') else f"/{link}")
                    page = requests.get(link, headers={"User-Agent":"Mozilla/5.0"}, timeout=15).text
                    s2 = BeautifulSoup(page, 'html.parser')
                    for pa in s2.find_all('a', href=True):
                        pdf = pa['href']
                        if '.pdf' in pdf:
                            if not pdf.startswith('http'):
                                pdf = "https://kitob.ws" + (pdf if pdf.startswith('/') else f"/{pdf}")
                            file_data = requests.get(pdf, timeout=30).content
                            if len(file_data) > 15000:
                                await update.message.reply_document(document=file_data, filename=f"{q}.pdf")
                                return
                except:
                    continue
        await update.message.reply_text(f"❌ {q} топилмади")
    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Хато бўлди")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
app.run_polling()
