# 8. Kode dan Data

Repositori kode: https://github.com/azkapersija1-hub/ai-epistemics-evidence-depth

Data yang dibagikan (repositori: `repo/`):

- Keluaran model per split dan per model di `results/` (berkas `nyata_<split>_<model>_u1.jsonl`). Setiap baris berisi ID observasi, hash prompt, waktu, dan vektor probabilitas tiga label. Kolom `raw` hanya memuat vektor probabilitas JSON pendek (paling panjang 59 karakter), tanpa teks artikel atau teks klaim.
- Tabel agregat untuk tiga model API pada set pelaporan utama 274 klaim non-pilot dan set 294 klaim (analisis tambahan), serta tabel kepekaan (a) dan (b), dalam berkas CSV dan MD (`results/utama294/`).
- Tabel agregat lapis 40, 36, 26, dan 19, serta hasil uji ulang kestabilan.
- Daftar ID klaim untuk lapis 40, lapis 36, dan set kepekaan, tanpa teks klaim dan tanpa label.
- Skrip harness dan skrip analisis, tanpa kunci API, praregistrasi beku dengan nilai hash, catatan amandemen, dan catatan deviasi.
- Gambar set 294 (analisis tambahan; H1 sampai H5) dalam bahasa Indonesia dan Inggris, beserta indeksnya, di `figures_294/`. Gambar G1 sampai G7 berada di `repo/figures/`; G3 sampai G7 dibangun dari data lapis 36.
- Sesi Gemini 3.8 Flash dicatat di `results/gemini_antigravity/`, tetapi tidak dianalisis dalam laporan ini.
- Video ringkasan dalam dua bahasa untuk set pelaporan utama 274 klaim non-pilot: `video/ringkasan274_en.mp4` dan `video/ringkasan274_id.mp4` (angka dicocokkan di `video/angka_pencocokan274_*.txt`; keterangan di `video/RINGKASAN_VIDEO274.md`). Video untuk set 294 (analisis tambahan) ada di `video/ringkasan294_en.mp4` dan `video/ringkasan294_id.mp4`.
- Ringkasan kelayakan butir dan pasangan kesepakatan tanpa nama penilai. Berkas sumber yang memuat nama penilai tidak dibagikan (lihat `EXCLUDED.md`). berkas versi ini dibuat sebelum dibagikan, karena berkas sumber memuat nama penilai.

Data yang tidak dibagikan (lihat `EXCLUDED.md`):

- Kunci jawaban, yaitu label jangkar per observasi beserta split dan article_id. Kunci dipisahkan agar benchmark tidak dapat dipelajari atau diuji secara langsung. Label ahli belum tersedia, sehingga tidak ada kunci ahli.
- Teks klaim, teks bukti, dan kolom prompt dari artikel, karena berasal dari artikel yang berhak cipta. Berkas items dan pasangan (`items_model.jsonl`, `pasangan_v2*.jsonl`) juga tidak dibagikan.
- Berkas penilai individual yang memuat nama dan catatan personal.
- Kredensial, profil API, dan catatan pemakaian token.
- Keluaran glm-5.3 yang dihentikan (D2). Keberadaan dan alasan penghentiannya dicatat di `results/glm_dihentikan/CATATAN.md`.
