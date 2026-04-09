import os
import anthropic
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return send_file("static/index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    text = data.get("text", "").strip()
    mode = data.get("mode", "auto")

    if not text:
        return jsonify({"error": "Ingen text skickades."}), 400

    prompts = {
        "auto": "You are a helpful assistant. Read the Swedish document and answer ALL questions and solve ALL tasks. Number each answer. Reply in Swedish.",
        "list": "You are a helpful assistant. Read the Swedish document and list ALL questions and tasks, numbered. Do NOT answer them. Reply in Swedish.",
        "check": "You are a helpful assistant. Read the Swedish document which may contain questions and answers. Review the answers, correct mistakes, give feedback. Reply in Swedish.",
    }

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=prompts.get(mode, prompts["auto"]),
            messages=[{"role": "user", "content": text}],
        )
        return jsonify({"answer": message.content[0].text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
