# 4. Hasil

## 4.1 Hasil utama 274 klaim non-pilot

Set pelaporan utama adalah 274 klaim non-pilot (dev 78, val 98, holdout 98) dengan tujuh presentasi bukti per klaim, yaitu 1.918 observasi per model. Tiga model API dianalisis: qwen3.8-flash, qwen4-max-preview, dan deepseek-v4.1-flash. Set 294 klaim yang mencakup 20 pilot disajikan sebagai analisis tambahan (Lampiran D, Tabel D1b). Penetapan set pelaporan 274 dilakukan setelah pengumpulan data dan dicatat terpisah dari protokol awal, yang melalui Amandemen 5 semula menetapkan 294 klaim sebagai analisis utama (docs/prareg/CATATAN_DEVIASI.md). Tabel 2 memuat metrik terpilih. Nilai lengkap ada di Lampiran D (Tabel D1).

**Tabel 2.** Hasil utama 274 klaim non-pilot per model: nilai [CI 95 persen]. Brier batas 1; angka n ditulis bila kurang dari 274 (deepseek-v4.1-flash: 8 gagal parse final, sehingga 268 klaim dapat dievaluasi untuk konsistensi R1 sampai R3 dan Brier own R3; qwen3.8-flash far R3: 273 observasi).

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier own R3 (SUPPORTED) | 0,0343 [0,0120; 0,0613] | 0,0235 [0,0103; 0,0408] | 0,0981 [0,0584; 0,1436] (n=268) |
| Brier near R3 (NEI) | 0,1441 [0,0937; 0,1985] | 0,2191 [0,1627; 0,2775] | 0,0622 [0,0275; 0,1041] |
| Brier far R3 (NEI) | 0,0934 [0,0542; 0,1399] (n=273) | 0,1502 [0,1017; 0,2011] | 0,0764 [0,0392; 0,1197] |
| Sesuai (R1 = R3) | 0,5146 [0,4562; 0,5730] | 0,5511 [0,4927; 0,6095] | 0,5000 [0,4440; 0,5597] (n=268) |
| Overkomit (tau 0,7) | 0,0073 [0,0000; 0,0182] | 0,0073 [0,0000; 0,0182] | 0,0187 [0,0037; 0,0373] (n=268) |
| False-support near R3 | 0,1233 [0,0957; 0,1537] | 0,2116 [0,1800; 0,2437] | 0,0614 [0,0424; 0,0831] |
| False-support far R3 | 0,0750 [0,0522; 0,1023] (n=273) | 0,1485 [0,1212; 0,1783] | 0,0528 [0,0324; 0,0766] |
| Selisih FS near-far R1 | 0,0334 [0,0173; 0,0508] | 0,0549 [0,0338; 0,0757] | 0,0235 [0,0053; 0,0418] |
| Selisih FS near-far R3 | 0,0483 [0,0190; 0,0790] | 0,0631 [0,0389; 0,0879] | 0,0086 [-0,0133; 0,0275] |

**Pengamatan.** Brier own R3 terkecil ada pada qwen4-max-preview (0,0235) dan terbesar pada deepseek-v4.1-flash (0,0981). Brier near R3 tertinggi ada pada qwen4-max-preview (0,2191). Pada R1, selisih false-support near dan far positif pada ketiga model dan intervalnya tidak mencakup nol. Pada R3, selisih positif tanpa mencakup nol hanya tampak pada qwen3.8-flash dan qwen4-max-preview; interval deepseek-v4.1-flash mencakup nol (Lampiran D, Tabel D1). Interval Sesuai ketiga model saling tumpang tindih. Nilai pada set 294 (analisis tambahan) berbeda paling banyak 0,0205 dari nilai pada set 274 (CATATAN_DEVIASI.md, D3).

Brier gabungan (rerata berbobot n dari lima baris Brier batas 1: own R3, near R1, near R3, far R1, far R3) tidak dilaporkan untuk set 274 karena tidak tersedia pada tabel hasil set itu. Nilai pada set 294 (analisis tambahan) adalah 0,0691 (qwen3.8-flash), 0,1119 (qwen4-max-preview), dan 0,0569 (deepseek-v4.1-flash), tanpa interval bootstrap gabungan, sehingga ini deviasi dari rencana dan tidak dapat dibandingkan langsung dengan interval per jenis bukti.

**Tafsiran.** Arah false-support near lebih tinggi daripada far tampak pada R1 di ketiga model, dan pada R3 di dua model qwen. Selisih antar model belum diuji secara formal: tidak ada uji signifikansi berpasangan antarmodel, dan interval kesesuaian R1 dan R3 tumpang tindih antarmodel. Pasangan near dan far belum divalidasi secara independen (Bagian 5.3). Jangkar bersifat mekanis dan sementara (own R3 SUPPORTED; near dan far NEI; tidak ada jangkar REFUTED). Hasil tidak membuktikan bahwa bukti yang lebih banyak memperbaiki ketepatan faktual.

Tabel D6 di Lampiran D memuat akurasi, ECE, dan AURC per jenis bukti pada set 294 (analisis tambahan; tidak ada padanan 274 pada tabel hasil). Pada seluruh sel, ECE berada pada rentang 0,0071 sampai 0,0460 dan akurasi pada rentang 0,8537 sampai 0,9932. Pada observasi NEI, akurasi sama dengan recall NEI.

**Gambar 1.** Panel ringkas set 294 klaim (analisis tambahan, termasuk 20 pilot) pada tiga model API. Interval kepercayaan 95 persen dari bootstrap klaster per artikel. Gambar ini bukan set pelaporan utama 274.

![Gambar 1](figures_294/H5_panel_ringkas_utama294_id.png)

## 4.2 Hasil per split

Pilot tidak dilaporkan sebagai hasil. Pada dev, val, dan holdout, false-support near R3 menunjukkan urutan yang sama: qwen4-max-preview (0,2164; 0,1959; 0,2235), lalu qwen3.8-flash (0,1082; 0,1229; 0,1357), lalu deepseek-v4.1-flash (0,0460; 0,0671; 0,0680). Brier own R3 deepseek-v4.1-flash juga paling besar di ketiga split (0,0791; 0,1373; 0,0739). Ini pengamatan dari tiga model dan tidak menunjukkan keunggulan model tertentu (Lampiran D, Tabel D2).

## 4.3 Kepekaan

Kepekaan dihitung pada himpunan bersarang dari set 294 (analisis tambahan), sehingga angka berikut bukan angka set 274 dan tidak punya padanan 274 pada tabel kepekaan. Himpunan itu tumpang tindih dan bukan replikasi independen. Pada seluruh metrik tabel kepekaan, nilai titik tanpa butir berstatus KELUAR (290 klaim) berubah paling banyak 0,0073 (kesesuaian qwen4-max-preview), dan pada set yang lebih ketat (280 klaim) paling banyak 0,0185 (pergeseran dN deepseek-v4.1-flash). Proporsi Sesuai naik dari set 294 ke set ketat pada ketiga model, yaitu qwen3.8-flash dari 0,5034 menjadi 0,5179, qwen4-max-preview dari 0,5306 menjadi 0,5464, dan deepseek-v4.1-flash dari 0,4896 menjadi 0,5073. Kenaikan ini hanya nilai titik karena set-set itu bersarang. Subset tervalidasi tim (36 klaim) memberi Sesuai 0,4286 sampai 0,5556 dan tidak diperlakukan sebagai hasil utama (Lampiran D, Tabel D3).

## 4.4 Pembanding jalur agen

GPT-6.1 Sol (tidak terverifikasi) diuji pada 40 klaim, 39 klaim efektif karena C0230 gagal pada seluruh 7 observasinya, dan tidak masuk set pelaporan utama. Pada subset 40 klaim, false-support near R3 (0,0156) dan far R3 (0,0080) GPT-6.1 Sol (tidak terverifikasi) lebih rendah daripada ketiga model API (Lampiran D, Tabel D4). Angka ini nilai titik tanpa interval, cakupan klaimnya berbeda, dan jalurnya belum terverifikasi, sehingga tidak dibaca sebagai perbandingan model.

## 4.5 Kestabilan uji ulang

Uji ulang 19 klaim (133 observasi per model) menghasilkan persen argmax yang sama sebesar 89,5 persen untuk qwen3.8-flash, 94,7 persen untuk qwen4-max-preview, dan 93,9 persen untuk deepseek-v4.1-flash pada pasangan valid (92,5 persen bila gagal parse dihitung sebagai beda). Pada R2 qwen3.8-flash, persen yang sama hanya 78,9 persen dari 19 observasi. GPT-6.1 Sol (tidak terverifikasi) pada sesi terpisah mencatat 99,2 persen (Lampiran D, Tabel D5). Argmax relatif stabil antar putaran. Angka ini mengukur konsistensi, bukan ketepatan vonis.

## 4.6 Kekokohan

Interval kepercayaan lebar, dan jumlah klaster artikel tetap menjadi batas kekokohan. Selisih antar model belum diuji secara formal, sehingga temuan bersifat deskriptif. Suhu dan mode berpikir tidak dapat diatur dari harness, sehingga hasil hanya berlaku untuk setelan default penyedia.
