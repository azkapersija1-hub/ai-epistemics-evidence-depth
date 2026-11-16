# Pemeriksaan sitasi naskah (langkah 2 dan 3)

Tanggal pemeriksaan: 2026-11-15. Berkas yang diperiksa: C:\EPIS_KERJA\GITHUB_REPO\report\v3\00_abstrak.md sampai 14_lampiran_E_keterbatasan_lengkap.md (nomor = berkas:baris, dihitung per berkas). Naskah tidak diubah. Daftar pustaka yang dipakai: REFERENSI_LAPORAN_v2.md dan referensi_tambahan_v2.csv.

Status yang dipakai:
- S1: rujukan terverifikasi ada dan sudah dikutip di teks.
- S2: rujukan terverifikasi ada, belum dikutip di teks (lokasi usulan tercantum).
- S3: belum ada rujukan terverifikasi. Tidak dicari pada langkah ini kecuali disebutkan.

Catatan: tidak ada kalimat sitasi baru yang ditulis di sini. Usulan hanya berupa lokasi dan kunci rujukan.

---

## A. Langkah 2: metode dan konsep metodologis tanpa sitasi

| No | Metode atau konsep | Lokasi di naskah | Sudah dikutip? | Status | Rujukan (kunci di v2) |
|---|---|---|---|---|---|
| 1 | Skor Brier (asal, forecast verification) | 01:3 (kalibrasi lewat Brier); 02:9 (Brier multikelas); 03:34; 09:11 (ARAL, preexisting) | tidak | S2 | brier1950 |
| 2 | Brier multikelas (jumlah selisih kuadrat tiga label, rentang 0 sampai 2) | 03:34; 12:51; 13:9-13 | tidak | S3 untuk bentuk multikelas | brier1950 hanya menjelaskan asal skor; kesesuaian bentuk multikelas belum diverifikasi isi |
| 3 | Kappa Cohen | 12:42 | tidak | S2 | cohen1960kappa |
| 4 | Kappa Fleiss | 03:26; 05:17; 12:43; 14:7 | tidak | S2 | fleiss1971kappa |
| 5 | Bootstrap (persentil) dan bootstrap klaster per article_id | 03:34 dan 12:57 (Efron 1979 sudah dikutip); 13:3 (tanpa kutipan) | sebagian | S1 untuk bootstrap umum; S3 untuk bootstrap klaster | efron1979bootstrap. Judul Efron 1979 bersifat umum; tidak ada rujukan terverifikasi yang khusus bootstrap klaster |
| 6 | ECE (Expected Calibration Error) | 01:3 (tanpa kutipan); 02:3 (Guo dikutip); 03:34 (tanpa); 04:26 (tanpa); 09:11 (tanpa); 12:53 (Guo dikutip); 13 Tabel D6 | sebagian | S1 (Guo sudah dikutip di 02:3 dan 12:53); S2 untuk 01:3, 03:34, 04:26 | guo2017calibration. Definisi ECE di isi makalah belum dibaca (catatan di daftar) |
| 7 | AURC (area under risk-coverage curve) | 03:34 (tanpa); 04:26 (tanpa); 12:53 (AURC diskret, tanpa); 13 Tabel D6 | tidak | S2 (metrik) dengan sumber sementara; S3 untuk asal metrik | zhou2024aurc (makalah karakterisasi, bukan sumber asal). Kandidat asal: geifman2017aurc_kandidat (BELUM_TERVERIFIKASI, abstrak tidak menyebut AURC) |
| 8 | Kalibrasi (konsep umum, "terkalibrasi", "kalibrasi dinilai") | 01:3; 11:19 (tanpa kutipan); 02:3 (sudah dikutip) | sebagian | S1 (02:3); S2 untuk 01:3 dan 11:19 | guo2017calibration; tian2023calibration; xiong2023uncertainty; kadavath2022knowing |
| 9 | Benchmark verifikasi klaim (FEVER, FEVEROUS, SciFact, HoVer, CLIMATE-FEVER, AVeriTeC) | 02:7 (sudah dikutip); 09:9-10 (instrumen dan validasi FEVER, preexisting, tanpa kutipan) | 02:7 ya; 09 tidak | S1 untuk 02:7; S2 untuk 09:9-10 | thorne2018b (FEVER), thorne2018sharedtask, wadden2020scifact, aly2021feverous, jiang2020hover, diggelmann2020climatefever, schlichtkrull2023averitec, karger2024forecastbench |
| 10 | CVI (Content Validity Index), validasi isi oleh panel | 12:70; 14:7 ("bukan CVI") | tidak | S3 | tidak dicari pada langkah ini |
| 11 | Praregistrasi (protokol, amandemen, uji konfirmatori) | 00:3; 01:11; 03:36-38; 08:11; 09:26; 12:60-62; 14:13 | tidak | S3 | tidak dicari pada langkah ini; konsep metodologis yang lazim, keputusan penulis |
| 12 | Holdout | 03:38; 05:20; 14:13 | tidak | S3 | tidak dicari pada langkah ini; keputusan penulis |
| 13 | Argmax, overkomit (tau 0,7), false-support, pergeseran dS dan dN, Brier gabungan | 03:34; 04:22; 04:46; 12:54-56; 12:79 | tidak perlu | definisi operasional naskah | Brier gabungan adalah deviasi yang sudah dicatat (12:79), bukan metode baku |

Catatan tambahan untuk langkah 2:
- Naeini (2015) dan Murphy (1973) masih BELUM_TERVERIFIKASI pada daftar. Keduanya tidak dikutip di naskah, dan tidak dicari pada langkah ini.
- Kandidat rujukan asal AURC: Geifman dan El-Yaniv (2017) ditemukan lewat pencarian arXiv (metadata terlihat), tetapi abstraknya tidak menyebut AURC atau risk-coverage curve, sehingga belum bisa menjadi sumber asal metrik.
- Untuk ECE, Guo dkk. (2017) sudah ada dan terverifikasi ulang pada 2026-11-15 lewat arXiv API. Isi makalah tentang definisi ECE tidak dibaca; naskah 12:53 menyebut "konsep kalibrasi", bukan rumus.

---

## B. Langkah 3: konsistensi sitasi dan daftar pustaka

### B1. Kutipan di naskah dan keberadaannya di daftar

| Kunci (naskah) | Lokasi kutipan | Ada di daftar v2? | Catatan |
|---|---|---|---|
| Guo dkk., 2017 | 02:3; 12:53 | ya | |
| Kadavath dkk., 2022 | 02:3 | ya | |
| Tian dkk., 2023 | 02:3 | ya | |
| Xiong dkk., 2023 | 02:3 | ya | Tahun memakai versi pertama arXiv (2023); venue ICLR 2024. Lihat B3 |
| Ren dkk., 2025 | 01:5; 02:5 | ya | |
| Fanous dkk., 2025 | 01:5; 02:5 | ya | |
| Cheng dkk., 2025 | 01:5; 02:5 | ya | Versi arXiv v2 (lihat daftar) |
| Kim dkk., 2025 | 01:5; 02:5 | ya | |
| Kalai dkk., 2025 | 02:5 | ya | |
| Thorne dkk., 2018a | 02:7 | ya | |
| Thorne dkk., 2018b | 02:7 | ya | |
| Aly dkk., 2021 | 02:7 | ya | |
| Wadden dkk., 2020 | 02:7 | ya | |
| Jiang dkk., 2020 | 02:7 | ya | |
| Diggelmann dkk., 2020 | 02:7 | ya | |
| Schlichtkrull dkk., 2023 | 02:7 | ya | |
| Karger dkk., 2024 | 02:7 | ya | Urutan nama Chen, Y.-H. kini terkonfirmasi (lihat LOG_VERIFIKASI_v2.md) |
| Efron, 1979 | 03:34; 12:57 | ya | |
| Alibaba Cloud (2026) | 12:9-11 (Tabel C1) | ya | |

Ringkasan B1: 19 kunci berbeda dikutip di naskah. Semuanya ada di daftar. Tidak ada kutipan yang tidak ada di daftar.

### B2. Entri di daftar yang tidak dikutip di naskah

- Apart Research (2026, sprint page). Tidak ada di teks mana pun. Pada daftar v1 disarankan untuk Keterbatasan dan etika. Keputusan penulis apakah akan dikutip.
- Entri baru v2 yang belum dikutip (diharapkan, karena baru ditambahkan): brier1950, cohen1960kappa, fleiss1971kappa, zhou2024aurc.

### B3. Masalah konsistensi lain

1. Urutan abjad daftar v1 salah: "Alibaba", "Apart", lalu "Aly". Aly harus sebelum Apart. Sudah diperbaiki di REFERENSI_LAPORAN_v2.md.
2. Tahun: naskah memakai tahun versi pertama arXiv (kebijakan konsisten untuk semua entri). Satu-satunya yang berbeda dengan tahun venue adalah Xiong dkk. (arXiv 2023, ICLR 2024). Keputusan penulis: pertahankan kebijakan atau ganti ke tahun venue. Pilihan harus seragam.
3. Klaim isi rujukan di 02 (tidak boleh dikarang, dan belum dibaca dari isi makalah). Kalimat berikut hanya didasarkan pada judul atau metadata:
   - 02:3 "Kadavath dkk. (2022) membahas apakah model bahasa dapat mengenali apa yang diketahuinya" (dari judul).
   - 02:5 "Ren dkk. (2025) memisahkan kejujuran dari akurasi" dan "Kim dkk. (2025) membahas epistemologi Bayes" (dari judul).
   - 02:7 "Thorne dkk. (2018b) memperkenalkan dataset FEVER" (dari judul dan metadata).
   - Kalimat tentang isi harus diperiksa ke makalah sebelum dikirim, atau diperlunak. Agen tidak mengubah naskah.
4. Brier 1950 menjelaskan skor Brier untuk peramalan. Naskah memakai "Brier multikelas" (03:34, 12:51) dan menyebut "Brier batas 1 dan 2" (12:17). Bentuk multikelas tidak terbukti dari rujukan ini. Perlu rujukan tersendiri atau catatan bahwa itu ekstensi penulis.
5. Efron 1979 dikutip untuk "bootstrap klaster per article_id" (03:34, 12:57). Judul makalah bersifat umum tentang bootstrap. Penerapan klaster perlu rujukan khusus, atau kalimat kutipan diperjelas.
6. ECE dikutip sebagai konsep dari Guo dkk. (2017) hanya di 02:3 dan 12:53. Di 01:3, 03:34, dan 04:26 ECE disebut tanpa kutipan.
7. Kappa Cohen (12:42) dan kappa Fleiss (03:26, 05:17, 12:43, 14:7) disebut tanpa kutipan. Rujukan Cohen 1960 dan Fleiss 1971 sekarang terverifikasi.
8. Penyebutan "Brier" dan "ECE" di 01:3 dan kata "kalibrasi" di 11:19 belum dikutip.

---

## C. Usulan lokasi penambahan rujukan (tanpa kalimat sitasi)

| Rujukan (kunci v2) | Lokasi usulan di naskah | Alasan |
|---|---|---|
| brier1950 | 01:3 (Brier); 02:9 (Brier multikelas); 03:34 (skor Brier) | Skor Brier disebut tanpa kutipan. Lihat B3 butir 4 |
| cohen1960kappa | 12:42 (kappa Cohen) | Disebut tanpa kutipan |
| fleiss1971kappa | 03:26; 05:17; 12:43; 14:7 (kappa Fleiss) | Disebut tanpa kutipan |
| zhou2024aurc | 03:34; 04:26; 12:53 (AURC) | AURC disebut tanpa kutipan. Keputusan: sumber asal belum terverifikasi |
| guo2017calibration | 01:3 (ECE); 03:34 (ECE); 04:26 (ECE) | ECE disebut tanpa kutipan di tiga tempat |
| guo2017calibration; tian2023calibration; xiong2023uncertainty | 01:3 dan 11:19 (kalibrasi) | Konsep kalibrasi disebut tanpa kutipan. Pilih sesuai konteks |
| thorne2018b | 09:9-10 (instrumen FEVER, preexisting) | Benchmark disebut tanpa kutipan. Keputusan penulis, karena bagian ini tentang pekerjaan terdahulu |
| apart2026sprint | 14 atau Lampiran B (keterbatasan dan etika) | Ada di daftar, tidak dikutip. Keputusan penulis |

---

## D. Masalah yang perlu keputusan penulis

1. AURC: tidak ada sumber asal terverifikasi. Pilihan: pakai zhou2024aurc sebagai rujukan metrik (dengan catatan bahwa itu makalah karakterisasi), atau tunggu verifikasi isi makalah asal, atau tandai metrik sebagai definisi operasional naskah.
2. Nama tengah Zhou (Han Zhou atau Han Qing Zhou) berbeda antar sumber. Inisial H. dipakai karena semua sumber setuju. Keputusan peneliti apakah nama tengah dicantumkan.
3. Tahun Xiong (2023 atau 2024) dan kebijakan tahun untuk semua entri.
4. Klaim isi di 02 (B3 butir 3) belum dibaca dari isi makalah.
5. Brier multikelas (B3 butir 4) dan bootstrap klaster (B3 butir 5) belum punya rujukan khusus.
6. Kebijakan Apart Research: dikutip atau tidak.
7. Konsep yang belum dicari (S3): CVI, praregistrasi, holdout, bootstrap klaster. Perlu langkah pencarian lanjutan bila penulis ingin rujukan untuk konsep ini.
