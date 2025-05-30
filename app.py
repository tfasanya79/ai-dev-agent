import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import List
from fastapi import HTTPException

from database import SessionLocal, engine
import models
import schemas

from agents.coordinator import CoordinatorAgent
from agents.code_generator import CodeGeneratorAgent
from agents.design_agent import DesignAgent
from agents.git_agent import GitAgent

# --------------------
# Init
# --------------------
load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------------
# Routes
# --------------------
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Dev Agent API"}

@app.post("/chat")
async def chat_endpoint(request: schemas.PromptRequest):
    prompt = request.message.strip()
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

    # Prompt Routing
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
async def upload_design(
    project_name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        content = await file.read()
        decoded = content.decode("utf-8")

        # Save file
        project_path = os.path.join(os.getcwd(), project_name)
        os.makedirs(project_path, exist_ok=True)
        design_path = os.path.join(project_path, "uploaded_design.md")
        with open(design_path, "w", encoding="utf-8") as f:
            f.write(decoded)

        # Update DB
        project = db.query(models.Project).filter(models.Project.name == project_name).first()
        if not project:
            project = models.Project(name=project_name, design_path=design_path)
            db.add(project)
        else:
            project.design_path = design_path
        db.commit()

        print(f"📥 Uploaded design saved to {design_path}")
        return JSONResponse(content={"message": "Custom design uploaded and saved."})
    except Exception as e:
        print(f"❌ Error uploading design: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/design")
def generate_design(metadata: schemas.ProjectMetadata, db: Session = Depends(get_db)):
    try:
        design_agent = DesignAgent()
        design = design_agent.generate_system_design(
            project_name=metadata.name,
            project_description=metadata.description
        )

        # Save to DB
        project = db.query(models.Project).filter(models.Project.name == metadata.name).first()
        if not project:
            project = models.Project(name=metadata.name, description=metadata.description, url=metadata.url)
            db.add(project)
        else:
            project.description = metadata.description
            project.url = metadata.url
        db.commit()

        return {"system_design": design}
    except Exception as e:
        print(f"❌ Error generating design: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/start-project")
def start_project(metadata: schemas.ProjectMetadata):
    try:
        git_agent = GitAgent(chat=None)
        path = git_agent.init_repo(metadata.name)

        # Launch VS Code
        os.system(f"code \"{path}\"")
        return {"message": f"Project '{metadata.name}' initialized and VS Code opened."}
    except Exception as e:
        print(f"❌ Error starting project: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/projects", response_model=List[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()
    return projects

@app.get("/projects/{name}", response_model=schemas.ProjectOut)
def get_project(name: str, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.name == name).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# --------------------
# Run (dev mode)
# --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
