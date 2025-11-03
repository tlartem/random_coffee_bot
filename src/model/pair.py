from sqlalchemy.orm import Mapped

from src import model


class Pair(model.Base):
    week_start: Mapped[str]
    user1_id: Mapped[int]
    user2_id: Mapped[int]
