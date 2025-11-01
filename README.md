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

2️⃣ Membuat template awal  

```bash
devcore new project --type wordpress --client "New Commerce Project" --stack "wordpress+woo"
```  

3️⃣ Build WordPress Project  
```bash
devcore wp init New-Commerce-Project
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

📁 Struktur Direktori DevCore  
```bash
dev-core-system/
│
├── core/
│   ├── command_config.py
│   ├── command_new.py
│   ├── command_wp.py
│   ├── config_manager.py
│   └── utils.py
│
├── templates/
│   └── wordpress/
│
├── .devcore.json
├── devcore_projects.db
├── README.md
└── DOCUMENTATION.md
```  

🧭 Roadmap Singkat  
| Fase    | Deskripsi                              | Status         |
| ------- | -------------------------------------- | -------------- |
| Phase 1 | Core CLI & Config Handler              | ✅ Selesai     |
| Phase 2 | WordPress Stack Builder                | 🚧 In Progress |
| Phase 3 | Integration Layer (GitHub, VPS Deploy) | ⏳ Planned     |
| Phase 4 | Automation & Backup                    | ⏳ Planned     |
| Phase 5 | DevCore Cloud Dashboard                | 🧩 Research    |

📜 Lisensi

MIT License © 2025 — [DevCore Project Team > Puji Ermanto<pujiermanto@gmail.com>]  

💬 Kontribusi

Pull Request, Issue, dan Feedback selalu terbuka.
Silakan buat branch baru sebelum commit ke main.  

