# 🤖 AI IT Helpdesk Assistant (PT Bumi Siak Pusako • SKK Migas)

Aplikasi Chatbot Helpdesk IT Internal berbasis **Retrieval-Augmented Generation (RAG)** yang dirancang untuk membantu karyawan menyelesaikan kendala operasional harian (Wi-Fi, Zoom, dan troubleshooting laptop) secara mandiri (*self-service*).

Tampilan antarmuka mengadopsi desain enterprise modern yang diintegrasikan langsung dari **Google Stitch UI**.

---

## 🏗️ Arsitektur Sistem (RAG Pipeline)

1. **Ingestion & Knowledge Base**: Dokumen SOP IT internal ([`panduan_it.txt`](panduan_it.txt)) dipecah menjadi bagian-bagian terstruktur (*chunks*).
2. **Vector Store & Embeddings**: Potongan dokumen diubah menjadi representasi makna menggunakan model embedding lokal gratis pada **ChromaDB**.
3. **Retrieval**: Saat pengguna memasukkan pertanyaan, ChromaDB mencari potongan panduan yang paling relevan (*semantic search*).
4. **Generation**: Model LLM di **Groq** (`qwen/qwen3.8-27b`) memproses pertanyaan bersama contekan dokumen untuk menghasilkan jawaban yang solutif, terstruktur, dan anti-halusinasi.

---

## 🚀 Fitur Utama

- **Self-Service Q&A**: Menjawab pertanyaan teknis seputar Wi-Fi dinas, Zoom audio/video, dan kendala laptop hang/freeze.
- **Strict Anti-Hallucination**: Jika solusi tidak terdapat di panduan resmi, AI secara jujur akan menyarankan pengguna menghubungi tim IT helpdesk (Email / Hotline Internal).
- **Enterprise Web UI**: Desain responsif bertema *dark-mode* resmi SKK Migas & PT Bumi Siak Pusako dari Google Stitch.
- **Multiple Interfaces**: Tersedia dalam mode Web Native (`server.py`), Web Streamlit (`app_web.py`), dan CLI Terminal (`app.py`).

---

## 🛠️ Persyaratan Sistem & Instalasi

- **Python**: Versi `3.12.x` (Direkomendasikan)
- **API Key**: Groq API Key ([console.groq.com](https://console.groq.com))

### 1. Kloning Repositori
```bash
git clone https://github.com/febrianaranti8-oss/chatbot-helpdesk.git
cd chatbot-helpdesk
```

### 2. Pasang Dependensi
```bash
py -3.12 -m pip install chromadb groq streamlit
```

### 3. Konfigurasi Lingkungan (.env)
Buat file `.env` di direktori utama:
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 💻 Cara Menjalankan Aplikasi

### Opsi A: Web Server Enterprise Stitch (Direkomendasikan)
```bash
py -3.12 server.py
```
Akses di browser: 👉 **http://localhost:8080**

### Opsi B: Web Streamlit
```bash
py -3.12 -m streamlit run app_web.py
```
Akses di browser: 👉 **http://localhost:8501**

### Opsi C: CLI Terminal
```bash
py -3.12 app.py
```

---

## 📁 Struktur Direktori
```text
├── panduan_it.txt         # Knowledge base SOP Helpdesk IT
├── server.py              # Server web utama + RAG backend
├── app_web.py             # Versi alternatif menggunakan Streamlit
├── app.py                 # Chatbot interaktif versi terminal (CLI)
├── test_retrieval.py      # Pengujian retrieval ChromaDB independen
├── stitch_output/         # Aset desain HTML, CSS Tailwind, dan Logo
│   ├── index.html         # Antarmuka Chat Helpdesk utama
│   ├── Panduan_WiFi.html  # Halaman panduan diagnosa mandiri
│   └── logo_bsp.png       # Logo resmi PT Bumi Siak Pusako
├── .gitignore             # Pengabaian file lokal sensitif (.env, database)
└── README.md              # Dokumentasi proyek
```

---

## 🛡️ Keamanan & Keterbatasan
- Kunci API dikelola melalui environment variable (`.env`) dan tidak dilacak oleh Git.
- Model membatasi jawaban hanya pada pengetahuan yang tertera di dokumen simulasi.

