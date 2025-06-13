FROM python:3.11-slim

ENV TZ=UTC

RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip ca-certificates lsb-release dos2unix tar cron && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgres.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/postgres.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && apt-get install -y postgresql-client-17 && \
    ln -sf /usr/lib/postgresql/17/bin/pg_dump /usr/local/bin/pg_dump && \
    wget https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian11-x86_64-100.9.4.tgz && \
    tar -xvzf mongodb-database-tools-debian11-x86_64-100.9.4.tgz && \
    cp mongodb-database-tools-*/bin/mongodump /usr/local/bin/ && \
    chmod +x /usr/local/bin/mongodump && \
    rm -rf mongodb-database-tools-*

# Create required directories
RUN mkdir -p /app/logs /var/log/cron

WORKDIR /app

COPY . .

RUN dos2unix /app/cronjob.txt
RUN crontab /app/cronjob.txt

RUN pip install --no-cache-dir -r requirements.txt

# 支持 build-arg 动态注入 .env
ARG ENV_FILE=.env.sv
COPY ${ENV_FILE} .env
ENV ENV_FILE=.env

CMD ["sh", "-c", "touch /app/logs/cron.log && cron && tail -f /app/logs/cron.log"]
