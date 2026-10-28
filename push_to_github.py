import subprocess
import os
import sys

def run_cmd(cmd):
    print(f"\n>> Menjalankan: {' '.join(cmd)}")
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.stdout:
            print(res.stdout.strip())
        if res.stderr:
            print(res.stderr.strip())
        return res.returncode
    except Exception as e:
        print(f"Error eksekusi: {e}")
        return 1

print("=" * 60)
print("🚀 OTOMATISASI PUSH PROYEK KE GITHUB")
print("=" * 60)

# 1. Inisialisasi Git
run_cmd(["git", "init"])

# 2. Tambahkan semua file (kecuali yang di .gitignore)
run_cmd(["git", "add", "."])

# 3. Commit
run_cmd(["git", "commit", "-m", "feat: AI Helpdesk Chatbot RAG with Stitch UI and Groq"])

# 4. Set branch main
run_cmd(["git", "branch", "-M", "main"])

# 5. Konfigurasi Remote URL
subprocess.run(["git", "remote", "remove", "origin"], capture_output=True)
run_cmd(["git", "remote", "add", "origin", "https://github.com/febrianaranti8-oss/chatbot-helpdesk.git"])

# 6. Push ke GitHub
print("\n>> Melakukan push ke GitHub (Mungkin akan muncul jendela browser/login GitHub)...")
push_res = subprocess.run(["git", "push", "-u", "origin", "main"])

if push_res.returncode == 0:
    print("\n✅ BERHASIL! Seluruh proyek sudah ter-push ke GitHub:")
    print("👉 https://github.com/febrianaranti8-oss/chatbot-helpdesk")
else:
    print("\n⚠️ Push belum selesai. Jika muncul jendela login GitHub, silakan selesaikan login Anda.")

