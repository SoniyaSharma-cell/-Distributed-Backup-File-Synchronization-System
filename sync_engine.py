import os
import shutil
from datetime import datetime
import database as db  # Database operations import kar rahe hain

# System ke paths setup kar rahe hain jahan files rahengi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(
    BASE_DIR, "source_folder"
)  # Workspace (Main folder)
BACKUP_DIR = os.path.join(
    BASE_DIR, "backup_folder"
)  # Vault (Backups ki jagah)


def sync_files():
    """Files check karta hai aur content badalne par new version backup banata hai."""
    print(f"\n🔄 [{datetime.now().strftime('%H:%M:%S')}] Sync Started...")

    # Folder exist na karein toh auto-create karne ke liye
    if not os.path.exists(SOURCE_DIR):
        os.makedirs(SOURCE_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    # Source folder ki saari files read kar rahe hain
    files = os.listdir(SOURCE_DIR)

    if not files:
        print("ℹ️ Source folder is empty.")
        return

    for filename in files:
        source_path = os.path.join(SOURCE_DIR, filename)

        # Direct folders ko skip karke sirf files process karne ke liye
        if not os.path.isfile(source_path):
            continue

        # 1. File ka current Hash fingerprint calculate kar rahe hain (Change detect karne ko)
        current_hash = db.calculate_sha256(source_path)

        # 2. Database se is file ka highest version number fetch kar rahe hain
        latest_version = db.get_latest_version(filename)

        # 3. Database se is file ka pichla saved Hash check kar rahe hain
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT file_hash FROM file_logs WHERE filename = ? ORDER BY version DESC LIMIT 1",
            (filename,),
        )
        last_entry = cursor.fetchone()
        conn.close()

        last_hash = last_entry["file_hash"] if last_entry else None

        # Agar Hash change hua h (matlab file me change/new file h) toh backup lenge
        if current_hash != last_hash:
            new_version = latest_version + 1  # Version 1 badha rahe hain

            # Backup file ka naya naam bana rahe hain (e.g., test_v1.txt)
            name_part, ext_part = os.path.splitext(filename)
            backup_filename = f"{name_part}_v{new_version}{ext_part}"
            backup_path = os.path.join(BACKUP_DIR, backup_filename)

            # Original file copy karke backup folder me save kar rahe hain
            shutil.copy2(source_path, backup_path)

            # DB me backup record entry kar rahe hain
            db.log_backup(
                filename, source_path, backup_path, current_hash, new_version
            )
            print(f" Backed up: {filename} -> {backup_filename} (v{new_version})")
        else:
            # Hash same mila toh copy skip kar rahe hain (Space bachane ke liye)
            print(f" Skipped: {filename} (No changes detected)")


def restore_file(filename, version, restore_location=None):
    """Old version  file restored in source folder."""
    conn = db.get_connection()
    cursor = conn.cursor()

    # Specified version ki file ka path DB se dhoondh rahe hain
    cursor.execute(
        "SELECT backup_path FROM file_logs WHERE filename = ? AND version = ?",
        (filename, version),
    )
    result = cursor.fetchone()
    conn.close()

    if not result:
        print(f" Version {version} Not present in DB!")
        return False

    backup_path = result["backup_path"]
    target_path = (
        restore_location
        if restore_location
        else os.path.join(SOURCE_DIR, filename)
    )

    # Backup file ko overwrite karke original workspace me paste kar rahe hain
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, target_path)
        print(f"🔄 Restored '{filename}' (v{version}) back to original folder")
        return True
    else:
        print(" Backup file is missing in folder.!")
        return False


# Code Direct Testing
if __name__ == "__main__":
    db.init_db()  # DB ready ensure kar rahe hain
    sync_files()  # Sync engine trigger kar rahe hain