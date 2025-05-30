import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from agents.coordinator import CoordinatorAgent
from agents.code_generator import CodeGeneratorAgent
from agents.design_agent import DesignAgent
from agents.git_agent import GitAgent

# Load environment variables
load_dotenv()

app = FastAPI()


# --------------------
# Data Models
# --------------------
class PromptRequest(BaseModel):
    message: str

class ProjectMetadata(BaseModel):
    name: str
    url: str | None = None
    description: str


# --------------------
# Routes
# --------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Dev Agent API"}


@app.post("/chat")
async def chat_endpoint(request: PromptRequest):
    prompt = request.message.strip()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    # Dispatch prompt to appropriate template
    prefix_map = {
        "code:": "Write code for: {task}",
        "bug:": "Fix the following bug: {task}",
        "test:": "Write tests for: {task}",
        "explain:": "Explain the following code: {task}",
        "refactor:": "Refactor the following code: {task}",
    }

    task = prompt
    for prefix, template_str in prefix_map.items():
        if prompt.lower().startswith(prefix):
            task = prompt[len(prefix):].strip()
            template = PromptTemplate.from_template(template_str)
            break
    else:
        template = PromptTemplate.from_template("{task}")

    chain = LLMChain(llm=llm, prompt=template)
    result = chain.run(task=task)
    return {"response": result}


@app.post("/upload-design")
async def upload_design(project_name: str = Form(...), file: UploadFile = File(...)):
    try:
        content = await file.read()
        decoded = content.decode("utf-8")

        project_path = os.path.join(os.getcwd(), project_name)
        os.makedirs(project_path, exist_ok=True)
        design_path = os.path.join(project_path, "uploaded_design.md")

        with open(design_path, "w", encoding="utf-8") as f:
            f.write(decoded)

        print(f"📥 Uploaded design saved to {design_path}")
        return JSONResponse(content={"message": "Custom design uploaded and saved."})
    except Exception as e:
        print(f"❌ Error uploading design: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/design")
def generate_design(metadata: ProjectMetadata):
    try:
        design_agent = DesignAgent()
        design = design_agent.generate_system_design(
            project_name=metadata.name,
            project_description=metadata.description
        )
        return {"system_design": design}
    except Exception as e:
        print(f"❌ Error generating design: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/start-project")
def start_project(metadata: ProjectMetadata):
    try:
        git_agent = GitAgent(chat=None)
        path = git_agent.init_repo(metadata.name)

        # Automatically open VS Code if available
        os.system(f"code \"{path}\"")
        return {"message": f"Project '{metadata.name}' initialized and VS Code opened."}
    except Exception as e:
        print(f"❌ Error starting project: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


# --------------------
# Run server (dev mode)
# --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
