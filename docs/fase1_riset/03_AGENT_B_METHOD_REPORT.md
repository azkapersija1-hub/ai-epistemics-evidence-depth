# AGENT B: Laporan Metode (fase riset saja)

Status: SIMULASI TEORETIS dan studi literatur. Tidak ada model yang dijalankan, tidak ada API model kandidat yang dipanggil, tidak ada hasil eksperimen, tidak ada dataset final. Semua angka simulasi ditandai "SIMULASI TEORETIS, bukan hasil model".

Berkas pendukung:
- `LITERATURE_EVIDENCE_MATRIX_AGENT_B.csv` (matriks literatur, pemisah titik koma)
- `agent_b_calc.py` (skrip stdlib Python, satu proses, hitungan Brier dan daya)

Catatan independensi: laporan ini tidak membaca folder `_kerja_agen_A` maupun berkas `AGENT_A_*`.

---

## 1. Desain pengukuran akurasi dan confidence

### 1.1 Tiga keluaran per butir
Setiap butir (klaim, bukti, label kunci) menghasilkan:
- label terpilih: SUPPORTED, REFUTED, atau NOT ENOUGH INFORMATION (NEI);
- distribusi tiga kelas p = (p_S, p_R, p_N) yang jumlahnya 1;
- akurasi = 1 jika label terpilih sama dengan kunci.

Akurasi adalah ukuran keputusan. Brier multikelas adalah ukuran kualitas probabilitas. Keduanya dilaporkan terpisah.

### 1.2 Cara mendapatkan probabilitas: perbandingan

| Metode | Cara | Kelebihan | Risiko utama |
|---|---|---|---|
| Verbalized single confidence | Model menulis satu angka untuk label terpilih | Sederhana, murah | Harus dibentuk jadi distribusi 3 kelas; sisa probabilitas tidak terukur (lihat 1.4) |
| Distribusi 3 kelas diminta langsung | Model diminta menulis tiga angka yang jumlahnya 1, format JSON tetap | Satu panggilan, menutup sisa probabilitas, cocok untuk Brier | Angka bisa tidak konsisten dengan penalaran; perlu validasi jumlah |
| Token logprob | Probabilitas token label dari API | Tidak bergantung pada pengakuan model | Tidak semua penyedia memberi logprob; bila model menulis penalaran dulu, token label tidak lagi sama dengan probabilitas keputusan; kadang tidak tersedia untuk model tertutup |
| Pengambilan sampel berulang (k kali) | Frekuensi label dari k sampel | Tidak bergantung pengakuan model; menangkap ketidakstabilan | Biaya k kali lipat; resolusi kasar (pada k=5, langkah 0,2) |

Literatur (lihat 1.5) menunjukkan confidence verbal sering terlalu yakin (overconfident) pada QA, tetapi juga dapat lebih baik daripada probabilitas kondisional pada model yang di-RLHF. Keduanya tidak boleh diasumsikan; harus diukur pada tugas kita.

Rekomendasi: primer = distribusi 3 kelas diminta langsung (satu panggilan). Sekunder = pengambilan sampel k=5 pada subset untuk uji stabilitas. Logprob hanya bila penyedia menyediakannya dan dicatat sebagai kondisi terpisah. Verbalized single confidence dipakai sebagai pembanding, bukan primer.

### 1.3 Brier multikelas: sifat dan contoh

Rumus: BS = (1/N) sum_i sum_k (p_ik - y_ik)^2, y one-hot.

Sifat yang diverifikasi dengan hitungan (skrip `agent_b_calc.py`):
- Rentang 0 sampai 2 (prediksi sempurna = 0; prediksi yakin pada kelas salah = 2).
- Baseline seragam 3 kelas, p = (1/3, 1/3, 1/3), dengan y = (1,0,0): (2/3)^2 + 2(1/3)^2 = 6/9 = 2/3 = 0,666667. Ini benar-benar angka yang dihitung skrip.
- Dekomposisi: karena BS multikelas = jumlah Brier biner per kelas k, dan Brier biner dapat diuraikan Murphy (1973) menjadi reliability - resolution + uncertainty, maka BS multikelas dapat diuraikan menjadi jumlah tiga suku per kelas. Ini turunan matematis saya, belum dicek terhadap sumber primer multikelas (TIDAK_TERVERIFIKASI sebagai sitasi). Dekomposisi dengan binning bersifat tidak aditif tepat; laporkan sebagai estimasi.

Contoh angka kecil (skrip, y = REFUTED = (0,1,0)):
- Prediksi (0,1,0) untuk y=(1,0,0): BS = 2,000.
- Satu confidence c=0,9 pada label salah, sisa dibagi rata: p=(0,9; 0,05; 0,05); BS = 1,715.
- Satu confidence c=0,9 pada label benar: p=(0,05; 0,9; 0,05); BS = 0,015.
- c=0,6 salah: BS = 1,040; c=0,6 benar: BS = 0,240.

Brier biner "jawaban terpilih benar" = (c - 1[benar])^2 untuk label terpilih saja. Untuk c=0,9 benar: 0,01; salah: 0,81. Ini TIDAK sama dengan Brier multikelas (0,015 dan 1,715) karena mengabaikan distribusi pada dua kelas lain. Jangan menyebut keduanya dengan nama yang sama.

### 1.4 Bila hanya satu confidence dilaporkan
Dari c dan label terpilih, distribusi 3 kelas harus dibentuk dengan asumsi tambahan. Aturan "sisa dibagi rata" (dipakai di skrip) memberi BS yang sangat bergantung pada asumsi itu. Risikonya: jika model sebenarnya ragu antara REFUTED dan NEI, membagi rata menyalahgambarkan sisa probabilitas. Mitigasi: (a) jadikan distribusi langsung sebagai primer; (b) bila hanya c yang tersedia, laporkan dua batas (sisa dibagi rata dan sisa semua ke kelas kedua yang tidak diketahui sehingga dibatasi) sebagai analisis sensitivitas, dan jangan membandingkan model yang memakai metode berbeda.

### 1.5 Apakah confidence verbal dapat dianggap terkalibrasi
Jawaban singkat: tidak untuk diasumsikan. Bukti yang diverifikasi:
- Xiong et al. (arXiv 2306.13063; ICLR 2024): confidence verbal cenderung terlalu yakin; metode berbasis konsistensi dan hybrid sering lebih baik; kesenjangan dengan white-box kecil (AUROC 0,522 ke 0,605 menurut ringkasan pencarian). Lihat CSV.
- Tian et al. (arXiv 2305.14975; EMNLP 2023): confidence verbal sering lebih terkalibrasi daripada probabilitas kondisional model RLHF pada TriviaQA, SciQ, TruthfulQA (ECE turun sekitar 50 persen relatif menurut ringkasan).
- Kadavath et al. (arXiv 2207.05221): kalibrasi baik pada multiple choice yang diformat baik; P(True) menjanjikan.
- Guo et al. (arXiv 1706.04599): ECE sebagai metrik; jaringan modern miskalibrasi; temperature scaling butuh set kalibrasi terpisah.
- Fact-check 2026 (search-level, belum dibaca penuh): PCC (arXiv 2601.02574) melaporkan ECE lebih rendah daripada verbal biasa; DAVinCI (arXiv 2604.21193) memakai downgrade ke NEI berdasarkan ambang.

Kesimpulan: confidence verbal adalah kandidat yang harus diuji dengan kurva kalibrasi dan Brier, bukan probabilitas terkalibrasi bawaan.

---

## 2. Ground truth dan kebocoran

- Kunci dibentuk oleh minimal dua anotator ahli independen dan satu adjudikator. Catat kesepakatan (Cohen kappa untuk dua anotator, Fleiss/Krippendorff untuk lebih). Butir dengan bukti tidak bulat dipisah sebagai stratum.
- Definisi NEI harus operasional: bukti dalam korpus tidak cukup untuk mendukung atau membantah klaim, dengan rentang pencarian yang dicatat. NEI tidak boleh berarti "anotator tidak tahu".
- Kualitas bukti tidak seragam: catat jenis sumber (abstrak, teks penuh, meta-analisis), tingkat langsung/tidak langsung, dan apakah bukti bertentangan. Ini menjadi variabel kovariat dan stratum analisis, bukan diabaikan.
- False confidence: bukti dari abstrak sering mengundang keyakinan palsu. Label ground truth harus menyebut batas bukti.
- Kebocoran kunci: kunci, rasional anotator, dan kolom kategori tidak boleh ada di prompt, nama berkas yang dibaca model, atau metadata yang dikirim. Simpan kunci di berkas terpisah yang tidak dimuat pipeline inferensi.
- Pemisahan data: pilot (mengembangkan prompt), development (memilih formula atau fitur), validation (perbandingan kondisi), final holdout (satu kali pakai). Karena 45 butir lama sudah dipakai mengembangkan prompt atau formula, 45 butir itu tidak boleh menjadi holdout; perlakukan sebagai pilot dan tandai. Korpus sekitar 20.000 artikel: holdout harus diambil berdasarkan artikel (bukan klaim) agar tidak bocor.

---

## 3. Rancangan perbandingan

| Kondisi | Isi konteks ke model | Status |
|---|---|---|
| A | Klaim + bukti + instruksi (tanpa F11x) | Baseline |
| B | A + skor F11x relevan | Intervensi: skor masuk konteks keputusan |
| C | F11x saja (tanpa bukti) | Diagnostik; hanya pada development split untuk menguji apakah skor berkorelasi dengan label |
| D | A + sinyal plasebo (angka acak dengan format, panjang, dan rentang sama dengan skor F11x) | Kontrol |

Apakah F11x itu pengukuran atau intervensi? Skor F11x adalah pengukuran di sisi kita, tetapi begitu ditulis ke prompt ia menjadi intervensi yang dapat mengubah keputusan model (anchoring, otoritas angka). Jadi B harus dibaca sebagai efek intervensi, bukan sebagai validasi skor.

Jangan mengasumsikan F11x membantu. F11x dikembangkan untuk tugas pengawasan antar-agen, dan validitasnya untuk penilaian bukti belum diketahui. Pra-registrasi arah hipotesis secara dua arah.

Ancaman validitas:
- Perancu format: skor muncul sebagai teks tambahan; kontrol D menyamakan format.
- Urutan: skor sebelum atau sesudah bukti; kontra-seimbangkan.
- Panjang prompt: samakan jumlah token; laporkan.
- Efek angka tambahan: plasebo angka acak menguji apakah angka apa pun memengaruhi model.
- Kebocoran rentang: skor F11x dan label berkorelasi melalui artikel; pakai split berbasis artikel.

Perbandingan lintas model (Qwen3.8-Max, DeepSeek, Claude Haiku, Gemini 3.8 Flash, GPT-6.1 Sol; nama dan ketersediaan belum saya verifikasi):
- Prompt tetap (satu templat untuk semua model) sebagai analisis utama; sensitivitas prompt per model sebagai analisis sekunder.
- Suhu 0 bila didukung; seed bila didukung; catat versi snapshot dan tanggal akses.
- Urutan butir diacak per run; urutan kondisi dikontra-seimbangkan dengan Latin square.
- Pengaruh provider tidak dapat dipisahkan dari model; nyatakan itu sebagai batas.

---

## 4. Rancangan analisis statistik

### 4.1 Primary outcome
Pilih SATU primary: selisih Brier multikelas berpasangan per butir antara kondisi B dan A (atau D dan A sebagai kontrol). Alasan: aturan penilaian tepat (proper scoring rule) yang memakai seluruh distribusi; tidak bergantung pada ambang NEI; sensitif terhadap kalibrasi dan diskriminasi sekaligus. Akurasi, ECE, dan reliabilitas dilaporkan sebagai sekunder dengan koreksi Holm.

### 4.2 Uji berpasangan dan ketergantungan
- Selisih Brier berpasangan per butir (butir sama di kondisi berbeda).
- Bootstrap berkluster per artikel (resampling artikel, bukan klaim) untuk interval kepercayaan 95 persen.
- Model efek campuran sebagai pilihan: acak untuk butir (klaim kembar dikelompokkan), artikel, dan model; kondisi tetap.
- Ketergantungan yang harus dimodelkan: artikel sama, klaim kembar dari satu artikel, pengulangan run, domain, bahasa.
- Koreksi perbandingan ganda: Holm untuk keluarga uji sekunder.

### 4.3 Reliabilitas
- Stabilitas antar-run: kesepakatan label antar k run (Fleiss kappa) dan standar deviasi Brier antar run.
- Konsistensi antar-model: Krippendorff alpha (nominal) untuk label.
- Disagreement antar-butir: proporsi butir dengan label tidak bulat.
- Kalibrasi per kategori bukti: kurva reliability dan ECE per stratum (dengan jumlah butir yang dilaporkan, karena ECE tidak stabil pada sel kecil).

KR-20 dan Cronbach alpha tidak sesuai: butir tidak homogen, labelnya nominal, dan ini tidak mengukur satu konstruk laten. Rasch dan CFA membutuhkan banyak butir (ratusan) dan model unidimensional; dengan 45 butir keduanya tidak layak dan tidak akan stabil.

### 4.4 Kelayakan ukuran sampel
Asumsi eksplisit: alpha 0,05 dua sisi; daya 0,80; SD selisih Brier per butir sigma = 0,35 (ASUMSI, belum diukur; wajib diestimasi dari pilot); desain paired.

Rumus: n = ((z_a/2 + z_b) * sigma / delta)^2 (hasil skrip, DEFF = 1).

| delta (selisih Brier) | n butir (DEFF=1) |
|---|---|
| 0,10 | 97 |
| 0,05 | 385 |
| 0,02 | 2404 |

Simulasi power (800 ulangan, z-test, skrip): n=100 -> power 0,32; n=200 -> 0,53; n=400 -> 0,83 (delta 0,05, sigma 0,35). Konsisten dengan rumus (385 untuk 0,80).

Efek klaster: DEFF = 1 + (m - 1) * ICC. Dengan m = 3 butir per artikel dan ICC = 0,2 (ASUMSI): DEFF = 1,40, n(delta 0,05) = 539 butir. Dengan ICC 0,3: DEFF 1,60, n = 616.

Daya instrumen lama (45 butir), delta 0,05, sigma 0,35, dengan rumus pendekatan: sekitar 0,16. Jadi 45 butir tidak cukup untuk mendeteksi efek kecil; cukup hanya untuk pilot dan estimasi sigma.

Tiga skala:
- Minimal (pilot): mendeteksi delta 0,10; ~97 butir, dengan DEFF 1,4 sekitar 136 butir; sekitar 32 sampai 45 artikel independen bila rata-rata 3 butir per artikel (97 atau 136 butir). Tujuan: estimasi sigma dan ICC, bukan konklusi.
- Standard: delta 0,05; 385 butir DEFF 1 atau 539 butir DEFF 1,4 (sekitar 180 artikel independen dengan m=3). Empat kondisi (A, B, C, D) dan dua model tidak termasuk dalam angka ini; hitung ulang per model.
- Extended (kondisi bukti bertentangan, pembaruan keputusan, robustness): delta 0,03 dengan DEFF 1,6 membutuhkan sekitar 1.710 butir (1068 x 1,6, dihitung dengan rumus; tidak disimulasikan).

Asumsi yang menentukan semua angka ini adalah sigma. Bila sigma sebenarnya 0,25, n Standard turun menjadi 197 (DEFF 1); bila 0,35 (dipakai), 385.

---

## 5. Estimasi kebutuhan API (tanpa harga)

Rumus:
- panggilan = butir x kondisi x model x pengulangan (+ panggilan ulang untuk gagal parse)
- token masuk per panggilan = token instruksi + token klaim + token bukti (+ skor F11x pada B dan D)
- token keluar = token JSON distribusi + penalaran bila diminta
- biaya = sum(token masuk x harga_masuk + token keluar x harga_keluar); harga per model: unknown (belum diverifikasi; tidak ada harga yang saya tulis)

Contoh Standard (asumsi): 539 butir x 4 kondisi x 5 model x 3 pengulangan = 32.340 panggilan. Dengan kontrol C hanya pada development split, tambahkan sekitar ratusan panggilan. Token per panggilan belum diukur; perlu pilot 20 butir untuk estimasi.

---

## 6. Risiko validitas, reliabilitas, dan penanganan kegagalan

- Keluaran tidak valid (JSON rusak, jumlah distribusi tidak 1): aturan: coba ulang sekali dengan input sama; bila gagal lagi, catat sebagai parse failure dan laporkan jumlahnya per model. Untuk Brier, laporkan dua batas: butir gagal dikeluarkan, dan butir gagal diberi BS maksimum (2) sebagai batas bawah kinerja.
- Normalisasi: jumlah 1 +- 0,01 diterima; selain itu dinormalisasi dan diberi bendera.
- Rate limit: backoff eksponensial, batas kuota harian tercatat, tidak ada paralel melebihi kuota.
- Model tidak tersedia atau snapshot berubah: ganti dengan pra-deklarasi, catat tanggal dan versi; jangan campur snapshot dalam satu perbandingan.
- Kebocoran kunci lewat metadata: uji otomatis bahwa kolom kunci tidak ada di berkas input.
- Kontrol kualitas: audit 5 persen butir secara manual; cek sebaran label per kondisi.
- Reproduksibilitas: simpan seed, versi model, hash prompt, tanggal, kode commit, dan semua keluaran mentah (JSONL) sebelum agregasi.

---

## 7. Tiga judul independen dan pendapat atas kandidat

Judul saya:
1. Calibrated Three-Way Evidence Judgment: A Replicable Brier-Based Protocol for Evaluating LLMs on Academic Claims (fokus metode, aman untuk fase riset).
2. Does a Non-Validated Signal Change LLM Evidence Verdicts? A Placebo-Controlled Test of an External Score (menempatkan F11x sebagai intervensi yang diuji).
3. Holdout-Governed Evaluation of Probability Judgments on Academic Evidence: Brier Decomposition, Ground-Truth Integrity, and Cross-Model Stability.

Pendapat atas kandidat:
- (1) When Evidence Disagrees: Evaluating LLM Evidence Judgment, Confidence Calibration, and Response to Counterevidence. Baik dan luas, tetapi tiga klaim sekaligus (judgment, calibration, respons terhadap kontra-bukti) berarti tiga primary, bertentangan dengan rencana satu primary. Layak bila kontra-bukti dijadikan satu kondisi saja. Versi lebih kuat: judul ini menjadi studi lanjutan setelah metode 1 tervalidasi.
- (2) Does External Evidence Verification Improve LLM Calibration? A Controlled Comparison With and Without F11x. Judulnya sudah mengandung kesimpulan ("improve"), dan menyebut "external evidence verification" padahal F11x belum tervalidasi untuk tugas ini. Saya tidak menyarankan judul ini; ganti dengan judul berbentuk pertanyaan netral seperti judul 2 saya.
- (3) Knowing When Evidence Is Insufficient: A Cross-Model Evaluation of Academic Evidence Judgment and Confidence. Paling sesuai dengan NEI dan lintas model, tetapi "knowing when" mengklaim kemampuan introspektif yang belum diuji; ganti "knowing" dengan "whether" atau tambahkan kriteria NEI operasional. Secara keseluruhan judul 3 paling kuat secara ilmiah bila klaim dibatasi.

---

## 8. Daftar yang tidak sempat diverifikasi

- Murphy (1973): hanya deskripsi sekunder; bentuk multikelas tidak dikonfirmasi dari sumber primer. TIDAK_TERVERIFIKASI.
- Naeini et al. (2015): hanya disebut oleh Guo et al. TIDAK_TERVERIFIKASI.
- DAVinCI (arXiv 2604.21193), PCC (arXiv 2601.02574), RRC (arXiv 2601.16555), "Scaling Truth" (arXiv 2509.08803), dan 2411.13343: hanya daftar pencarian, belum dibuka penuh. Angka ECE dari PCC tidak saya verifikasi.
- Angka FEVER (31,87 persen dan 50,91 persen): dari ringkasan pencarian, belum dicek di PDF.
- Angka Tian et al. (pengurangan ECE sekitar 50 persen) dan Xiong et al. (AUROC 0,522 ke 0,605): dari ringkasan pencarian.
- Harga API semua penyedia: unknown.
- Keberadaan dan nama snapshot model kandidat (Qwen3.8-Max, GPT-6.1 Sol, Gemini 3.8 Flash, versi DeepSeek): tidak diverifikasi.
- Jumlah dan daftar 20.000 artikel korpus dan 45 butir: belum diperiksa (tidak membaca folder kerja).

## 9. Pernyataan jujur tentang model yang saya gunakan

Saya (Agent B) berjalan sebagai Claude Haiku 5.5 (claude-haiku-5-5). Pekerjaan ini hanya memakai pencarian web, pembukaan ringkasan pencarian, dan Python stdlib untuk hitungan matematika. Saya tidak menjalankan, memanggil, atau menguji model kandidat mana pun, dan tidak menghitung hasil eksperimen apa pun. Angka pada Bagian 1.3 dan 4.4 adalah hitungan matematika dengan asumsi yang dinyatakan, bukan hasil model.
