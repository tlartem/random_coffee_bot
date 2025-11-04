from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src import model


class Pair(model.Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[int]
    week_start: Mapped[str]
    user1_id: Mapped[int]
    user2_id: Mapped[int]

    __table_args__ = (
        UniqueConstraint(
            "group_id", "week_start", "user1_id", "user2_id", name="uix_pairs_week_user"
        ),
    )
