from core.github_integration import github_init
from core.db import add_project, update_repo_url
from core.template_engine import generate_readme
from core.env_manager import choose_environment
from datetime import datetime
import os
import subprocess
import zipfile
import requests
import shutil
from pathlib import Path

def init_wp_project(project_name):
    env, base_dir = choose_environment()
    project_dir = base_dir / project_name
    wp_zip_path = project_dir / "wordpress.zip"
    wp_url = "https://wordpress.org/latest.zip"

    print(f"🚀 Membuat project WordPress di {env.upper()}: {project_dir}")
    os.makedirs(project_dir, exist_ok=True)

    # === 1. Download WordPress ===
    print("⬇️  Downloading WordPress core...")
    r = requests.get(wp_url)
    with open(wp_zip_path, "wb") as f:
        f.write(r.content)

    # === 2. Extract WordPress ===
    print("📦 Ekstrak WordPress...")
    with zipfile.ZipFile(wp_zip_path, "r") as zip_ref:
        zip_ref.extractall(project_dir)

    # === 3. Pindahkan isi folder "wordpress" ke root ===
    wp_src = project_dir / "wordpress"
    if wp_src.exists():
        for item in wp_src.iterdir():
            dest = project_dir / item.name
            # Kalau sudah ada, hapus dulu
            if dest.exists():
                if dest.is_dir():
                    shutil.rmtree(dest)
                else:
                    dest.unlink()
            # Gunakan move, bukan rename (rename rawan error di Windows)
            shutil.move(str(item), str(dest))
        shutil.rmtree(wp_src)

    # Hapus file zip setelah selesai
    if wp_zip_path.exists():
        wp_zip_path.unlink()

    # === 4. Buat struktur tambahan ===
    print("🧩 Membuat struktur Dev Core...")
    os.makedirs(project_dir / "src/themes", exist_ok=True)
    os.makedirs(project_dir / "src/plugins", exist_ok=True)

    # === 5. Buat file .env ===
    if env == "laragon":
        wp_home = f"http://{project_name}.test"
        wp_siteurl = f"http://{project_name}.test/wp"
    else:
        wp_home = f"http://localhost/{project_name}"
        wp_siteurl = f"http://localhost/{project_name}/wp"

    env_content = f"""# Environment WordPress
DB_NAME={project_name}_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
WP_HOME={wp_home}
WP_SITEURL={wp_siteurl}
"""
    with open(project_dir / ".env", "w") as f:
        f.write(env_content)

    # === 6. Buat docker-compose.yml ===
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
    with open(project_dir / "docker-compose.yml", "w") as f:
        f.write(docker_content)

    # === 7. Inisialisasi Git ===
    print("📤 Inisialisasi Git repository...")
    subprocess.run(["git", "init"], cwd=project_dir)
    subprocess.run(["git", "add", "."], cwd=project_dir)
    subprocess.run(["git", "commit", "-m", "Initialize WordPress project"], cwd=project_dir)
    subprocess.run(["git", "branch", "-M", "main"], cwd=project_dir)

     # === 8. Push otomatis ke GitHub ===
    print("🌐 Menghubungkan ke GitHub...")
    github_init(project_name, project_dir)

    print("✅ WordPress project berhasil dibuat dan diunggah ke GitHub!")
    
    add_project(
        name=project_name,
        client_name="default",  # nanti bisa diisi dari argumen CLI
        project_type="wordpress",
        stack="wordpress+docker",
        path=str(project_dir),
        repo_url=f"https://github.com/codesyariah122/{project_name}",
        status="pushed"
    )

    print("📊 Metadata project tersimpan di devcore_projects.db")
    
    context = {
        "name": project_name,
        "client_name": "default",
        "project_type": "wordpress",
        "stack": "wordpress+docker",
        "created_at": datetime.utcnow().isoformat()
    }
    generate_readme(project_dir, context)
    
    # === 7. Optional: Auto-create MySQL database for local env ===
    if env in ["xampp", "laragon"]:
        # Nama database = nama project, diubah biar aman buat MySQL
        db_name = project_name.lower().replace("-", "_").replace(" ", "_") + "_db"

        print(f"🧩 Membuat database lokal '{db_name}' di MySQL...")

        try:
            subprocess.run(["mysql", "-u", "root", "-e", f"CREATE DATABASE IF NOT EXISTS {db_name};"], check=True)
            print(f"✅ Database '{db_name}' berhasil dibuat di MySQL lokal.")

            # Cek kalau ada file SQL default
            default_sql = Path(__file__).resolve().parent.parent / "templates" / "default_wp.sql"
            if default_sql.exists():
                print(f"📥 Mengimpor data default dari {default_sql.name}...")
                subprocess.run(["mysql", "-u", "root", db_name, "<", str(default_sql)], shell=True, check=True)
                print("✅ Import data default berhasil.")
            else:
                print("ℹ️  Tidak ada file default_wp.sql, dilewati.")
        except FileNotFoundError:
            print("⚠️  MySQL CLI tidak ditemukan di PATH. Lewati auto-create database.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Gagal membuat database: {e}")


