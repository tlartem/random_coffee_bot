import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, PollAnswer

from src import usecase
from src.adapter import database

log = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=["create_pairs"]))
async def create_pairs_command(_message: Message):
    async with database.session_getter() as session:
        await usecase.create_pairs(session)


@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    async with database.session_getter() as session:
        await usecase.handle_quiz_answer(session, poll_answer)


@router.message(Command(commands=["send_quiz"]))
async def send_quiz_command(_message: Message):
    await usecase.send_quiz()
