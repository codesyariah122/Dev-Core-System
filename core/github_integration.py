import os
import json
import subprocess
import requests
from pathlib import Path

CONFIG_PATH = Path.home() / ".devcore" / "config.json"


# ==============================
# Utility: Config Management
# ==============================
def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(data):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)


# ==============================
# GitHub Login / Token Setup
# ==============================
def github_login():
    print("Masukkan GitHub Personal Access Token (PAT):")
    token = input("> ").strip()
    if not token.startswith("ghp_") and not token.startswith("github_"):
        print("⚠️  Token tidak valid. Pastikan menggunakan format GitHub PAT.")
        return

    config = load_config()
    config["github_token"] = token
    save_config(config)
    print("✅ Token GitHub disimpan di ~/.devcore/config.json")


# ==============================
# GitHub Repo Creation
# ==============================
def create_github_repo(repo_name, private=True, description=""):
    config = load_config()
    token = config.get("github_token")
    if not token:
        print("❌ Belum login GitHub. Jalankan 'devcore login github' dulu.")
        return None

    api_url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    payload = {
        "name": repo_name,
        "private": private,
        "description": description or f"Repository for {repo_name} with devcore system by puji",
    }

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 201:
        repo_data = response.json()
        print(f"✅ Repository berhasil dibuat: {repo_data['html_url']}")
        return repo_data["clone_url"]
    else:
        print("❌ Gagal membuat repository:", response.text)
        return None


# ==============================
# Local Git Initialization
# ==============================
def init_local_git(project_path, repo_url):
    try:
        # Cek apakah sudah ada repo git
        git_dir = Path(project_path) / ".git"
        if not git_dir.exists():
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=project_path, check=True)
        else:
            # Sudah ada repo, pastikan ada perubahan baru
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)
            subprocess.run(["git", "commit", "-m", "Sync commit"], cwd=project_path)

        # Set remote origin (replace kalau sudah ada)
        subprocess.run(["git", "remote", "remove", "origin"], cwd=project_path, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=project_path, check=True)

        # Push ke GitHub
        subprocess.run(["git", "push", "-u", "origin", "main"], cwd=project_path, check=True)
        print("🚀 Project berhasil di-push ke GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Gagal menjalankan git command: {e}")



# ==============================
# Public API for CLI
# ==============================
def github_init(project_name, project_path):
    print(f"🔧 Membuat repository untuk project: {project_name}")
    repo_url = create_github_repo(project_name)
    if repo_url:
        init_local_git(project_path, repo_url)


def github_connect(project_path, existing_repo_url):
    print(f"🔗 Menghubungkan project ke repo: {existing_repo_url}")
    init_local_git(project_path, existing_repo_url)
