# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 546; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 5; gagal setelah ulang (dicatat): 2

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 76 | 2 | 0.0791 | 0.1284 | 0.0791 [0.0187; 0.1629] | 0.9474 | 0.0571 | 0.0029 | - | 0.0000 | 0 |
| near | R1 | anchor | 78 | 0 | 0.0026 | 0.0026 | 0.0026 [0.0015; 0.0039] | 1.0000 | 0.0256 | 0.0000 | 1.0000 | 1.0000 | 78 |
| near | R3 | anchor | 78 | 0 | 0.0305 | 0.0305 | 0.0305 [0.0032; 0.0826] | 0.9872 | 0.0206 | 0.0125 | 0.9872 | 1.0000 | 78 |
| far | R1 | anchor | 78 | 0 | 0.0466 | 0.0466 | 0.0466 [0.0007; 0.1210] | 0.9744 | 0.0113 | 0.0027 | 0.9744 | 1.0000 | 78 |
| far | R3 | anchor | 78 | 0 | 0.0643 | 0.0643 | 0.0643 [0.0016; 0.1366] | 0.9615 | 0.0221 | 0.0024 | 0.9615 | 1.0000 | 78 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 76 | 0.4868 [0.3684; 0.6053] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 76 | 0.4297 [0.3262; 0.5321] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 76 | 0.4193 [0.3177; 0.5215] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 76 | 0.0132 [0.0000; 0.0395] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0256 [0.0191; 0.0328] | 0.0371 [0.0105; 0.0751] | -0.0114 [-0.0497; 0.0151] |
| R3 | 0.0460 [0.0258; 0.0759] | 0.0474 [0.0132; 0.0876] | -0.0014 [-0.0362; 0.0235] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 24 | 0.6667 | 0.0000 | -0.0779 | -0.0588 |
| en | 40 | 0.4500 | 0.0000 | 0.0224 | 0.0207 |
| unk | 12 | 0.2500 | 0.0833 | 0.0033 | 0.0358 |
