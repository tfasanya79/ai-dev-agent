def generate_backend_code(spec: dict) -> dict:
    return {
        "backend/app.py": """from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify(message="Welcome to the backend API")

if __name__ == "__main__":
    app.run(debug=True)
""",

        "backend/requirements.txt": "flask\n",

        "backend/.env": "FLASK_ENV=development\n",
    }
