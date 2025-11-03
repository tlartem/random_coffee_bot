import asyncio
import logging
import sys

from aiogram import Dispatcher

from shared.logger import configure_logging
from src.adapter import database, telegram
from src.controller.scheduler import schedule_tasks, setup_scheduler
from src.controller.tg_handlers import router

log = logging.getLogger(__name__)


async def on_startup():
    try:
        configure_logging(
            level_name=logging.INFO,
            log_file="shared/logs/bot.log",
            admin_notify_func=telegram.send_message_to_admin,
        )

        await database.create_tables()
        await setup_scheduler()
        await schedule_tasks()

    except Exception as e:
        log.error(f"Ошибка при инициализации: {e}")
        sys.exit(1)


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)

    log.info("Запуск бота...")
    await dp.start_polling(telegram.get_bot(), skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
