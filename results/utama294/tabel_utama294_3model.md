# Utama-294: analisis utama praregistrasi (3 model API)

Status: HASIL MODEL (BELUM DIVERIFIKASI). Hanya sah bila sesuai praregistrasi.

Pilot adalah tahap teknis menurut praregistrasi dan tidak dilaporkan sebagai hasil. Baris UTAMA-294 memasukkannya sesuai permintaan; UTAMA-274 adalah baris tanpa pilot.

Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed default]. Brier batas 2 tanpa CI. Tau = 0,7. HASIL MODEL, BELUM DIVERIFIKASI.

## UTAMA-294: semua 294 klaim (pilot+dev+val+holdout)

n klaim = 294, n observasi = 2058

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier batas 1 own R3 (anchor SUPPORTED) | 0.0322 [0.0112; 0.0579] | 0.0222 [0.0092; 0.0381] | 0.0919 [0.0547; 0.1340] |
| Brier batas 1 near R1 (anchor NEI) | 0.0537 [0.0273; 0.0841] | 0.1121 [0.0786; 0.1492] | 0.0339 [0.0098; 0.0625] |
| Brier batas 1 near R3 (anchor NEI) | 0.1466 [0.0977; 0.2013] | 0.2312 [0.1753; 0.2932] | 0.0749 [0.0361; 0.1164] |
| Brier batas 1 far R1 (anchor NEI) | 0.0259 [0.0082; 0.0505] | 0.0482 [0.0263; 0.0746] | 0.0134 [0.0011; 0.0318] |
| Brier batas 1 far R3 (anchor NEI) | 0.0871 [0.0505; 0.1307] | 0.1455 [0.1010; 0.1938] | 0.0712 [0.0355; 0.1144] |
| Brier batas 2 own R3 (gagal = 2,0) | 0.0322 | 0.0222 | 0.1308 |
| Brier batas 2 near R1 (gagal = 2,0) | 0.0537 | 0.1121 | 0.0339 |
| Brier batas 2 near R3 (gagal = 2,0) | 0.1466 | 0.2312 | 0.0749 |
| Brier batas 2 far R1 (gagal = 2,0) | 0.0259 | 0.0482 | 0.0134 |
| Brier batas 2 far R3 (gagal = 2,0) | 0.0936 | 0.1455 | 0.0712 |
| Sesuai (label R1 = label R3) | 0.5034 [0.4456; 0.5612] | 0.5306 [0.4728; 0.5850] | 0.4896 [0.4340; 0.5486] |
| Pergeseran dS | 0.4788 [0.4316; 0.5263] | 0.4226 [0.3798; 0.4656] | 0.4282 [0.3747; 0.4773] |
| Pergeseran dN | 0.4525 [0.4068; 0.4974] | 0.3897 [0.3490; 0.4311] | 0.4102 [0.3574; 0.4575] |
| Overkomit (tau 0,7) | 0.0068 [0.0000; 0.0170] | 0.0068 [0.0000; 0.0170] | 0.0208 [0.0069; 0.0382] |
| False-support near R1 | 0.0718 [0.0551; 0.0907] | 0.1473 [0.1261; 0.1696] | 0.0446 [0.0312; 0.0599] |
| False-support far R1 | 0.0347 [0.0235; 0.0489] | 0.0834 [0.0689; 0.1005] | 0.0201 [0.0124; 0.0295] |
| Selisih FS near-far R1 | 0.0371 [0.0210; 0.0546] | 0.0639 [0.0433; 0.0837] | 0.0245 [0.0089; 0.0414] |
| False-support near R3 | 0.1270 [0.0998; 0.1580] | 0.2198 [0.1890; 0.2523] | 0.0689 [0.0479; 0.0908] |
| False-support far R3 | 0.0707 [0.0503; 0.0952] | 0.1487 [0.1230; 0.1765] | 0.0499 [0.0304; 0.0731] |
| Selisih FS near-far R3 | 0.0563 [0.0262; 0.0853] | 0.0711 [0.0464; 0.0953] | 0.0190 [-0.0040; 0.0407] |

## UTAMA-274: 274 klaim tanpa pilot (dev+val+holdout)

n klaim = 274, n observasi = 1918

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier batas 1 own R3 (anchor SUPPORTED) | 0.0343 [0.0120; 0.0613] | 0.0235 [0.0103; 0.0408] | 0.0981 [0.0584; 0.1436] |
| Brier batas 1 near R1 (anchor NEI) | 0.0517 [0.0250; 0.0867] | 0.1036 [0.0689; 0.1412] | 0.0352 [0.0098; 0.0671] |
| Brier batas 1 near R3 (anchor NEI) | 0.1441 [0.0937; 0.1985] | 0.2191 [0.1627; 0.2775] | 0.0622 [0.0275; 0.1041] |
| Brier batas 1 far R1 (anchor NEI) | 0.0276 [0.0085; 0.0534] | 0.0512 [0.0280; 0.0778] | 0.0143 [0.0011; 0.0356] |
| Brier batas 1 far R3 (anchor NEI) | 0.0934 [0.0542; 0.1399] | 0.1502 [0.1017; 0.2011] | 0.0764 [0.0392; 0.1197] |
| Brier batas 2 own R3 (gagal = 2,0) | 0.0343 | 0.0235 | 0.1397 |
| Brier batas 2 near R1 (gagal = 2,0) | 0.0517 | 0.1036 | 0.0352 |
| Brier batas 2 near R3 (gagal = 2,0) | 0.1441 | 0.2191 | 0.0622 |
| Brier batas 2 far R1 (gagal = 2,0) | 0.0276 | 0.0512 | 0.0143 |
| Brier batas 2 far R3 (gagal = 2,0) | 0.1004 | 0.1502 | 0.0764 |
| Sesuai (label R1 = label R3) | 0.5146 [0.4562; 0.5730] | 0.5511 [0.4927; 0.6095] | 0.5000 [0.4440; 0.5597] |
| Pergeseran dS | 0.4683 [0.4210; 0.5173] | 0.4090 [0.3648; 0.4547] | 0.4162 [0.3643; 0.4682] |
| Pergeseran dN | 0.4439 [0.3961; 0.4925] | 0.3781 [0.3361; 0.4225] | 0.4007 [0.3505; 0.4508] |
| Overkomit (tau 0,7) | 0.0073 [0.0000; 0.0182] | 0.0073 [0.0000; 0.0182] | 0.0187 [0.0037; 0.0373] |
| False-support near R1 | 0.0691 [0.0525; 0.0885] | 0.1404 [0.1188; 0.1641] | 0.0437 [0.0302; 0.0604] |
| False-support far R1 | 0.0357 [0.0237; 0.0511] | 0.0855 [0.0695; 0.1034] | 0.0203 [0.0122; 0.0323] |
| Selisih FS near-far R1 | 0.0334 [0.0173; 0.0508] | 0.0549 [0.0338; 0.0757] | 0.0235 [0.0053; 0.0418] |
| False-support near R3 | 0.1233 [0.0957; 0.1537] | 0.2116 [0.1800; 0.2437] | 0.0614 [0.0424; 0.0831] |
| False-support far R3 | 0.0750 [0.0522; 0.1023] | 0.1485 [0.1212; 0.1783] | 0.0528 [0.0324; 0.0766] |
| Selisih FS near-far R3 | 0.0483 [0.0190; 0.0790] | 0.0631 [0.0389; 0.0879] | 0.0086 [-0.0133; 0.0275] |

