import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone

from src.adapter import database
from src.config import settings
from src.usecase.create_pairs import create_pairs
from src.usecase.send_quiz import send_quiz

log = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def setup_scheduler():
    scheduler.configure(timezone=timezone("Europe/Moscow"))
    if not scheduler.running:
        scheduler.start()
        log.info("Планировщик запущен.")
    scheduler.remove_all_jobs()


async def send_quiz_to_all_groups():
    if not settings.bot.group_chat_ids:
        log.info("No groups configured, skipping quiz")
        return
    for group_id in settings.bot.group_chat_ids:
        async with database.session_getter() as session:
            await send_quiz(session, group_id)


async def create_pairs_for_all_groups():
    if not settings.bot.group_chat_ids:
        log.info("No groups configured, skipping pair creation")
        return
    for group_id in settings.bot.group_chat_ids:
        async with database.session_getter() as session:
            await create_pairs(session, group_id)


async def schedule_tasks():
    scheduler.add_job(
        send_quiz_to_all_groups, CronTrigger(day_of_week="fri", hour=17, minute=0)
    )
    scheduler.add_job(
        create_pairs_for_all_groups, CronTrigger(day_of_week="sun", hour=19, minute=0)
    )
    log.info("Задачи добавлены в планировщик.")
