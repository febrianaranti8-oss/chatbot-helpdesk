import chromadb

# 1. Inisialisasi ChromaDB (data disimpan di folder lokal ./chroma_db)
client = chromadb.PersistentClient(path="./chroma_db")

# 2. Buat atau ambil koleksi dokumen helpdesk
collection = client.get_or_create_collection(name="helpdesk_faq")

# 3. Baca file panduan dan pecah menjadi beberapa potongan (chunks) berdasarkan topik
with open("panduan_it.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Memecah teks berdasarkan judul bagian ("## ")
raw_chunks = text.split("## ")
chunks = []
ids = []

for i, chunk in enumerate(raw_chunks):
    cleaned = chunk.strip()
    if cleaned:
        chunks.append(cleaned)
        ids.append(f"doc_{i}")

# Masukkan potongan dokumen ke dalam ChromaDB
# ChromaDB secara otomatis akan mengubah teks menjadi angka (vektor embedding)
collection.upsert(
    documents=chunks,
    ids=ids
)

print(f"Berhasil menyimpan {len(chunks)} bagian dokumen ke ChromaDB!\n")

# 4. Uji coba pencarian (Retrieval)
pertanyaan_tes = "suara saya tidak keluar saat meeting zoom"
print(f"Menguji pencarian dengan pertanyaan: '{pertanyaan_tes}'...")

hasil = collection.query(
    query_texts=[pertanyaan_tes],
    n_results=1 # Mengambil 1 dokumen yang paling relevan
)

print("\nHasil dokumen yang ditemukan:")
print("--------------------------------------------------")
print(hasil['documents'][0][0])
print("--------------------------------------------------")

