Simulasi Algoritma Garis DDA & Bresenham
Halo! Ini program interaktif yang gue bikin pakai Python dan PyQt6 buat menuhin tugas mata kuliah Grafik Komputer.

Intinya, aplikasi ini dibikin buat nunjukin gimana sih cara kerja Algoritma DDA (Digital Differential Analyzer) sama Bresenham pas ngegambar garis di layar monitor. Daripada pakai fungsi gambar instan bawaan library, di sini koordinat per-pikselnya bener-bener diitung manual dari nol pakai murni logika matematika. Biar gampang ngetesnya, gue bikinin UI yang lumayan asik dan interaktif.

Fitur-fiturnya Apa Aja?
1. Kalkulasi Murni (From Scratch): Itung-itungan piksel di algoritma DDA dan Bresenham beneran dibikin manual tanpa cheat fungsi otomatis.
2.  Kanvas Klik-Klik (Interaktif): Males ngetik angka koordinat? Tinggal arahin kursor ke kanvas, klik buat nentuin titik awal, terus klik lagi buat titik akhir. Garisnya langsung jadi!
3. Penggaris Tepi (Ruler): Di pinggiran kanvas udah gue tambahin penggaris X sama Y, lengkap sama angkanya biar gampang ngira-ngira letak piksel.
4. Bisa di-Zoom!: Kanvasnya bisa di-zoom in/out (maksimal 500%). Kerennya lagi, angka di penggarisnya bakal ikutan melar/merapat nyesuain skala zoom. Caranya tinggal tahan Ctrl + Scroll Mouse aja.
5. Undo & Redo System: Kalo salah tarik garis, santai aja. Tinggal pencet shortcut Ctrl+Z buat Undo atau Ctrl+Y buat Redo sampai kanvasnya bersih lagi.
6.  Hapus Kanvas: Ada satu tombol sakti buat nge-clear semua coretan balik jadi kertas putih bersih.

Syarat Buat Jalanin
Nggak ribet kok, lu cuma butuh:
Python 3.x (udah pasti lah ya)
Library GUI: PyQt6

Cara Install & Pakenya
Clone atau download source code ini ke laptop lu.
Buka terminal/CMD, arahin ke folder projectnya.
Kalo belum ada PyQt6, install dulu ketik ini:

Bash
pip install PyQt6

Kalo udah, tinggal run aja programnya:

Bash
python denah_rumah.py

Cara Mainnya
Di panel kiri, pilih dulu mau ngetes pakai algoritma yang mana (DDA atau Bresenham).
Cara Ngetik: Masukin angka di kolom Titik Awal (x1, y1) sama Akhir (x2, y2), terus klik tombol Gambar Garis.
Cara Cepet: Langsung aja arahin mouse ke area kanvas putih, klik kiri sekali buat start, klik lagi di tempat lain buat finish.
Buat nge-zoom, tahan tombol Ctrl di keyboard terus puter scroll mouse lu ke atas atau ke bawah.
Kalo garisnya salah, langsung aja pencet Ctrl+Z di keyboard.

Ngintip Daleman Kodenya (Clean Code)
Kodenya sengaja gue pisah-pisah biar rapi dan gampang dibaca (modular):
AlgoritmaGaris: Ini "otak" matematikanya. Nggak ada urusan sama tampilan UI, murni cuma fungsi itung-itungan rumus aja.
KanvasGambar: Ini bagian yang ngurusin gambar-menggambar (kertas digital, penggaris, deteksi klik mouse, sampe logika buat zoom).
AplikasiUtama: Ini kerangka utama aplikasinya yang nyusun tombol, letak tulisan, panel kiri, dan jadi jembatan penghubung ke kanvas.


Dibuat oleh:
Nama: Muhamad Fathan Fahrizy
Kampus: Universitas Gunadarma
Mata Kuliah: Grafik Komputer