import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from keyboards import start_options_kb

# Загружаем переменные из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Пример простого хэндлера
@dp.message()
async def echo(message):
    print(f"[LOG] {message.from_user.full_name}: {message.text}")  # лог в консоль Render
    await message.answer("Привет! Я теперь работаю по webhook 🚀")

async def on_startup(app):
    await bot.set_webhook(f"{os.getenv('WEBHOOK_URL')}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# Запуск aiohttp-приложения
async def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    # Только webhook для Telegram
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    web.run_app(create_app(), port=int(os.getenv("PORT", 8080)))
