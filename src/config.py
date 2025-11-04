import logging

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

log = logging.getLogger(__name__)


class BotSettings(BaseModel):
    token: str  # токен бота
    group_chat_ids: list[int]  # список id групповых чатов
    admin_chat_ids: list[int]  # список id админов


class DatabaseSettings(BaseModel):
    url: str  # Database URL (supports both SQLite and PostgreSQL)


class Settings(BaseSettings):
    bot: BotSettings = Field()
    db: DatabaseSettings = Field()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_nested_delimiter": "__",
        "extra": "ignore",
    }


settings = Settings()


# Helper functions for accessing settings
def get_bot_token() -> str:
    return settings.bot.token


def get_group_chat_id() -> list[int]:
    return settings.bot.group_chat_ids


def get_admin_chat_id() -> int:
    return settings.bot.admin_chat_ids[0] if settings.bot.admin_chat_ids else 0


def is_admin(user_id: int) -> bool:
    return user_id in settings.bot.admin_chat_ids


def add_group(group_id: int) -> None:
    if group_id not in settings.bot.group_chat_ids:
        settings.bot.group_chat_ids.append(group_id)
        _save_env()


def remove_group(group_id: int) -> bool:
    if group_id in settings.bot.group_chat_ids:
        settings.bot.group_chat_ids.remove(group_id)
        _save_env()
        return True
    return False


def _save_env() -> None:
    import os
    env_path = ".env"
    with open(env_path, "r") as f:
        lines = f.readlines()

    with open(env_path, "w") as f:
        for line in lines:
            if line.startswith("bot__group_chat_ids="):
                f.write(f"bot__group_chat_ids='{settings.bot.group_chat_ids}'\n")
            else:
                f.write(line)
