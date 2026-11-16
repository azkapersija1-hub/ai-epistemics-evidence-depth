# 4. Hasil

## 4.1 Hasil utama 294 klaim

Analisis utama memakai 294 klaim dengan 2058 observasi per model, mencakup pilot, dev, val, dan holdout. Tiga model API dianalisis: qwen3.8-flash, qwen4-max-preview, dan deepseek-v4.1-flash. Tabel 2 memuat tujuh metrik terpilih dan Brier gabungan. Nilai lengkap ada di Lampiran D (Tabel D1).

**Tabel 2.** Hasil utama 294 klaim per model: nilai [CI 95 persen]. Brier batas 1; angka n ditulis bila kurang dari 294.

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier own R3 (SUPPORTED) | 0,0322 [0,0112; 0,0579] | 0,0222 [0,0092; 0,0381] | 0,0919 [0,0547; 0,1340] (n=288) |
| Brier near R3 (NEI) | 0,1466 [0,0977; 0,2013] | 0,2312 [0,1753; 0,2932] | 0,0749 [0,0361; 0,1164] |
| Brier far R3 (NEI) | 0,0871 [0,0505; 0,1307] (n=293) | 0,1455 [0,1010; 0,1938] | 0,0712 [0,0355; 0,1144] |
| Sesuai (R1 = R3) | 0,5034 [0,4456; 0,5612] | 0,5306 [0,4728; 0,5850] | 0,4896 [0,4340; 0,5486] (n=288) |
| Overkomit (tau 0,7) | 0,0068 [0,0000; 0,0170] | 0,0068 [0,0000; 0,0170] | 0,0208 [0,0069; 0,0382] (n=288) |
| False-support near R3 | 0,1270 [0,0998; 0,1580] | 0,2198 [0,1890; 0,2523] | 0,0689 [0,0479; 0,0908] |
| False-support far R3 | 0,0707 [0,0503; 0,0952] (n=293) | 0,1487 [0,1230; 0,1765] | 0,0499 [0,0304; 0,0731] |
| Brier gabungan (rerata berbobot n lima jenis bukti, tanpa CI) | 0,0691 | 0,1119 | 0,0569 |

**Pengamatan.** Brier own R3 terkecil ada pada qwen4-max-preview (0,0222) dan terbesar pada deepseek-v4.1-flash (0,0919). Brier near R3 tertinggi ada pada qwen4-max-preview (0,2312). Pada R1, selisih false-support near dan far positif pada ketiga model dan intervalnya tidak mencakup nol. Pada R3, selisih positif tanpa mencakup nol hanya tampak pada qwen3.8-flash dan qwen4-max-preview; interval deepseek-v4.1-flash mencakup nol (Lampiran D, Tabel D1). Interval Sesuai ketiga model saling tumpang tindih. Tanpa pilot (274 klaim), nilai berubah paling banyak 0,0205.

Brier gabungan adalah rerata berbobot n dari lima baris Brier batas 1 (own R3, near R1, near R3, far R1, far R3) per model. Nilai ini dipakai sebagai pengganti metrik primer tunggal yang tidak tersedia di berkas CSV. Interval bootstrap untuk nilai gabungan belum dihitung, sehingga ini deviasi dari rencana dan tidak dapat dibandingkan langsung dengan interval per jenis bukti.

**Tafsiran.** Arah false-support near lebih tinggi daripada far tampak pada R1 di ketiga model, dan pada R3 di dua model qwen. Selisih antar model belum diuji secara formal, dan pasangan near dan far belum divalidasi secara independen (Bagian 5.3).

Tabel D6 di Lampiran D memuat akurasi, ECE, dan AURC per jenis bukti. Pada seluruh sel, ECE berada pada rentang 0,0071 sampai 0,0460 dan akurasi pada rentang 0,8537 sampai 0,9932. Pada observasi NEI, akurasi sama dengan recall NEI.

**Gambar 1.** Panel ringkas hasil utama 294 klaim pada tiga model API. Interval kepercayaan 95 persen dari bootstrap klaster per artikel.

![Gambar 1](figures_294/H5_panel_ringkas_utama294_id.png)

## 4.2 Hasil per split

Pilot tidak dilaporkan sebagai hasil. Pada dev, val, dan holdout, false-support near R3 menunjukkan urutan yang sama: qwen4-max-preview (0,2164; 0,1959; 0,2235), lalu qwen3.8-flash (0,1082; 0,1229; 0,1357), lalu deepseek-v4.1-flash (0,0460; 0,0671; 0,0680). Brier own R3 deepseek-v4.1-flash juga paling besar di ketiga split (0,0791; 0,1373; 0,0739). Ini pengamatan dari tiga model dan tidak menunjukkan keunggulan model tertentu (Lampiran D, Tabel D2).

## 4.3 Kepekaan

Pada seluruh metrik tabel kepekaan, nilai titik tanpa butir berstatus KELUAR (290 klaim) berubah paling banyak 0,0073 (kesesuaian qwen4-max-preview), dan pada set yang lebih ketat (280 klaim) paling banyak 0,0185 (pergeseran dN deepseek-v4.1-flash). Proporsi Sesuai naik dari 294 ke set ketat pada ketiga model, yaitu qwen3.8-flash dari 0,5034 menjadi 0,5179, qwen4-max-preview dari 0,5306 menjadi 0,5464, dan deepseek-v4.1-flash dari 0,4896 menjadi 0,5073. Kenaikan ini hanya nilai titik karena set-set itu bersarang. Subset tervalidasi tim (36 klaim) memberi Sesuai 0,4286 sampai 0,5556 dan tidak diperlakukan sebagai hasil utama (Lampiran D, Tabel D3).

## 4.4 Pembanding jalur agen

GPT-6.1 Sol (tidak terverifikasi) diuji pada 40 klaim, 39 klaim efektif karena C0230 gagal pada seluruh 7 observasinya, dan tidak masuk analisis utama. Pada subset 40 klaim, false-support near R3 (0,0156) dan far R3 (0,0080) GPT-6.1 Sol (tidak terverifikasi) lebih rendah daripada ketiga model API (Lampiran D, Tabel D4). Angka ini nilai titik tanpa interval, cakupan klaimnya berbeda, dan jalurnya belum terverifikasi, sehingga tidak dibaca sebagai perbandingan model.

## 4.5 Kestabilan uji ulang

Uji ulang 19 klaim (133 observasi per model) menghasilkan persen argmax yang sama sebesar 89,5 persen untuk qwen3.8-flash, 94,7 persen untuk qwen4-max-preview, dan 93,9 persen untuk deepseek-v4.1-flash pada pasangan valid (92,5 persen bila gagal parse dihitung sebagai beda). Pada R2 qwen3.8-flash, persen yang sama hanya 78,9 persen dari 19 observasi. GPT-6.1 Sol (tidak terverifikasi) pada sesi terpisah mencatat 99,2 persen (Lampiran D, Tabel D5). Argmax relatif stabil antar putaran. Angka ini mengukur konsistensi, bukan ketepatan vonis.

## 4.6 Kekokohan

Interval kepercayaan lebar, dan jumlah klaster artikel tetap menjadi batas kekokohan. Selisih antar model belum diuji secara formal, sehingga temuan bersifat deskriptif. Suhu dan mode berpikir tidak dapat diatur dari harness, sehingga hasil hanya berlaku untuk setelan default penyedia.
