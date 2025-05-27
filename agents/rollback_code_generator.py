import subprocess
import os

class CodeGeneratorAgent:
    def __init__(self, chat):
        self.chat = chat

    def generate_code(self, spec, path):
        if spec["framework"] == "react":
            subprocess.run(["npx", "create-react-app", "frontend"], cwd=path)
            self.chat.show("Created React app in 'frontend' directory.")
