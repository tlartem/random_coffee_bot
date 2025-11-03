from aiogram.enums import PollType

from src.adapter.telegram.connection import bot
from src.config import settings


async def send_message_to_admin(message: str) -> None:
    await bot.send_message(chat_id=settings.bot.admin_chat_id, text=message)


async def send_message_to_group(message: str) -> None:
    await bot.send_message(chat_id=settings.bot.group_chat_id, text=message, parse_mode="Markdown")


async def send_quiz() -> None:
    await bot.send_poll(
        chat_id=settings.bot.group_chat_id,
        question="Будешь участвовать в рандом кофе на следующей неделе?",
        options=["Да", "Нет"],
        is_anonymous=False,
        type=PollType.REGULAR,
    )
