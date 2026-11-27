import os
import requests
from flask import Flask, request, jsonify

app = Flask("FRIDAY")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_INSTRUCTION = """
You are FRIDAY, a personal AI assistant.

Your creator is Sir Prashant Tamang.
Address your creator as Boss.

Your personality:
- Friendly, intelligent, calm and respectful.
- Speak naturally and clearly.
- Answer questions helpfully and accurately.
- Explain difficult topics in simple language.
- Be honest when you don't know something.
- Never pretend to have abilities you do not have.
- Your name is FRIDAY.
"""

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
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message required"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "AI key is not configured"}), 500

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/"
        f"models/{GEMINI_MODEL}:generateContent"
    )

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "systemInstruction": {
            "parts": [{"text": SYSTEM_INSTRUCTION}]
        },
        "contents": [{
            "role": "user",
            "parts": [{"text": message}]
        }]
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        result = response.json()

        reply = result["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({
            "assistant": "FRIDAY",
            "reply": reply
        })

    except requests.exceptions.Timeout:
        return jsonify({"error": "Gemini took too long to respond."}), 504

    except requests.exceptions.RequestException:
        app.logger.exception("Gemini API request failed")
        return jsonify({"error": "FRIDAY could not reach her AI brain."}), 502

    except (KeyError, IndexError, TypeError):
        return jsonify({"error": "FRIDAY received an unexpected AI response."}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
