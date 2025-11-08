# core/template_engine.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

TEMPLATE_DIR = Path.cwd() / "templates"

def create_default_templates():
    """
    Membuat folder templates dan file README.md.j2 default
    jika belum ada di direktori kerja.
    """
    TEMPLATE_DIR.mkdir(exist_ok=True)

    readme_template = TEMPLATE_DIR / "README.md.j2"

    if not readme_template.exists():
        readme_template.write_text(
            """# {{ name | title }}

Client: {{ client_name }}
Project Type: {{ project_type }}
Stack: {{ stack }}

Generated automatically by **DevCore CLI** on {{ created_at }}.

## 🚀 Quick Start
1. Jalankan local server (Laragon/XAMPP/Docker)
2. Buka {{ stack }} di browser
3. Enjoy building your project 🎉
""",
            encoding="utf-8",
        )
        print("📁 Default template README.md.j2 dibuat otomatis.")
    else:
        print("✅ Template README.md.j2 sudah ada, skip pembuatan.")
def render_readme(context):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("README.md.j2")
    return template.render(context)

def generate_readme(project_path, context):
    output_path = Path(project_path) / "README.md"
    readme_content = render_readme(context)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("🧾 README.md otomatis dibuat.")
