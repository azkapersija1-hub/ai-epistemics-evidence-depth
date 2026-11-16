# Lampiran C. Metode rinci

## C.1 Model dan jalur pengumpulan

**Tabel C1.** Model dan jalur pengumpulan.

| Model | Jalur | Cakupan | max_tokens | Catatan |
|---|---|---|---|---|
| qwen3.8-flash | API (profil qwen_plan) | pilot, dev, val, holdout | 512 | ID: Alibaba Cloud (2026); 1 gagal parse final |
| deepseek-v4.1-flash | API (profil qwen_plan) | pilot (diulang), dev, val, holdout | 4000 | Amandemen 1; ID: Alibaba Cloud (2026); 8 gagal parse final, 6 klaim keluar dari uji konsistensi |
| qwen4-max-preview | API (profil qwen_plan) | pilot, dev, val, holdout | 4000 | Amandemen 2; ID: Alibaba Cloud (2026); tanpa gagal parse final |
| GPT-6.1 Sol (tidak terverifikasi) | Sesi agen terpisah | pilot dan dev (40 klaim dikirim, 39 klaim efektif karena C0230 dilewati (SKIP); 280 baris, 7 di antaranya gagal parse); uji ulang 19 klaim (133 observasi) | tidak tercatat | Versi model tidak ditampilkan; pembanding jalur agen pada subset |
| Gemini 3.8 Flash (Antigravity) | Sesi agen terpisah | pilot (140 baris) dan holdout (686 baris) | tidak tercatat | Dicatat di repositori, tidak dianalisis dalam laporan ini; D1 |

Model menerima claim_text dan evidence_text. Keluaran berupa distribusi tiga label dengan jumlah 1 ± 0,01. Jika parse gagal, pemanggilan diulang sekali dan kegagalan yang tersisa dicatat. Suhu dan mode berpikir tidak dapat diatur melalui harness API. Hash prompt API tercantum pada Lampiran A. Keluaran per model tersimpan sebagai vektor probabilitas tiga label tanpa teks artikel.

Gagal parse pada analisis utama: qwen3.8-flash 1 gagal percobaan pertama dan 1 gagal final; qwen4-max-preview 1 gagal percobaan pertama dan 0 gagal final; deepseek-v4.1-flash 20 gagal percobaan pertama dan 8 gagal final. Brier batas 1 mengeluarkan butir gagal, dan batas 2 memberi nilai 2,0.

## C.2 Pasangan bukti dan bahasa

Dua berkas pasangan dan dua aturan tercatat dalam berkas sumber.

- Skrip c_pasangan_v21.py: bukti sebahasa dengan klaim, peringkat kemiripan 5 sampai 20 untuk near, dan 30 persen kemiripan terendah untuk far. Berkas pasangan_v2_1.jsonl dihasilkan dari skrip ini dan menjadi sumber items analisis.
- Laporan Agen 1: peringkat 3 sampai 10 untuk near. Berkas pasangan_v2.jsonl memuat rentang ini.

Hasil pemeriksaan kolom bahasa:

- pasangan_v2_1.jsonl: 294 dari 294 pasangan near dan 294 dari 294 pasangan far sebahasa dengan klaim menurut heuristik abstrak.
- pasangan_v2.jsonl: 137 dari 294 pasangan near dan 194 dari 294 pasangan far lintas bahasa. Angka ini cocok dengan catatan Agen 1 bila ID bukti dipetakan ke bahasa pada pool_v2.jsonl (pemetaan itu dilakukan penulis laporan ini, bukan berkas pasangan itu sendiri). Berkas ini bukan sumber items.

Bahasa klaim pada items: 155 bahasa Inggris, 100 Indonesia, dan 39 tidak terdeteksi (unk). Bahasa diambil dari heuristik pada abstrak, sehingga seluruh pemeriksaan bahasa bergantung pada heuristik tersebut.

Penanda risiko jangkar: laporan Agen 1 mencatat 19 pasangan ditandai karena kata isi klaim di atas 0,6. Kolom risiko_jangkar pada kunci items bernilai salah untuk seluruh observasi. Kolom near_kw_diganti pada pasangan_v2_1.jsonl mencatat 35 penggantian kata kunci pada 18 dari 294 pasangan near (terverifikasi dari berkas). Angka 19 tidak dipakai dan tidak tampak pada pasangan_v2_1.jsonl, karena tidak ada pasangan dengan risiko kata di atas 0,6. Asal angka 19 belum dipastikan [PENULIS MEMASTIKAN].

## C.3 Validasi butir oleh tiga penulis

Keputusan per butir: dua suara LAYAK menghasilkan DIPAKAI, dua suara PERLU_REVISI menghasilkan DIREVISI, dan dua suara TIDAK_LAYAK menghasilkan KELUAR. Tiga suara berbeda dibahas bersama dan dikeluarkan bila tetap tidak sepakat. Dua suara berbeda menghasilkan PERLU_PENILAI_KETIGA dan tidak masuk daftar KELUAR (Amandemen 6). Setiap PERLU_REVISI atau TIDAK_LAYAK wajib disertai catatan. Penilai tidak membuka hasil model per butir sebelum selesai menilai, menurut rancangan Amandemen 5. Kebutaan itu tidak dapat diverifikasi dari berkas. Keluaran dev dan val tercatat pada 11 sampai 12 November 2026, sedangkan penilaian dan perundingan tercatat pada 13 November 2026 (Lampiran A).

Angka kesepakatan:

- Persen sepakat keseluruhan: 61,7 persen dari 120 perbandingan pasangan penilai (40 pernyataan).
- Kappa Cohen untuk tiga pasangan penilai: 0,030, 0,122, dan -0,063.
- Kappa Fleiss: -0,025 (40 pernyataan yang dinilai semua penilai).

Hasil item: empat butir keluar, yaitu C0056, C0057, C0225, dan C0295. Catatan deviasi mencatat satu suara REVISI, satu suara TIDAK_LAYAK, dan dua penilai tidak melanjutkan penilaian pada keempat butir. Keputusan keluar didasarkan pada perundingan tiga penulis pada 13 November 2026. Satu butir (C0230) berstatus DIREVISI dan tetap masuk analisis utama. Dua pernyataan ubahan, C0085 dan C0233, ditandai KELUAR sementara oleh satu penilai sebagai draf ubahan, bukan jangkar. Sebagai jangkar keduanya DIPAKAI berdasarkan tiga suara LAYAK, sehingga angka analisis tidak berubah.

Pasangan bukti: tim mencatat 30 pasangan near sebagai membahas hal yang sama, berdasarkan keterangan peneliti. Ini kesepakatan tim, bukan penilaian independen. Pemeriksaan agen atas 30 pasangan near (hanya 260 karakter awal abstrak) menilai 22 jelas tidak membahas klaim, 8 ambigu, dan 0 membahas klaim yang sama. Pertanyaan lembar berbunyi "membahas atau menjawab", sedangkan jangkar NEI mengasumsikan bukti tidak menjawab klaim. Kedua penilaian belum didamaikan. Belum dipastikan apakah keduanya memakai kelompok 30 pasangan yang sama. Kesepakatan tim juga tidak dihitung sebagai kappa independen.

## C.4 Metrik dan definisi

- Brier multikelas per observasi: jumlah selisih kuadrat ketiga label, rentang 0 sampai 2.
- Batas 1: observasi gagal parse dikeluarkan dari rerata. Batas 2: observasi gagal diberi nilai 2,0.
- Metrik sekunder: akurasi, ECE dengan 10 bin (konsep kalibrasi dari Guo dkk., 2017), AURC diskret, serta recall dan presisi NEI.
- Konsistensi R1 dan R3: argmax pada own. Pergeseran dS adalah p(SUPPORTED) pada R3 dikurangi pada R1. Pergeseran dN adalah p(NEI) pada R1 dikurangi pada R3.
- Overkomit: maksimum p(SUPPORTED) atau p(REFUTED) pada R1 mencapai 0,7 dan label R3 berbeda. Ambang ini dibekukan sejak praregistrasi. Seri argmax dimenangkan NEI.
- Massa false-support: p(SUPPORTED) ditambah p(REFUTED) pada observasi near atau far.
- Interval kepercayaan 95 persen: bootstrap klaster per article_id (Efron, 1979), B = 2.000, seed 20261111 (seed default harness).
- Uji ulang kestabilan: 19 klaim lapis 19 dengan 133 observasi per jalur.

## C.5 Praregistrasi, amandemen, dan penyimpangan

Protokol dibekukan pada 11 November 2026 pukul 23.08.13 WIB. Keluaran pilot pertama tercatat pada 23.08.36 WIB. Tanggal dan jam tiap berkas tercantum pada Lampiran A.

Amandemen (ringkas):

- Amandemen 1: max_tokens DeepSeek dinaikkan ke 4000 setelah 20 dari 140 keluaran pilot kosong pada batas 512.
- Amandemen 2: qwen4-max-preview ditambahkan. Holdout model lain sudah dilihat, dan dinyatakan tidak ada penyetelan.
- Amandemen 3: GLM-5.3 ditambahkan dengan pernyataan yang sama.
- Amandemen 4: GLM-5.3 dikeluarkan karena biaya token.
- Amandemen 5: penilaian kelayakan oleh tim penulis, bukan CVI, dengan analisis kepekaan (a) dan (b).
- Amandemen 6: daftar KELUAR final dan daftar ketat, serta aturan PERLU_PENILAI_KETIGA.

Penyimpangan:

- D1: Gemini 3.8 Flash menyelesaikan sebagian batch holdout sekaligus, bukan per tiga batch. Batas persisnya tidak dapat dipastikan dari log.
- D2: GLM-5.3 dihentikan pada 12 November 2026 setelah 594 dari 686 observasi holdout. Keluaran parsial tidak dianalisis dan tidak dipakai untuk klaim apa pun.
- D3: sembilan klaim pilot berada di lapis 36. Praregistrasi menyatakan pilot sebagai uji teknis yang tidak dilaporkan sebagai hasil, tetapi juga menetapkan analisis utama pada 294 klaim yang mencakup pilot. Tabel utama menyajikan 274 klaim tanpa pilot sebagai pembanding. Lapis 36 memakai keputusan perundingan tim pada 13 November 2026, yang dibuat setelah keluaran dev tersedia.

Deviasi (dicatat): Brier gabungan dihitung sebagai rerata berbobot n dari lima Brier per jenis bukti tanpa CI bootstrap gabungan, sedangkan praregistrasi mensyaratkan CI bootstrap klaster untuk metrik primer. Deviasi ini belum tercatat di CATATAN_DEVIASI.md.

Klaim bahwa holdout dijalankan sekali belum diverifikasi ulang dari log. Penulis perlu memastikannya sebelum laporan final.

## C.6 Keterbatasan metode lengkap

(a) Confound bahasa. Pasangan sebahasa menurut heuristik abstrak tidak membuktikan bahwa bahasa tidak memberi petunjuk. Angka lintas bahasa dari catatan Agen 1 (137 near dan 194 far) berasal dari pasangan_v2.jsonl dan bukan sumber items. Laporan Agen 1 mencatat bahwa peneliti memutuskan tidak menambah aturan bahasa.

(b) Dua aturan near. Skrip c_pasangan_v21.py dan laporan Agen 1 memakai rentang peringkat yang berbeda (lihat C.2). Versi yang menghasilkan data belum dipastikan [PENULIS MEMASTIKAN].

(c) Validitas jangkar NEI belum selesai. Kesepakatan tim dan pemeriksaan agen berbeda, dan keduanya belum didamaikan (lihat C.3). [PENULIS MEMUTUSKAN] apakah jangkar diterima dengan catatan ketidakpastian atau diuji ulang.

(d) Pilot termasuk dalam lapis 40 dan lapis 36, serta analisis utama (D3).

(e) Keluaran dev dan val sudah ada sebelum penilaian kelayakan. Kebutaan penilai tidak dapat diverifikasi.

(f) Empat butir keluar lewat perundingan tim dengan alasan satu suara revisi dan satu suara tidak layak. Catatan deviasi juga mencatat dua penilai tidak melanjutkan penilaian pada keempat butir. Amandemen 6 mengatur dua suara berbeda sebagai PERLU_PENILAI_KETIGA. [PENULIS MEMASTIKAN] apakah penilai ketiga sudah dimintai.

Keterbatasan umum lain: label jangkar berupa proksi, tidak ada jangkar REFUTED, kesepakatan penilai rendah, penilai adalah penulis dan bukan panel independen, jumlah klaim per lapis kecil, satu ulangan utama dan satu uji ulang untuk setiap model, dan suhu tidak terkendali. Jalur agen hanya dibandingkan pada subset: GPT-6.1 Sol pada 40 klaim dikirim (39 efektif, C0230 dilewati; versi tidak terverifikasi). Sesi Gemini 3.8 Flash dicatat di repositori, tetapi tidak dianalisis dalam laporan ini.

## C.7 Gambar

**Gambar C1.** Corong butir: 294 kolam, 40 jangkar, 36 utama, lapis 26 dan 19, dan kotak kesepakatan penilai. Gambar ini tersedia di repositori sebagai G2_corong_butir (berkas id). Angka pada gambar diambil dari berkas sumber yang sama dengan Bagian 3.2 dan Lampiran C.3.
