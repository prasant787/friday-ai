
from flask import Flask, request, jsonify

app = Flask("FRIDAY")

@app.route("/")
def home():
    return jsonify({
        "assistant": "FRIDAY",
        "status": "online",
        "message": "Hello Boss! FRIDAY is ready."
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message required"}), 400

    return jsonify({
        "assistant": "FRIDAY",
        "reply": f"Hello Boss! You said: {message}"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
