from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

from config import TELEGRAM_TOKEN
from routers.content_generation import router as content_router

# Логгирование
logging.basicConfig(level=logging.INFO)

# Инициализация
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Роутеры
dp.include_router(content_router)

async def main():
    await dp.start_polling(bot)
