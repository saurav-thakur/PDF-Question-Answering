import os
from pathlib import Path

project_name = "pdf_question_answering"

list_of_files = [
    ".github/workflows/action.yml",
    f"{project_name}/__init__.py",
    f"{project_name}/helper.py",
    f"{project_name}/prompt.py",
    f"{project_name}/routes.py",
    f"{project_name}/schemas.py",
    f"{project_name}/storage.py",
    f"{project_name}/websockets.py",
    f"{project_name}/models.py",
    f"{project_name}/config.py",
    f"{project_name}/app.py",
    "notebooks/01_experiment.ipynb",
    "tests/__init__.py",
    "tests/test_app.py",
    ".env",
    "Dockerfile",
    ".dockerignore",
    "main.py",
]

for filepath in list_of_files:
    file_path = Path(filepath)
    filedir, filename = os.path.split(file_path)

    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        print(f"creating directory: {filedir} for file: {filename}")

    if (not os.path.exists(file_path)) or (os.path.getsize(file_path) == 0):
        os.system(f"touch {file_path}")
        print(f"file created at: {file_path}")

    else:
        print(f"file already exists!!")
