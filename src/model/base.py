from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    # Авто имя таблиц по названию класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"
