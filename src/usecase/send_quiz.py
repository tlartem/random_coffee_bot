import logging

from src.adapter import telegram

log = logging.getLogger(__name__)


async def send_quiz() -> None:
    await telegram.send_quiz()
