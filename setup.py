from setuptools import setup, find_packages

setup(
    name="devcore-cli",
    version="1.0.0",
    author="Puji Ermanto | <Engineer>",
    author_email="puji@gmail.com",
    description="DevCore — WordPress & Laravel project automation CLI",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2>=3.1.2",
    ],
    entry_points={
        "console_scripts": [
            "devcore=devcore_cli:main",
        ],
    },
    python_requires=">=3.8",
)
