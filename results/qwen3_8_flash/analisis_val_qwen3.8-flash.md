# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
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
