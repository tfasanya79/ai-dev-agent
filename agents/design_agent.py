# agents/design_agent.py

class DesignAgent:
    def __init__(self):
        pass

    def generate_design(self, project_name, description):
        # Stub: You can later expand this to use LLMs for detailed specs
        design = {
            "project_name": project_name,
            "description": description,
            "components": ["frontend", "backend", "API"],
            "tech_stack": {
                "frontend": "React",
                "backend": "FastAPI",
                "database": "SQLite"
            }
        }
        return design
