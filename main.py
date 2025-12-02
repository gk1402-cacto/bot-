from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Xin chào! Bot đang chạy 24/7 trên Railway đây \n"
        "Gõ gì mình rep lại nha!"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Bạn vừa gửi: {message.text}")

async def main():
    print("Bot đang khởi động...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
