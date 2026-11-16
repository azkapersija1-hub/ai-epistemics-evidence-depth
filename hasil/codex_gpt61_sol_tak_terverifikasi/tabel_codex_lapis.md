# Codex (gpt-6.1-sol, tak terverifikasi): skor per lapis

Status: HASIL MODEL (BELUM DIVERIFIKASI). Versi model tidak terverifikasi.
Sumber: sesi 40 klaim (hasil_40.jsonl), pilot + dev. Lapis 19 dan 26 = irisan klaim dari sesi 40, BUKAN sesi 19 (sesi 19 hanya untuk kestabilan, lihat KESTABILAN_codex.md).
Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed tetap]. Brier batas 2 tidak punya CI. Selisih terhadap lapis 40 hanya angka titik.
Observasi SKIP (C0230, 7 baris) diimpor sebagai gagal parse (tanpa nilai pengganti): batas 1 mengeluarkannya, batas 2 memberinya 2,0, dan klaim C0230 tidak masuk uji konsistensi (n klaim uji = 39 pada lapis 40).

## Jumlah klaim dan observasi

| Lapis | n klaim (items) | n observasi | n klaim uji konsistensi (R1 & R3 valid) | n baris keluaran (pilot+dev) | parse gagal percobaan 1 | parse gagal final |
|---|---|---|---|---|---|---|
| 40 | 40 | 280 | 39 | 280 | 7 | 7 |
| 26 | 26 | 182 | 26 | 182 | 0 | 0 |
| 19 | 19 | 133 | 19 | 133 | 0 | 0 |

## Skor per metrik (nilai [CI 95%])

| Metrik | codex L40 | codex L26 | codex L19 |
|---|---|---|---|
| Brier batas 1 own R3 (anchor SUPPORTED) | 0.0305 [0.0003; 0.0890] | 0.0450 [0.0002; 0.1330] | 0.0614 [0.0001; 0.1818] |
| Brier batas 1 near R1 (anchor NEI) | 0.0010 [0.0001; 0.0026] | 0.0011 [0.0000; 0.0033] | 0.0015 [0.0000; 0.0044] |
| Brier batas 1 near R3 (anchor NEI) | 0.0044 [0.0002; 0.0127] | 0.0064 [0.0001; 0.0186] | 0.0084 [0.0001; 0.0250] |
| Brier batas 1 far R1 (anchor NEI) | 0.0005 [0.0000; 0.0013] | 0.0001 [0.0000; 0.0002] | 0.0001 [0.0000; 0.0003] |
| Brier batas 1 far R3 (anchor NEI) | 0.0010 [0.0000; 0.0028] | 0.0003 [0.0000; 0.0008] | 0.0001 [0.0000; 0.0004] |
| Brier batas 2 own R3 (gagal = 2,0) | 0.0797 | 0.0450 | 0.0614 |
| Brier batas 2 near R1 (gagal = 2,0) | 0.0509 | 0.0011 | 0.0015 |
| Brier batas 2 near R3 (gagal = 2,0) | 0.0543 | 0.0064 | 0.0084 |
| Brier batas 2 far R1 (gagal = 2,0) | 0.0504 | 0.0001 | 0.0001 |
| Brier batas 2 far R3 (gagal = 2,0) | 0.0510 | 0.0003 | 0.0001 |
| Sesuai (label R1 = R3) | 0.4615 [0.3077; 0.6154] | 0.6538 [0.4615; 0.8462] | 0.7368 [0.5263; 0.9474] |
| Pergeseran dS | 0.4854 [0.3547; 0.6169] | 0.3082 [0.1688; 0.4621] | 0.2311 [0.0859; 0.3930] |
| Pergeseran dN | 0.4928 [0.3584; 0.6239] | 0.3214 [0.1777; 0.4712] | 0.2496 [0.0984; 0.4112] |
| Overkomit (tau 0,7) | 0.0000 [0.0000; 0.0000] | 0.0000 [0.0000; 0.0000] | 0.0000 [0.0000; 0.0000] |
| False-support near R1 | 0.0099 [0.0049; 0.0175] | 0.0096 [0.0037; 0.0194] | 0.0111 [0.0036; 0.0237] |
| False-support far R1 | 0.0053 [0.0022; 0.0105] | 0.0033 [0.0020; 0.0057] | 0.0038 [0.0021; 0.0070] |
| Selisih FS near-far R1 | 0.0046 [-0.0020; 0.0132] | 0.0063 [0.0003; 0.0164] | 0.0073 [-0.0005; 0.0203] |
| False-support near R3 | 0.0156 [0.0061; 0.0329] | 0.0192 [0.0056; 0.0426] | 0.0220 [0.0049; 0.0525] |
| False-support far R3 | 0.0080 [0.0028; 0.0155] | 0.0058 [0.0022; 0.0108] | 0.0045 [0.0021; 0.0083] |
| Selisih FS near-far R3 | 0.0076 [-0.0048; 0.0262] | 0.0135 [0.0001; 0.0372] | 0.0175 [-0.0002; 0.0484] |

## Selisih titik terhadap lapis 40 (lapis minus 40)

| Metrik | codex L26-40 | codex L19-40 |
|---|---|---|
| Brier batas 1 own R3 (anchor SUPPORTED) | +0.0146 | +0.0309 |
| Brier batas 1 near R1 (anchor NEI) | +0.0002 | +0.0005 |
| Brier batas 1 near R3 (anchor NEI) | +0.0020 | +0.0041 |
| Brier batas 1 far R1 (anchor NEI) | -0.0004 | -0.0004 |
| Brier batas 1 far R3 (anchor NEI) | -0.0007 | -0.0009 |
| Brier batas 2 own R3 (gagal = 2,0) | -0.0347 | -0.0184 |
| Brier batas 2 near R1 (gagal = 2,0) | -0.0498 | -0.0494 |
| Brier batas 2 near R3 (gagal = 2,0) | -0.0479 | -0.0458 |
| Brier batas 2 far R1 (gagal = 2,0) | -0.0504 | -0.0503 |
| Brier batas 2 far R3 (gagal = 2,0) | -0.0507 | -0.0509 |
| Sesuai (label R1 = R3) | +0.1923 | +0.2753 |
| Pergeseran dS | -0.1772 | -0.2543 |
| Pergeseran dN | -0.1714 | -0.2432 |
| Overkomit (tau 0,7) | +0.0000 | +0.0000 |
| False-support near R1 | -0.0003 | +0.0012 |
| False-support far R1 | -0.0019 | -0.0015 |
| Selisih FS near-far R1 | +0.0016 | +0.0026 |
| False-support near R3 | +0.0036 | +0.0064 |
| False-support far R3 | -0.0023 | -0.0036 |
| Selisih FS near-far R3 | +0.0059 | +0.0100 |
