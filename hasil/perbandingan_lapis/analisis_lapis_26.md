# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 182; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 26 | 0 | 0.0398 | 0.0398 | 0.0398 [0.0003; 0.1184] | 0.9615 | 0.0388 | 0.0015 | - | 0.0000 | 0 |
| near | R1 | anchor | 26 | 0 | 0.0792 | 0.0792 | 0.0792 [0.0047; 0.2062] | 0.9615 | 0.0712 | 0.0063 | 0.9615 | 1.0000 | 26 |
| near | R3 | anchor | 26 | 0 | 0.1776 | 0.1776 | 0.1776 [0.0130; 0.3714] | 0.8846 | 0.1027 | 0.0304 | 0.8846 | 1.0000 | 26 |
| far | R1 | anchor | 26 | 0 | 0.0733 | 0.0733 | 0.0733 [0.0010; 0.2131] | 0.9615 | 0.0292 | 0.0063 | 0.9615 | 1.0000 | 26 |
| far | R3 | anchor | 26 | 0 | 0.1213 | 0.1213 | 0.1213 [0.0040; 0.2914] | 0.9231 | 0.0758 | 0.0093 | 0.9231 | 1.0000 | 26 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 26 | 0.6154 [0.4231; 0.8077] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 26 | 0.3962 [0.2487; 0.5497] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 26 | 0.3721 [0.2291; 0.5219] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 26 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0838 [0.0265; 0.1627] | 0.0588 [0.0104; 0.1369] | 0.0250 [-0.0104; 0.0677] |
| R3 | 0.1465 [0.0546; 0.2577] | 0.0954 [0.0181; 0.1954] | 0.0512 [-0.0615; 0.1719] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 14 | 0.6429 | 0.0000 | 0.0007 | -0.0300 |
| en | 7 | 0.5714 | 0.0000 | 0.0729 | 0.1214 |
| unk | 5 | 0.6000 | 0.0000 | 0.0260 | 0.1800 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 182; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 26 | 0 | 0.0074 | 0.0074 | 0.0074 [0.0028; 0.0146] | 1.0000 | 0.0502 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 26 | 0 | 0.0859 | 0.0859 | 0.0859 [0.0148; 0.2071] | 0.9615 | 0.0769 | 0.0138 | 0.9615 | 1.0000 | 26 |
| near | R3 | anchor | 26 | 0 | 0.1877 | 0.1877 | 0.1877 [0.0641; 0.3572] | 0.8846 | 0.1350 | 0.0546 | 0.8846 | 1.0000 | 26 |
| far | R1 | anchor | 26 | 0 | 0.0794 | 0.0794 | 0.0794 [0.0070; 0.1818] | 0.9231 | 0.0881 | 0.0061 | 0.9231 | 1.0000 | 26 |
| far | R3 | anchor | 26 | 0 | 0.2774 | 0.2774 | 0.2774 [0.0808; 0.5124] | 0.8077 | 0.1038 | 0.0439 | 0.8077 | 1.0000 | 26 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 26 | 0.6538 [0.4615; 0.8077] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 26 | 0.3133 [0.1798; 0.4613] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 26 | 0.2763 [0.1604; 0.4071] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 26 | 0.0000 [0.0000; 0.0000] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1258 [0.0727; 0.1985] | 0.1069 [0.0485; 0.1831] | 0.0188 [-0.0269; 0.0585] |
| R3 | 0.2127 [0.1315; 0.3112] | 0.2112 [0.1023; 0.3450] | 0.0015 [-0.0904; 0.0846] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 14 | 0.7143 | 0.0000 | 0.0007 | -0.0564 |
| en | 7 | 0.5714 | 0.0000 | 0.0743 | 0.1286 |
| unk | 5 | 0.6000 | 0.0000 | -0.0080 | -0.0140 |

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 182; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 3; gagal setelah ulang (dicatat): 1

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 25 | 1 | 0.1091 | 0.1818 | 0.1091 [0.0054; 0.2724] | 0.9200 | 0.0636 | 0.0049 | - | 0.0000 | 0 |
| near | R1 | anchor | 26 | 0 | 0.0041 | 0.0041 | 0.0041 [0.0009; 0.0095] | 1.0000 | 0.0281 | 0.0000 | 1.0000 | 1.0000 | 26 |
| near | R3 | anchor | 26 | 0 | 0.0096 | 0.0096 | 0.0096 [0.0026; 0.0189] | 1.0000 | 0.0465 | 0.0000 | 1.0000 | 1.0000 | 26 |
| far | R1 | anchor | 26 | 0 | 0.0753 | 0.0753 | 0.0753 [0.0003; 0.2247] | 0.9615 | 0.0258 | 0.0063 | 0.9615 | 1.0000 | 26 |
| far | R3 | anchor | 26 | 0 | 0.0561 | 0.0561 | 0.0561 [0.0003; 0.1664] | 0.9615 | 0.0431 | 0.0015 | 0.9615 | 1.0000 | 26 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 25 | 0.5200 [0.3200; 0.7200] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 25 | 0.3328 [0.1612; 0.5060] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 25 | 0.3250 [0.1586; 0.4974] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 25 | 0.0400 [0.0000; 0.1200] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0281 [0.0146; 0.0458] | 0.0500 [0.0077; 0.1277] | -0.0219 [-0.1031; 0.0285] |
| R3 | 0.0465 [0.0246; 0.0715] | 0.0435 [0.0046; 0.1119] | 0.0031 [-0.0677; 0.0523] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 14 | 0.6429 | 0.0000 | -0.0643 | -0.0429 |
| en | 6 | 0.5000 | 0.0000 | 0.0386 | 0.0586 |
| unk | 5 | 0.2000 | 0.2000 | 0.0120 | 0.0540 |
