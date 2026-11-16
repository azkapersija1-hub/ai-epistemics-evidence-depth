# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
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
