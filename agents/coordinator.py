import os
import re
from agents.planner_agent import PlannerAgent
from agents.design import DesignAgent
from agents.git_agent import GitAgent
from agents.tester import TesterAgent
from chat.chat_interface import ChatInterface
from agents.code_generator import CodeGeneratorAgent
from agents.executor import ExecutorAgent
from utils.readme_writer import generate_readme
from utils.github_manager import create_github_issues
from utils.installer import install_requirements

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

    def run(self):
        user_input = input("🤖 What are we building today?\n🧑 You: ")
        project_name = sanitize_project_name(user_input)
        use_pdf = self.chat.prompt_user("Do you want to upload a design PDF? (y/n)").lower()

        if use_pdf == 'y':
            pdf_path = self.chat.prompt_user("Enter the full path to the PDF:")
            spec = self.design_agent.parse_pdf(pdf_path)
        else:
            spec = self.design_agent.generate_spec(project_name)

        self.chat.show("📐 Here's the generated spec:")
        self.chat.show(str(spec))

        # Create local repo
        path = self.git_agent.init_repo(project_name)

        # Generate code
        self.codegen_agent.generate_code(spec, path)

        # Run initial tests
        self.tester_agent.run_tests(path)

        # ✅ Generate README.md
        generate_readme(path, project_name, str(spec))

        # ✅ Generate task plan
        task_list = self.planner_agent.generate_task_plan(spec)
        print("🤖 Here's the generated task plan:")
        for task in task_list:
            print(f" - {task}")

        # ✅ Save task plan to file
        task_path = os.path.join(path, "task_plan.txt")
        with open(task_path, "w") as f:
            for task in task_list:
                f.write(f"{task}\n")

        # ✅ Create GitHub issues & labels
        self.chat.show("📌 Creating GitHub issues from task plan...")
        create_github_issues(project_name, task_list)

        # ✅ Install project requirements
        install_requirements(path)

        # ✅ Ask to run the executor
        run_executor = self.chat.prompt_user("🚀 Do you want to run the task executor now? (y/n)").lower()
        if run_executor == 'y':
            self.executor_agent.run_tasks(task_path, path)

        self.chat.show("✅ Project is ready! You can now test or request updates 😊")