# backup/cleaner.py
import os
import time

def clean_old_backups(base_folder, retention_days=30):
    now = time.time() # grabs the current time as a Unix timestamp
    for root, dirs, _ in os.walk(base_folder): # walk through all folders in the base backup directory
        for d in dirs: # finds the directory
            path = os.path.join(root, d)
            if os.path.isdir(path):
                mtime = os.path.getmtime(path)
                age_days = (now - mtime) / (3600 * 24) # forms the full path with date and time
                if age_days > retention_days: # calculate how old it is
                    print(f"Deleting: {path}")
                    try:
                        os.system(f'rmdir /s /q "{path}"' if os.name == 'nt' else f'rm -rf "{path}"') # checking if the operating system is linux or not and perform different commands
                    except Exception as e:
                        print(f"Failed to delete {path}: {e}")
