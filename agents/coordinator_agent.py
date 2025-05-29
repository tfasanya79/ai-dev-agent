import os
from agents.design_agent import DesignAgent
from agents.git_agent import GitAgent
# from agents.design_agent import DesignAgent  # Uncomment when implemented
# from agents.code_generator import CodeGeneratorAgent  # Uncomment when implemented

class CoordinatorAgent:
    def __init__(self):
        self.chat = None  # Placeholder for chat context if needed
        self.git_agent = GitAgent(chat=self.chat)
        # self.design_agent = DesignAgent()
        # self.codegen_agent = CodeGeneratorAgent(chat_model=None)

    def run(self):
        print("👋 Hello! Welcome to the AI Dev Agent.")
        print("Let's start by setting up your project.\n")

        # Collect user inputs
        project_name = input("📦 What should we name your project? ").strip()
        repo_url = input("🔗 (Optional) Provide a GitHub repo URL (or leave blank): ").strip()
        description = input("📝 Briefly describe what you're trying to build: ").strip()

        print("\n🧠 Generating initial design draft based on your input... (stubbed)")

        # Placeholder for design suggestion (replace with actual agent call)
        design = self.design_agent.generate_design(project_name, description)
"""         design = {
            "name": project_name,
            "description": description,
            "components": ["backend", "frontend"],
        } """
        print(f"\n🧾 Proposed Design:\n{design}")

        satisfied = input("\n✅ Are you satisfied with this design? (y/n): ").strip().lower()
        if satisfied != "y":
            print("📎 You can upload your own finalized design via future UI or API endpoints.")
            return

        print("\n📁 Initializing Git repo, virtualenv, and opening in VS Code...")
        project_path = self.git_agent.init_repo(project_name)

        # Proceed with code generation (placeholder)
        # self.codegen_agent.generate_code_from_spec(design)

        print("\n🚀 All set. Your project is ready in VS Code.")
        print("You can now watch files being created live as the agents work.")
