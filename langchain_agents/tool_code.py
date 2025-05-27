from langchain.tools import tool
import os
import subprocess

@tool
def codegen_tool(input: str) -> str:
    """Generates boilerplate frontend/backend code in a target directory."""
    path = os.path.expanduser("~/dev/generated_project")
    os.makedirs(path, exist_ok=True)
    subprocess.run(["npx", "create-react-app", "frontend"], cwd=path)
    return f"React app created at {path}/frontend"
