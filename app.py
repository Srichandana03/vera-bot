from flask import Flask, request, jsonify
from core.intent import detect_intent
from core.actions import handle_action

app = Flask(__name__)

state = {}

@app.route("/")
def home():
    return "Vera Bot is running 🚀"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    intent = detect_intent(user_input)
    result = handle_action(intent, user_input, state)

    return jsonify(result)
