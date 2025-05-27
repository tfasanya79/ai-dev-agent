from langchain.tools import tool

@tool
def design_tool(input: str) -> str:
    """Generates a basic app design spec from a user input or document."""
    return f"Designing system based on: {input}\nProject Type: Web App\nFramework: React + Flask\nFeatures: Login, Dashboard, Logs Viewer"
