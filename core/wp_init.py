from core.github_integration import github_init
from core.db import add_project
from core.template_engine import generate_readme
from core.env_manager import choose_environment, get_mysql_path, add_to_system_path
from datetime import datetime

import os
import subprocess
import zipfile
import requests
import shutil
from pathlib import Path

def init_wp_project(project_name, include_setup=False):
    # === 1. Pilih environment (xampp / laragon / laradock) ===
    env, base_dir = choose_environment()
    mysql_path = get_mysql_path(env)

    # === 2. Setup MySQL path ===
    if mysql_path:
        print(f"🔍 Mengecek PATH MySQL untuk {env}: {mysql_path}")
        add_to_system_path(mysql_path)
        mysql_executable = str(mysql_path / "mysql")
    else:
        print("⚠️ Tidak menemukan lokasi MySQL untuk environment ini.")
        mysql_executable = "mysql"  # fallback

    project_dir = base_dir / project_name
    wp_zip_path = project_dir / "wordpress.zip"
    wp_url = "https://wordpress.org/latest.zip"

    print(f"🚀 Membuat project WordPress di {env.upper()}: {project_dir}")
    os.makedirs(project_dir, exist_ok=True)

    # === 3. Download WordPress core ===
    print("⬇️  Downloading WordPress core...")
    r = requests.get(wp_url)
    with open(wp_zip_path, "wb") as f:
        f.write(r.content)

    # === 4. Extract dan pindahkan isi ===
    print("📦 Ekstrak WordPress...")
    with zipfile.ZipFile(wp_zip_path, "r") as zip_ref:
        zip_ref.extractall(project_dir)

    wp_src = project_dir / "wordpress"
    if wp_src.exists():
        for item in wp_src.iterdir():
            shutil.move(str(item), str(project_dir / item.name))
        shutil.rmtree(wp_src)

    wp_zip_path.unlink(missing_ok=True)

    # === 5. Struktur tambahan ===
    print("🧩 Membuat struktur Dev Core tambahan...")
    os.makedirs(project_dir / "src/themes", exist_ok=True)
    os.makedirs(project_dir / "src/plugins", exist_ok=True)

    # === 6. File .env ===
    wp_home = f"http://{project_name}.test" if env == "laragon" else f"http://localhost/{project_name}"
    wp_siteurl = f"{wp_home}/wp"

    env_content = f"""# Environment WordPress
DB_NAME={project_name}_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
WP_HOME={wp_home}
WP_SITEURL={wp_siteurl}
"""
    (project_dir / ".env").write_text(env_content)

    # === 7. docker-compose.yml ===
    docker_content = f"""version: '3.8'
services:
  db:
    image: mysql:5.7
    container_name: {project_name}_db
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: {project_name}_db
    volumes:
      - ./db_data:/var/lib/mysql
    ports:
      - "3306:3306"

  wordpress:
    image: wordpress:latest
    container_name: {project_name}_wp
    depends_on:
      - db
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: root
      WORDPRESS_DB_PASSWORD: root
      WORDPRESS_DB_NAME: {project_name}_db
    ports:
      - "8080:80"
    volumes:
      - ./:/var/www/html
"""
    (project_dir / "docker-compose.yml").write_text(docker_content)

    # === 8. Git init ===
    print("📤 Inisialisasi Git repository...")
    subprocess.run(["git", "init"], cwd=project_dir, check=False)
    subprocess.run(["git", "add", "."], cwd=project_dir, check=False)
    subprocess.run(["git", "commit", "-m", "Initialize WordPress project"], cwd=project_dir, check=False)
    subprocess.run(["git", "branch", "-M", "main"], cwd=project_dir, check=False)

    # === 9. Push otomatis ke GitHub ===
    print("🌐 Menghubungkan ke GitHub...")
    github_init(project_name, project_dir)

    # === 10. Simpan metadata project ===
    add_project(
        name=project_name,
        client_name="default",
        project_type="wordpress",
        stack="wordpress+docker",
        path=str(project_dir),
        repo_url=f"https://github.com/codesyariah122/{project_name}",
        status="pushed"
    )

    print("📊 Metadata project tersimpan di devcore_projects.db")

    # === 11. Generate README ===
    context = {
        "name": project_name,
        "client_name": "default",
        "project_type": "wordpress",
        "stack": "wordpress+docker",
        "created_at": datetime.utcnow().isoformat()
    }
    generate_readme(project_dir, context)

    # === 12. Optional: Buat database lokal ===
    if env in ["xampp", "laragon"]:
        db_name = project_name.lower().replace("-", "_").replace(" ", "_") + "_db"
        print(f"🧩 Membuat database lokal '{db_name}'...")

        try:
            subprocess.run([mysql_executable, "-u", "root", "-e", f"CREATE DATABASE IF NOT EXISTS {db_name};"], check=True)
            print(f"✅ Database '{db_name}' berhasil dibuat di MySQL lokal.")
        except FileNotFoundError:
            print("⚠️ MySQL CLI tidak ditemukan di PATH atau lokasi umum.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal membuat database: {e}")
            
    # === 12.1 Buat devcore_project.json default jika belum ada ===
    config_path = project_dir / "devcore_project.json"
    if not config_path.exists():
        default_config = {
            "project_name": project_name,
            "plugins": ["woocommerce", "jetpack"],
            "themes": ["blocksy", "blocksy-child"]
        }
        with open(config_path, "w", encoding="utf-8") as f:
            import json
            json.dump(default_config, f, indent=4)
        print("🧾 devcore_project.json default dibuat otomatis.")
    else:
        print("✅ devcore_project.json sudah ada, skip pembuatan.")

    # === 13. Install plugin & theme dari devcore_project.json ===
    install_plugins_and_themes(project_dir)
    print("🎉 WordPress project berhasil dibuat lengkap!\n")
    
def install_plugins_and_themes(project_dir):
    """Baca devcore_project.json lalu install plugin & theme sesuai daftar"""
    import json
    import shutil

    config_path = project_dir / "devcore_project.json"
    if not config_path.exists():
        print("⚠️ Tidak menemukan devcore_project.json, skip instalasi plugin/theme.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    plugins = config.get("plugins", [])
    themes = config.get("themes", [])

    if not plugins and not themes:
        print("ℹ️ Tidak ada plugin atau theme untuk diinstall.")
        return

    # === Cari wp-cli ===
    wp_cli = shutil.which("wp")
    if not wp_cli:
        tools_dir = Path(__file__).resolve().parent.parent / "tools" / "wp-cli"
        tools_dir.mkdir(parents=True, exist_ok=True)
        wp_phar = tools_dir / "wp-cli.phar"

        if not wp_phar.exists():
            print("⬇️  WP-CLI belum ada. Mengunduh dari https://github.com/wp-cli/builds...")
            url = "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
            r = requests.get(url, timeout=30)
            wp_phar.write_bytes(r.content)
            print(f"✅ WP-CLI berhasil diunduh ke {wp_phar}")

        php_path = shutil.which("php")
        if not php_path:
            print("❌ PHP CLI tidak ditemukan di PATH. Instalasi plugin/theme dibatalkan.")
            return

        wp_cli_cmd = [php_path, str(wp_phar)]
    else:
        wp_cli_cmd = [wp_cli]
        
    # === Clear cache sebelum instalasi ===
    print("🧹 Membersihkan cache WP-CLI...")
    subprocess.run(wp_cli_cmd + ["cache", "clear"], cwd=project_dir, check=False)

    # === Pastikan wp-config.php sudah ada ===
    wp_config = project_dir / "wp-config.php"
    if not wp_config.exists():
        print("🧾 Membuat wp-config.php otomatis ...")
        subprocess.run(
            wp_cli_cmd + [
                "config", "create",
                "--dbname=" + f"{project_dir.name.lower().replace('-', '_')}_db",
                "--dbuser=root",
                "--dbpass=",
                "--dbhost=localhost",
                "--skip-check"
            ],
            cwd=project_dir,
            check=False
        )

        # === Pastikan wp-config.php ada ===
    db_name = f"{project_dir.name.lower().replace('-', '_')}_db"
    wp_config = project_dir / "wp-config.php"

    if not wp_config.exists():
        print(f"🧱 Membuat wp-config.php untuk {db_name} ...")

        subprocess.run([
            wp_cli,
            "config",
            "create",
            f"--dbname={db_name}",
            "--dbuser=root",
            "--dbpass=",
            "--dbhost=localhost"
        ], cwd=project_dir, check=False)

        if wp_config.exists():
            print("✅ wp-config.php berhasil dibuat.")
        else:
            print("⚠️ Gagal membuat wp-config.php, cek WP-CLI dan izin folder.")

    # === Jalankan wp core install jika belum ada wp_options ===
    print("⚙️  Menjalankan instalasi WordPress awal ...")
    subprocess.run(
        wp_cli_cmd + [
            "core", "install",
            "--url=http://localhost/" + project_dir.name,
            "--title=" + project_dir.name,
            "--admin_user=admin",
            "--admin_password=admin",
            "--admin_email=admin@example.com"
        ],
        cwd=project_dir,
        check=False
    )

    print("🔌 Menginstal plugin dan theme sesuai devcore_project.json ...")

    # Jalankan instalasi plugin
    for plugin in plugins:
        print(f"➡️  Install plugin: {plugin}")
        subprocess.run(wp_cli_cmd + ["plugin", "install", plugin, "--activate"], cwd=project_dir, check=False)

    # Jalankan instalasi theme
    for theme in themes:
        print(f"🎨 Install theme: {theme}")
        subprocess.run(wp_cli_cmd + ["theme", "install", theme, "--activate"], cwd=project_dir, check=False)

    print("✅ Semua plugin dan theme selesai diinstall.")



