from flask import Flask, request, jsonify, render_template
from utils.token_tracker import TokenCounter
from langchain_agents.chat_agent import get_ai_response
from dotenv import load_dotenv
import os
import traceback

# ✅ Load environment variables from .env
load_dotenv()

app = Flask(__name__)
token_counter = TokenCounter()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')
        print(f"User message received: {user_message}")

        # Create the message history
        message_history = [{"role": "user", "content": user_message}]
        print(f"Message history: {message_history}")

        # Count input tokens
        tokens_used = token_counter.add_tokens(message_history)
        print(f"Tokens used (input): {tokens_used}, Total tokens: {token_counter.total_tokens}")

        # Get AI response
        ai_response = get_ai_response(user_message)
        print(f"AI Response: {ai_response}")

        # Count output tokens
        tokens_used = token_counter.add_tokens([{"role": "assistant", "content": ai_response}])
        print(f"Tokens used (output): {tokens_used}, Total tokens: {token_counter.total_tokens}")

        return jsonify({'response': ai_response})

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'response': "Something went wrong..."}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    global message_history
    message_history = []
    token_counter.reset()
    return jsonify({'status': 'chat history cleared'})


if __name__ == '__main__':
    app.run(debug=True)
