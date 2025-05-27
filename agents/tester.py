import subprocess
import os

class TesterAgent:
    def __init__(self, chat):
        self.chat = chat

    def run_tests(self, path):
        frontend_path = os.path.join(path, "frontend")
        if os.path.exists(frontend_path):
            subprocess.run(["npm", "test"], cwd=frontend_path)
            self.chat.show("✅ Ran frontend tests.")
