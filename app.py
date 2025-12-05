import os
from flask import Flask, render_template, request, jsonify
from llm_talks import ConversationManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global state to hold the conversation manager instance
# In a real production app, this should be stored in a session or database
conversation_manager = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_conversation():
    global conversation_manager
    data = request.json
    topic = data.get('topic', 'The future of AI')
    
    # Models configuration from request or fallback to env
    # Allowing frontend to override would be nice, but for now stick to backend env for keys safety
    # We can allow model names to be passed
    
    model_a_name = data.get('model_a', os.getenv("MODEL_A_NAME"))
    model_b_name = data.get('model_b', os.getenv("MODEL_B_NAME"))

    conf_a = {
        "api_key": os.getenv("MODEL_A_API_KEY", os.getenv("OPENROUTER_API_KEY")),
        "base_url": os.getenv("MODEL_A_BASE_URL", os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")),
        "name": model_a_name
    }
    
    conf_b = {
        "api_key": os.getenv("MODEL_B_API_KEY", os.getenv("LOCAL_API_KEY", "ollama")),
        "base_url": os.getenv("MODEL_B_BASE_URL", os.getenv("LOCAL_BASE_URL", "http://localhost:11434/v1")),
        "name": model_b_name
    }

    conversation_manager = ConversationManager(topic, conf_a, conf_b)
    
    # Return initial history (Moderator message)
    return jsonify({
        "status": "started",
        "history": conversation_manager.get_history()
    })

@app.route('/api/next', methods=['POST'])
def next_turn():
    global conversation_manager
    if not conversation_manager:
        return jsonify({"error": "No conversation started"}), 400
        
    try:
        message = conversation_manager.next_turn()
        return jsonify(message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    global conversation_manager
    conversation_manager = None
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
