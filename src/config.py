import logging

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_settings import BaseSettings

log = logging.getLogger(__name__)


class BotSettings(BaseModel):
    token: str  # токен бота
    group_chat_id: int  # id группового чата
    admin_chat_id: int  # id чата админа


class DatabaseSettings(BaseModel):
    url: PostgresDsn


class Settings(BaseSettings):
    bot: BotSettings = Field()
    db: DatabaseSettings = Field()


settings = Settings()
