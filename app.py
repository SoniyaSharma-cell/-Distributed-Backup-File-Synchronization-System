from flask import Flask, render_template, redirect, url_for, flash
import database as db  # Database operations import kar rahe hain
import sync_engine as sync  # Sync functions import kar rahe hain

# Flask app instance
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Flash messages ke liye key


@app.route("/")
def index():
    """Main Dashboard: Logs table show karta hai."""
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM file_logs ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return render_template("index.html", logs=logs)


@app.route("/sync")
def trigger_sync():
    """Manual Sync Trigger Button."""
    sync.sync_files()
    flash("🔄 Manual Sync Completed!", "success")
    return redirect(url_for("index"))


@app.route("/restore/<filename>/<int:version>")
def restore(filename, version):
    """Restore specific file version."""
    success = sync.restore_file(filename, version)
    if success:
        flash(f"✅ Restored '{filename}' (Version {version}) successfully!", "success")
    else:
        flash(f"❌ Failed to restore '{filename}'.", "danger")
    return redirect(url_for("index"))


# Server direct start (bina condition ke taaki run pakka ho)
db.init_db()
print("🚀 Starting Flask Web Server...")
app.run(host="127.0.0.1", port=5000, debug=True)