# System ke built-in database (SQLite) ko import kar rahe hain
import sqlite3

# File ka digital fingerprint (unique hash) banane ke liye library
import hashlib

# System paths handle karne ke liye module
import os

# Database file ka fixed naam
DB_NAME = "backup_system.db"


def get_connection():
    # SQLite DB se connection bana rahe hain
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    # Connection open karke table bana rahe hain
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            source_path TEXT NOT NULL,
            backup_path TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            version INTEGER NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def get_latest_version(filename):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(version) FROM file_logs WHERE filename = ?", (filename,))
    result = cursor.fetchone()[0]
    conn.close()
    return result if result is not None else 0


def log_backup(filename, source_path, backup_path, file_hash, version):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO file_logs (filename, source_path, backup_path, file_hash, version)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, source_path, backup_path, file_hash, version))
    conn.commit()
    conn.close()


# Main Execution
if __name__ == "__main__":
    init_db()
    print("✅ Database created Successfully")