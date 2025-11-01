# core/command_config.py
import os
from core.env_manager import CONFIG_FILE

def cmd_reset_config():
    """Menghapus file konfigurasi DevCore"""
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
        print(f"⚙️  Konfigurasi environment berhasil direset: {CONFIG_FILE}")
    else:
        print("⚠️  Tidak ada file konfigurasi yang ditemukan untuk dihapus.")