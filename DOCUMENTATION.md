
---

## 📘 2️⃣ `DOCUMENTATION.md`
```markdown
# 📘 DevCore CLI — Dokumentasi Resmi

> Versi: 1.0.0  
> Format: Laravel Artisan Docs Style  

---

## 🔧 Instalasi Awal

Pastikan Python sudah terinstal (`>=3.10`) dan path sudah terdaftar di environment variable.

```bash
git clone https://github.com/username/dev-core-system.git
cd dev-core-system
pip install -r requirements.txt
```  

#### ⚙️ Konfigurasi Global

File konfigurasi utama berada di:  

```bash
.devcore.json
```  

Contoh konfigurasi:  
```json
{
  "xampp": "C:/xampp/htdocs",
  "laragon": "C:/laragon/www",
  "laradock": "C:/Users/Laptop Store 95/tw-project/laradock"
}
```  

> Pastikan semua path ditulis dengan slash (/) forward, bukan backslash (\), untuk mencegah error encoding pada JSON.  

#### 🔐 Login ke GitHub

Gunakan command berikut untuk mengautentikasi:  
```bash
devcore login github
```  
Setelah login, DevCore otomatis menyimpan token ke dalam database internal (devcore_projects.db).  

#### 🧱 Membuat Project Baru

Gunakan perintah berikut:  

```bash
devcore new project --type wordpress --client "Client Name" --stack "wordpress+woo"
```  

Parameter:

- --type: Jenis project (wordpress, laravel, static)

- --client: Nama client

- --stack: Jenis stack (misal: wordpress+woo, wordpress+elementor)  

#### ⚡ WordPress Builder

Setelah template dibuat, jalankan:  
```bash
devcore wp init New-Commerce-Project
```  

###### Perintah ini akan:

1. Membuat direktori WordPress project.

2. Menyalin template dasar dari /templates/wordpress.

3. Melakukan konfigurasi database dan environment.

4. Menjalankan setup plugin dasar (WooCommerce, Elementor, JetEngine, dsb).  

#### 🔁 Config Management

Reset seluruh konfigurasi DevCore:  
```bash
devcore config reset
```  

Rebuild ulang konfigurasi dari awal:  
```bash
devcore config rebuild
```  

#### 💾 Database Project

Database internal DevCore:  
```bash
devcore_projects.db
```  
###### Berisi:

- Metadata project

- Path environment

- Status deployment

- Token user (jika ada)

Untuk menghapus database:  
```bash
del devcore_projects.db
```  

#### 🧭 Roadmap Detail  
| Fase | Fitur                                | Status | Target  |
| ---- | ------------------------------------ | ------ | ------- |
| 1    | Core CLI (login, config, DB handler) | ✅      | Q4 2025 |
| 2    | WordPress Stack Builder              | 🚧     | Q4 2025 |
| 3    | GitHub & VPS Integration             | ⏳      | Q1 2026 |
| 4    | Backup/Restore Automation            | ⏳      | Q2 2026 |
| 5    | Cloud Dashboard                      | 🧩     | Q3 2026 |

### 💬 Kontribusi

Buat branch baru dari main:  
```bash
git checkout -b feature/nama-fitur
```  

Commit sesuai standar:  
```bash
git commit -m "feat: menambahkan command reset config"
```  

Push ke repo:
```bash
git push origin feature/nama-fitur
```  

### 📚 Lisensi

MIT License © 2025 — DevCore Team  | Puji Ermanto<pujiermanto@gmail.com> As Software Engineer




