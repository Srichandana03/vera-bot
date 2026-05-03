from flask import Flask, request, jsonify
from core.intent import detect_intent
from core.actions import handle_action
import os

app = Flask(__name__)

state = {}

# -------------------------------
# HEALTH
# -------------------------------
@app.route("/v1/healthz", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


# -------------------------------
# METADATA
# -------------------------------
@app.route("/v1/metadata", methods=["GET"])
def metadata():
    return jsonify({
        "bot_name": "Vera Bot",
        "version": "1.0",
        "description": "Appointment booking assistant"
    })


# -------------------------------
# CONTEXT
# -------------------------------
@app.route("/v1/context", methods=["POST"])
def context():
    return jsonify({"status": "context received"})


# -------------------------------
# TICK
# -------------------------------
@app.route("/v1/tick", methods=["POST"])
def tick():
    return jsonify({"status": "tick processed"})


# -------------------------------
# REPLY (MAIN LOGIC)
# -------------------------------
@app.route("/v1/reply", methods=["POST"])
def reply():
    data = request.get_json()
    user_input = data.get("message", "")

    intent = detect_intent(user_input)
    result = handle_action(intent, user_input, state)

    return jsonify(result)


# -------------------------------
# ROOT
# -------------------------------
@app.route("/")
def home():
    return "Vera Bot is running 🚀"


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
