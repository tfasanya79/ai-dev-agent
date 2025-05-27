from PyPDF2 import PdfReader

class DesignAgent:
    def __init__(self, chat):
        self.chat = chat

    def generate_spec(self, user_input):
        return {
            "project_type": "web",
            "framework": "react",
            "features": ["login", "dashboard", "settings"]
        }

    def parse_pdf(self, pdf_path):
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return self.generate_spec(text)
