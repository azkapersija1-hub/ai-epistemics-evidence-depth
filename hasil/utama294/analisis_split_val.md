# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set SPLIT-val: split val

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set SPLIT-val (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0520 | 0.0520 | 0.0520 [0.0044; 0.1134] | 0.9694 | 0.0291 | 0.0016 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.0668 | 0.0668 | 0.0668 [0.0115; 0.1403] | 0.9694 | 0.0290 | 0.0139 | 0.9694 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.1523 | 0.1523 | 0.1523 [0.0696; 0.2528] | 0.9082 | 0.0388 | 0.0322 | 0.9082 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0194 | 0.0194 | 0.0194 [0.0024; 0.0522] | 0.9898 | 0.0151 | 0.0006 | 0.9898 | 1.0000 | 98 |
| far | R3 | anchor | 97 | 1 | 0.0696 | 0.0893 | 0.0696 [0.0133; 0.1445] | 0.9588 | 0.0196 | 0.0053 | 0.9588 | 1.0000 | 97 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.5306 [0.4388; 0.6327] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.4660 [0.3847; 0.5482] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.4382 [0.3594; 0.5185] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0102 [0.0000; 0.0306] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0708 [0.0413; 0.1072] | 0.0327 [0.0176; 0.0560] | 0.0382 [0.0022; 0.0791] |
| R3 | 0.1229 [0.0769; 0.1780] | 0.0536 [0.0203; 0.0942] | 0.0692 [0.0238; 0.1192] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 36 | 0.5833 | 0.0278 | -0.0108 | 0.0174 |
| en | 48 | 0.5208 | 0.0000 | 0.0877 | 0.1006 |
| unk | 14 | 0.4286 | 0.0000 | -0.0057 | 0.0914 |

## Model: qwen4-max-preview | set SPLIT-val (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0394 | 0.0394 | 0.0394 [0.0097; 0.0813] | 0.9796 | 0.0528 | 0.0013 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.1401 | 0.1401 | 0.1401 [0.0719; 0.2199] | 0.9082 | 0.0542 | 0.0218 | 0.9082 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.2075 | 0.2075 | 0.2075 [0.1205; 0.3127] | 0.8673 | 0.0227 | 0.0876 | 0.8673 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0334 | 0.0334 | 0.0334 [0.0092; 0.0693] | 0.9796 | 0.0492 | 0.0011 | 0.9796 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1313 | 0.1313 | 0.1313 [0.0658; 0.2123] | 0.9082 | 0.0359 | 0.0179 | 0.9082 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.5204 [0.4184; 0.6224] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.4362 [0.3634; 0.5089] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.4085 [0.3408; 0.4777] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1547 [0.1140; 0.2023] | 0.0735 [0.0537; 0.0978] | 0.0812 [0.0387; 0.1283] |
| R3 | 0.1959 [0.1487; 0.2522] | 0.1381 [0.1000; 0.1842] | 0.0579 [0.0248; 0.0972] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 36 | 0.5833 | 0.0000 | 0.0425 | 0.0278 |
| en | 48 | 0.5000 | 0.0000 | 0.1029 | 0.0665 |
| unk | 14 | 0.4286 | 0.0000 | 0.1064 | 0.1057 |

## Model: deepseek-v4.1-flash | set SPLIT-val (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 8; gagal setelah ulang (dicatat): 3

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 96 | 2 | 0.1373 | 0.1753 | 0.1373 [0.0562; 0.2321] | 0.9167 | 0.0350 | 0.0186 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.0537 | 0.0537 | 0.0537 [0.0025; 0.1186] | 0.9694 | 0.0098 | 0.0078 | 0.9694 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.0742 | 0.0742 | 0.0742 [0.0178; 0.1530] | 0.9592 | 0.0087 | 0.0120 | 0.9592 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0015 | 0.0015 | 0.0015 [0.0007; 0.0027] | 1.0000 | 0.0132 | 0.0000 | 1.0000 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.0528 | 0.0528 | 0.0528 [0.0006; 0.1223] | 0.9694 | 0.0198 | 0.0012 | 0.9694 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 96 | 0.5312 [0.4375; 0.6250] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 96 | 0.4127 [0.3292; 0.5002] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 96 | 0.3983 [0.3164; 0.4823] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 96 | 0.0104 [0.0000; 0.0312] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0516 [0.0239; 0.0864] | 0.0132 [0.0081; 0.0194] | 0.0385 [0.0102; 0.0735] |
| R3 | 0.0671 [0.0356; 0.1096] | 0.0366 [0.0085; 0.0733] | 0.0305 [0.0023; 0.0635] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.5588 | 0.0000 | 0.0047 | 0.0172 |
| en | 48 | 0.5625 | 0.0208 | 0.0767 | 0.0419 |
| unk | 14 | 0.3571 | 0.0000 | -0.0057 | 0.0257 |
