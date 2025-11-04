import logging

from aiogram.types import PollAnswer, User
from sqlalchemy.ext.asyncio import AsyncSession

from src import model
from src.adapter import database

log = logging.getLogger(__name__)


async def handle_quiz_answer(session: AsyncSession, poll_answer: PollAnswer, group_id: int):
    user: User | None = poll_answer.user
    if not user:
        log.error("no user for poll answer")
        return

    if not poll_answer.option_ids:  # Отменил голос
        await database.participant.delete_by_user_id(session, group_id, user.id)
        return

    answer = poll_answer.option_ids[0]
    if answer != 0:  # Нет
        await database.participant.delete_by_user_id(session, group_id, user.id)
        return

    p = model.Participant(
        group_id=group_id,
        user_id=user.id,
        username=user.username,
        full_name=user.full_name,
    )

    await database.participant.create_or_update(session, p)
