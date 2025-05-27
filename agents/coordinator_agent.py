# agents/coordinator_agent.py

from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from agents.design_agent import generate_app_spec  # ✅ Add this import


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5, openai_api_key=api_key)

# Persistent context history
conversation_history = []

def reset_conversation():
    global conversation_history
    conversation_history = []

def coordinator_respond(user_input: str) -> str:
    global conversation_history
    conversation_history.append(HumanMessage(content=user_input))

    # Call design agent if message is a build request
    if any(word in user_input.lower() for word in ["build", "website", "app", "project", "system"]):
        design = generate_app_spec(user_input)
        conversation_history.append(AIMessage(content=design))
        return design

    # Otherwise continue chat
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful Coordinator AI."),
        *conversation_history
    ])

    chain = prompt | chat
    ai_response = chain.invoke({}).content
    conversation_history.append(AIMessage(content=ai_response))
    return ai_response
