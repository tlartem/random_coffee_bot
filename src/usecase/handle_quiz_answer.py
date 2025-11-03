import logging

from aiogram.types import PollAnswer, User
from sqlalchemy.ext.asyncio import AsyncSession

from src import model
from src.adapter import database

log = logging.getLogger(__name__)


async def handle_quiz_answer(session: AsyncSession, poll_answer: PollAnswer):
    user: User | None = poll_answer.user
    if not user:
        log.error("no user for poll answer")
        return

    answer = poll_answer.option_ids[0]
    if answer != 0:  # Нет
        return

    p = model.Participant(
        user_id=user.id,
        username=user.username,
        fullname=user.full_name,
    )

    await database.participant.create_or_update(session, p)
