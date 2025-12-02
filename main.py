from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

# Lấy token từ Render Environment Variables
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("LỖI: Không tìm thấy TOKEN! Kiểm tra Environment Variables trên Render.")
    exit()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Xin chào! Bot đang chạy 24/7 thật sự trên Render Background Worker 🚀\n"
        "Gõ gì mình rep lại nha!"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Bạn vừa gửi: {message.text}")

async def main():
    print("Bot Telegram đang khởi động 24/7 (Background Worker)...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
