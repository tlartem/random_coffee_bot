import asyncio
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Awaitable, Callable, Optional


class AdminNotificationHandler(logging.Handler):
    def __init__(self, notify_func: Optional[Callable[[str], Awaitable[None]]] = None):
        super().__init__()
        self.notify_func = notify_func
        self.setLevel(logging.ERROR)

    def emit(self, record):
        """Отправляет уведомление администратору при ошибке."""
        if self.notify_func and record.levelno >= logging.ERROR:
            try:
                message = self.format(record)
                # Создаем задачу для асинхронной отправки уведомления
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(
                        self.notify_func(f"🚨 Ошибка в системе:\n{message}")
                    )
                else:
                    asyncio.run(self.notify_func(f"🚨 Ошибка в системе:\n{message}"))
            except Exception:
                # Если не удается отправить уведомление, просто игнорируем
                # чтобы не создавать бесконечный цикл ошибок
                pass


def configure_logging(
    level_name: int = logging.INFO,
    log_file: str | None = None,
    max_bytes: int = 10 * 1024 * 1024,  # 10 МБ по умолчанию
    backup_count: int = 5,  # 5 файлов ротации по умолчанию
    admin_notify_func: Optional[Callable[[str], Awaitable[None]]] = None,
) -> None:
    log_format = "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logging.basicConfig(level=level_name, datefmt=date_format, format=log_format)

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Используем RotatingFileHandler вместо FileHandler
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(
            logging.Formatter(fmt=log_format, datefmt=date_format)
        )
        logging.getLogger().addHandler(file_handler)

    # Добавляем обработчик для уведомлений администратору при ошибках
    if admin_notify_func:
        admin_handler = AdminNotificationHandler(admin_notify_func)
        admin_handler.setFormatter(
            logging.Formatter(fmt=log_format, datefmt=date_format)
        )
        logging.getLogger().addHandler(admin_handler)

    # logging.getLogger("uvicorn").setLevel(logging.INFO)
