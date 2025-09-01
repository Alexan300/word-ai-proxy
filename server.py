from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key)
# 🔑 API-ключ берём из переменной окружения (лучше задать через GitHub Secrets → Codespaces)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Исправь ошибки в тексте:\n{text}"}]
    )

    answer = resp.choices[0].message.content
    return jsonify({"result": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
