import os
import re
import subprocess
from agents.planner_agent import PlannerAgent
from agents.design import DesignAgent
from agents.git_agent import GitAgent
from agents.tester import TesterAgent
from agents.code_generator import CodeGeneratorAgent
from agents.executor import ExecutorAgent
from chat.chat_interface import ChatInterface

def sanitize_project_name(text: str) -> str:
    text = text.strip().lower()
    match = re.search(r'build (?:a|an|the)?\s*(.+)', text)
    if match:
        text = match.group(1)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'\s+', '-', text)
    return text[:50]

class CoordinatorAgent:
    def __init__(self):
        self.chat = ChatInterface()
        self.design_agent = DesignAgent(self.chat)
        self.git_agent = GitAgent(self.chat)
        self.tester_agent = TesterAgent(self.chat)
        self.codegen_agent = CodeGeneratorAgent(self.chat)
        self.planner_agent = PlannerAgent(self.chat)
        self.executor_agent = ExecutorAgent(self.chat)

    def generate_readme(self, spec, path):
        readme_content = f"# {spec.get('title', 'Project')}\n\n"
        readme_content += f"{spec.get('description', 'No description provided.')}\n\n"
        readme_content += "## Features\n"
        for feat in spec.get('features', []):
            readme_content += f"- {feat}\n"
        readme_content += "\n## Tech Stack\n- Frontend: React\n- Backend: Python\n\n"
        readme_content += "## Setup\n```bash\nnpm install\nnpm run dev\n```\n"

        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(readme_content)
        print("📄 README.md generated.")

    def create_issues(self, task_list, path):
        issues_path = os.path.join(path, "issues.txt")
        with open(issues_path, "w") as f:
            for i, task in enumerate(task_list, start=1):
                label = "backend" if "API" in task or "database" in task.lower() else "frontend"
                f.write(f"Issue #{i}: {task} [label: {label}]\n")
        print("🐛 Issues drafted in issues.txt (simulate GitHub creation).")

    def install_requirements(self, path):
        print("📦 Installing dependencies...")
        frontend_path = os.path.join(path, "frontend")
        backend_path = os.path.join(path, "backend")

        try:
            if os.path.exists(frontend_path):
                subprocess.run(["npm", "install"], cwd=frontend_path, check=True)
            if os.path.exists(os.path.join(backend_path, "requirements.txt")):
                subprocess.run(["pip", "install", "-r", "requirements.txt"], cwd=backend_path, check=True)
        except subprocess.CalledProcessError as e:
            print("⚠️ Error installing requirements:", e)
        print("✅ Requirements installed.")

    def run_app(self, path):
        frontend_path = os.path.join(path, "frontend")
        try:
            print("🚀 Starting frontend (React)...")
            subprocess.Popen(["npm", "run", "dev"], cwd=frontend_path)
            print("🌐 Visit http://localhost:5173 or similar to test the frontend.")
        except Exception as e:
            print("❌ Error running app:", e)

    def run(self):
        user_input = input("🤖 What are we building today?\n🧑 You: ")
        project_name = sanitize_project_name(user_input)
        use_pdf = self.chat.prompt_user("Do you want to upload a design PDF? (y/n)").lower()

        spec = self.design_agent.parse_pdf(
            self.chat.prompt_user("Enter the full path to the PDF:")
        ) if use_pdf == 'y' else self.design_agent.generate_spec(project_name)

        self.chat.show("📐 Here's the generated spec:")
        self.chat.show(str(spec))

        path = self.git_agent.init_repo(project_name)
        self.codegen_agent.generate_code(spec, path)
        self.generate_readme(spec, path)

        task_list = self.planner_agent.generate_task_plan(spec)
        task_path = os.path.join(path, "task_plan.txt")

        print("🧠 Task Plan:")
        with open(task_path, "w") as f:
            if isinstance(task_list, list):
                for task in task_list:
                    print(f" - {task}")
                    f.write(f"{task}\n")
            else:
                print(task_list)
                f.write(str(task_list))

        self.create_issues(task_list, path)

        self.install_requirements(path)
        self.tester_agent.run_tests(path)

        self.chat.show(f"✅ Project '{project_name}' has been created at: {path}")
        self.git_agent.auto_commit(path, message="Initial commit with code, README, and tasks")

        if self.chat.prompt_user("🚀 Do you want to run the app locally now? (y/n)").lower() == "y":
            self.run_app(path)

        if self.chat.prompt_user("🚀 Do you want to run the task executor now? (y/n)").lower() == "y":
            self.executor_agent.run_tasks(task_path, path)

        while True:
            feedback = self.chat.prompt_user("💬 Would you like to suggest changes or improvements? (type 'n' to skip):")
            if feedback.lower() == "n":
                break
            fix_response = self.chat.ask_ai(f"Apply this improvement to the project: {feedback}")
            print("🧠 Applied Fix:\n", fix_response)
            self.git_agent.auto_commit(path, message=f"User improvement: {feedback}")
