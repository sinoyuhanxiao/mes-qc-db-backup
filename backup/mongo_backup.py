# backup/mongo_backup.py
import os
import subprocess # for shell command execution
from backup.config import MONGO_URI, BACKUP_BASE_DIR, TIMESTAMP # import config

def backup_mongo():
    # path construction like /app/backups/mongodb/2025-06-06_14-00/
    folder = os.path.join(BACKUP_BASE_DIR, 'mongodb', TIMESTAMP)
    os.makedirs(folder, exist_ok=True)

    # use built in knife guest's mongodump with preset config
    cmd = [
         "/usr/local/bin/mongodump",
        "--uri", MONGO_URI,
        "--out", folder
    ]

    subprocess.run(cmd, check=True)
    return folder
