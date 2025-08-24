from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 🔑 API-ключ берём из переменной окружения (лучше задать через GitHub Secrets → Codespaces)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "z7NnuHYnbHlFjs5kNPoAuDtKkHQjN76ywjQ1Jk5tn8di5Dm2hT3BlbkFJMqQJ_KWoLMerhEq98tZjHZvzKAgE3spNFExFIIDOaAqAxRG0ppXg6cIEpKU9IBHCcJhqDUBmkA"))

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
