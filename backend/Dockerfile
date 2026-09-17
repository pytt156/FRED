FROM python:3.14-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv
RUN uv sync --no-dev

COPY backend ./backend
COPY azure/consumer-entrypoint.sh /app/consumer-entrypoint.sh

RUN chmod +x /app/consumer-entrypoint.sh

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["/app/consumer-entrypoint.sh"]