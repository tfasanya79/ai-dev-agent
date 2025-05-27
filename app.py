from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from utils.token_tracker import TokenCounter
from langchain_agents.chat_agent import get_ai_response
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

app = Flask(__name__)
# Replace '*' with your frontend URL in production for security!
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL", "*")}})

token_counter = TokenCounter()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        print(f"User message received: {user_message}")

        message_history = [{"role": "user", "content": user_message}]
        tokens_used = token_counter.add_tokens(message_history)
        print(f"Tokens used (input): {tokens_used}, Total tokens: {token_counter.total_tokens}")

        ai_response = get_ai_response(user_message)
        tokens_used = token_counter.add_tokens([{"role": "assistant", "content": ai_response}])
        print(f"Tokens used (output): {tokens_used}, Total tokens: {token_counter.total_tokens}")

        return jsonify({'response': ai_response})

    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        return jsonify({'response': "Something went wrong..."}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    global message_history
    message_history = []
    token_counter.reset()
    return jsonify({'status': 'chat history cleared'})

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
