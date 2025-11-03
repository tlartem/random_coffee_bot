import typing as t

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src import model


async def create(session: AsyncSession, pair: model.Pair) -> None:
    session.add(pair)
    await session.commit()


async def get_all(session: AsyncSession) -> t.Sequence[model.Pair]:
    res = await session.scalars(select(model.Pair))
    return res.all()


async def create_batch(session: AsyncSession, pairs: t.Sequence[model.Pair]) -> None:
    if not pairs:
        return
    session.add_all(pairs)
    await session.commit()


async def get_available_pairs(
    session: AsyncSession,
) -> t.Sequence[tuple[model.Participant, model.Participant]]:
    p1, p2 = aliased(model.Participant), aliased(model.Participant)
    existing = (
        select(model.Pair)
        .where(
            or_(
                and_(model.Pair.user1_id == p1.user_id, model.Pair.user2_id == p2.user_id),
                and_(model.Pair.user1_id == p2.user_id, model.Pair.user2_id == p1.user_id),
            )
        )
        .exists()
    )
    stmt = (
        select(p1.user_id, p2.user_id, p1.username, p2.username)
        .where(p1.user_id < p2.user_id)
        .where(~existing)
        .order_by(func.random())
    )
    res = await session.execute(stmt)
    return res.scalars().all()
