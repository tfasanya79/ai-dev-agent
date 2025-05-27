import os
import subprocess

def install_requirements(project_path):
    frontend = os.path.join(project_path, "frontend")
    backend = os.path.join(project_path, "backend")

    print("📦 Installing frontend dependencies...")
    if os.path.exists(frontend):
        subprocess.run(["npm", "install"], cwd=frontend)

    print("🐍 Installing backend dependencies...")
    requirements = os.path.join(backend, "requirements.txt")
    if os.path.exists(requirements):
        subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=backend)

    print("✅ Dependencies installed.")
