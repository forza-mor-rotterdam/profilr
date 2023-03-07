FROM python:3.9.15-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN apt-get update && apt-get install -y \
    build-essential \
    python-dev \
    git \
    locales \
    && pip install --upgrade pip \
    && sed -i '/nl_NL.UTF-8/s/^# //g' /etc/locale.gen && \
        locale-gen

ENV LANG=nl_NL.UTF-8 \
    LANGUAGE=nl_NL \
    LC_ALL=nl_NL.UTF-8

COPY . /app/

RUN mkdir -p /media && mkdir -p /static && chown 2000 /media && chown 2000 /static \
    && mkdir -p /srv/web/var/cache && chown 2000 /srv/web/var/cache \
    && chmod +x /app/deploy/docker-entrypoint.sh && chown root:root /app/deploy/docker-entrypoint.sh \
    && pip install --no-cache-dir -r /app/requirements.txt

CMD ["bash", "/app/deploy/docker-entrypoint.sh"]
