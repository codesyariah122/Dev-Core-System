# 🧠 DevCore CLI

DevCore adalah sistem otomatisasi untuk setup, konfigurasi, dan deployment stack WordPress modern melalui Command Line Interface (CLI).  
Didesain untuk developer yang ingin mempercepat workflow WordPress Development, mulai dari inisialisasi proyek, konfigurasi environment, hingga sinkronisasi GitHub — semua hanya lewat terminal.

---

## 🚀 Fitur Utama

- ⚙️ **WordPress Auto Installer & Setup**  
  Buat project WordPress siap-pakai hanya dengan satu perintah.

- 🧩 **Template Builder**  
  Dukung stack: `WordPress + WooCommerce + Elementor`.

- 💾 **Database Handler (SQLite)**  
  Menyimpan metadata project dan konfigurasi CLI dengan aman.

- 🔐 **Konfigurasi Environment Otomatis**  
  Termasuk rebuild & reset config.

- 🔄 **Auto Sync ke GitHub**  
  Login GitHub langsung dari CLI.

- 🧱 **Modular CLI Structure**  
  Setiap perintah terpisah secara modular di direktori `core/`.

---

## ⚡ Perintah Dasar DevCore

#### 1️⃣ Login GitHub terlebih dahulu
```bash
devcore login github
```  

#### Setup project 
```bash
devcore wp setup --generate
```  

2️⃣ Membuat template awal  

```bash
devcore new project --type wordpress --client "New-Commerce-Project" --stack "wordpress+woo"
```  

3️⃣ Build WordPress Project  
```bash
devcore wp init New-Commerce-Project
```  
#### Setup WordPress Plugins & Themes
Installs plugins and themes automatically using WP-CLI based on configuration files.

```bash
devcore wp init New-Commerce-Project --include-setup
```  

4️⃣ Reset atau Rebuild Konfigurasi
```bash
devcore config rebuild
devcore config reset
```  

5️⃣ Menghapus Database Project
```bash
del devcore_projects.db
```  

## For Laravel Project 
with filament :
```bash
devcore new project --type laravel --client "Code Sparks" --stack "laravel+vite" --init-git --with-filament --serve
```  
without filament :
```bash
devcore new project --type laravel --client "Code Sparks" --stack "laravel+vite" --serve
```

📁 Struktur Direktori DevCore  
```bash
dev-core-system/
│
├── core/
│   ├── command_config.py
│   ├── command_new_setup.py
│   ├── db.py
│   ├── env_manager.py
│   └── wp_init.py
│   └── wp_dropdb.py
│   └── github_integration.py
│   └── template_engine.py
│
├── templates/
│   └── .env.example (autogenerate)
│   └── docker-compose.yml (autogenerate)
│   └── README.md (autogenerate)
│
├── .devcore.json
├── devcore_projects.db
├── devcore.py
├── devcore.cmd
├── README.md
└── DOCUMENTATION.md
```  


#### Lists of commands  
| Command                                                                | Fungsi                                             | Status |
| ---------------------------------------------------------------------- | -------------------------------------------------- | ------ |
| `devcore login github`                                                 | Login ke GitHub (via `core/github_integration.py`) | ✅      |
| `devcore wp setup --generate`                                          | Generate `devcore_project.json`                    | 
✅      |
| `devcore wp new project --type wordpress --client "New-Commerce-Project"` | Buat scaffolding baru                              | ✅      |
| `devcore wp init New-Commerce-Project`                                 | Buat WP project baru                               | ✅      |
| `devcore wp init New-Commerce-Project --include-setup`                 | Build project + setup plugin & theme               | ✅      |
| `devcore config rebuild` / `config reset`                              | Reset config environment                           | ✅      |
| `devcore wp dropdb <nama_project>`                                     | Hapus database dan folder                          | ✅      |


🧭 Roadmap Singkat  
| Fase    | Deskripsi                              | Status         |
| ------- | -------------------------------------- | -------------- |
| Phase 1 | Core CLI & Config Handler              | ✅ Selesai     |
| Phase 2 | WordPress Stack Builder                | 🚧 In Progress |
| Phase 3 | Integration Layer (GitHub, VPS Deploy) | ⏳ Planned     |
| Phase 4 | Automation & Backup                    | ⏳ Planned     |
| Phase 5 | DevCore Cloud Dashboard                | 🧩 Research    |
<img width="1024" height="1536" alt="devcore-system-roadmap" src="https://github.com/user-attachments/assets/a4b64b39-068e-4ef2-8044-b2aadf9d4b39" />

📜 Lisensi

MIT License © 2025 — [DevCore Project Team > Puji Ermanto<pujiermanto@gmail.com>]  


#### Notes Error fixed   
```bash
rm -rf build dist *.egg-info
pip uninstall devcore-cli -y
```  

#### Rebuild & publish  
```bash
python -m build
pip install --upgrade build
twine upload dist/*

# 1️⃣ Bersihkan dulu build lama
rm -rf build dist *.egg-info

# 2️⃣ Build ulang package
python setup.py sdist bdist_wheel

# 3️⃣ Install ulang ke environment aktif
pip install --upgrade --force-reinstall dist/devcore_cli-1.0.3-py3-none-any.whl

# 1. Bersihkan build lama
rm -rf build dist *.egg-info

# 2. Build ulang
python -m build

# 3. Upload ke PyPI
twine upload dist/*

# 4. Instal versi terbaru
pip install --no-cache-dir -U devcore-cli

```  


#### Testing 
```bash
pip install --no-cache-dir -U devcore-cli
devcore --help
```

💬 Kontribusi

Pull Request, Issue, dan Feedback selalu terbuka.
Silakan buat branch baru sebelum commit ke main.  

