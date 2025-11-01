# core/template_engine.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

TEMPLATE_DIR = Path.cwd() / "templates"

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
