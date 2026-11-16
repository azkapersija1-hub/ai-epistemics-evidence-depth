# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set SPLIT-holdout: split holdout

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set SPLIT-holdout (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0149 | 0.0149 | 0.0149 [0.0016; 0.0402] | 0.9898 | 0.0303 | 0.0001 | - | - | 0 |
| near | R1 | anchor | 98 | 0 | 0.0539 | 0.0539 | 0.0539 [0.0147; 0.1088] | 0.9796 | 0.0422 | 0.0071 | 0.9796 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.1542 | 0.1542 | 0.1542 [0.0751; 0.2443] | 0.9082 | 0.0453 | 0.0319 | 0.9082 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0365 | 0.0365 | 0.0365 [0.0019; 0.0896] | 0.9796 | 0.0166 | 0.0014 | 0.9796 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1556 | 0.1556 | 0.1556 [0.0756; 0.2529] | 0.8980 | 0.0577 | 0.0318 | 0.8980 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.4898 [0.3980; 0.5918] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.4798 [0.4000; 0.5567] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.4557 [0.3767; 0.5314] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0102 [0.0000; 0.0306] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0790 [0.0526; 0.1120] | 0.0389 [0.0177; 0.0701] | 0.0401 [0.0163; 0.0664] |
| R3 | 0.1357 [0.0915; 0.1871] | 0.1147 [0.0682; 0.1691] | 0.0210 [-0.0369; 0.0750] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.5882 | 0.0294 | 0.0288 | 0.0009 |
| en | 53 | 0.4528 | 0.0000 | 0.0438 | 0.0425 |
| unk | 11 | 0.3636 | 0.0000 | 0.0573 | -0.0200 |

## Model: qwen4-max-preview | set SPLIT-holdout (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 1; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0212 | 0.0212 | 0.0212 [0.0063; 0.0464] | 0.9898 | 0.0461 | 0.0002 | - | - | 0 |
| near | R1 | anchor | 98 | 0 | 0.0962 | 0.0962 | 0.0962 [0.0472; 0.1560] | 0.9286 | 0.0709 | 0.0100 | 0.9286 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.2409 | 0.2409 | 0.2409 [0.1478; 0.3516] | 0.8571 | 0.0493 | 0.0701 | 0.8571 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0618 | 0.0618 | 0.0618 [0.0194; 0.1215] | 0.9592 | 0.0410 | 0.0042 | 0.9592 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1511 | 0.1511 | 0.1511 [0.0750; 0.2456] | 0.9082 | 0.0365 | 0.0468 | 0.9082 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.5612 [0.4694; 0.6531] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.3889 [0.3164; 0.4611] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.3533 [0.2847; 0.4203] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0102 [0.0000; 0.0306] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1447 [0.1115; 0.1838] | 0.0919 [0.0642; 0.1262] | 0.0528 [0.0230; 0.0849] |
| R3 | 0.2235 [0.1730; 0.2820] | 0.1469 [0.1021; 0.1998] | 0.0765 [0.0305; 0.1227] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.6471 | 0.0294 | 0.0362 | 0.0312 |
| en | 53 | 0.5472 | 0.0000 | 0.0664 | 0.1021 |
| unk | 11 | 0.3636 | 0.0000 | 0.0382 | 0.0936 |

## Model: deepseek-v4.1-flash | set SPLIT-holdout (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 5; gagal setelah ulang (dicatat): 3

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 96 | 2 | 0.0739 | 0.1132 | 0.0739 [0.0218; 0.1400] | 0.9583 | 0.0261 | 0.0057 | - | 0.0000 | 0 |
| near | R1 | anchor | 98 | 0 | 0.0426 | 0.0426 | 0.0426 [0.0031; 0.1023] | 0.9796 | 0.0106 | 0.0175 | 0.9796 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.0755 | 0.0755 | 0.0755 [0.0200; 0.1591] | 0.9592 | 0.0111 | 0.0108 | 0.9592 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0013 | 0.0013 | 0.0013 [0.0006; 0.0020] | 1.0000 | 0.0140 | 0.0000 | 1.0000 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.1097 | 0.1097 | 0.1097 [0.0367; 0.1972] | 0.9388 | 0.0479 | 0.0099 | 0.9388 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 96 | 0.4792 [0.3854; 0.5833] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 96 | 0.4091 [0.3218; 0.4946] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 96 | 0.3884 [0.3013; 0.4744] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 96 | 0.0312 [0.0000; 0.0729] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0502 [0.0269; 0.0822] | 0.0140 [0.0095; 0.0193] | 0.0362 [0.0146; 0.0661] |
| R3 | 0.0680 [0.0367; 0.1112] | 0.0733 [0.0340; 0.1202] | -0.0053 [-0.0497; 0.0350] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 33 | 0.6061 | 0.0606 | 0.0309 | -0.0003 |
| en | 52 | 0.4231 | 0.0192 | 0.0419 | 0.0004 |
| unk | 11 | 0.3636 | 0.0000 | 0.0255 | -0.0482 |
