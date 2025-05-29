import os
import subprocess

class GitAgent:
    def __init__(self, chat=None):
        self.chat = chat

    def init_repo(self, project_name):
        path = os.path.join(os.getcwd(), project_name)
        os.makedirs(path, exist_ok=True)

        # Initialize Git
        subprocess.run(["git", "init"], cwd=path)
        subprocess.run(["git", "checkout", "-b", "main"], cwd=path)
        print(f"📁 Initialized Git repo at: {path}")

        # Create virtual environment
        self.create_virtualenv(path)

        return path

    def create_virtualenv(self, path):
        print("🐍 Creating Python virtual environment (.venv)...")
        subprocess.run(["python3", "-m", "venv", ".venv"], cwd=path)
        print("✅ Virtual environment created.")

    def open_in_vscode(self, path):
        try:
            print("🚀 Opening in VS Code...")
            subprocess.run(["code", path])
        except FileNotFoundError:
            print("❌ VS Code CLI not found. Make sure 'code' is in your PATH.")

    def auto_commit(self, path, message="Auto commit"):
        try:
            subprocess.run(["git", "add", "."], cwd=path, check=True)
            subprocess.run(["git", "commit", "-m", message], cwd=path, check=True)
            print(f"✅ Git commit made: {message}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git commit failed: {e}")
