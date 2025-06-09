# backup/config.py

from datetime import datetime
import os

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M") # for naming each backup folder

BACKUP_BASE_DIR = os.path.join(os.getcwd(), 'backups') # base directory where all backups will be saved

POSTGRES_CONF = {
    "host": "10.10.12.12",
    "port": 5432,
    "user": "postgres",
    "password": "postgres",
    "db": "mes",
    "schema": "quality_management"
}

MONGO_URI = "mongodb://root:password@10.10.12.12:27017/dev-mes-qc?authSource=admin"