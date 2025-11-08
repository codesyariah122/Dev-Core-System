from setuptools import setup, find_packages
from pathlib import Path

# Baca file README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="devcore-cli",
    version="1.0.7",
    author="Puji Ermanto | <Engineer>",
    author_email="puji@gmail.com",
    description="DevCore — WordPress & Laravel project automation CLI",
    long_description=long_description,  # ← Tambahkan ini
    long_description_content_type="text/markdown",  # ← Supaya PyPI bisa render markdown
    url="https://github.com/pujiermanto/devcore-cli",  # optional tapi direkomendasikan
    packages=find_packages(include=["core", "core.*"]),
    package_dir={"core": "core"},
    py_modules=["devcore"],
    include_package_data=True,
    install_requires=[
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "devcore=devcore:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Environment :: Console",
    ],
)
