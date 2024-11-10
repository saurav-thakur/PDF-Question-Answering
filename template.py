import os
from pathlib import Path

project_name = "pdf_question_answering"

list_of_files = [
    ".github/workflows/action.yml",
    f"{project_name}/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/db/config.py",
    f"{project_name}/db/database.py",
    f"{project_name}/db/models.py",
    f"{project_name}/db/schemas.py",
    f"{project_name}/db/storage.py",
    f"{project_name}/db/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/llm/embeddings.py",
    f"{project_name}/llm/llm.py",
    f"{project_name}/llm/llm_service.py",
    f"{project_name}/llm/vector_db.py",
    f"{project_name}/llm/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/routers/routes.py",
    f"{project_name}/routers/__init__.py",
    f"{project_name}/utils/read_pdf.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/websocket/websockets.py",
    f"{project_name}/websocket/__init__.py",
    "notebooks/01_experiment.ipynb",
    "tests/test_app.py",
    "tests/__init__.py",
    ".env",
    "Dockerfile",
    ".dockerignore",
    ".gitignore",
    "app.py",
    "LICENSE",
    "main.py",
    "poetry.lock",
    "pyproject.toml",
    "README.md",
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
