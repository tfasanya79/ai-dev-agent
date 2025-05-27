from langchain.tools import tool
import subprocess
import os

@tool
def test_tool(input: str) -> str:
    """Runs frontend unit tests (npm test)."""
    path = os.path.expanduser("~/dev/generated_project/frontend")
    result = subprocess.run(["npm", "test", "--", "--watchAll=false"], cwd=path, capture_output=True, text=True)
    return result.stdout
