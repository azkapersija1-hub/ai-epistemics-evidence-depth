# 3. Metode

## 3.1 Desain bukti dan label jangkar

Setiap klaim diuji pada tujuh observasi (lihat Lampiran C). Own R1, R2, dan R3 memakai bukti dari artikel asal klaim. Near dan far memakai bukti dari artikel lain. Label jangkar bersifat mekanis: own R3 diberi SUPPORTED dari kalimat kesimpulan penulis artikel, near dan far diberi NEI, dan own R1 dan R2 tidak berlabel. Tidak ada jangkar REFUTED dan label ahli belum diisi, sehingga skor mengukur kecocokan dengan jangkar.

Pada pasangan_v2_1.jsonl, sumber items analisis, label bahasa near dan far sama dengan label bahasa klaim pada 294 dari 294 pasangan (heuristik atas abstrak). Pada 39 klaim berlabel unk (78 pasangan), kesamaan itu hanya berarti sama-sama tidak dikenali, sehingga bahasa sebenarnya tidak dipastikan. Kata kunci pada sebagian pasangan near diganti: 35 penggantian pada 18 dari 294 pasangan (rincian di Lampiran C.2). Aturan peringkat near belum dipastikan: skrip c_pasangan_v21.py memakai peringkat 5 sampai 20, sedangkan laporan Agen 1 menulis 3 sampai 10. Versi yang menghasilkan data tidak dapat dipastikan dari catatan yang tersedia, sehingga hal ini dilaporkan sebagai keterbatasan reproduksibilitas.

## 3.2 Data dan pemilihan klaim

Katalog internal menyediakan 294 klaim dengan tujuh observasi masing-masing (2.058 observasi). Split pilot berisi 20 klaim, dev 78, val 98, dan holdout 98. Set pelaporan utama adalah 274 klaim non-pilot (dev, val, holdout), dengan tujuh presentasi bukti per klaim dan 1.918 observasi per model. Set 294 klaim, yang mencakup 20 pilot, merupakan analisis tambahan.

Tim menilai 40 klaim (10 pilot dan 30 dev). Empat klaim keluar setelah perundingan, sehingga lapis 36 berisi 9 klaim pilot dan 27 klaim dev. Satu klaim berstatus DIREVISI dan tetap masuk, sehingga versi teks yang diuji perlu dipastikan. Lapis 26 dan 19 adalah subset lapis 40; aturan pemilihannya tidak terdokumentasi pada catatan yang tersedia dan dilaporkan sebagai keterbatasan.

Amandemen 5 semula menetapkan seluruh 294 klaim sebagai analisis utama. Penetapan set pelaporan 274 klaim dilakukan setelah pengumpulan data dan dicatat terpisah dari protokol awal (lihat docs/prareg/CATATAN_DEVIASI.md). Kepekaan resmi (Amandemen 6) adalah (a) tanpa butir KELUAR final (290 klaim) dan (b) ketat, yaitu tanpa butir yang menerima setidaknya satu suara TIDAK_LAYAK (280 klaim). Kedua himpunan kepekaan berasal dari set 294 dan tumpang tindih, sehingga bukan replikasi independen. Hanya 40 klaim yang kelayakannya dinilai tim.
**Tabel 1.** Set analisis.

| Set | Klaim | Observasi | Keterangan |
|---|---|---|---|
| Utama (set pelaporan) | 274 | 1.918 | Dev 78, val 98, holdout 98; tanpa pilot |
| Tambahan | 294 | 2.058 | Semua split, termasuk 20 pilot (analisis tambahan) |
| Kepekaan (a), dari set 294 | 290 | 2.030 | Tanpa 4 butir KELUAR |
| Kepekaan (b), dari set 294 | 280 | 1.960 | Tanpa 14 butir dengan minimal satu suara TIDAK_LAYAK |

## 3.3 Validasi butir oleh tiga penulis

Tiga penulis dengan latar rekayasa, psikometri, dan penulisan menilai setiap pernyataan sebagai LAYAK, PERLU_REVISI, atau TIDAK_LAYAK, dengan suara terbanyak sebagai keputusan. Penilai mengetahui hipotesis (Amandemen 5), dan penilaian ini bukan validitas isi oleh panel ahli eksternal. Kesepakatan pada 40 pernyataan sebesar 61,7 persen dari 120 perbandingan pasangan, dan kappa Fleiss (Fleiss, 1971) sebesar -0,025, sehingga penilaian tidak stabil antarpenulis. Kesepakatan tim pada 30 pasangan near belum didamaikan dengan pemeriksaan agen. Cara menilai validitas jangkar NEI tidak ditetapkan dalam studi ini; jangkar diperlakukan sebagai acuan sementara dan hasil tidak ditafsirkan sebagai ketepatan faktual.

## 3.4 Model dan jalur pengumpulan

Model mengeluarkan distribusi tiga label dengan jumlah 1 ± 0,01. Tiga model API dijalankan pada seluruh split. GPT-6.1 Sol (tidak terverifikasi) dijalankan pada subset sebagai pembanding jalur agen (40 klaim dikirim, 39 efektif karena C0230 dilewati). Sesi Gemini 3.8 Flash dicatat di repositori, tetapi tidak dianalisis dalam laporan ini. Pada set pelaporan utama, deepseek-v4.1-flash memiliki 8 gagal parse final, sehingga 268 dari 274 klaim non-pilot dapat dievaluasi untuk konsistensi R1 sampai R3 (288 dari 294 pada set tambahan). Suhu tidak dapat diatur melalui harness API. Tabel jalur lengkap ada pada Tabel C1 (Lampiran C).

## 3.5 Metrik dan analisis

Brier multikelas (Brier, 1950) per observasi adalah jumlah selisih kuadrat ketiga label, dengan rentang 0 sampai 2. Metrik primer memakai observasi berjangkar, yaitu own R3 SUPPORTED serta near dan far NEI. Interval 95 persen memakai bootstrap klaster per article_id (Efron, 1979) dengan B = 2.000 dan seed 20261111. Konsistensi R1 dan R3 memakai argmax pada own. Overkomit memakai ambang tau 0,7, dan massa false-support adalah p(SUPPORTED) ditambah p(REFUTED) pada near dan far. Metrik sekunder mencakup akurasi, ECE (Guo dkk., 2017), dan AURC (lihat Zhou dkk., 2024), yang dilaporkan di Lampiran D. Nilai Brier gabungan dihitung sebagai rerata berbobot n dari lima Brier per jenis bukti (own R3, near R1, near R3, far R1, far R3), tanpa CI bootstrap gabungan; deviasi ini dicatat di Lampiran C.5. Hasil utama (274 klaim) disajikan pada Tabel 2 (Bagian 4). Gambar 1 memakai set 294 (analisis tambahan).

## 3.6 Praregistrasi dan penyimpangan

Protokol dibekukan pada 11 November 2026 (23.08.13 WIB), sebelum keluaran pilot pertama. Urutannya adalah pilot (teknis), dev, val, lalu holdout satu kali. Klaim bahwa holdout dijalankan sekali belum diverifikasi ulang dari log, sehingga holdout tidak dibaca sebagai uji konfirmatori murni. Praregistrasi menyatakan pilot tidak dilaporkan sebagai hasil, sedangkan Amandemen 5 semula menetapkan 294 klaim (termasuk pilot) sebagai analisis utama. Set pelaporan utama kini 274 klaim non-pilot, dan penetapannya dicatat terpisah dari protokol awal setelah pengumpulan data. Set 294 hanya dilaporkan sebagai analisis tambahan. Enam amandemen dan tiga penyimpangan dirinci di Lampiran C. D3 dicatat di CATATAN_DEVIASI.md pada 15 November 2026, setelah kejadian. Tanggal dan jam pekerjaan tercantum pada Lampiran A.

## 3.7 Keterbatasan metode

Keterbatasan utama: (a) heuristik bahasa, (b) dua aturan peringkat near, (c) validitas jangkar NEI, (d) pilot dalam analisis utama, (e) kebutaan penilai, dan (f) empat butir keluar lewat perundingan. Uraian di Lampiran C.6.
