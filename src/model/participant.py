from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped

from src import model


class Participant(model.Base):
    user_id: Mapped[int]
    username: Mapped[str]
    full_name: Mapped[str]

    __table_args__ = (
        UniqueConstraint(
            "week_start", "user1_id", "user2_id", name="uix_pairs_week_user"
        ),
    )
