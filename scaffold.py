# scaffold.py
# ----------------------------
# Usage:
#   $ git clone https://github.com/your-username/create-myapp
#   $ cd create-myapp
#   $ python3 scaffold.py
#
# This script generates a basic Python project structure
# Supports Flask or CLI apps
# Optional libs: requests, SQLAlchemy
# Generates .env, README.md, .gitignore, requirements.txt
# Auto-inits git and makes first commit

import os
import subprocess
import sys

PROJECT_OPTIONS = ["flask", "cli"]
OPTIONAL_LIBS = ["requests", "sqlalchemy"]


def ask(prompt, options=None):
    while True:
        value = input(f"{prompt}: ").strip()
        if not options or value in options:
            return value
        print(f"Please choose from {options}.")


def make_folder(path):
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def create_gitignore(path):
    content = """__pycache__/
*.pyc
venv/
.env
"""
    write_file(os.path.join(path, ".gitignore"), content)


def create_env(path):
    content = """FLASK_ENV=development
SECRET_KEY=your-secret-key
"""
    write_file(os.path.join(path, ".env"), content)


def create_readme(path, name):
    content = f"""# {name}

Generated with scaffold.py. Edit this README to document your project.
"""
    write_file(os.path.join(path, "README.md"), content)


def create_requirements(path, app_type, libs):
    reqs = []
    if app_type == "flask":
        reqs.append("flask")
    if app_type == "django":
        reqs.append("django")
    reqs.extend(libs)
    write_file(os.path.join(path, "requirements.txt"), "\n".join(reqs) + "\n")


def create_main_file(path, app_type):
    if app_type == "flask":
        content = ("""from flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef hello():\n    return 'Hello from Flask!'\n\nif __name__ == '__main__':\n    app.run(debug=True)\n""")
    else:
        content = ("""def main():\n    print('Hello from CLI app!')\n\nif __name__ == '__main__':\n    main()\n""")
    write_file(os.path.join(path, "main.py"), content)


def create_tests_folder(path):
    test_content = """def test_sample():\n    assert 1 + 1 == 2\n"""
    test_path = os.path.join(path, "tests")
    make_folder(test_path)
    write_file(os.path.join(test_path, "test_sample.py"), test_content)


def init_git(path):
    try:
        subprocess.run(["git", "init"], cwd=path, check=True)
        subprocess.run(["git", "add", "."], cwd=path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path, check=True)
    except subprocess.CalledProcessError:
        print("[!] Git init failed. Is git installed?")


def create_venv(path):
    try:
        subprocess.run(["python3", "-m", "venv", "venv"], cwd=path, check=True)
    except subprocess.CalledProcessError:
        print("[!] Failed to create virtualenv.")


def main():
    print("=== Python Project Scaffold ===")
    name = ask("Project name")
    app_type = ask("App type (flask or cli)", PROJECT_OPTIONS)
    libs = []

    print("Select optional libraries (press enter to skip):")
    for lib in OPTIONAL_LIBS:
        if input(f"Include {lib}? (y/n): ").strip().lower() == "y":
            libs.append(lib)

    base_path = os.path.abspath(name)
    make_folder(base_path)

    create_main_file(base_path, app_type)
    create_requirements(base_path, app_type, libs)
    create_gitignore(base_path)
    create_env(base_path)
    create_readme(base_path, name)
    create_tests_folder(base_path)
    create_venv(base_path)
    init_git(base_path)

    print(f"\n[✓] Project '{name}' created at {base_path}")
    print("Next:")
    print(f"  cd {name}")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")


if __name__ == "__main__":
    main()
