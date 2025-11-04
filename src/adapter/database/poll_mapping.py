from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import model


async def create(session: AsyncSession, poll_id: str, group_id: int) -> None:
    mapping = model.PollMapping(poll_id=poll_id, group_id=group_id)
    await session.merge(mapping)
    await session.commit()


async def get_group_id(session: AsyncSession, poll_id: str) -> int | None:
    res = await session.scalar(
        select(model.PollMapping.group_id).where(model.PollMapping.poll_id == poll_id)
    )
    return res
