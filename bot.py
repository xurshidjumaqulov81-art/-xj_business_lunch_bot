import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from database.db import init_db
from handlers.start import router as start_router
from handlers.menu import router as menu_router
from handlers.contest import router as contest_router
from handlers.registration import router as registration_router
from handlers.admin import router as admin_router


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    await init_db()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Admin ва start биринчи.
    dp.include_router(admin_router)
    dp.include_router(start_router)

    # Меню contest FSM'дан ОЛДИН туриши керак.
    # Шунда "Савол-жавоб" каби меню тугмалари анкета жавоби сифатида ушланмайди.
    dp.include_router(menu_router)
    dp.include_router(registration_router)
    dp.include_router(contest_router)

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

