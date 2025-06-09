# main.py
#!/usr/local/bin/python
from backup.postgres_backup import backup_postgres
from backup.mongo_backup import backup_mongo
from backup.cleaner import clean_old_backups
from backup.config import BACKUP_BASE_DIR

if __name__ == "__main__":
    print("🔁 Starting backup...")

    try:
        pg_file = backup_postgres()
        print(f"✅ PostgreSQL backup: {pg_file}")
    except Exception as e:
        print(f"❌ PostgreSQL backup failed: {e}")

    try:
        mongo_dir = backup_mongo()
        print(f"✅ MongoDB backup: {mongo_dir}")
    except Exception as e:
        print(f"❌ MongoDB backup failed: {e}")

    print("🧹 Cleaning old backups...")
    clean_old_backups(BACKUP_BASE_DIR)

    print("✅ Backup finished.")

    # Limit log size to last 10000 lines
    log_file = "/app/logs/cron.log"
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if len(lines) > 10000:
            with open(log_file, "w", encoding="utf-8") as f:
                f.writelines(lines[-10000:])
    except Exception as e:
        print(f"⚠️ Failed to trim log file: {e}")
