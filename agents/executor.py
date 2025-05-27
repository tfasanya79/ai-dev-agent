import os

class ExecutorAgent:
    def __init__(self, chat):
        self.chat = chat  # ChatInterface (or any LLM wrapper)

    def run_tasks(self, task_file_path, project_path):
        if not os.path.exists(task_file_path):
            print("❌ No task file found.")
            return
        
        with open(task_file_path, "r") as f:
            tasks = f.readlines()
        
        for task in tasks:
            task = task.strip()
            if not task:
                continue
            
            print(f"\n🚀 Executing task: {task}")
            
            prompt = f"You are a senior software engineer. Implement this task for a {project_path} project:\n\n{task}\n"
            response = self.chat.ask_ai(prompt)
            
            # For now, just print the AI's response. You can later write it to a file if you want.
            print("🧠 AI Response:")
            print(response)
