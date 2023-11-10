FROM python:3.8.10

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    redis-server \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD redis-server --daemonize yes && gunicorn -b 0.0.0.0:8000 --reload app:app & celery -A tasks worker -P threads --loglevel=debug
