# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash (ulangan 1)
- Jumlah observasi: 252; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 36 | 0 | 0.0765 | 0.0765 | 0.0765 [0.0004; 0.1985] | 0.9444 | 0.0384 | 0.0032 | - | 0.0000 | 0 |
| near | R1 | anchor | 36 | 0 | 0.0589 | 0.0589 | 0.0589 [0.0048; 0.1524] | 0.9722 | 0.0536 | 0.0041 | 0.9722 | 1.0000 | 36 |
| near | R3 | anchor | 36 | 0 | 0.1388 | 0.1388 | 0.1388 [0.0209; 0.2866] | 0.9167 | 0.0881 | 0.0260 | 0.9167 | 1.0000 | 36 |
| far | R1 | anchor | 36 | 0 | 0.0541 | 0.0541 | 0.0541 [0.0018; 0.1551] | 0.9722 | 0.0128 | 0.0050 | 0.9722 | 1.0000 | 36 |
| far | R3 | anchor | 36 | 0 | 0.0900 | 0.0900 | 0.0900 [0.0053; 0.2112] | 0.9444 | 0.0533 | 0.0057 | 0.9444 | 1.0000 | 36 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 36 | 0.5278 [0.3611; 0.6944] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 36 | 0.4689 [0.3396; 0.6075] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 36 | 0.4443 [0.3182; 0.5809] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 36 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0711 [0.0286; 0.1308] | 0.0508 [0.0153; 0.1075] | 0.0203 [-0.0072; 0.0511] |
| R3 | 0.1336 [0.0650; 0.2153] | 0.0814 [0.0242; 0.1511] | 0.0522 [-0.0344; 0.1411] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | 0.0038 | -0.0063 |
| en | 14 | 0.5000 | 0.0000 | 0.0336 | 0.0771 |
| unk | 6 | 0.5000 | 0.0000 | 0.0333 | 0.1500 |

## Model: qwen4-max-preview (ulangan 1)
- Jumlah observasi: 252; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 36 | 0 | 0.0083 | 0.0083 | 0.0083 [0.0029; 0.0151] | 1.0000 | 0.0500 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 36 | 0 | 0.0696 | 0.0696 | 0.0696 [0.0174; 0.1565] | 0.9722 | 0.0736 | 0.0089 | 0.9722 | 1.0000 | 36 |
| near | R3 | anchor | 36 | 0 | 0.1725 | 0.1725 | 0.1725 [0.0755; 0.2937] | 0.8889 | 0.1425 | 0.0471 | 0.8889 | 1.0000 | 36 |
| far | R1 | anchor | 36 | 0 | 0.0773 | 0.0773 | 0.0773 [0.0143; 0.1539] | 0.9167 | 0.0956 | 0.0056 | 0.9167 | 1.0000 | 36 |
| far | R3 | anchor | 36 | 0 | 0.2630 | 0.2630 | 0.2630 [0.1088; 0.4386] | 0.8333 | 0.0981 | 0.0515 | 0.8333 | 1.0000 | 36 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 36 | 0.5556 [0.3889; 0.7222] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 36 | 0.4119 [0.2899; 0.5447] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 36 | 0.3749 [0.2595; 0.4975] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 36 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1217 [0.0808; 0.1736] | 0.1100 [0.0603; 0.1694] | 0.0117 [-0.0283; 0.0467] |
| R3 | 0.2122 [0.1475; 0.2842] | 0.2200 [0.1308; 0.3200] | -0.0078 [-0.0744; 0.0539] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.6250 | 0.0000 | -0.0175 | -0.0562 |
| en | 14 | 0.5000 | 0.0000 | 0.0536 | 0.0629 |
| unk | 6 | 0.5000 | 0.0000 | -0.0083 | -0.0433 |

## Model: deepseek-v4.1-flash (ulangan 1)
- Jumlah observasi: 252; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 3; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 35 | 1 | 0.1225 | 0.1746 | 0.1225 [0.0072; 0.2675] | 0.9143 | 0.0763 | 0.0068 | - | 0.0000 | 0 |
| near | R1 | anchor | 36 | 0 | 0.0035 | 0.0035 | 0.0035 [0.0012; 0.0075] | 1.0000 | 0.0289 | 0.0000 | 1.0000 | 1.0000 | 36 |
| near | R3 | anchor | 36 | 0 | 0.0076 | 0.0076 | 0.0076 [0.0025; 0.0150] | 1.0000 | 0.0394 | 0.0000 | 1.0000 | 1.0000 | 36 |
| far | R1 | anchor | 36 | 0 | 0.0994 | 0.0994 | 0.0994 [0.0004; 0.2519] | 0.9444 | 0.0417 | 0.0049 | 0.9444 | 1.0000 | 36 |
| far | R3 | anchor | 36 | 0 | 0.0898 | 0.0898 | 0.0898 [0.0007; 0.2274] | 0.9444 | 0.0381 | 0.0032 | 0.9444 | 1.0000 | 36 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 35 | 0.4286 [0.2571; 0.6000] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 35 | 0.4449 [0.2923; 0.5977] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 35 | 0.4359 [0.2847; 0.5870] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 35 | 0.0286 [0.0000; 0.0857] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0289 [0.0183; 0.0417] | 0.0631 [0.0089; 0.1408] | -0.0342 [-0.1117; 0.0217] |
| R3 | 0.0394 [0.0228; 0.0592] | 0.0611 [0.0083; 0.1375] | -0.0217 [-0.0942; 0.0317] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | -0.1075 | -0.0906 |
| en | 13 | 0.3846 | 0.0000 | 0.0307 | 0.0321 |
| unk | 6 | 0.1667 | 0.1667 | 0.0100 | 0.0367 |

## Model: codex (gpt-6.1-sol, tak terverifikasi) (ulangan 1)
- Jumlah observasi: 252; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 7; gagal setelah ulang (dicatat): 7

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 35 | 1 | 0.0339 | 0.0885 | 0.0339 [0.0003; 0.0988] | 0.9714 | 0.0322 | 0.0008 | - | - | 0 |
| near | R1 | anchor | 35 | 1 | 0.0009 | 0.0564 | 0.0009 [0.0001; 0.0026] | 1.0000 | 0.0092 | 0.0000 | 1.0000 | 1.0000 | 35 |
| near | R3 | anchor | 35 | 1 | 0.0048 | 0.0602 | 0.0048 [0.0001; 0.0139] | 1.0000 | 0.0160 | 0.0000 | 1.0000 | 1.0000 | 35 |
| far | R1 | anchor | 35 | 1 | 0.0005 | 0.0561 | 0.0005 [0.0000; 0.0014] | 1.0000 | 0.0056 | 0.0000 | 1.0000 | 1.0000 | 35 |
| far | R3 | anchor | 35 | 1 | 0.0011 | 0.0567 | 0.0011 [0.0000; 0.0031] | 1.0000 | 0.0086 | 0.0000 | 1.0000 | 1.0000 | 35 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 35 | 0.5143 [0.3429; 0.6857] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 35 | 0.4301 [0.2909; 0.5639] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 35 | 0.4385 [0.2993; 0.5706] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 35 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0092 [0.0043; 0.0175] | 0.0056 [0.0022; 0.0110] | 0.0036 [-0.0032; 0.0127] |
| R3 | 0.0160 [0.0055; 0.0343] | 0.0086 [0.0028; 0.0170] | 0.0074 [-0.0056; 0.0273] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 16 | 0.5625 | 0.0000 | -0.0042 | -0.0079 |
| en | 13 | 0.4615 | 0.0000 | 0.0141 | 0.0268 |
| unk | 6 | 0.5000 | 0.0000 | 0.0018 | 0.0065 |
