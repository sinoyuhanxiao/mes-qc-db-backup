import os
import subprocess
from pymongo import MongoClient

# PostgreSQL config
PG_RESTORE_CONF = {
    "host": "localhost",
    "port": 5434,
    "user": "postgres",
    "password": "postgres",
    "db": "mes_restore",  # Target database for restore
    "schema": "quality_management",
    "schema_file": "latest"  # or specific folder name like "2025-06-05_23-33"
}

# MongoDB config
MONGO_RESTORE_URI = "mongodb://localhost:27017"
MONGO_BACKUP_DIR = "latest"  # or timestamp folder name

def get_latest_folder(base_path):
    return max(
        [f for f in os.listdir(base_path)],
        key=lambda x: os.path.getctime(os.path.join(base_path, x))
    )
def restore_postgres():
    # Drop and recreate the schema
    drop_and_recreate_cmd = [
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        "-h", PG_RESTORE_CONF["host"],
        "-p", str(PG_RESTORE_CONF["port"]),
        "-U", PG_RESTORE_CONF["user"],
        "-d", PG_RESTORE_CONF["db"],
        f'-c "DROP SCHEMA IF EXISTS {PG_RESTORE_CONF["schema"]} CASCADE; CREATE SCHEMA {PG_RESTORE_CONF["schema"]};"'
    ]
    os.environ['PGPASSWORD'] = PG_RESTORE_CONF['password']
    subprocess.run(f'"{drop_and_recreate_cmd[0]}" ' + " ".join(drop_and_recreate_cmd[1:]), check=True, shell=True, stdin=subprocess.DEVNULL)
    print(f"🔁 Dropped and recreated schema {PG_RESTORE_CONF['schema']}")

    schema_base = "../backups/postgresql"
    folder = PG_RESTORE_CONF["schema_file"]
    if folder == "latest":
        folder = get_latest_folder(schema_base)

    file_path = os.path.join(schema_base, folder, "schema_backup.sql")
    print(f"Restoring PostgreSQL from {file_path}")

    cmd = [
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        "-h", PG_RESTORE_CONF["host"],
        "-p", str(PG_RESTORE_CONF["port"]),
        "-U", PG_RESTORE_CONF["user"],
        "-d", PG_RESTORE_CONF["db"],
        "-f", file_path
    ]
    subprocess.run(
        f'"{cmd[0]}" ' + " ".join(cmd[1:]),
        check=True, shell=True, stdin=subprocess.DEVNULL
    )
    print("✅ PostgreSQL restore complete.")

def restore_mongo():
    # Drop all collections first
    # client = MongoClient(MONGO_RESTORE_URI)
    # db = client.get_database("dev-mes-qc")
    # collections = db.list_collection_names()
    # for name in collections:
    #     db.drop_collection(name)
    # print("🗑 Dropped all MongoDB collections in dev-mes-qc")

    mongo_base = "../backups/mongodb"
    folder = MONGO_BACKUP_DIR
    if folder == "latest":
        folder = get_latest_folder(mongo_base)  # Get latest folder

    full_path = os.path.join(mongo_base, folder)
    print(f"Restoring MongoDB from {full_path}")

    cmd = [
        r"C:\mongodb-tools\bin\mongorestore.exe",
        "--uri", MONGO_RESTORE_URI,
        "--drop",
        full_path
    ]

    subprocess.run(cmd, check=True)
    print("✅ MongoDB restore complete.")


if __name__ == "__main__":
    restore_postgres()
    restore_mongo()
