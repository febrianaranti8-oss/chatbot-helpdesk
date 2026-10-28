import os
import chromadb
from groq import Groq

# 1. Konfigurasi API Key Groq
def load_env():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

load_env()
client_groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. Hubungkan ke ChromaDB yang sudah berisi panduan IT
client_chroma = chromadb.PersistentClient(path="./chroma_db")
collection = client_chroma.get_or_create_collection(name="helpdesk_faq")

def get_available_model():
    try:
        models = [m.id for m in client_groq.models.list().data]
        for target in ["llama-3.3-70b-versatile", "llama-3.2-3b-preview", "llama-3.2-1b-preview", "llama3-70b-8192", "llama3-8b-8192"]:
            if target in models:
                return target
        return models[0] if models else "llama-3.3-70b-versatile"
    except Exception:
        return "llama-3.3-70b-versatile"

active_model = get_available_model()

def cari_dokumen(pertanyaan: str) -> str:
    """Mencari potongan panduan yang paling cocok dengan pertanyaan pengguna."""
    hasil = collection.query(
        query_texts=[pertanyaan],
        n_results=1
    )
    if hasil['documents'] and hasil['documents'][0]:
        return hasil['documents'][0][0]
    return "Tidak ada informasi terkait di dokumen."

def jawab_pertanyaan(pertanyaan: str) -> str:
    """Mengirim pertanyaan dan konteks dokumen ke Groq untuk dijawab."""
    # Langkah RAG 1: Ambil contekan dari database vektor
    konteks = cari_dokumen(pertanyaan)
    
    # Langkah RAG 2: Susun instruksi dan berikan contekan ke AI
    system_prompt = (
        "Anda adalah asisten AI Helpdesk IT Internal yang ramah dan solutif. "
        "Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks dokumen yang diberikan. "
        "Aturan ketat:\n"
        "1. Jika solusinya ada di dokumen, berikan langkah perbaikan yang jelas dan terstruktur.\n"
        "2. Jika solusinya TIDAK ADA di dokumen panduan, jangan mengarang jawaban. "
        "Katakan dengan jujur bahwa Anda belum memiliki panduan untuk hal tersebut dan sarankan "
        "menghubungi tim IT Helpdesk (Email: it-helpdesk@kantor.local atau ext 104/105).\n\n"
        f"Konteks Dokumen:\n{konteks}"
    )
    
    # Langkah RAG 3: Groq menghasilkan jawaban
    response = client_groq.chat.completions.create(
        model=active_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pertanyaan}
        ],
        temperature=0.2 # Nilai rendah agar jawaban konsisten dan tidak berhalusinasi
    )
    return response.choices[0].message.content

# 3. Antarmuka Tanya Jawab Interaktif di Terminal
print("=" * 60)
print("🤖 SELAMAT DATANG DI AI IT HELPDESK KANTOR")
print("Ketik pertanyaan Anda tentang Wi-Fi, Zoom, atau kendala laptop.")
print("Ketik 'keluar' untuk mengakhiri sesi.")
print("=" * 60)

while True:
    pertanyaan = input("\nAnda: ").strip()
    if not pertanyaan:
        continue
    if pertanyaan.lower() in ["keluar", "exit"]:
        print("Sampai jumpa! Semoga harimu menyenangkan.")
        break
    
    print("\nSedang mencari solusi...")
    jawaban = jawab_pertanyaan(pertanyaan)
    print(f"\nHelpdesk AI:\n{jawaban}")
    print("-" * 60)

