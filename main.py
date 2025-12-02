from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

# ĐỔI TÊN BIẾN Ở ĐÂY CHO ĐÚNG VỚI RENDER
TOKEN = os.getenv("TOKEN")        # ← đổi từ "BOT_TOKEN" thành "TOKEN"

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Xin chào! Bot đang chạy 24/7 trên Render đây 🚀\n"
        "Gõ gì mình rep lại nha!"
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Bạn vừa gửi: {message.text}")

# ==================== THÊM ĐOẠN NÀY ĐỂ RENDER KHÔNG SLEEP ====================
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def keep_alive():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("", port), _Handler)
    server.serve_forever()

# ===========================================================================

async def main():
    print("Bot đang khởi động...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Bật web server nhỏ để Render luôn awake
    Thread(target=keep_alive, daemon=True).start()
    
    # Chạy bot
    asyncio.run(main())
