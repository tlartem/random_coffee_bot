import typing as t

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import model


async def create_or_update(
    session: AsyncSession, participant: model.Participant
) -> None:
    await session.merge(participant)
    await session.commit()


async def get_all(session: AsyncSession) -> t.Sequence[model.Participant]:
    res = await session.scalars(select(model.Participant))
    return res.all()


async def clear_all(session: AsyncSession) -> None:
    await session.execute(delete(model.Participant))
    await session.commit()
