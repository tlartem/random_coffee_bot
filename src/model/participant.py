from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src import model


class Participant(model.Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int]
    user_id: Mapped[int]
    username: Mapped[str]
    full_name: Mapped[str]
