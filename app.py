import os
import ast
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi import File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from agents.coordinator import CoordinatorAgent
from agents.code_generator import CodeGeneratorAgent
from agents.design_agent import DesignAgent
from agents.git_agent import GitAgent

load_dotenv()
app = FastAPI()

class PromptRequest(BaseModel):
    message: str

class ProjectMetadata(BaseModel):
    name: str
    url: str = None
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Dev Agent API"}

@app.post("/chat")
async def chat_endpoint(request: PromptRequest):
    prompt = request.message.strip()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    if prompt.lower().startswith("code:"):
        task = prompt[5:].strip()
        template = PromptTemplate.from_template("Write code for: {task}")
    elif prompt.lower().startswith("bug:"):
        task = prompt[4:].strip()
        template = PromptTemplate.from_template("Fix the following bug: {task}")
    elif prompt.lower().startswith("test:"):
        task = prompt[5:].strip()
        template = PromptTemplate.from_template("Write tests for: {task}")
    elif prompt.lower().startswith("explain:"):
        task = prompt[8:].strip()
        template = PromptTemplate.from_template("Explain the following code: {task}")
    elif prompt.lower().startswith("refactor:"):
        task = prompt[9:].strip()
        template = PromptTemplate.from_template("Refactor the following code: {task}")
    else:
        task = prompt
        template = PromptTemplate.from_template("{task}")

    chain = LLMChain(llm=llm, prompt=template)
    result = chain.run(task=task)
    return {"response": result}

@app.post("/upload-design")
async def upload_design(project_name: str = Form(...), file: UploadFile = File(...)):
    try:
        content = await file.read()
        decoded = content.decode("utf-8")

        # Save design in the appropriate project directory
        project_path = os.path.join(os.getcwd(), project_name)
        os.makedirs(project_path, exist_ok=True)
        design_path = os.path.join(project_path, "uploaded_design.md")
        with open(design_path, "w") as f:
            f.write(decoded)

        print(f"📥 Uploaded design saved to {design_path}")
        return JSONResponse(content={"message": "Custom design uploaded and saved."})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/design")
def generate_design(metadata: ProjectMetadata):
    design_agent = DesignAgent()
    design = design_agent.generate_system_design(
        project_name=metadata.name,
        project_description=metadata.description
    )
    return {"system_design": design}

@app.post("/start-project")
def start_project(metadata: ProjectMetadata):
    git_agent = GitAgent(chat=None)
    path = git_agent.init_repo(metadata.name)
    os.system(f"code {path}")
    return {"message": f"Project '{metadata.name}' initialized and VS Code opened."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
