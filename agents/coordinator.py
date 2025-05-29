# agents/coordinator.py

from typing import Dict
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


class CoordinatorAgent:
    def __init__(self):
        self.chat_model = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    def welcome(self):
        print("👋 Welcome to the AI Dev Agent!")
        print("Let's get started building your app.\n")

    def collect_project_info(self) -> Dict:
        print("📝 What would you like to build today?")
        name = input("Repository Name: ").strip()
        url = input("Repository URL (leave blank to skip for now): ").strip()
        description = input("Brief Description of the Project Goal: ").strip()

        return {
            "repo_name": name,
            "repo_url": url,
            "description": description,
        }

    def propose_design(self, description: str) -> str:
        template = PromptTemplate.from_template("""
        Based on the following app description, propose a technical architecture design.

        Description:
        {description}

        Return the design in clear markdown format with:
        - Architecture type
        - Key components
        - Suggested tech stack
        - Major features/modules
        """)
        chain = LLMChain(llm=self.chat_model, prompt=template)
        return chain.run(description)

    def confirm_or_upload_design(self) -> str:
        print("\n📐 Do you accept this design, or would you like to upload your own?")

        while True:
            choice = input("Type [accept/upload]: ").strip().lower()
            if choice == "accept":
                return "accept"
            elif choice == "upload":
                path = input("Path to your custom design markdown or PDF: ").strip()
                return path
            else:
                print("❌ Invalid choice. Please type 'accept' or 'upload'.")

    def run(self):
        self.welcome()
        project_info = self.collect_project_info()
        design = self.propose_design(project_info["description"])
        print("\n📄 Proposed Design:\n")
        print(design)

        user_choice = self.confirm_or_upload_design()
        if user_choice == "accept":
            print("✅ Great! We'll proceed with the proposed design.")
            # Pass `design` to next agent
        else:
            print(f"📥 You chose to upload a custom design from: {user_choice}")
            # Parse uploaded design (PDF or markdown) here

