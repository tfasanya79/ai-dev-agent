import subprocess
import os
from generators.frontend_generator import generate_frontend_code
from generators.backend_generator import generate_backend_code
from generators.file_writer import write_project_files


class CodeGeneratorAgent:
    def __init__(self, chat_model=None):
        self.chat_model = chat_model

    def generate_code(self, spec: dict, path: str):
        print("🤖 Generating frontend code...")
        frontend_files = generate_frontend_code(spec)

        print("🤖 Generating backend code...")
        backend_files = generate_backend_code(spec)

        all_files = {**frontend_files, **backend_files}

        print(f"🤖 Writing {len(all_files)} files to disk...")
        write_project_files(all_files, path)

        print("✅ Code generation complete.")

    def generate_code_from_spec(self, spec: str) -> str:
        # This method is used in 'spec' mode
        return f"Generated code for spec:\n\n{spec}"
