import os
import anthropic
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder="static")
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "You are a helpful assistant. The user will send you a document written in Swedish. "
    "Read it carefully and answer ALL questions and solve ALL tasks you find in it. "
    "Number each answer clearly. Always reply in Swedish. "
    "If a task requires physical presence, explain the concept instead and note that the user must check it themselves."
)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    text = data.get("text", "").strip()
    mode = data.get("mode", "auto")

    if not text:
        return jsonify({"error": "Ingen text skickades."}), 400

    prompts = {
        "auto": (
            "You are a helpful assistant. Read the Swedish document and answer ALL questions "
            "and solve ALL tasks. Number each answer. Reply in Swedish."
        ),
        "list": (
            "You are a helpful assistant. Read the Swedish document and list ALL questions "
            "and tasks you find, numbered. Do NOT answer them. Reply in Swedish."
        ),
        "check": (
            "You are a helpful assistant. Read the Swedish document which may contain questions "
            "and answers. Review the answers, correct mistakes, give feedback. Reply in Swedish."
        ),
    }

    try:
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=4096,
            system=prompts.get(mode, prompts["auto"]),
            messages=[{"role": "user", "content": text}],
        )
        answer = message.content[0].text
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
