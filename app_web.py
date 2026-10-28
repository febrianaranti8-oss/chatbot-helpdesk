import os
import streamlit as st
import chromadb
from groq import Groq

# 1. Konfigurasi Halaman Web
st.set_page_config(page_title="IT Helpdesk AI", page_icon="🤖", layout="centered")

st.title("🤖 IT Helpdesk AI Assistant")
st.caption("Solusi mandiri kendala Wi-Fi, Zoom, dan laptop kantor berbasis RAG.")

# 2. Inisialisasi API Groq & ChromaDB
def load_env():
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    os.environ[k] = v

load_env()
client_groq = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@st.cache_resource
def get_chroma_collection():
    """Cache koneksi database agar tidak dimuat berulang-ulang setiap pesan baru."""
    client_chroma = chromadb.PersistentClient(path="./chroma_db")
    return client_chroma.get_or_create_collection(name="helpdesk_faq")

collection = get_chroma_collection()

@st.cache_resource
def get_available_model():
    """Mengambil model chat teks aktif yang tersedia di Groq."""
    try:
        models = [m.id for m in client_groq.models.list().data]
        # Utamakan keluarga Llama yang stabil
        for target in ["llama-3.3-70b-versatile", "llama-3.2-3b-preview", "llama-3.2-1b-preview", "llama3-70b-8192", "llama3-8b-8192"]:
            if target in models:
                return target
        return models[0] if models else "llama-3.3-70b-versatile"
    except Exception:
        return "llama-3.3-70b-versatile"

active_model = get_available_model()

def cari_dokumen(pertanyaan: str) -> str:
    """Mencari potongan panduan dari ChromaDB."""
    hasil = collection.query(query_texts=[pertanyaan], n_results=1)
    if hasil['documents'] and hasil['documents'][0]:
        return hasil['documents'][0][0]
    return "Tidak ada informasi terkait di dokumen."

def jawab_pertanyaan(pertanyaan: str) -> str:
    """RAG Flow: Mengambil konteks dan meminta jawaban dari Groq."""
    konteks = cari_dokumen(pertanyaan)
    
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
    
    response = client_groq.chat.completions.create(
        model=active_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pertanyaan}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

# 3. Pengelolaan Riwayat Chat di Web
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Halo! Ada kendala IT seputar Wi-Fi, Zoom, atau laptop yang bisa saya bantu?"}
    ]

# Tampilkan seluruh riwayat pesan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Input Pertanyaan Pengguna
if user_input := st.chat_input("Ketik kendala Anda di sini..."):
    # Simpan dan tampilkan pesan pengguna
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Proses jawaban AI
    with st.chat_message("assistant"):
        with st.spinner("Mencari solusi di panduan IT..."):
            jawaban = jawab_pertanyaan(user_input)
            st.markdown(jawaban)
    
    # Simpan jawaban asisten ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": jawaban})

