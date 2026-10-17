import os, asyncio, logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("📚 Салом! Таджикча китоб номини ёзинг!\n\nМасалан: Фирдавси Шохнома")

@dp.message(F.text)
async def search(m: types.Message):
    q = m.text
    await m.answer(f"🔍 {q} қидирилмоқда...\n\n📖 Топилди: {q} - PDF")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
