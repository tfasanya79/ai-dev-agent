# agents/planner_agent.py

class PlannerAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model

    def generate_task_plan(self, project_spec: dict) -> list:
        prompt = f"""
You are a senior software planner. A user has asked to build a project with this spec:
{project_spec}

Break this down into a list of clear engineering tasks. Include both frontend and backend work.
Return each task as a short string.
"""
        response = self.chat_model.ask_ai(prompt)
        return self._parse_tasks(response)

    def _parse_tasks(self, response: str) -> list:
        tasks = []
        for line in response.strip().split("\n"):
            if line.strip():
                tasks.append(line.strip("•- ").strip())
        return tasks
