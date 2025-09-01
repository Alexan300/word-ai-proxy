from flask import Flask, request, jsonify
from openai import OpenAI
import os
from io import BytesIO


app = Flask(__name__)

# 🔑 API-ключ берём из переменной окружения (лучше задать через GitHub Secrets → Codespaces)
client = OpenAI(api_key=os.getenv("API_KEY"))

# создаём ассистента один раз
assistant = client.beta.assistants.create(
    name="Lawyer Assistant",
    instructions="Ты юридический помощник. Используй загруженные документы для ответов.",
    model="gpt-4o-mini",
    tools=[{"type": "file_search"}]
)

file_ids = []

@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    data = f.read()
    uploaded = client.files.create(
        file=(f.filename, BytesIO(data)),
        purpose="assistants"
    )
    file_ids.append(uploaded.id)
    return jsonify({"status": "Файл принят", "file_id": uploaded.id})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")

    content = [{"type": "input_text", "text": text}]
    for fid in file_ids:
        content.append({"type": "input_file", "file_id": fid})

    resp = client.responses.create(
        model="gpt-4.1-mini",
        input=[{"role": "user", "content": content}]
    )

    # Собираем текст из всех блоков output
    answer = ""
    if resp.output and len(resp.output) > 0:
        for block in resp.output[0].content:
            if hasattr(block, "text"):   # у текстовых блоков есть .text
                answer += block.text

    return jsonify({"result": answer})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
