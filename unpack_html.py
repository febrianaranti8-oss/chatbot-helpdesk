import json
import os

files = ["stitch_output/Chat.html", "stitch_output/Panduan_WiFi.html"]

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            parsed = json.loads(content)
            if "dataString" in parsed:
                with open(fpath, "w", encoding="utf-8") as out:
                    out.write(parsed["dataString"])
                print(f"Berhasil mengekstrak raw HTML ke {fpath}!")
        except Exception as e:
            print(f"File {fpath} sudah berbentuk raw atau error: {e}")

