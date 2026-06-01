FROM python:3.13-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.13-slim

WORKDIR /app
COPY --from=builder /install /usr/local
COPY app/ ./app/
COPY migrations/ ./migrations/
COPY pyproject.toml .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["./entrypoint.sh"]
