import os

def write_project_files(files: dict, base_path: str):
    for relative_path, content in files.items():
        full_path = os.path.join(base_path, relative_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
