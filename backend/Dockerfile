FROM python:3.9.15-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && apt-get install -y build-essential python-dev
RUN pip install --upgrade pip

COPY . /app/

RUN mkdir -p /media && mkdir -p /static && chown 2000 /media && chown 2000 /static

RUN mkdir -p /srv/web/var/cache && chown 2000 /srv/web/var/cache

RUN chmod +x /app/deploy/docker-entrypoint.sh && chown root:root /app/deploy/docker-entrypoint.sh

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["bash", "/app/deploy/docker-entrypoint.sh"]
