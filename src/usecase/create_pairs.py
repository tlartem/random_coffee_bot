import logging
import typing as t
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src import model
from src.adapter import database, telegram

log = logging.getLogger(__name__)


async def create_pairs(session: AsyncSession):
    available_pairs: t.Sequence[
        tuple[model.Participant, model.Participant]
    ] = await database.pair.get_available_pairs(session)

    if not available_pairs:
        await telegram.send_message_to_group("Недостаточно участников или нет уникальных пар")
        return

    # Автоматическое определение начала недели (понедельник)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник текущей недели
    week_start = start_of_week.strftime("%Y-%m-%d")  # Форматируем дату как строку

    pairs = [
        model.Pair(
            week_start=week_start,
            user1_id=x.user_id,
            user2_id=y.user_id,
        )
        for x, y in available_pairs
    ]

    await database.pair.create_batch(session, pairs)

    message = "*Пары Random Coffee на эту неделю* ☕️\n\n"
    for couple in available_pairs:
        message += f"▫️@{couple[0].username} x @{couple[1].username}\n\n"

    message += "_Напиши прямо сейчас собеседнику в личку и договорись о месте (в том числе онлайн) и времени, чтобы не забыть!_"
    await telegram.send_message_to_group(message)

    await database.participant.clear_all(session)
