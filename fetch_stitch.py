import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("STITCH_API_KEY", "")
os.makedirs("stitch_output", exist_ok=True)

screens = [
    {"name": "Chat", "file": "stitch_output/Chat.json"},
    {"name": "Panduan_WiFi", "file": "stitch_output/Panduan_WiFi.json"}
]

def download_file(url, out_path):
    print(f"Mengunduh ke {out_path}...")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "X-Goog-Api-Key": API_KEY
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp, open(out_path, "wb") as out:
            out.write(resp.read())
        print(f"-> SUKSES tersimpan di {out_path} ({os.path.getsize(out_path)} bytes)")
    except urllib.error.HTTPError as e:
        print(f"-> GAGAL ({e.code}): {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"-> ERROR: {e}")

for sc in screens:
    if not os.path.exists(sc["file"]):
        print(f"File {sc['file']} tidak ditemukan.")
        continue
        
    with open(sc["file"], "r", encoding="utf-8") as f:
        data = json.load(f)
        
    structured = data.get("result", {}).get("structuredContent", {})
    if not structured:
        # Fallback coba parse dari content text
        for item in data.get("result", {}).get("content", []):
            try:
                structured = json.loads(item.get("text", "{}"))
                break
            except Exception:
                pass

    print(f"\nMemproses {sc['name']}: {structured.get('title')}")
    
    # Download Screenshot Image
    img_info = structured.get("screenshot", {})
    if "downloadUrl" in img_info:
        download_file(img_info["downloadUrl"], f"stitch_output/{sc['name']}.png")
        
    # Download HTML Code
    html_info = structured.get("htmlCode", {})
    if "downloadUrl" in html_info:
        download_file(html_info["downloadUrl"], f"stitch_output/{sc['name']}.html")

print("\nSelesai! Seluruh aset HTML dan Gambar Stitch berhasil diunduh.")
