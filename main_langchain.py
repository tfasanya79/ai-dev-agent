import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.agents.agent_types import AgentType

from langchain_agents.tool_design import design_tool
from langchain_agents.tool_code import codegen_tool
from langchain_agents.tool_git import git_tool
from langchain_agents.tool_test import test_tool

from utils.token_tracker import TokenCounter

token_counter = TokenCounter()


load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Missing OPENAI_API_KEY. Ensure it's set in your .env file.")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

tools = [design_tool, codegen_tool, git_tool, test_tool]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": user_input}
]

tokens_used = token_counter.add_tokens(messages)
print(f"Tokens used in this interaction: {tokens_used}")
print(f"Total tokens so far: {token_counter.total_tokens}")



if __name__ == "__main__":
    agent.run("We're building a Splunk admin automation web dashboard. Handle the design, code, repo setup, and testing.")
