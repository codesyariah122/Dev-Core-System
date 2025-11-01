import json
import subprocess
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / ".devcore.json"

DEFAULT_CONFIG = {
    "xampp": "C:/xampp/htdocs",
    "laragon": "C:/laragon/www",
    "laradock": "C:/laradock/projects"
}

def load_env_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG

def save_env_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print(f"✅ Konfigurasi environment tersimpan di {CONFIG_FILE}")

def check_mysql_running():
    """Cek apakah MySQL sedang berjalan di XAMPP, Laragon, atau Docker"""
    try:
        # Coba jalankan perintah mysql -V (cek versi)
        subprocess.run(["mysql", "-V"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("✅ MySQL CLI terdeteksi di sistem.")
        return True
    except Exception:
        print("⚠️ MySQL CLI tidak terdeteksi di PATH.")

    # Cek Docker container mysql (untuk Laradock)
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=mysql", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        if "mysql" in result.stdout:
            print("🐳 MySQL container (Laradock) sedang berjalan.")
            return True
    except Exception:
        pass

    print("❌ MySQL belum aktif. Jalankan XAMPP/Laragon/Docker MySQL terlebih dahulu.")
    return False

def choose_environment():
    if not check_mysql_running():
        print("⛔ Tidak dapat melanjutkan tanpa MySQL aktif.")
        return None, None  # keluar dari proses

    config = load_env_config()
    print("Pilih environment lokal:")
    print(f"[1] XAMPP ({config['xampp']})")
    print(f"[2] Laragon ({config['laragon']})")
    print(f"[3] Laradock ({config['laradock']})")

    choice = input("> ").strip()
    if choice == "1":
        env, base = "xampp", Path(config["xampp"])
    elif choice == "2":
        env, base = "laragon", Path(config["laragon"])
    elif choice == "3":
        env, base = "laradock", Path(config["laradock"])
    else:
        print("❌ Pilihan tidak valid, default ke current directory.")
        env, base = "unknown", Path.cwd()

    base.mkdir(parents=True, exist_ok=True)
    print(f"📂 Environment dipilih: {env} → {base}")
    return env, base

def set_custom_env():
    config = load_env_config()
    print("🛠️  Konfigurasi environment custom:")
    for key in config.keys():
        new_path = input(f"Masukkan path untuk {key} (Enter untuk skip): ").strip()
        if new_path:
            config[key] = new_path.replace("\\", "/")
    save_env_config(config)
    
def rebuild_env_config():
    """Hapus dan buat ulang file konfigurasi environment DevCore"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        print("🗑️  File konfigurasi lama dihapus.")
    save_env_config(DEFAULT_CONFIG)
    print("✅ Konfigurasi default berhasil dibuat ulang.")
