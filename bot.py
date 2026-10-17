import asyncio, logging, os, requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from bs4 import BeautifulSoup

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("📚 Китоб номини ёзинг!")

@dp.message(F.text)
async def search(m: types.Message):
    q = m.text.strip()
    await m.answer(f"🔍 {q} қидирилмоқда...")
    
    try:
        url = f"https://kitob.ws/?s={q}"
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(r.text, 'lxml')
        
        for a in soup.find_all('a', href=True)[:10]:
            href = a['href']
            try:
                if 'kitob.ws' in href:
                    page = requests.get(href, headers={"User-Agent":"Mozilla/5.0"}, timeout=10)
                    s2 = BeautifulSoup(page.text, 'lxml')
                    for pdf_a in s2.find_all('a', href=True):
                        pdf_href = pdf_a['href']
                        if pdf_href.endswith('.pdf'):
                            if not pdf_href.startswith('http'):
                                pdf_href = "https://kitob.ws" + pdf_href
                            pdf_data = requests.get(pdf_href, timeout=20).content
                            if len(pdf_data) > 5000:
                                await m.answer_document(
                                    document=types.BufferedInputFile(pdf_data, filename=f"{q}.pdf"),
                                    caption=f"📖 Мана шу китоб: {q}"
                                )
                                return
            except:
                continue
        
        await m.answer(f"📖 Мана шу китоб: {q}\nҲозирча топилмади, бошқа ном ёзинг.")
    except:
        await m.answer(f"📖 Мана шу китоб: {q}\nХато бўлди, қайта ёзинг.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
