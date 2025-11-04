# Базовый образ Python
FROM python:3.13-slim

WORKDIR /app

# Установка uv для управления зависимостями
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Копирование файлов проекта
COPY pyproject.toml uv.lock ./

# Установка зависимостей
RUN uv sync --frozen --no-dev

# Копирование исходного кода
COPY . .

# Команда для запуска бота
CMD ["uv", "run", "python", "-m", "src.main"]