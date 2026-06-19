# Stage 1: build frontend
FROM node:20-slim AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: install Python deps
FROM python:3.13-slim AS py-builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 3: final image
FROM python:3.13-slim
WORKDIR /app
COPY --from=py-builder /install /usr/local
COPY backend/app/ ./app/
COPY backend/migrations/ ./migrations/
COPY backend/pyproject.toml .
COPY backend/entrypoint.sh .
RUN chmod +x entrypoint.sh
COPY --from=frontend-builder /frontend/dist ./frontend_dist/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000
CMD ["./entrypoint.sh"]
