import typing as t

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src import model


async def create_or_update(
    session: AsyncSession, participant: model.Participant
) -> None:
    await session.merge(participant)
    await session.commit()


async def get_all(session: AsyncSession, group_id: int) -> t.Sequence[model.Participant]:
    res = await session.scalars(
        select(model.Participant).where(model.Participant.group_id == group_id)
    )
    return res.all()


async def clear_all(session: AsyncSession, group_id: int) -> None:
    await session.execute(
        delete(model.Participant).where(model.Participant.group_id == group_id)
    )
    await session.commit()


async def delete_by_user_id(session: AsyncSession, group_id: int, user_id: int) -> None:
    await session.execute(
        delete(model.Participant).where(
            model.Participant.group_id == group_id,
            model.Participant.user_id == user_id,
        )
    )
    await session.commit()
