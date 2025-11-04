import logging
import typing as t
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src import model
from src.adapter import database, telegram

log = logging.getLogger(__name__)


async def create_pairs(session: AsyncSession, group_id: int):
    available_pairs: t.Sequence[
        tuple[model.Participant, model.Participant]
    ] = await database.pair.get_available_pairs(session, group_id)

    if not available_pairs:
        await telegram.send_message_to_group(
            group_id, "Недостаточно участников или нет уникальных пар"
        )
        return

    # Фильтруем пары так, чтобы каждый участник был только в одной паре
    used_users = set()
    final_pairs = []
    for p1, p2 in available_pairs:
        if p1.user_id not in used_users and p2.user_id not in used_users:
            final_pairs.append((p1, p2))
            used_users.add(p1.user_id)
            used_users.add(p2.user_id)

    if not final_pairs:
        await telegram.send_message_to_group(
            group_id, "Не удалось создать уникальные пары"
        )
        return

    # Автоматическое определение начала недели (понедельник)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())  # Понедельник текущей недели
    week_start = start_of_week.strftime("%Y-%m-%d")  # Форматируем дату как строку

    pairs = [
        model.Pair(
            group_id=group_id,
            week_start=week_start,
            user1_id=x.user_id,
            user2_id=y.user_id,
        )
        for x, y in final_pairs
    ]

    await database.pair.create_batch(session, pairs)

    message = "Пары Random Coffee на эту неделю ☕️\n\n"
    for couple in final_pairs:
        message += f"▫️@{couple[0].username} x @{couple[1].username}\n\n"

    message += "Напиши прямо сейчас собеседнику в личку и договорись о месте (в том числе онлайн) и времени, чтобы не забыть!"

    # Сообщение для тех, кто остался без пары
    all_participants = await database.participant.get_all(session, group_id)
    unpaired = [p for p in all_participants if p.user_id not in used_users]

    if unpaired:
        message += f"\n\n😔 К сожалению, без пары: "
        message += ", ".join([f"@{p.username}" for p in unpaired])

    await telegram.send_message_to_group(group_id, message)

    await database.participant.clear_all(session, group_id)
