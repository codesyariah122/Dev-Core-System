import os
import sys
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

from core.env_manager import choose_environment, load_env_config
from core.template_engine import create_default_templates, generate_readme


def run_command(cmd, cwd=None):
    """Jalankan perintah shell dengan error handling"""
    try:
        subprocess.check_call(cmd, cwd=cwd, shell=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error saat menjalankan: {cmd}")
        sys.exit(1)


def create_laravel_project(client_name, name, stack, init_git=False, with_filament=False, serve=False):
    """Membuat project Laravel otomatis dengan Filament, Seeder, dan Auto Serve"""
    env_name, base_path = choose_environment()
    project_path = base_path / name.replace(" ", "-")

    if project_path.exists():
        print(f"⚠️ Folder {project_path} sudah ada, hapus dulu atau gunakan nama lain.")
        sys.exit(1)

    print(f"🚀 Membuat Laravel project di {project_path} ...")
    os.makedirs(project_path, exist_ok=True)

    # 1️⃣ Install Laravel
    run_command(f'composer create-project laravel/laravel "{project_path}"')

    # 2️⃣ Konfigurasi database
    print("\n🛠️  Konfigurasi Database Laravel:")
    db_name = input("Nama database (contoh: db_codesparks): ").strip()
    db_user = input("User database (default: root): ").strip() or "root"
    db_pass = input("Password database (boleh kosong): ").strip()

    env_file = project_path / ".env"
    if env_file.exists():
        env_content = env_file.read_text(encoding="utf-8")
        env_content = (
            env_content.replace("DB_DATABASE=laravel", f"DB_DATABASE={db_name}")
                        .replace("DB_USERNAME=root", f"DB_USERNAME={db_user}")
                        .replace("DB_PASSWORD=", f"DB_PASSWORD={db_pass}")
        )
        env_file.write_text(env_content, encoding="utf-8")
        print(f"✅ File .env diperbarui dengan database: {db_name}")

    # 3️⃣ Jalankan migrasi awal Laravel
    print("🧱 Menjalankan migrasi awal database bawaan Laravel...")
    run_command("php artisan migrate", cwd=project_path)

    # 4️⃣ Buat model + migration untuk tabel posts
    print("🧩 Membuat model + migration untuk tabel posts...")
    run_command("php artisan make:model Post -m", cwd=project_path)

    migration_dir = project_path / "database" / "migrations"
    for file in migration_dir.glob("*create_posts_table*.php"):
        content = file.read_text(encoding="utf-8")
        if "$table->id();" in content:
            # ⚙️ Tambahkan field tanpa duplikasi timestamps()
            updated = content.replace(
                "$table->id();",
                "$table->id();\n            $table->string('title');\n            $table->text('content')->nullable();"
            )
            file.write_text(updated, encoding="utf-8")
            print("✅ Migration posts_table diperbarui dengan field title & content.")
            break

    # 5️⃣ Jalankan ulang migrasi (fresh supaya tabel posts dibuat bersih)
    print("🔁 Menjalankan ulang migrasi dari awal...")
    run_command("php artisan migrate:fresh", cwd=project_path)

    # 6️⃣ Tambahkan data dummy otomatis
    seeder_code = """<?php
namespace Database\\Seeders;

use Illuminate\\Database\\Seeder;
use Illuminate\\Support\\Facades\\DB;

class PostSeeder extends Seeder {
    public function run(): void {
        DB::table('posts')->insert([
            ['title' => 'Hello Filament', 'content' => 'Post pertama otomatis dibuat oleh DevCore.'],
            ['title' => 'DevCore CLI', 'content' => 'Tool super cepat untuk scaffold Laravel & WordPress.'],
            ['title' => 'Laravel + Filament', 'content' => 'Dashboard admin otomatis siap pakai.'],
        ]);
    }
}
"""
    seeder_path = project_path / "database" / "seeders" / "PostSeeder.php"
    seeder_path.write_text(seeder_code, encoding="utf-8")
    print("🧩 Seeder PostSeeder dibuat otomatis.")

    run_command("php artisan db:seed --class=PostSeeder", cwd=project_path)
    print("🌱 Data dummy PostSeeder berhasil dimasukkan ke database.")

    # 7️⃣ Instalasi Filament (opsional)
    if with_filament:
        print("⚡ Menginstal Filament Admin Panel...")
        run_command("composer require filament/filament:\"^3.0\" -W", cwd=project_path)

        print("🧱 Menjalankan instalasi Filament panel default...")
        run_command("php artisan filament:install --panels --no-interaction", cwd=project_path)

        print("\n👤 Membuat user admin Filament")
        admin_name = input("Nama admin (default: Admin): ").strip() or "Admin"
        admin_email = input("Email admin (contoh: admin@example.com): ").strip()
        admin_pass = input("Password admin (default: password): ").strip() or "password"

        if not admin_email:
            print("❌ Email wajib diisi untuk user admin Filament.")
            sys.exit(1)

        run_command(f'php artisan make:filament-user --name="{admin_name}" --email="{admin_email}" --password="{admin_pass}"', cwd=project_path)
        print(f"✅ User admin berhasil dibuat: {admin_email} / {admin_pass}")

        # 📦 CRUD Filament Sample
        print("🧩 Membuat sample CRUD Filament untuk Post...")
        run_command("php artisan make:filament-resource Post --generate", cwd=project_path)

        resource_path = project_path / "app" / "Filament" / "Resources" / "PostResource.php"
        if resource_path.exists():
            content = resource_path.read_text(encoding="utf-8")

            # Form fields
            content = content.replace(
                "->schema([",
                """->schema([
                Forms\\Components\\TextInput::make('title')
                    ->label('Judul')
                    ->required()
                    ->maxLength(255),
                Forms\\Components\\Textarea::make('content')
                    ->label('Deskripsi')
                    ->rows(5),
            """,
            )

            # Table columns
            content = content.replace(
                "->columns([",
                """->columns([
                Tables\\Columns\\TextColumn::make('title')->label('Judul')->searchable()->sortable(),
                Tables\\Columns\\TextColumn::make('content')->label('Deskripsi')->limit(50),
            """,
            )

            resource_path.write_text(content, encoding="utf-8")
            print("✅ PostResource diperbarui otomatis dengan field title + deskripsi.")
        else:
            print("⚠️ File PostResource.php belum ditemukan, mungkin struktur Filament berubah.")

    # 8️⃣ Tambahkan README otomatis
    create_default_templates()
    context = {
        "name": name,
        "client_name": client_name,
        "project_type": "laravel",
        "stack": stack,
        "created_at": datetime.utcnow().isoformat(),
    }
    generate_readme(project_path, context)

    # 9️⃣ Inisialisasi Git
    if init_git:
        print("🌀 Inisialisasi Git repository...")
        run_command("git init", cwd=project_path)
        run_command("git add --all", cwd=project_path)
        run_command('git commit -m "chore: initial laravel scaffold by devcore"', cwd=project_path)

    print(f"✅ Laravel project berhasil dibuat di: {project_path}")

    # 🔟 Jalankan serve + auto open browser
    if serve:
        print("🚀 Menjalankan Laravel server di http://127.0.0.1:8000 ...")
        subprocess.Popen(["php", "artisan", "serve"], cwd=project_path)
        print("🖥️ Server Laravel berjalan di background (Ctrl+C untuk hentikan).")

        try:
            print("🌐 Membuka browser otomatis...")
            # Arahkan langsung ke dashboard Filament jika terpasang
            if with_filament:
                webbrowser.open("http://127.0.0.1:8000/admin/login")
            else:
                webbrowser.open("http://127.0.0.1:8000")
        except Exception as e:
            print(f"⚠️ Gagal membuka browser otomatis: {e}")

    return str(project_path)
