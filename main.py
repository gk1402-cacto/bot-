from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os

# ====================== KEEP-ALIVE SIÊU ỔN ĐỊNH CHO RENDER ======================
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

class _KeepAliveHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def start_keep_alive():
    port = int(os.environ.get("PORT", 8080))  # Render tự động cấp PORT
    server = HTTPServer(("", port), _KeepAliveHandler)
    print(f"[Keep-alive] Server đang chạy trên port {port} – Render sẽ không sleep nữa!")
    server.serve_forever()

# Bắt đầu keep-alive NGAY LẬP TỨC (phải để trước mọi thứ)
Thread(target=start_keep_alive, daemon=True).start()
# ===============================================================================

# -------------------------- PHẦN BOT TELEGRAM CỦA BẠN --------------------------
TOKEN = os.getenv("TOKEN")

# Kiểm tra token (tránh lỗi ngớ ngẩn)
if not TOKEN:
    print("LỖI: TOKEN không tồn tại! Hãy kiểm tra Environment Variables trên Render.")
    exit()

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

async def main():
    print("Bot Telegram đang khởi động...")
    await dp.start_polling(bot)

# ===============================================================================

if __name__ == "__main__":
    asyncio.run(main())
