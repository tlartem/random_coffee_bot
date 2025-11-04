from sqlalchemy.orm import Mapped, mapped_column

from src import model


class PollMapping(model.Base):
    poll_id: Mapped[str] = mapped_column(primary_key=True)
    group_id: Mapped[int]
