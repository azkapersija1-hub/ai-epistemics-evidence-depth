# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: profil_qwen_plan (ulangan 1)
- Jumlah observasi: 546; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 78 | 0 | 0.0062 | 0.0062 | 0.0062 [0.0036; 0.0098] | 1.0000 | 0.0479 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 78 | 0 | 0.0669 | 0.0669 | 0.0669 [0.0251; 0.1249] | 0.9615 | 0.0768 | 0.0049 | 0.9615 | 1.0000 | 78 |
| near | R3 | anchor | 78 | 0 | 0.2064 | 0.2064 | 0.2064 [0.1183; 0.3077] | 0.8590 | 0.0292 | 0.0456 | 0.8590 | 1.0000 | 78 |
| far | R1 | anchor | 78 | 0 | 0.0604 | 0.0604 | 0.0604 [0.0212; 0.1131] | 0.9487 | 0.0701 | 0.0025 | 0.9487 | 1.0000 | 78 |
| far | R3 | anchor | 78 | 0 | 0.1729 | 0.1729 | 0.1729 [0.0821; 0.2782] | 0.8846 | 0.0717 | 0.0239 | 0.8846 | 1.0000 | 78 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 78 | 0.5769 [0.4615; 0.6923] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 78 | 0.4000 [0.3121; 0.4846] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 78 | 0.3711 [0.2870; 0.4535] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 78 | 0.0128 [0.0000; 0.0385] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.1169 [0.0876; 0.1536] | 0.0924 [0.0626; 0.1276] | 0.0245 [-0.0008; 0.0503] |
| R3 | 0.2164 [0.1623; 0.2733] | 0.1637 [0.1106; 0.2205] | 0.0527 [0.0091; 0.0935] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 24 | 0.7083 | 0.0000 | -0.0212 | -0.0254 |
| en | 42 | 0.5476 | 0.0238 | 0.0519 | 0.1188 |
| unk | 12 | 0.4167 | 0.0000 | 0.0200 | -0.0225 |
