# ai-dev-agent

A local AI development assistant you drive from a chat interface. Give it a goal in plain English, or drop in a PDF design, and it scaffolds a working web or mobile application.

## What it does

- Chat driven interface, so the workflow is conversation rather than a CLI incantation
- Accepts a plain text brief or a PDF design document as the starting point
- Scaffolds a working project rather than snippets: files, structure and entry points
- Initialises a git repository, creates a Python virtual environment and installs dependencies
- Optionally pushes the result to GitHub

## Requirements

- Python 3.10 or later
- An API key for your chosen model provider, set as an environment variable. It is never written to the repository
- Git on the PATH if you want the initialise and push steps

## Quick start

```bash
git clone https://github.com/tfasanya79/ai-dev-agent.git
cd ai-dev-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MODEL_API_KEY=your-key-here
python main.py
```

## Notes

Generated projects land in a new directory under the working folder. Review the generated code before pushing it anywhere. The agent writes scaffolding, not production ready code, and the useful part is the starting structure rather than the finished result.

## Status

Personal tool, built to remove the repetitive first hour of a new project. Not maintained as a library and no API stability guarantee.
