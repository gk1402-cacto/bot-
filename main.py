from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
from flask import Flask
from threading import Thread

# ==================== FLASK KEEP-ALIVE (không 502, không wake up) ====================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive! 🚀", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # Render yêu cầu host='0.0.0.0'
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

Thread(target=run_flask, daemon=True).start()
print("[Keep-alive] Flask đang chạy → Render sẽ luôn online 24/7!")
# ====================================================================================

# ========================== BOT TELEGRAM (aiogram 3) ==========================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("LỖI: TOKEN không tồn tại! Hãy kiểm tra Environment Variables.")
    exit()

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Xin chào! Bot đang chạy 24/7 trên Render đây 🚀\n"
        "Gõ gì mình cũng rep lại nha!"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Bạn vừa gửi: {message.text}")

async def main():
    print("Bot Telegram đang khởi động...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
# ================================================================================
