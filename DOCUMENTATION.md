# 🧱 DevCore System Documentation

A unified CLI framework to automate development workflows for WordPress, Laravel, and hybrid stacks. Inspired by **Laravel Artisan**, designed with simplicity, speed, and cross-environment automation in mind.

---

## 1️⃣ Installation & Setup

### 1.1 Prerequisites

* Node.js v18+
* Git (with GitHub account configured)
* Either **XAMPP**, **Laragon**, or **Laradock** installed locally.

### 1.2 Global Installation

```bash
npm install -g devcore
```

### 1.3 Initialize Configuration

Create or rebuild configuration for the first time:

```bash
devcore config rebuild
```

Reset configuration (remove `.devcore_config.json`):

```bash
devcore config reset
```

---

## 2️⃣ Authentication

### 2.1 GitHub Login

Authenticate your GitHub account for project initialization and version control.

```bash
devcore login github
```

---

## 3️⃣ Project Management Commands

### 3.1 Create a New Template

```bash
devcore new project --type wordpress --client "New Commerce Project" --stack "wordpress+woo"
```

This command scaffolds the base structure for your client project with proper stack settings.

### 3.2 Initialize WordPress Build

```bash
devcore wp init New-Commerce-Project
```

Automatically builds and configures a full WordPress + WooCommerce environment based on your stack setup.

### 3.3 Remove Database

```bash
del devcore_projects.db
```

Deletes the local DevCore database, resetting stored project records.

---

## 4️⃣ Environment Configuration

### 4.1 Supported Environments

* XAMPP → `C:/xampp/htdocs`
* Laragon → `C:/laragon/www`
* Laradock → `C:/Users/<YourUser>/tw-project/laradock`

> ⚠️ Make sure your local stack (XAMPP, Laragon, or Laradock) is **running** before initializing or deploying a project.

### 4.2 Environment Path Fix

If paths with spaces fail (like `Laptop Store 95`), wrap the path in quotes or escape them properly in `.devcore_config.json`.

Example:

```json
{
  "xampp": "C:/xampp/htdocs",
  "laragon": "C:/laragon/www",
  "laradock": "C:/Users/Laptop Store 95/tw-project/laradock"
}
```

---

## 5️⃣ Roadmap & Milestones

| Milestone | Description                                    | Status         |
| --------- | ---------------------------------------------- | -------------- |
| v0.1      | Base CLI setup, config handler, WordPress init | ✅ Done         |
| v0.2      | Laravel + Hybrid Stack integration             | 🔄 In Progress |
| v0.3      | DevCore Dashboard UI (web-based CLI logs)      | ⏳ Planned      |
| v1.0      | Plugin Marketplace + Auto-deploy Git Actions   | 🚧 Coming Soon |

> 📄 See the visual roadmap image: `roadmap-devcore.png`

---

## 6️⃣ Contributing

1. Fork this repo
2. Create a new branch for your feature
3. Commit and push your updates
4. Submit a pull request with detailed notes

---

## 7️⃣ License

MIT License © 2025 DevCore Authors

---

## 📘 DOCUMENTATION.md (Extended Guide)

### Overview

`DevCore CLI` is an automation layer for local WordPress & Laravel environments, built to:

* Reduce repetitive setup tasks
* Maintain consistent project scaffolding
* Integrate version control and environment sync automatically

### Command Reference

| Command                  | Description                         |
| ------------------------ | ----------------------------------- |
| `devcore login github`   | Authenticate GitHub for repo access |
| `devcore new project`    | Create new client or stack project  |
| `devcore wp init`        | Setup and build WordPress structure |
| `devcore config rebuild` | Reinitialize global configuration   |
| `devcore config reset`   | Delete config and start fresh       |

### Configuration File

`.devcore_config.json` is stored globally in your user home directory. Example:

```json
{
  "xampp": "C:/xampp/htdocs",
  "laragon": "C:/laragon/www",
  "laradock": "C:/Users/puji/tw-project/laradock"
}
```

### Error Handling

If `devcore` cannot detect your environment, run:

```bash
devcore config rebuild
```

Or manually check permissions on your local server folder.

### Advanced Usage

Generate boilerplate code for stacks (planned for v0.3):

```bash
devcore generate stack laravel-wordpress
```

---

**Author:** Puji Ermanto
**Maintainer:** GPT-5 x DevCore System
**Version:** 0.2.0-alpha
