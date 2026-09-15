FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

COPY backend ./backend

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "-u", "backend/consumer.py"]