# ---------- Stage 1: build the Vue frontend ----------
FROM node:20-alpine AS frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---------- Stage 2: Python runtime (API + built site) ----------
FROM python:3.11-slim
WORKDIR /app

COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ ./backend/
# Bring in the compiled site; the backend serves it on the same origin.
COPY --from=frontend /app/frontend/dist ./frontend/dist

WORKDIR /app/backend
ENV PORT=8000
EXPOSE 8000
CMD ["python", "main.py"]
