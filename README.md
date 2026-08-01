# 📁 Automated File Sync & Versioning System

A lightweight, local version control and backup management tool built with Python, Flask, and SQLite. The system automatically tracks file changes using cryptographic hashing (SHA-256), creates versioned backups, and provides an intuitive web interface for 1-click file restoration.

## 📌 Features

* **🔐 Cryptographic Integrity (SHA-256):** Calculates unique file signatures to accurately detect content modifications.
* **⚡ Smart Storage Optimization:** Automatically skips backup creation if file contents remain unchanged.
* **📦 Incremental Versioning (`v1`, `v2`...):** Maintains clean version copies in a dedicated backup folder.
* **🔄 1-Click Disaster Recovery:** Restores deleted or corrupted files to any historical version directly from the UI.
* **📊 Web Dashboard:** Real-time interface built with Flask & Bootstrap 5 to track audit logs, hashes, and timestamps.
* **🗄️ Database Logging:** Stores persistent history using SQLite.

---
## 🛠️ Tech Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite3
* **Frontend:** HTML5, Bootstrap 5
* **Core Modules:** `hashlib`, `shutil`, `os`, `sqlite3`

---
## 📂 Project Structure

....text
File_Sync_System/
│
├── source_folder/        # Active working directory being monitored
├── backup_folder/        # Stores versioned backup files (e.g., notes_v1.txt)
├── templates/
│   └── index.html        # Bootstrap web dashboard UI
├── app.py                # Flask web server & route controllers
├── database.py           # SQLite database schema & connection handler
├── sync_engine.py        # Core SHA-256 hashing & backup logic
└── backup_system.db      # SQLite database (Auto-generated)

Quick Start (All-in-One Command)
Run the following commands one by one in your terminal to clone, setup dependencies, and launch the application:

Bash
git clone [https://github.com/SoniyaSharma-cell/File_Sync_System.git](https://github.com/SoniyaSharma-cell/File_Sync_System.git) 
cd File_Sync_System 
pip install flask 
python app.py
......................
Dashboard Access: Open your web browser and go to http://127.0.0.1:5000
