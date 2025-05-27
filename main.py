import os
import ast
from dotenv import load_dotenv
from agents.coordinator import CoordinatorAgent
from agents.code_generator import CodeGeneratorAgent  # Use class not function

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if __name__ == "__main__":
    mode = input("Select mode [coordinator/spec]: ").strip().lower()
    if mode == "coordinator":
        agent = CoordinatorAgent()
        agent.run()
    elif mode == "spec":
        print("Paste the structured project spec dictionary. End input with a blank line:")
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)

        spec_input = "\n".join(lines)

        try:
            spec = ast.literal_eval(spec_input)
            codegen = CodeGeneratorAgent(chat_model=None)  # pass proper chat model later
            print(codegen.generate_code_from_spec(spec))
        except Exception as e:
            print("❌ Failed to parse the spec. Make sure it's a valid Python dict.")
            print(f"Error: {e}")