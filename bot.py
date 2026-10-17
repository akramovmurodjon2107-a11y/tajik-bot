import os, requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Китоб номини ёзинг!")

async def kitob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text.strip()
    if len(q) < 2:
        return
    await update.message.reply_text(f"🔍 {q} қидирилмоқда...")
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://kitob.ws/?s={q}"
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for a in soup.find_all('a', href=True):
            link = a['href']
            if 'kitob.ws' in link and '/books/' in link or 'kitob.ws' in link and len(link) > 20:
                try:
                    page = requests.get(link, headers=headers, timeout=15).text
                    s2 = BeautifulSoup(page, 'html.parser')
                    for x in s2.find_all('a', href=True):
                        pdf_url = x['href']
                        if '.pdf' in pdf_url.lower():
                            if not pdf_url.startswith('http'):
                                pdf_url = "https://kitob.ws" + pdf_url if pdf_url.startswith('/') else f"https://kitob.ws/{pdf_url}"
                            data = requests.get(pdf_url, headers=headers, timeout=30).content
                            if len(data) > 30000:
                                await update.message.reply_document(document=data, filename=f"{q}.pdf", caption=f"📖 {q}")
                                return
                except:
                    continue
        
        await update.message.reply_text("❌ PDF топилмади, бошқа ном билан уриниб кўринг")
    except Exception as e:
        await update.message.reply_text("❌ Хато бўлди")

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, kitob))
    app.run_polling()
