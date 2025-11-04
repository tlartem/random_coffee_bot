from aiogram.enums import PollType

from src.adapter.telegram.connection import bot
from src.config import settings


async def send_message_to_admin(message: str) -> None:
    for admin_id in settings.bot.admin_chat_ids:
        await bot.send_message(chat_id=admin_id, text=message[:4000])


async def send_message_to_group(group_id: int, message: str) -> None:
    await bot.send_message(chat_id=group_id, text=message)


async def send_quiz(group_id: int):
    return await bot.send_poll(
        chat_id=group_id,
        question="Будешь участвовать в рандом кофи на следующей неделе?",
        options=["Да", "Нет"],
        is_anonymous=False,
        type=PollType.REGULAR,
    )
