from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("LỖI: TOKEN không tồn tại! Kiểm tra Environment Variables trên Render.")
    exit()

# FIX CHÍNH: Xóa parse_mode khỏi đây
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "<b>Xin chào!</b> Bot đang chạy 24/7 trên Render miễn phí 🚀\n"
        "Gõ gì mình rep lại nha!",
        parse_mode="HTML"   # ← parse_mode phải để ở đây
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Bạn vừa gửi: <i>{message.text}</i>", parse_mode="HTML")

async def main():
    print("Bot đang khởi động...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
