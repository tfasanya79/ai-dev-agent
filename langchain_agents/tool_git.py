from langchain.tools import tool
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@tool
def git_tool(input: str) -> str:
    """Initializes Git repo and pushes to GitHub."""
    path = os.path.expanduser("~/dev/generated_project")
    subprocess.run(["git", "init"], cwd=path)
    subprocess.run(["git", "remote", "add", "origin", input], cwd=path)
    subprocess.run(["git", "add", "."], cwd=path)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=path)
    subprocess.run(["git", "push", "-u", "origin", "master"], cwd=path)
    return "✅ Repo pushed to GitHub!"
