import os
import json
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
import chromadb
from groq import Groq

# Salin logo resmi PT BSP ke folder stitch_output jika tersedia
src_logo = r"C:\Users\ranti.febriana\.gemini\antigravity\brain\dc9404e1-5bb2-48a7-afdb-0c19b924da75\.user_uploaded\media_1793163268127_b5d1ce5b.png"
dst_logo = os.path.join("stitch_output", "logo_bsp.png")
if os.path.exists(src_logo):
    try:
        shutil.copyfile(src_logo, dst_logo)
        print("[Init] Logo PT Bumi Siak Pusako berhasil dimuat!")
    except Exception as e:
        print(f"[Init Warning] Gagal salin logo: {e}")

# 1. Konfigurasi Groq & ChromaDB
def load_env():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

load_env()
client_groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_available_model():
    # Daftar model chat generasi teks resmi yang aktif di akun Anda
    candidate_chat_models = [
        "qwen/qwen3.8-27b",
        "openai/gpt-oss-20b",
        "openai/gpt-oss-120b"
    ]
    try:
        available_ids = [m.id for m in client_groq.models.list().data]
        for candidate in candidate_chat_models:
            if candidate in available_ids:
                return candidate
    except Exception:
        pass
    return "qwen/qwen3.8-27b"

active_model = get_available_model()

# Hubungkan ke ChromaDB
client_chroma = chromadb.PersistentClient(path="./chroma_db")
collection = client_chroma.get_or_create_collection(name="helpdesk_faq")

def cari_dokumen(pertanyaan: str) -> str:
    try:
        hasil = collection.query(query_texts=[pertanyaan], n_results=1)
        if hasil['documents'] and hasil['documents'][0]:
            return hasil['documents'][0][0]
    except Exception as e:
        print(f"[ChromaDB Warning] {e}")
    return "Tidak ada informasi spesifik di panduan IT."

def proses_rag(pertanyaan: str) -> str:
    konteks = cari_dokumen(pertanyaan)
    system_prompt = (
        "Anda adalah asisten AI Helpdesk IT Internal PT Bumi Siak Pusako / SKK Migas yang ramah dan solutif. "
        "Tugas Anda adalah menjawab pertanyaan pengguna berdasarkan konteks dokumen yang diberikan.\n"
        "Aturan ketat:\n"
        "1. Jika solusinya ada di dokumen, berikan langkah perbaikan yang jelas, bernomor, dan mudah dipahami.\n"
        "2. Jika solusinya TIDAK ADA di dokumen, jangan berhalusinasi. "
        "Sampaikan dengan jujur bahwa panduan belum tersedia dan arahkan untuk menghubungi tim IT Helpdesk "
        "(Email: it-helpdesk@kantor.local atau Telepon Ext: 104/105 / Intercom: 4022).\n\n"
        f"Konteks Dokumen:\n{konteks}"
    )
    
    # Gunakan candidate models jika salah satu kena rate limit atau kendala
    for model_name in [active_model, "openai/gpt-oss-20b", "openai/gpt-oss-120b"]:
        try:
            response = client_groq.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pertanyaan}
                ],
                temperature=0.2
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[Error model {model_name}] {e}")
            continue

    return "Maaf, seluruh model chat sedang tidak dapat diakses saat ini. Silakan hubungi tim IT Helpdesk."

# 2. HTTP Server Request Handler
class RAGRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="stitch_output", **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length).decode("utf-8")
                data = json.loads(body)
                user_msg = data.get("message", "")
                
                print(f"\n[User Query] {user_msg}")
                jawaban = proses_rag(user_msg)
                print(f"[AI Reply] {jawaban[:70]}...")

                response_data = json.dumps({"reply": jawaban}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(response_data)))
                self.end_headers()
                self.wfile.write(response_data)
            except Exception as e:
                print(f"[Server Error] {e}")
                err_resp = json.dumps({"reply": f"Terjadi kendala pada sistem backend: {str(e)}"}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(err_resp)))
                self.end_headers()
                self.wfile.write(err_resp)
        else:
            self.send_error(404, "Endpoint not found")

PORT = 8080
print("=" * 65)
print(f"🚀 SERVER STITCH + RAG AKTIF: http://localhost:{PORT}")
print(f"Model Chat Groq : {active_model}")
print(f"Database Vektor : ChromaDB (helpdesk_faq)")
print("Buka browser Anda di: http://localhost:8080")
print("Biarkan terminal ini tetap terbuka selama menggunakan aplikasi web.")
print("=" * 65)

server = HTTPServer(("0.0.0.0", PORT), RAGRequestHandler)
server.serve_forever()
