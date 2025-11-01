# core/wp_dropdb.py
from core.env_manager import choose_environment
import os
import sqlite3
import subprocess
import shutil
from pathlib import Path

DB_PATH = os.path.join(os.getcwd(), "devcore_projects.db")

def detect_env():
    """Deteksi environment (Docker / XAMPP / Unknown)"""
    if Path("docker-compose.yml").exists():
        return "docker"
    elif "xampp" in str(Path.cwd()).lower() or "mysql" in str(Path.cwd()).lower():
        return "xampp"
    else:
        return "unknown"

def confirm(prompt):
    """Konfirmasi interaktif sebelum eksekusi fatal"""
    ans = input(f"{prompt} (y/n): ").strip().lower()
    return ans == "y"

def drop_wp_database(project_name):
    env = detect_env()
    print(f"🧩 Detected environment: {env}")

    db_name = f"{project_name}_db".replace("-", "_").lower()

    # Konfirmasi dulu
    print(f"⚠️  Ini akan menghapus permanen database '{db_name}' dan folder project '{project_name}'")
    if not confirm("Lanjutkan penghapusan?"):
        print("❎ Dibatalkan oleh pengguna.")
        return

    # Hapus database (Docker / XAMPP)
    if env == "docker":
        print(f"🧨 Menghapus volume Docker untuk {db_name}...")
        try:
            subprocess.run(["docker-compose", "down", "-v"], check=True)
            print("✅ Docker volume berhasil dihapus.")
        except subprocess.CalledProcessError:
            print("⚠️  Gagal menghapus volume Docker.")
    elif env == "xampp":
        print(f"🧨 Menghapus database lokal '{db_name}'...")
        try:
            subprocess.run(["mysql", "-u", "root", "-e", f"DROP DATABASE IF EXISTS {db_name};"], check=True)
            print(f"✅ Database {db_name} berhasil dihapus dari MySQL.")
        except FileNotFoundError:
            print("⚠️  MySQL CLI tidak ditemukan. Pastikan MySQL ada di PATH.")
    else:
        print("❌ Tidak bisa mendeteksi environment database, dilewati.")

    # Hapus folder project
    project_path = Path.cwd() / project_name
    if project_path.exists():
        print(f"🗑️  Menghapus folder project: {project_path}")
        shutil.rmtree(project_path, ignore_errors=True)
        print("✅ Folder project berhasil dihapus.")
    else:
        print("⚠️  Folder project tidak ditemukan, dilewati.")

    # Hapus record dari SQLite
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM projects WHERE name = ?", (project_name,))
        conn.commit()
        conn.close()
        print("🧾 Record project dihapus dari devcore_projects.db.")
    else:
        print("⚠️  File devcore_projects.db tidak ditemukan, dilewati.")

    print(f"🔥 Cleanup project '{project_name}' selesai total!\n")
