import os
from groq import Groq

api_key = os.environ.get("GROQ_API_KEY")
if not api_key and os.path.exists(".env"):
    with open(".env") as f:
        for l in f:
            if l.startswith("GROQ_API_KEY="):
                api_key = l.split("=", 1)[1].strip()

client = Groq(api_key=api_key)
models = client.models.list()
model_ids = [m.id for m in models.data]

with open("models_list.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(model_ids))

print(f"Total models: {len(model_ids)}")
print(f"Models: {model_ids}")

