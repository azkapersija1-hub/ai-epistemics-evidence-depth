# 17 Kontribusi yang dapat diajukan di sprint

Tiap kontribusi ditandai: **BARU** (dibuat 13-15 Nov), **PREEXISTING** (wajib diungkap), **DIKLAIM-BERSYARAT** (hanya jika terpenuhi).

| # | Kontribusi | Status | Syarat / catatan |
|---|---|---|---|
| 1 | Protokol evaluasi tiga-label (SUPPORTED/REFUTED/NEI) untuk klaim **akademik** dengan Brier multikelas sebagai primary dan batas parse failure | BARU | Perbedaan dengan P1 (4 Nov, biner, sanggahan) dan FEVER umum harus dijelaskan |
| 2 | Kumpulan butir baru dari korpus akademik dengan aturan konstruksi tertulis dan split berbasis artikel | BARU | Jumlah butir aktual menentukan klaim; bila <385 → eksploratif |
| 3 | Perbandingan lintas model dengan prompt tunggal, pelaporan klaster-per-artikel | BARU | Akses semua model belum terverifikasi; hanya laporkan model yang benar dijalankan |
| 4 | Uji intervensi sinyal eksternal (F11x-adaptasi) vs plasebo | DIKLAIM-BERSYARAT | Hanya jika definisi dibekukan sebelum data; hasil dilaporkan dua arah, termasuk nol |
| 5 | Audit konstruk instrumen: ceiling effect 45 butir lama dan estimasi daya | BARU (analisis) / data PREEXISTING | Data hasil 29 Okt disebut preexisting |
| 6 | Kode skoring, parser, uji kebocoran kunci | BARU | Repo publik hanya setelah persetujuan |

## Yang tidak boleh diklaim
- "Pertama kali" mengukur kalibrasi pada klaim akademik (abstensi di SciFact sudah ada; arXiv 2602.14189 belum dibuka).
- F11x sebagai pengukur kebenaran bukti atau rumus baru.
- Banyaknya model atau besarnya korpus sebagai bukti validitas.
- Hasil Swarm, ARAL, atau 45 butir sebagai hasil sprint.

## Pembeda terhadap contoh resmi Track 1
Confidence Audit (hasil belakangan), FlipRate (sanggahan bertingkat), MisleadBench (multi-giliran). Studi ini: klaim akademik + bukti tertentu + tiga label + skor probabilistik multikelas + lintas model + praregistrasi. Pembeda nyata hanya bila kontribusi 1-3 tuntas dan jelas dibandingkan dengan ketiganya.
