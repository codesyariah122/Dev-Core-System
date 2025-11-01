# core/command_wp_setup.py
import os
import json
import subprocess
from pathlib import Path

GLOBAL_CONFIG = Path(__file__).resolve().parent.parent / ".devcore.json"

def load_global_config():
    if GLOBAL_CONFIG.exists():
        with open(GLOBAL_CONFIG, "r") as f:
            return json.load(f)
    return {}

def load_project_config(project_dir):
    project_config = Path(project_dir) / "devcore_project.json"
    if project_config.exists():
        with open(project_config, "r") as f:
            return json.load(f)
    return {}

def run_wp_cli(commands, cwd):
    """Menjalankan WP-CLI command di direktori WordPress project"""
    for cmd in commands:
        print(f"🚀 Menjalankan: wp {cmd}")
        try:
            subprocess.run(["wp"] + cmd.split(), cwd=cwd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal menjalankan: wp {cmd} ({e})")

def cmd_wp_setup(project_dir="."):
    """Menginstall plugin & theme sesuai konfigurasi"""
    print("🔍 Membaca konfigurasi DevCore...")
    global_config = load_global_config()
    project_config = load_project_config(project_dir)

    plugins = project_config.get("plugins") or global_config.get("default_plugins", [])
    themes = project_config.get("themes") or global_config.get("default_themes", [])

    if not plugins and not themes:
        print("⚠️ Tidak ada plugin atau theme yang terdaftar untuk diinstall.")
        return

    print(f"📦 Plugin terdeteksi: {plugins}")
    print(f"🎨 Theme terdeteksi: {themes}")

    # Jalankan instalasi plugin
    plugin_cmds = [f"plugin install {p} --activate" for p in plugins]
    theme_cmds = [f"theme install {t} --activate" for t in themes]

    run_wp_cli(plugin_cmds + theme_cmds, cwd=project_dir)

    print("✅ Instalasi plugin & theme selesai!")
