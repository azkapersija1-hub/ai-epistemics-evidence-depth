# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Set SPLIT-pilot: split pilot (teknis menurut praregistrasi, bukan hasil)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Model: qwen3.8-flash | set SPLIT-pilot (ulangan 1)
- Jumlah observasi: 140; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 20 | 0 | 0.0023 | 0.0023 | 0.0023 [0.0005; 0.0052] | 1.0000 | 0.0230 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 20 | 0 | 0.0816 | 0.0816 | 0.0816 [0.0142; 0.1946] | 0.9500 | 0.0690 | 0.0051 | 0.9500 | 1.0000 | 20 |
| near | R3 | anchor | 20 | 0 | 0.1802 | 0.1802 | 0.1802 [0.0268; 0.3993] | 0.9000 | 0.1010 | 0.0386 | 0.9000 | 1.0000 | 20 |
| far | R1 | anchor | 20 | 0 | 0.0037 | 0.0037 | 0.0037 [0.0004; 0.0086] | 1.0000 | 0.0210 | 0.0000 | 1.0000 | 1.0000 | 20 |
| far | R3 | anchor | 20 | 0 | 0.0014 | 0.0014 | 0.0014 [0.0001; 0.0035] | 1.0000 | 0.0120 | 0.0000 | 1.0000 | 1.0000 | 20 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 20 | 0.3500 [0.1500; 0.5500] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 20 | 0.6225 [0.4440; 0.7890] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 20 | 0.5702 [0.4027; 0.7310] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 20 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1100 [0.0420; 0.2010] | 0.0210 [0.0050; 0.0420] | 0.0890 [0.0240; 0.1770] |
| R3 | 0.1775 [0.0795; 0.3005] | 0.0120 [0.0020; 0.0255] | 0.1655 [0.0680; 0.2885] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 6 | 0.3333 | 0.0000 | 0.0583 | 0.1200 |
| en | 12 | 0.4167 | 0.0000 | 0.1000 | 0.1342 |
| unk | 2 | 0.0000 | 0.0000 | 0.1150 | 0.4900 |

## Model: qwen4-max-preview | set SPLIT-pilot (ulangan 1)
- Jumlah observasi: 140; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 20 | 0 | 0.0047 | 0.0047 | 0.0047 [0.0018; 0.0088] | 1.0000 | 0.0425 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 20 | 0 | 0.2293 | 0.2293 | 0.2293 [0.0703; 0.4549] | 0.9000 | 0.1660 | 0.0632 | 0.9000 | 1.0000 | 20 |
| near | R3 | anchor | 20 | 0 | 0.3973 | 0.3973 | 0.3973 [0.1657; 0.6820] | 0.7500 | 0.2215 | 0.1988 | 0.7500 | 1.0000 | 20 |
| far | R1 | anchor | 20 | 0 | 0.0074 | 0.0074 | 0.0074 [0.0031; 0.0126] | 1.0000 | 0.0555 | 0.0000 | 1.0000 | 1.0000 | 20 |
| far | R3 | anchor | 20 | 0 | 0.0814 | 0.0814 | 0.0814 [0.0303; 0.1369] | 1.0000 | 0.1505 | 0.0000 | 1.0000 | 1.0000 | 20 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 20 | 0.2500 [0.1000; 0.4500] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 20 | 0.6090 [0.4420; 0.7585] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 20 | 0.5487 [0.3817; 0.7005] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 20 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.2425 [0.1450; 0.3645] | 0.0555 [0.0400; 0.0730] | 0.1870 [0.0925; 0.3095] |
| R3 | 0.3315 [0.2065; 0.4800] | 0.1505 [0.0880; 0.2165] | 0.1810 [0.0685; 0.3115] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 6 | 0.3333 | 0.0000 | 0.1017 | 0.1250 |
| en | 12 | 0.2500 | 0.0000 | 0.1925 | 0.1725 |
| unk | 2 | 0.0000 | 0.0000 | 0.4100 | 0.4000 |

## Model: deepseek-v4.1-flash | set SPLIT-pilot (ulangan 1)
- Jumlah observasi: 140; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 2; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 20 | 0 | 0.0092 | 0.0092 | 0.0092 [0.0025; 0.0182] | 1.0000 | 0.0460 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 20 | 0 | 0.0165 | 0.0165 | 0.0165 [0.0031; 0.0356] | 1.0000 | 0.0570 | 0.0000 | 1.0000 | 1.0000 | 20 |
| near | R3 | anchor | 20 | 0 | 0.2480 | 0.2480 | 0.2480 [0.0213; 0.5326] | 0.8500 | 0.0915 | 0.0374 | 0.8500 | 1.0000 | 20 |
| far | R1 | anchor | 20 | 0 | 0.0020 | 0.0020 | 0.0020 [0.0002; 0.0045] | 1.0000 | 0.0180 | 0.0000 | 1.0000 | 1.0000 | 20 |
| far | R3 | anchor | 20 | 0 | 0.0006 | 0.0006 | 0.0006 [0.0001; 0.0013] | 1.0000 | 0.0100 | 0.0000 | 1.0000 | 1.0000 | 20 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 20 | 0.3500 [0.1500; 0.5500] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 20 | 0.5890 [0.4030; 0.7650] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 20 | 0.5367 [0.3515; 0.7087] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 20 | 0.0500 [0.0000; 0.1500] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0570 [0.0260; 0.0930] | 0.0180 [0.0070; 0.0330] | 0.0390 [0.0115; 0.0695] |
| R3 | 0.1710 [0.0500; 0.3225] | 0.0100 [0.0035; 0.0185] | 0.1610 [0.0435; 0.3095] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 6 | 0.3333 | 0.0000 | 0.0600 | 0.1733 |
| en | 12 | 0.4167 | 0.0833 | 0.0342 | 0.1033 |
| unk | 2 | 0.0000 | 0.0000 | 0.0050 | 0.4700 |
