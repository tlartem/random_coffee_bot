import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, PollAnswer

from src import usecase
from src.adapter import database
from src.config import settings, is_admin, add_group, remove_group

log = logging.getLogger(__name__)
router = Router()


@router.message(Command(commands=["create_pairs"]))
async def create_pairs_command(message: Message):
    if not message.from_user or not is_admin(message.from_user.id):
        return
    log.info(f"/create_pairs from chat {message.chat.id if message.chat else 'unknown'}")
    if not message.chat or message.chat.type == "private":
        return
    async with database.session_getter() as session:
        await usecase.create_pairs(session, message.chat.id)


@router.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer):
    poll_id = str(poll_answer.poll_id)
    log.info(f"Poll answer received for poll {poll_id}")
    async with database.session_getter() as session:
        group_id = await database.poll_mapping.get_group_id(session, poll_id)
        if not group_id:
            log.error(f"No group mapping found for poll {poll_id}")
            return
        await usecase.handle_quiz_answer(session, poll_answer, group_id)


@router.message(Command(commands=["send_quiz"]))
async def send_quiz_command(message: Message):
    if not message.from_user or not is_admin(message.from_user.id):
        return
    log.info(f"/send_quiz from chat {message.chat.id if message.chat else 'unknown'}")
    if not message.chat or message.chat.type == "private":
        return
    async with database.session_getter() as session:
        await usecase.send_quiz(session, message.chat.id)


@router.message(Command(commands=["groups"]))
async def list_groups_command(message: Message):
    if not message.from_user or not is_admin(message.from_user.id):
        return
    groups = "\n".join([f"- {gid}" for gid in settings.bot.group_chat_ids])
    await message.answer(f"Настроенные группы:\n{groups}")


@router.message(Command(commands=["add_group"]))
async def add_group_command(message: Message):
    if not message.from_user or not is_admin(message.from_user.id):
        return
    if not message.chat:
        return
    add_group(message.chat.id)
    await message.answer(f"Группа {message.chat.id} добавлена")


@router.message(Command(commands=["remove_group"]))
async def remove_group_command(message: Message):
    if not message.from_user or not is_admin(message.from_user.id):
        return
    if not message.chat:
        return
    if remove_group(message.chat.id):
        await message.answer(f"Группа {message.chat.id} удалена")
    else:
        await message.answer(f"Группа {message.chat.id} не найдена")


@router.message()
async def debug_all_messages(message: Message):
    log.info(f"Unhandled message: {message.text}, chat: {message.chat.id if message.chat else 'unknown'}, type: {message.chat.type if message.chat else 'unknown'}")
