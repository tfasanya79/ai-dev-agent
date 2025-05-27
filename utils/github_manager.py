import os

def create_github_issues(project_name, tasks):
    issues_dir = os.path.join(os.getcwd(), "mock_github_issues", project_name)
    os.makedirs(issues_dir, exist_ok=True)

    for i, task in enumerate(tasks, start=1):
        issue_file = os.path.join(issues_dir, f"issue_{i:02}.md")
        with open(issue_file, "w") as f:
            f.write(f"# Task {i}\n\n{task}\n\nLabels: planning, auto-generated\n")

    print(f"📌 {len(tasks)} mock GitHub issues created at: {issues_dir}")
