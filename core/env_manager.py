import os
import json
import shutil
import platform
import subprocess
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent.parent / ".devcore.json"

def get_default_paths():
    """Tentukan path default berdasarkan sistem operasi"""
    system = platform.system().lower()

    if "windows" in system:
        return {
            "xampp": Path("C:/xampp/htdocs"),
            "laragon": Path("C:/laragon/www"),
            "laradock": Path("C:/laradock/projects")
        }
    elif "darwin" in system:  # macOS
        return {
            "xampp": Path("/Applications/XAMPP/htdocs"),
            "laragon": Path.home() / "Sites/laragon",
            "laradock": Path.home() / "Sites/laradock"
        }
    else:  # Linux
        return {
            "xampp": Path("/opt/lampp/htdocs"),
            "laragon": Path.home() / "Projects/laragon",
            "laradock": Path.home() / "Projects/laradock"
        }

def load_env_config():
    """Muat konfigurasi environment, jika belum ada buat otomatis"""
    defaults = get_default_paths()

    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    else:
        config = {k: str(v) for k, v in defaults.items()}
        save_env_config(config)

    # Pastikan semua path ada
    for key, path_str in config.items():
        path = Path(path_str)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Path '{path}' dibuat otomatis untuk {key}")

    return config

def save_env_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print(f"✅ Konfigurasi environment tersimpan di {CONFIG_FILE}")

def choose_environment():
    """Pilih environment dan pastikan path-nya ada"""
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
        
    defaults = {k: str(v) for k, v in get_default_paths().items()}
    save_env_config(defaults)
    print("✅ Konfigurasi default berhasil dibuat ulang.")

    
def get_mysql_path(env_name: str) -> Path | None:
    """Kembalikan path MySQL sesuai environment"""
    system = platform.system().lower()

    if "windows" in system:
        if env_name == "xampp":
            return Path("C:/xampp/mysql/bin")
        elif env_name == "laragon":
            # deteksi otomatis versi MySQL (jika ada)
            base = Path("C:/laragon/bin/mysql")
            if base.exists():
                versions = sorted(base.glob("mysql*/bin"), reverse=True)
                if versions:
                    return versions[0]
            return base / "mysql-8.0.30-winx64/bin"  # fallback
        elif env_name == "laradock":
            return Path("C:/laradock/mysql/bin")
    else:
        # Mac/Linux
        if env_name == "xampp":
            return Path("/opt/lampp/bin")
        elif env_name == "laradock":
            return Path.home() / "Projects/laradock/mysql/bin"

    return None

def add_to_system_path(path_to_add: Path):
    """Tambahkan folder ke Environment PATH (permanent)"""
    system = platform.system().lower()
    path_str = str(path_to_add.resolve())

    if not path_to_add.exists():
        print(f"⚠️  Path tidak ditemukan: {path_to_add}")
        return False

    if "windows" in system:
        # Ambil PATH sekarang dengan ekspansi variabel
        current_path = os.environ.get("PATH", "")
        if path_str in current_path:
            print(f"✔️  PATH sudah mengandung: {path_str}")
            return True

        new_path = f"{current_path};{path_str}"

        try:
            subprocess.run(f'setx PATH "{new_path}"', shell=True, check=True)
            print(f"✅ PATH berhasil ditambahkan di Windows: {path_str}")
        except subprocess.CalledProcessError:
            print(f"❌ Gagal menambahkan PATH ke Windows.")
    elif "darwin" in system or "linux" in system:
        shell_rc = Path.home() / (".zshrc" if Path.home().joinpath(".zshrc").exists() else ".bashrc")
        with open(shell_rc, "a") as f:
            f.write(f'\n# Added by DevCore setup\nexport PATH="$PATH:{path_str}"\n')
        print(f"✅ PATH ditambahkan ke {shell_rc}: {path_str}")
    else:
        print("⚠️  Sistem operasi tidak dikenali, PATH tidak diubah.")
        return False

    return True


def detect_mysql_cli():
    """Cari lokasi file mysql.exe / mysql CLI di environment umum"""
    # 1️⃣ Coba cari di PATH sistem
    mysql_path = shutil.which("mysql")
    if mysql_path:
        return Path(mysql_path)

    # 2️⃣ Coba lokasi bawaan Laragon
    laragon_mysql = Path("C:/laragon/bin/mysql")
    if laragon_mysql.exists():
        for version_dir in sorted(laragon_mysql.glob("mysql*/bin/mysql.exe"), reverse=True):
            return version_dir

    # 3️⃣ Coba lokasi bawaan XAMPP
    xampp_mysql = Path("C:/xampp/mysql/bin/mysql.exe")
    if xampp_mysql.exists():
        return xampp_mysql

    # 4️⃣ Coba lokasi global Linux / Mac
    if platform.system() != "Windows":
        for path in ["/usr/bin/mysql", "/usr/local/mysql/bin/mysql"]:
            if Path(path).exists():
                return Path(path)

    return None
