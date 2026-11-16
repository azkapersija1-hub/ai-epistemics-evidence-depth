# 18 Daftar risiko penelitian

Skala: Kemungkinan (R/S/T) x Dampak (R/S/T). Mitigasi = tindakan sebelum eksekusi.

| # | Risiko | K | D | Mitigasi |
|---|---|---|---|---|
| 1 | Pelabelan ahli tidak selesai dalam 3 hari (Standard tidak tercapai) | T | T | Komit ke Minimal; laporkan sebagai eksploratif; mulai pelabelan sebelum 13 Nov |
| 2 | Tumpang tindih dengan Confidence Audit/FlipRate/arXiv 2602.14189 (belum dibuka) | S | T | Buka dan baca 2602.14189 sebelum klaim kebaruan; nyatakan pembeda |
| 3 | Kebocoran kunci/kategori ke prompt atau nama berkas | S | T | Uji otomatis; kunci di folder terpisah |
| 4 | Kebocoran artikel antar-split | S | T | Split berbasis artikel; dedupe 187 kelompok DOI |
| 5 | Sigma/ICC asumsi salah → daya salah | T | S | Pilot 20-45 butir; hitung ulang n |
| 6 | F11x tidak valid untuk tugas ini; hasil dibaca sebagai validasi | T | S | Plasebo D; hipotesis dua arah; sekunder |
| 7 | Akses/kuota model belum terverifikasi; Haiku/Gemini harga unknown | T | S | Verifikasi sebelum pilot; laporkan hanya model yang jalan |
| 8 | Perubahan versi/alias model selama sprint | S | S | Pin snapshot; catat tanggal |
| 9 | Tahun/metadata korpus tidak bisa dipakai; bahasa campur | T | R | Jangan memakai tahun sebagai variabel; stratifikasi bahasa |
| 10 | Hak cipta redistribusi PDF | S | S | Repo hanya DOI/ID dan kutipan pendek |
| 11 | Parse failure tinggi pada beberapa model | S | S | Dua batas Brier; dilaporkan per model |
| 12 | Dua agen Haiku satu keluarga: bias bersama | T | S | Jangan sebut independen statistik; verifikasi sumber oleh peneliti |
| 13 | Sumber 2026 hanya ringkasan web (angka salah) | T | S | Tidak dikutip sebelum dibuka (`19`) |
| 14 | Tumpang tindih proyek dengan P1 4 Nov; batas 2 proyek/orang | S | S | Putuskan proyek mana; ungkap |
| 15 | Ceiling effect lagi (butir terlalu mudah) | S | S | Butir lebih sulit; uji pada pilot |
| 16 | Tenggat: 23.59 AoE = 16 Nov 18.59 WIB; keliru zona | R | T | Targetkan selesai 15 Nov WIB malam |
| 17 | Sprint Swarm 6-8 Nov tercampur | R | S | Pisahkan folder dan klaim |
