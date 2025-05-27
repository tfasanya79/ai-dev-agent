import os
import subprocess

class GitAgent:
    def __init__(self, chat):
        self.chat = chat

    def init_repo(self, project_name):
        path = os.path.join(os.getcwd(), project_name)
        os.makedirs(path, exist_ok=True)
        subprocess.run(["git", "init"], cwd=path)
        subprocess.run(["git", "checkout", "-b", "main"], cwd=path)
        print(f"📁 Initialized Git repo at: {path}")
        return path

    def auto_commit(self, path, message="Auto commit"):
        try:
            subprocess.run(["git", "add", "."], cwd=path, check=True)
            subprocess.run(["git", "commit", "-m", message], cwd=path, check=True)
            print(f"✅ Git commit made: {message}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git commit failed: {e}")
