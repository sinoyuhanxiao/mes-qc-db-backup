FROM python:3.11-slim

ENV TZ=UTC

# Install PostgreSQL 16, mongodump, and cron
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip ca-certificates lsb-release dos2unix tar cron && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && apt-get install -y postgresql-client-16 && \
    ln -sf /usr/lib/postgresql/16/bin/pg_dump /usr/local/bin/pg_dump && \
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

CMD ["sh", "-c", "touch /app/logs/cron.log && cron && tail -f /app/logs/cron.log"]
