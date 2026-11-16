# HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)

Analisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan.

## Provider: luar_antigravity (ulangan 1)
- Jumlah observasi: 686; prompt_hash: 0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530
- Parse gagal percobaan pertama: 0; gagal setelah ulang (dicatat): 0

### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)
| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) | Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| own | R3 | anchor | 98 | 0 | 0.0007 | 0.0007 | 0.0007 [0.0006; 0.0008] | 1.0000 | 0.0207 | 0.0000 | - | - | 0 |
| near | R1 | anchor | 98 | 0 | 0.0193 | 0.0193 | 0.0193 [0.0006; 0.0566] | 0.9898 | 0.0112 | 0.0001 | 0.9898 | 1.0000 | 98 |
| near | R3 | anchor | 98 | 0 | 0.0518 | 0.0518 | 0.0518 [0.0012; 0.1159] | 0.9694 | 0.0101 | 0.0012 | 0.9694 | 1.0000 | 98 |
| far | R1 | anchor | 98 | 0 | 0.0006 | 0.0006 | 0.0006 [0.0006; 0.0006] | 1.0000 | 0.0200 | 0.0000 | 1.0000 | 1.0000 | 98 |
| far | R3 | anchor | 98 | 0 | 0.0557 | 0.0557 | 0.0557 [0.0006; 0.1293] | 0.9694 | 0.0094 | 0.0006 | 0.9694 | 1.0000 | 98 |

### B. Konsistensi per klaim (own R1 vs R3)
| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |
|---|---|---|
| Sesuai (label R1 = label R3) | 98 | 0.4796 [0.3776; 0.5816] |
| Pergeseran dS = p_S(R3) - p_S(R1) | 98 | 0.5067 [0.4182; 0.5913] |
| Pergeseran dN = p_N(R1) - p_N(R3) | 98 | 0.4767 [0.3918; 0.5606] |
| Overkomit (max p_S,p_R di R1 >= tau=0.7, label R3 berbeda) | 98 | 0.0204 [0.0000; 0.0510] |

### C. Near vs far (false-support mass pada observasi berjangkar NEI)
| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |
|---|---|---|---|
| R1 | 0.0307 [0.0204; 0.0504] | 0.0200 [0.0200; 0.0200] | 0.0107 [0.0004; 0.0304] |
| R3 | 0.0508 [0.0235; 0.0860] | 0.0487 [0.0200; 0.0869] | 0.0021 [-0.0345; 0.0381] |

### D. Per bahasa
| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |
|---|---|---|---|---|---|
| id | 34 | 0.5294 | 0.0588 | 0.0006 | -0.0276 |
| en | 53 | 0.4717 | 0.0000 | 0.0194 | 0.0057 |
| unk | 11 | 0.3636 | 0.0000 | 0.0000 | 0.0773 |
