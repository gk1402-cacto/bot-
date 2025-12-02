from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
import socket
from threading import Thread
import time  # Thêm để delay nhỏ

# ==================== KEEP-ALIVE SOCKET FIX 502 (bind 0.0.0.0, delay ổn định) ====================
def keep_alive():
    # Delay 1 giây để asyncio ổn định trước khi bind port
    time.sleep(1)
    
    port = int(os.environ.get("PORT", 10000))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # FIX QUAN TRỌNG: Bind đúng host '0.0.0.0' cho Render (không phải '' hoặc localhost)
    try:
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"[Keep-alive] Socket server đang chạy trên 0.0.0.0:{port} – Fix 502 thành công!")
    except Exception as e:
        print(f"[Keep-alive] Lỗi bind port: {e}")
        return  # Thoát nếu bind fail
    
    while True:
        try:
            client, addr = s.accept()
            request = client.recv(1024)
            # Response đơn giản để Render nhận diện
            client.send(b'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nBot is alive! 🚀')
            client.close()
        except Exception as e:
            print(f"[Keep-alive] Lỗi xử lý request: {e}")
            break

# Bắt đầu thread keep-alive NGAY SAU DELAY
keep_thread = Thread(target=keep_alive, daemon=True)
keep_thread.start()
# =================================================================================================

# ========================== BOT TELEGRAM (aiogram 3) ==========================
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("LỖI: TOKEN không tồn tại! Kiểm tra Environment Variables trên Render.")
    exit(1)  # Exit rõ ràng hơn

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "Xin chào! Bot đang chạy 24/7 trên Render đây 🚀\n"
        "Gõ gì mình rep lại nha!"
    )

@dp.message()
async def echo_handler(message: types.Message):
    await message.answer(f"Bạn vừa gửi: {message.text}")

async def main():
    print("Bot Telegram đang khởi động...")
    # Thêm timeout và error handler để tránh crash nếu Telegram 502 tạm thời
    await dp.start_polling(
        bot,
        timeout=20,  # Timeout polling để tránh block
        handle_signals=False  # Để Render quản lý shutdown
    )

if __name__ == "__main__":
    # Chờ thread keep-alive ổn định
    time.sleep(2)
    asyncio.run(main())
