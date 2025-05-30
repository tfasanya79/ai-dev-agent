cat > example_design.md <<EOF
# System Design for Sample App

## Purpose
A simple web app that allows users to chat with an AI assistant that can:
- Generate code
- Propose system designs
- Fix bugs
- Explain code

## Components
1. Frontend (React)
2. Backend (FastAPI with LangChain)
3. Git Integration
4. VS Code automation

## Workflow
1. User enters a project idea
2. The agent generates a system design
3. The agent sets up a project structure
4. VS Code opens with initialized repo
EOF
