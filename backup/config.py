# backup/config.py

from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M") # for naming each backup folder

BACKUP_BASE_DIR = os.path.join(os.getcwd(), 'backups') # base directory where all backups will be saved

POSTGRES_CONF = {
    "host": os.getenv("PG_HOST"),
    "port": int(os.getenv("PG_PORT", "5432")),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "db": os.getenv("PG_DBNAME"),
    "schema": "quality_management"
}

MONGO_URI = os.getenv("MONGO_URI")