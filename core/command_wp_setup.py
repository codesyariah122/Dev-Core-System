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
    
    
def generate_project_config(project_dir="."):
    """Generate ulang devcore_project.json berdasarkan input user atau default global"""
    print("🧱 Membuat ulang devcore_project.json ...")

    global_config = load_global_config()

    default_plugins = global_config.get("default_plugins", ["woocommerce"])
    default_themes = global_config.get("default_themes", ["flatsome"])

    project_name = input("📝 Nama proyek: ") or "New-Project"
    plugins_input = input(f"🔌 Plugin (pisahkan koma, default: {', '.join(default_plugins)}): ").strip()
    themes_input = input(f"🎨 Theme (pisahkan koma, default: {', '.join(default_themes)}): ").strip()

    plugins = [p.strip() for p in plugins_input.split(",")] if plugins_input else default_plugins
    themes = [t.strip() for t in themes_input.split(",")] if themes_input else default_themes

    config_data = {
        "project_name": project_name,
        "plugins": plugins,
        "themes": themes
    }

    config_path = Path(project_dir) / "devcore_project.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2)

    print(f"✅ File devcore_project.json berhasil dibuat di {config_path}")
