FROM python:3.11-slim-bookworm
COPY src src
COPY requirements.txt .
COPY alembic.ini .
COPY migrations migrations
RUN pip install -r requirements.txt
RUN mkdir instance
RUN cat > instance/config.json <<EOF
    {
        "SECRET_KEY": "$(openssl rand -base64 32)",
        "ACCESS_CONTROL_ALLOW_ORIGIN": "http://disc4days.stanleyhicks.me",
        "SQLALCHEMY_DATABASE_URI": "postgresql+psycopg2rdsiam://disc4days_api@database-1.cp8bsjrjvguq.us-west-2.rds.amazonaws.com:5432/disc4days?aws_region_name=us-west-2"
    }
EOF
RUN alembic upgrade head
CMD gunicorn -w 4 src:app --bind=0.0.0.0:5000
EXPOSE 5000