from flask import Flask, request, jsonify
from core.intent import detect_intent
from core.actions import handle_action
import os

app = Flask(__name__)

# simple in-memory state (single user)
state = {}

@app.route("/")
def home():
    return "Vera Bot is running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_input = data.get("message", "")

        intent = detect_intent(user_input)
        result = handle_action(intent, user_input, state)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "action": "error",
            "response": f"Something went wrong: {str(e)}"
        })

# 🔥 IMPORTANT: Render requires this
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
