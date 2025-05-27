from openai import OpenAI
import os

class ChatInterface:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def prompt_user(self, prompt: str) -> str:
        return input(f"{prompt}\n🧑 ")

    def show(self, message: str):
        print(f"{message}")

    def ask_ai(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a senior full-stack developer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
