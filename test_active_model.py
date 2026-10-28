import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key and os.path.exists(".env"):
    with open(".env") as f:
        for l in f:
            if l.startswith("GROQ_API_KEY="):
                api_key = l.split("=", 1)[1].strip()

client = Groq(api_key=api_key)

test_models = ["qwen/qwen3.8-27b", "openai/gpt-oss-20b", "openai/gpt-oss-120b"]

for m in test_models:
    try:
        res = client.chat.completions.create(
            model=m,
            messages=[{"role": "user", "content": "Halo, tes respon singkat 1 kata."}],
            max_tokens=10
        )
        print(f"Model {m} BERHASIL: {res.choices[0].message.content.strip()}")
        break
    except Exception as e:
        print(f"Model {m} GAGAL: {e}")

