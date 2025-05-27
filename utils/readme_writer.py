import os

def generate_readme(project_path, project_title, project_description):
    template_path = os.path.join(os.path.dirname(__file__), "../templates/README_template.md")
    readme_path = os.path.join(project_path, "README.md")

    if not os.path.exists(template_path):
        print("❌ README template not found.")
        return

    with open(template_path, "r") as template_file:
        content = template_file.read()

    content = content.replace("{project_title}", project_title)
    content = content.replace("{project_description}", project_description)

    with open(readme_path, "w") as readme_file:
        readme_file.write(content)

    print("📄 README.md created.")
