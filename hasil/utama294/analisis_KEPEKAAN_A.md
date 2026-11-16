# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set KEPEKAAN-A: 294 dikurangi 4 JANGKAR KELUAR (Amandemen 6a)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set KEPEKAAN-A (ulangan 1)
- Jumlah observasi: 2030; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 290 | 0 | 0.0326 | 0.0326 | 0.0326 [0.0118; 0.0595] | 0.9793 | 0.0169 | 0.0007 | - | 0.0000 | 0 |
| near | R1 | anchor | 290 | 0 | 0.0539 | 0.0539 | 0.0539 [0.0269; 0.0860] | 0.9759 | 0.0284 | 0.0080 | 0.9759 | 1.0000 | 290 |
| near | R3 | anchor | 290 | 0 | 0.1485 | 0.1485 | 0.1485 [0.1003; 0.2013] | 0.9138 | 0.0292 | 0.0300 | 0.9138 | 1.0000 | 290 |
| far | R1 | anchor | 290 | 0 | 0.0263 | 0.0263 | 0.0263 [0.0085; 0.0500] | 0.9862 | 0.0117 | 0.0012 | 0.9862 | 1.0000 | 290 |
| far | R3 | anchor | 289 | 1 | 0.0883 | 0.0949 | 0.0883 [0.0507; 0.1335] | 0.9446 | 0.0233 | 0.0112 | 0.9446 | 1.0000 | 289 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 290 | 0.5103 [0.4517; 0.5655] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 290 | 0.4727 [0.4257; 0.5185] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 290 | 0.4463 [0.3989; 0.4908] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 290 | 0.0069 [0.0000; 0.0172] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0717 [0.0553; 0.0903] | 0.0351 [0.0239; 0.0490] | 0.0366 [0.0212; 0.0538] |
| R3 | 0.1284 [0.1015; 0.1562] | 0.0713 [0.0493; 0.0967] | 0.0571 [0.0258; 0.0874] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 100 | 0.5900 | 0.0200 | 0.0098 | 0.0212 |
| en | 153 | 0.4837 | 0.0000 | 0.0544 | 0.0682 |
| unk | 37 | 0.4054 | 0.0000 | 0.0351 | 0.1070 |

## Model: qwen4-max-preview | set KEPEKAAN-A (ulangan 1)
- Jumlah observasi: 2030; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 290 | 0 | 0.0223 | 0.0223 | 0.0223 [0.0098; 0.0386] | 0.9897 | 0.0434 | 0.0003 | - | 0.0000 | 0 |
| near | R1 | anchor | 290 | 0 | 0.1136 | 0.1136 | 0.1136 [0.0805; 0.1530] | 0.9276 | 0.0412 | 0.0154 | 0.9276 | 1.0000 | 290 |
| near | R3 | anchor | 290 | 0 | 0.2339 | 0.2339 | 0.2339 [0.1792; 0.2895] | 0.8517 | 0.0307 | 0.0768 | 0.8517 | 1.0000 | 290 |
| far | R1 | anchor | 290 | 0 | 0.0488 | 0.0488 | 0.0488 [0.0274; 0.0744] | 0.9655 | 0.0459 | 0.0021 | 0.9655 | 1.0000 | 290 |
| far | R3 | anchor | 290 | 0 | 0.1471 | 0.1471 | 0.1471 [0.1044; 0.1969] | 0.9069 | 0.0099 | 0.0278 | 0.9069 | 1.0000 | 290 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 290 | 0.5379 [0.4828; 0.5931] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 290 | 0.4164 [0.3751; 0.4573] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 290 | 0.3838 [0.3431; 0.4220] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 290 | 0.0069 [0.0000; 0.0172] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1484 [0.1273; 0.1709] | 0.0839 [0.0692; 0.1009] | 0.0645 [0.0438; 0.0846] |
| R3 | 0.2212 [0.1895; 0.2522] | 0.1491 [0.1237; 0.1771] | 0.0720 [0.0484; 0.0960] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 100 | 0.6200 | 0.0100 | 0.0286 | 0.0220 |
| en | 153 | 0.5163 | 0.0065 | 0.0842 | 0.1020 |
| unk | 37 | 0.4054 | 0.0000 | 0.0800 | 0.0832 |

## Model: deepseek-v4.1-flash | set KEPEKAAN-A (ulangan 1)
- Jumlah observasi: 2030; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 20; gagal setelah ulang (dicatat): 8

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 284 | 6 | 0.0931 | 0.1325 | 0.0931 [0.0551; 0.1371] | 0.9437 | 0.0246 | 0.0084 | - | 0.0000 | 0 |
| near | R1 | anchor | 290 | 0 | 0.0343 | 0.0343 | 0.0343 [0.0103; 0.0657] | 0.9828 | 0.0126 | 0.0086 | 0.9828 | 1.0000 | 290 |
| near | R3 | anchor | 290 | 0 | 0.0759 | 0.0759 | 0.0759 [0.0384; 0.1191] | 0.9586 | 0.0074 | 0.0141 | 0.9586 | 1.0000 | 290 |
| far | R1 | anchor | 290 | 0 | 0.0136 | 0.0136 | 0.0136 [0.0011; 0.0324] | 0.9931 | 0.0072 | 0.0007 | 0.9931 | 1.0000 | 290 |
| far | R3 | anchor | 290 | 0 | 0.0722 | 0.0722 | 0.0722 [0.0361; 0.1158] | 0.9586 | 0.0282 | 0.0036 | 0.9586 | 1.0000 | 290 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 284 | 0.4965 [0.4331; 0.5528] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 284 | 0.4212 [0.3687; 0.4747] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 284 | 0.4030 [0.3521; 0.4552] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 284 | 0.0211 [0.0070; 0.0387] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0448 [0.0320; 0.0612] | 0.0202 [0.0123; 0.0300] | 0.0247 [0.0085; 0.0421] |
| R3 | 0.0696 [0.0496; 0.0925] | 0.0504 [0.0308; 0.0743] | 0.0191 [-0.0030; 0.0417] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 97 | 0.5876 | 0.0206 | -0.0029 | 0.0024 |
| en | 150 | 0.4800 | 0.0200 | 0.0471 | 0.0271 |
| unk | 37 | 0.3243 | 0.0270 | 0.0065 | 0.0316 |
