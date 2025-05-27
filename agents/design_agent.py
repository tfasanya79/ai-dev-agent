# agents/design_agent.py

from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(model_name="gpt-4", temperature=0.3, openai_api_key=api_key)

def generate_app_spec(user_idea: str) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You're an expert software architect. Given a user idea, generate a full app spec with:\n"
                   "- App Summary\n- Features list\n- Pages/UI components\n- Suggested tech stack."),
        ("user", user_idea)
    ])

    chain = prompt | chat
    response = chain.invoke({})

    return response.content
