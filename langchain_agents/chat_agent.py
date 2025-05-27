from dotenv import load_dotenv
import os
from agents.coordinator_agent import coordinator_respond


load_dotenv()  # Load environment variables

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage

chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)

def get_ai_response(user_message: str) -> str:
    response = chat_model.invoke([HumanMessage(content=user_message)])
    return response.content

def get_ai_response(user_message: str) -> str:
    # Trigger coordinator if message looks like a request to build
    keywords = ["build", "website", "app", "system", "project"]
    if any(word in user_message.lower() for word in keywords):
        return coordinator_respond(user_message)

    # Default: generic chatbot
    response = chat_model.invoke(user_message)
    return response.content
