FROM python:3.11-slim-bookworm
COPY src src
COPY requirements.txt .
COPY alembic.ini .
COPY migrations migrations
RUN pip install -r requirements.txt
RUN mkdir instance
RUN echo "{\"SECRET_KEY\": \"$(openssl rand -base64 32)\"}" > instance/config.json
RUN alembic upgrade head
CMD ["gunicorn", "-w", "4", "src:app", "--bind=0.0.0.0:5000"]
EXPOSE 5000