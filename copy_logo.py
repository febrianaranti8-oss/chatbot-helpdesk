import shutil
import os

src = r"C:\Users\ranti.febriana\.gemini\antigravity\brain\dc9404e1-5bb2-48a7-afdb-0c19b924da75\.user_uploaded\media_1793163268127_b5d1ce5b.png"
dst = r"d:\Belajar AI\AI Help Desk 2\stitch_output\logo_bsp.png"

if os.path.exists(src):
    shutil.copyfile(src, dst)
    print("Logo PT Bumi Siak Pusako berhasil diperbarui!")
else:
    print("File sumber tidak ditemukan.")
