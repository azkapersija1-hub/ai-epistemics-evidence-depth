# Lampiran D. Tabel hasil lengkap

Set pelaporan utama adalah 274 klaim non-pilot (Tabel D1); set 294 klaim adalah analisis tambahan. Tabel D3 dan D6 memakai set 294 (analisis tambahan) karena tidak punya padanan 274 pada tabel hasil. Angka berasal dari berkas CSV pada `HASIL_PENGUJIAN\_utama294`, `HASIL_PENGUJIAN\_lapis36`, dan `HASIL_PENGUJIAN\_retest_lapis19`. Desimal memakai koma. Nilai ditulis dengan empat desimal, pembulatan setengah ke atas. Interval kepercayaan 95 persen adalah bootstrap klaster per artikel (B=2000).

**Tabel D1.** Set pelaporan utama: 274 klaim non-pilot (dev 78, val 98, holdout 98; 1.918 observasi per model), per model: nilai [CI 95 persen]. Angka n ditulis bila kurang dari 274 (deepseek-v4.1-flash: 268 klaim dievaluasi untuk konsistensi R1 sampai R3 dan Brier own R3; qwen3.8-flash far R3: 273 observasi). Sumber: baris UTAMA-274 pada `results/utama294/tabel_utama294_3model.csv`.

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier batas 1 own R3 (SUPPORTED) | 0,0343 [0,0120; 0,0613] | 0,0235 [0,0103; 0,0408] | 0,0981 [0,0584; 0,1436] (n=268) |
| Brier batas 1 near R1 (NEI) | 0,0517 [0,0250; 0,0867] | 0,1036 [0,0689; 0,1412] | 0,0352 [0,0098; 0,0671] |
| Brier batas 1 near R3 (NEI) | 0,1441 [0,0937; 0,1985] | 0,2191 [0,1627; 0,2775] | 0,0622 [0,0275; 0,1041] |
| Brier batas 1 far R1 (NEI) | 0,0276 [0,0085; 0,0534] | 0,0512 [0,0280; 0,0778] | 0,0143 [0,0011; 0,0356] |
| Brier batas 1 far R3 (NEI) | 0,0934 [0,0542; 0,1399] (n=273) | 0,1502 [0,1017; 0,2011] | 0,0764 [0,0392; 0,1197] |
| Sesuai (label R1 = label R3) | 0,5146 [0,4562; 0,5730] | 0,5511 [0,4927; 0,6095] | 0,5000 [0,4440; 0,5597] (n=268) |
| Pergeseran dS | 0,4683 [0,4210; 0,5173] | 0,4090 [0,3648; 0,4547] | 0,4162 [0,3643; 0,4682] (n=268) |
| Pergeseran dN | 0,4439 [0,3961; 0,4925] | 0,3781 [0,3361; 0,4225] | 0,4007 [0,3505; 0,4508] (n=268) |
| Overkomit (tau 0,7) | 0,0073 [0,0000; 0,0182] | 0,0073 [0,0000; 0,0182] | 0,0187 [0,0037; 0,0373] (n=268) |
| False-support near R1 | 0,0691 [0,0525; 0,0885] | 0,1404 [0,1188; 0,1641] | 0,0437 [0,0302; 0,0604] |
| False-support far R1 | 0,0357 [0,0237; 0,0511] | 0,0855 [0,0695; 0,1034] | 0,0203 [0,0122; 0,0323] |
| Selisih FS near-far R1 | 0,0334 [0,0173; 0,0508] | 0,0549 [0,0338; 0,0757] | 0,0235 [0,0053; 0,0418] |
| False-support near R3 | 0,1233 [0,0957; 0,1537] | 0,2116 [0,1800; 0,2437] | 0,0614 [0,0424; 0,0831] |
| False-support far R3 | 0,0750 [0,0522; 0,1023] (n=273) | 0,1485 [0,1212; 0,1783] | 0,0528 [0,0324; 0,0766] |
| Selisih FS near-far R3 | 0,0483 [0,0190; 0,0790] | 0,0631 [0,0389; 0,0879] | 0,0086 [-0,0133; 0,0275] |

**Tabel D1b.** Set 294 klaim, termasuk 20 pilot (analisis tambahan, bukan set pelaporan utama), per model: nilai [CI 95 persen]. Angka n ditulis bila kurang dari 294.

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier batas 1 own R3 (SUPPORTED) | 0,0322 [0,0112; 0,0579] | 0,0222 [0,0092; 0,0381] | 0,0919 [0,0547; 0,1340] (n=288) |
| Brier batas 1 near R1 (NEI) | 0,0537 [0,0273; 0,0841] | 0,1121 [0,0786; 0,1492] | 0,0339 [0,0098; 0,0625] |
| Brier batas 1 near R3 (NEI) | 0,1466 [0,0977; 0,2013] | 0,2312 [0,1753; 0,2932] | 0,0749 [0,0361; 0,1164] |
| Brier batas 1 far R1 (NEI) | 0,0259 [0,0082; 0,0505] | 0,0482 [0,0263; 0,0746] | 0,0134 [0,0011; 0,0318] |
| Brier batas 1 far R3 (NEI) | 0,0871 [0,0505; 0,1307] (n=293) | 0,1455 [0,1010; 0,1938] | 0,0712 [0,0355; 0,1144] |
| Sesuai (label R1 = label R3) | 0,5034 [0,4456; 0,5612] | 0,5306 [0,4728; 0,5850] | 0,4896 [0,4340; 0,5486] (n=288) |
| Pergeseran dS | 0,4788 [0,4316; 0,5263] | 0,4226 [0,3798; 0,4656] | 0,4282 [0,3747; 0,4773] (n=288) |
| Pergeseran dN | 0,4525 [0,4068; 0,4974] | 0,3897 [0,3490; 0,4311] | 0,4102 [0,3574; 0,4575] (n=288) |
| Overkomit (tau 0,7) | 0,0068 [0,0000; 0,0170] | 0,0068 [0,0000; 0,0170] | 0,0208 [0,0069; 0,0382] (n=288) |
| False-support near R1 | 0,0718 [0,0551; 0,0907] | 0,1473 [0,1261; 0,1696] | 0,0446 [0,0312; 0,0599] |
| False-support far R1 | 0,0347 [0,0235; 0,0489] | 0,0834 [0,0689; 0,1005] | 0,0201 [0,0124; 0,0295] |
| Selisih FS near-far R1 | 0,0371 [0,0210; 0,0546] | 0,0639 [0,0433; 0,0837] | 0,0245 [0,0089; 0,0414] |
| False-support near R3 | 0,1270 [0,0998; 0,1580] | 0,2198 [0,1890; 0,2523] | 0,0689 [0,0479; 0,0908] |
| False-support far R3 | 0,0707 [0,0503; 0,0952] (n=293) | 0,1487 [0,1230; 0,1765] | 0,0499 [0,0304; 0,0731] |
| Selisih FS near-far R3 | 0,0563 [0,0262; 0,0853] | 0,0711 [0,0464; 0,0953] | 0,0190 [-0,0040; 0,0407] |

**Tabel D2.** Hasil per split (nilai titik tanpa interval; pilot tidak dilaporkan sebagai hasil). Untuk deepseek-v4.1-flash, n adalah 76 pada dev dan 96 pada val dan holdout, karena ada observasi gagal parse.

| Split (klaim) | Model | Brier own R3 | Brier near R3 | Brier far R3 | Sesuai | FS near R3 | FS far R3 |
|---|---|---|---|---|---|---|---|
| dev (78) | qwen3.8-flash | 0,0366 | 0,1211 | 0,0449 | 0,5256 | 0,1082 | 0,0518 |
| dev (78) | qwen4-max-preview | 0,0062 | 0,2064 | 0,1729 | 0,5769 | 0,2164 | 0,1637 |
| dev (78) | deepseek-v4.1-flash | 0,0791 | 0,0305 | 0,0643 | 0,4868 | 0,0460 | 0,0474 |
| val (98) | qwen3.8-flash | 0,0520 | 0,1523 | 0,0696 | 0,5306 | 0,1229 | 0,0536 |
| val (98) | qwen4-max-preview | 0,0394 | 0,2075 | 0,1313 | 0,5204 | 0,1959 | 0,1381 |
| val (98) | deepseek-v4.1-flash | 0,1373 | 0,0742 | 0,0528 | 0,5313 | 0,0671 | 0,0366 |
| holdout (98) | qwen3.8-flash | 0,0149 | 0,1542 | 0,1556 | 0,4898 | 0,1357 | 0,1147 |
| holdout (98) | qwen4-max-preview | 0,0212 | 0,2409 | 0,1511 | 0,5612 | 0,2235 | 0,1469 |
| holdout (98) | deepseek-v4.1-flash | 0,0739 | 0,0755 | 0,1097 | 0,4792 | 0,0680 | 0,0733 |

**Tabel D3.** Kepekaan pada himpunan bersarang dari set 294 (analisis tambahan; bukan set 274): nilai [CI 95 persen]. Himpunan tumpang tindih, bukan replikasi independen. Subset tervalidasi tim adalah 36 klaim tanpa holdout; set kepekaan bersarang sehingga tidak diuji secara statistik.

| Set | Model | Sesuai | Brier own R3 | FS near R3 |
|---|---|---|---|---|
| Set 294 (analisis tambahan) (294) | qwen3.8-flash | 0,5034 [0,4456; 0,5612] | 0,0322 [0,0112; 0,0579] | 0,1270 [0,0998; 0,1580] |
| Set 294 (analisis tambahan) (294) | qwen4-max-preview | 0,5306 [0,4728; 0,5850] | 0,0222 [0,0092; 0,0381] | 0,2198 [0,1890; 0,2523] |
| Set 294 (analisis tambahan) (294) | deepseek-v4.1-flash | 0,4896 [0,4340; 0,5486] | 0,0919 [0,0547; 0,1340] | 0,0689 [0,0479; 0,0908] |
| KEPEKAAN-A (290) | qwen3.8-flash | 0,5103 [0,4517; 0,5655] | 0,0326 [0,0118; 0,0595] | 0,1284 [0,1015; 0,1562] |
| KEPEKAAN-A (290) | qwen4-max-preview | 0,5379 [0,4828; 0,5931] | 0,0223 [0,0098; 0,0386] | 0,2212 [0,1895; 0,2522] |
| KEPEKAAN-A (290) | deepseek-v4.1-flash | 0,4965 [0,4331; 0,5528] | 0,0931 [0,0552; 0,1371] | 0,0696 [0,0496; 0,0925] |
| KEPEKAAN-B (280) | qwen3.8-flash | 0,5179 [0,4607; 0,5786] | 0,0276 [0,0086; 0,0527] | 0,1294 [0,0993; 0,1594] |
| KEPEKAAN-B (280) | qwen4-max-preview | 0,5464 [0,4857; 0,6071] | 0,0228 [0,0093; 0,0399] | 0,2215 [0,1896; 0,2548] |
| KEPEKAAN-B (280) | deepseek-v4.1-flash | 0,5073 [0,4489; 0,5657] | 0,0908 [0,0526; 0,1328] | 0,0713 [0,0501; 0,0953] |
| Subset tervalidasi tim (36) | qwen3.8-flash | 0,5278 [0,3611; 0,6944] | 0,0765 [0,0004; 0,1985] | 0,1336 [0,0650; 0,2153] |
| Subset tervalidasi tim (36) | qwen4-max-preview | 0,5556 [0,3889; 0,7222] | 0,0083 [0,0029; 0,0151] | 0,2122 [0,1475; 0,2842] |
| Subset tervalidasi tim (36) | deepseek-v4.1-flash | 0,4286 [0,2571; 0,6000] | 0,1225 [0,0072; 0,2675] | 0,0394 [0,0228; 0,0592] |

**Tabel D4.** Pembanding pada subset 40 klaim (nilai titik dari tabel pembanding lapis 40; CI tidak tersedia untuk lapis 40). GPT-6.1 Sol (tidak terverifikasi) adalah jalur agen dan tidak terverifikasi; diuji pada 40 klaim, 39 klaim efektif karena C0230 gagal pada seluruh 7 observasinya. Angka n: qwen3.8-flash dan qwen4-max-preview 40 pada semua metrik. deepseek-v4.1-flash 39 pada Brier own R3, Sesuai, pergeseran, dan overkomit (satu observasi gagal parse), dan 40 pada metrik near dan far. GPT-6.1 Sol (tidak terverifikasi) 39 pada semua metrik.

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash | GPT-6.1 Sol (tidak terverifikasi) |
|---|---|---|---|---|
| Brier own R3 (SUPPORTED) | 0,0689 | 0,0086 | 0,1110 | 0,0305 |
| Brier near R3 (NEI) | 0,1253 | 0,1593 | 0,0069 | 0,0044 |
| Brier far R3 (NEI) | 0,0813 | 0,2401 | 0,0809 | 0,0010 |
| Sesuai (label R1 = label R3) | 0,4750 | 0,5000 | 0,3846 | 0,4615 |
| Overkomit (tau 0,7) | 0,0000 | 0,0000 | 0,0256 | 0,0000 |
| False-support near R3 | 0,1228 | 0,2028 | 0,0373 | 0,0156 |
| False-support far R3 | 0,0760 | 0,2095 | 0,0560 | 0,0080 |

**Tabel D5.** Kestabilan uji ulang 19 klaim lapis 19 (dalam persen; rerata absolut selisih p(SUPPORTED) dalam desimal). GPT-6.1 Sol (tidak terverifikasi) diuji pada sesi terpisah dan belum terverifikasi. Interval Codex: semua 99,2 persen [97,7; 100,0]; R1 98,2 persen [94,7; 100,0].

| Model | Tingkat | n observasi | Argmax sama (%) | Argmax sama, gagal = beda (%) | Rerata abs selisih p(SUPPORTED) |
|---|---|---|---|---|---|
| qwen3.8-flash | R1 | 57 | 93,0 | 93,0 | 0,0449 |
| qwen3.8-flash | R2 | 19 | 78,9 | 78,9 | 0,0932 |
| qwen3.8-flash | R3 | 57 | 89,5 | 89,5 | 0,0302 |
| qwen3.8-flash | Semua | 133 | 89,5 | 89,5 | 0,0455 |
| qwen4-max-preview | R1 | 57 | 94,7 | 94,7 | 0,0218 |
| qwen4-max-preview | R2 | 19 | 94,7 | 94,7 | 0,0297 |
| qwen4-max-preview | R3 | 57 | 94,7 | 94,7 | 0,0115 |
| qwen4-max-preview | Semua | 133 | 94,7 | 94,7 | 0,0185 |
| deepseek-v4.1-flash | R1 | 57 | 94,7 | 94,7 | 0,0321 |
| deepseek-v4.1-flash | R2 | 19 | 94,7 | 94,7 | 0,0468 |
| deepseek-v4.1-flash | R3 | 55 pasangan valid dari 57 | 92,7 | 89,5 | 0,0207 |
| deepseek-v4.1-flash | Semua | 131 pasangan valid dari 133 | 93,9 | 92,5 | 0,0295 |
| GPT-6.1 Sol (tidak terverifikasi) | R1 | 57 | 98,2 | - | 0,0223 |
| GPT-6.1 Sol (tidak terverifikasi) | R2 | 19 | 100,0 | - | 0,0210 |
| GPT-6.1 Sol (tidak terverifikasi) | R3 | 57 | 100,0 | - | 0,0043 |
| GPT-6.1 Sol (tidak terverifikasi) | Semua | 133 | 99,2 | - | 0,0144 |

**Tabel D6.** Akurasi, ECE, dan AURC per jenis bukti pada set 294 klaim (analisis tambahan; tidak ada padanan 274), per model (sumber: analisis_UTAMA294.md, bagian A). Akurasi pada observasi NEI sama dengan recall NEI. Brier batas 1 tidak diulang di sini (lihat Tabel D1 dan D1b).

| Model | Jenis bukti | n | Akurasi | ECE | AURC |
|---|---|---|---|---|---|
| qwen3.8-flash | own R3 (SUPPORTED) | 294 | 0,9796 | 0,0171 | 0,0007 |
| qwen3.8-flash | near R1 (NEI) | 294 | 0,9762 | 0,0292 | 0,0080 |
| qwen3.8-flash | near R3 (NEI) | 294 | 0,9150 | 0,0284 | 0,0293 |
| qwen3.8-flash | far R1 (NEI) | 294 | 0,9864 | 0,0116 | 0,0012 |
| qwen3.8-flash | far R3 (NEI) | 293 | 0,9454 | 0,0226 | 0,0111 |
| qwen4-max-preview | own R3 (SUPPORTED) | 294 | 0,9898 | 0,0437 | 0,0003 |
| qwen4-max-preview | near R1 (NEI) | 294 | 0,9286 | 0,0416 | 0,0151 |
| qwen4-max-preview | near R3 (NEI) | 294 | 0,8537 | 0,0286 | 0,0757 |
| qwen4-max-preview | far R1 (NEI) | 294 | 0,9660 | 0,0460 | 0,0020 |
| qwen4-max-preview | far R3 (NEI) | 294 | 0,9082 | 0,0097 | 0,0276 |
| deepseek-v4.1-flash | own R3 (SUPPORTED) | 288 | 0,9444 | 0,0241 | 0,0083 |
| deepseek-v4.1-flash | near R1 (NEI) | 294 | 0,9830 | 0,0128 | 0,0085 |
| deepseek-v4.1-flash | near R3 (NEI) | 294 | 0,9592 | 0,0071 | 0,0139 |
| deepseek-v4.1-flash | far R1 (NEI) | 294 | 0,9932 | 0,0073 | 0,0007 |
| deepseek-v4.1-flash | far R3 (NEI) | 294 | 0,9592 | 0,0277 | 0,0035 |
