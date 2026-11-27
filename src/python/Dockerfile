# Build from the src/ folder so the image can include the migrations:
#   docker build -f python/Dockerfile -t natyasutra-api .
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv

COPY python/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY python/app ./app
COPY migrations ./migrations

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# The same image runs the migrations: override the command with
#   alembic -c migrations/alembic.ini upgrade head
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
