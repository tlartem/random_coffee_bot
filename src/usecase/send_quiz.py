import logging

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapter import database, telegram

log = logging.getLogger(__name__)


async def send_quiz(session: AsyncSession, group_id: int) -> None:
    result = await telegram.send_quiz(group_id)
    poll_id = str(result.poll.id)
    log.info(f"Poll {poll_id} created for group {group_id}")
    await database.poll_mapping.create(session, poll_id, group_id)
