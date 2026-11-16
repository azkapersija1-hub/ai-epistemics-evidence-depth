# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set KEPEKAAN-B: 294 dikurangi 14 JANGKAR dengan suara TIDAK_LAYAK (Amandemen 6b)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set KEPEKAAN-B (ulangan 1)
- Jumlah observasi: 1960; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 280 | 0 | 0.0276 | 0.0276 | 0.0276 [0.0086; 0.0527] | 0.9821 | 0.0204 | 0.0005 | - | 0.0000 | 0 |
| near | R1 | anchor | 280 | 0 | 0.0556 | 0.0556 | 0.0556 [0.0287; 0.0868] | 0.9750 | 0.0281 | 0.0084 | 0.9750 | 1.0000 | 280 |
| near | R3 | anchor | 280 | 0 | 0.1525 | 0.1525 | 0.1525 [0.1011; 0.2063] | 0.9107 | 0.0309 | 0.0305 | 0.9107 | 1.0000 | 280 |
| far | R1 | anchor | 280 | 0 | 0.0271 | 0.0271 | 0.0271 [0.0083; 0.0520] | 0.9857 | 0.0110 | 0.0012 | 0.9857 | 1.0000 | 280 |
| far | R3 | anchor | 279 | 1 | 0.0911 | 0.0980 | 0.0911 [0.0517; 0.1350] | 0.9427 | 0.0257 | 0.0116 | 0.9427 | 1.0000 | 279 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 280 | 0.5179 [0.4607; 0.5786] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 280 | 0.4661 [0.4181; 0.5136] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 280 | 0.4397 [0.3934; 0.4857] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 280 | 0.0071 [0.0000; 0.0179] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0729 [0.0556; 0.0916] | 0.0353 [0.0232; 0.0495] | 0.0376 [0.0207; 0.0555] |
| R3 | 0.1294 [0.0993; 0.1594] | 0.0723 [0.0491; 0.0970] | 0.0571 [0.0273; 0.0886] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 98 | 0.6020 | 0.0204 | 0.0095 | 0.0183 |
| en | 146 | 0.4863 | 0.0000 | 0.0573 | 0.0699 |
| unk | 36 | 0.4167 | 0.0000 | 0.0342 | 0.1100 |

## Model: qwen4-max-preview | set KEPEKAAN-B (ulangan 1)
- Jumlah observasi: 1960; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 280 | 0 | 0.0228 | 0.0228 | 0.0228 [0.0093; 0.0399] | 0.9893 | 0.0432 | 0.0004 | - | 0.0000 | 0 |
| near | R1 | anchor | 280 | 0 | 0.1166 | 0.1166 | 0.1166 [0.0821; 0.1557] | 0.9250 | 0.0387 | 0.0160 | 0.9250 | 1.0000 | 280 |
| near | R3 | anchor | 280 | 0 | 0.2375 | 0.2375 | 0.2375 [0.1804; 0.2971] | 0.8500 | 0.0347 | 0.0774 | 0.8500 | 1.0000 | 280 |
| far | R1 | anchor | 280 | 0 | 0.0480 | 0.0480 | 0.0480 [0.0257; 0.0740] | 0.9679 | 0.0435 | 0.0021 | 0.9679 | 1.0000 | 280 |
| far | R3 | anchor | 280 | 0 | 0.1443 | 0.1443 | 0.1443 [0.0990; 0.1910] | 0.9071 | 0.0094 | 0.0271 | 0.9071 | 1.0000 | 280 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 280 | 0.5464 [0.4857; 0.6071] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 280 | 0.4074 [0.3631; 0.4526] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 280 | 0.3749 [0.3340; 0.4162] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 280 | 0.0071 [0.0000; 0.0179] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1497 [0.1277; 0.1734] | 0.0827 [0.0676; 0.0988] | 0.0671 [0.0461; 0.0898] |
| R3 | 0.2215 [0.1896; 0.2548] | 0.1458 [0.1189; 0.1731] | 0.0757 [0.0504; 0.1015] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 98 | 0.6327 | 0.0102 | 0.0321 | 0.0236 |
| en | 146 | 0.5205 | 0.0068 | 0.0867 | 0.1071 |
| unk | 36 | 0.4167 | 0.0000 | 0.0825 | 0.0908 |

## Model: deepseek-v4.1-flash | set KEPEKAAN-B (ulangan 1)
- Jumlah observasi: 1960; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 20; gagal setelah ulang (dicatat): 8

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 274 | 6 | 0.0908 | 0.1317 | 0.0908 [0.0526; 0.1328] | 0.9453 | 0.0216 | 0.0086 | - | 0.0000 | 0 |
| near | R1 | anchor | 280 | 0 | 0.0355 | 0.0355 | 0.0355 [0.0104; 0.0647] | 0.9821 | 0.0119 | 0.0088 | 0.9821 | 1.0000 | 280 |
| near | R3 | anchor | 280 | 0 | 0.0785 | 0.0785 | 0.0785 [0.0380; 0.1237] | 0.9571 | 0.0084 | 0.0148 | 0.9571 | 1.0000 | 280 |
| far | R1 | anchor | 280 | 0 | 0.0083 | 0.0083 | 0.0083 [0.0010; 0.0224] | 0.9964 | 0.0104 | 0.0006 | 0.9964 | 1.0000 | 280 |
| far | R3 | anchor | 280 | 0 | 0.0685 | 0.0685 | 0.0685 [0.0327; 0.1088] | 0.9607 | 0.0264 | 0.0035 | 0.9607 | 1.0000 | 280 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 274 | 0.5073 [0.4489; 0.5657] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 274 | 0.4101 [0.3565; 0.4635] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 274 | 0.3917 [0.3396; 0.4457] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 274 | 0.0219 [0.0073; 0.0401] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0453 [0.0317; 0.0612] | 0.0174 [0.0115; 0.0259] | 0.0279 [0.0123; 0.0451] |
| R3 | 0.0713 [0.0501; 0.0953] | 0.0484 [0.0288; 0.0706] | 0.0229 [0.0002; 0.0452] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 95 | 0.6000 | 0.0211 | 0.0054 | 0.0111 |
| en | 143 | 0.4895 | 0.0210 | 0.0482 | 0.0281 |
| unk | 36 | 0.3333 | 0.0278 | 0.0067 | 0.0339 |
