import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional

# Import your agents
from agents.coordinator import CoordinatorAgent
from agents.design_agent import DesignAgent  # You'll need to create this
from agents.code_generator import CodeGeneratorAgent
from agents.git_agent import GitAgent  # You'll need to create this
#from agents.deployment_agent import DeploymentAgent  # You'll need to create this

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "🚀 Welcome to AI Dev Agent! Use /docs to explore the API."}



# In-memory user session store (replace with DB or cache later)
user_sessions = {}

# ===== Models =====
class ProjectStartRequest(BaseModel):
    repo_name: str
    repo_url: str
    description: str

class DesignConfirmationRequest(BaseModel):
    confirmed: bool

class FeedbackRequest(BaseModel):
    feedback: str

# ===== Endpoint: Start Project =====
@app.post("/start")
async def start_project(req: ProjectStartRequest):
    project_id = req.repo_name.lower().replace(" ", "_")
    if project_id in user_sessions:
        raise HTTPException(status_code=400, detail="Project with this repo name already exists.")

    # Initialize Coordinator Agent and get initial design proposal
    coordinator = CoordinatorAgent()
    design_proposal = coordinator.propose_design(req.description)  # Implement this method in CoordinatorAgent

    # Save session data
    user_sessions[project_id] = {
        "repo_url": req.repo_url,
        "description": req.description,
        "design_proposal": design_proposal,
        "final_design": None,
        "status": "design_proposed",
    }

    return {
        "project_id": project_id,
        "design_proposal": design_proposal,
        "message": "Design proposed. Please confirm or upload your final design."
    }

# ===== Endpoint: Confirm or Upload Design =====
@app.post("/design/{project_id}")
async def design_confirmation(project_id: str, confirmed: Optional[bool] = None, file: Optional[UploadFile] = File(None)):
    if project_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Project not found")

    if confirmed:
        # User accepts the proposed design
        user_sessions[project_id]["final_design"] = user_sessions[project_id]["design_proposal"]
        user_sessions[project_id]["status"] = "design_confirmed"
        return {"message": "Design confirmed. Ready to build."}

    if file:
        content = await file.read()
        try:
            design = json.loads(content.decode())
            user_sessions[project_id]["final_design"] = design
            user_sessions[project_id]["status"] = "design_uploaded"
            return {"message": "Custom design uploaded successfully."}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid design file: {str(e)}")

    raise HTTPException(status_code=400, detail="You must confirm the design or upload a design file.")

# ===== Endpoint: Build & Deploy =====
@app.post("/build/{project_id}")
async def build_project(project_id: str):
    if project_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Project not found")

    session = user_sessions[project_id]
    if session["status"] not in ["design_confirmed", "design_uploaded"]:
        raise HTTPException(status_code=400, detail="Design not confirmed or uploaded yet.")

    # Instantiate agents
    codegen = CodeGeneratorAgent()
    git_agent = GitAgent()
    deploy_agent = DeploymentAgent()

    # Generate codebase from final design/spec
    spec = session["final_design"]
    try:
        codebase_path = codegen.generate_code_from_spec(spec)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Code generation failed: {str(e)}")

    # Setup git repo, commit, and push
    try:
        git_agent.initialize_repo(session["repo_url"], codebase_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Git operation failed: {str(e)}")

    # Deploy MVP and get URL
    try:
        mvp_url = deploy_agent.deploy(codebase_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

    session["status"] = "built_and_deployed"
    session["mvp_url"] = mvp_url

    return {
        "message": "Project built and deployed successfully.",
        "mvp_url": mvp_url,
    }

# ===== Endpoint: Receive Feedback & Iterate =====
@app.post("/feedback/{project_id}")
async def receive_feedback(project_id: str, feedback_req: FeedbackRequest):
    if project_id not in user_sessions:
        raise HTTPException(status_code=404, detail="Project not found")

    session = user_sessions[project_id]
    if session["status"] != "built_and_deployed":
        raise HTTPException(status_code=400, detail="Project not deployed yet.")

    # Process feedback: create issues, update code, retest, redeploy
    # You may want to create an IterationAgent or extend existing ones

    # For now, simulate acknowledgment
    return {
        "message": "Feedback received and processing started.",
        "feedback": feedback_req.feedback,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
