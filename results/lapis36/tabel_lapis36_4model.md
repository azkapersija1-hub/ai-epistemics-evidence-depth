# Lapis 36: skor empat model (HASIL MODEL, BELUM DIVERIFIKASI)

Status: HASIL MODEL (BELUM DIVERIFIKASI). Lapis 36 = 40 klaim jangkar dikurangi C0056, C0295, C0057, C0225 (keputusan perundingan tim). Daftar: bahan/v2/hasil_olahan_final/lapis_36_claim_id.txt.
Sumber: items_lapis_36.jsonl dan kunci_lapis_36.jsonl (turunan dari items dan kunci lapis 40). API: keluaran nyata pilot, dev, dan val. Codex: impor sesi 40 pilot dan dev.
Codex: klaim C0230 dilewati (SKIP) di 7 observasi. Perlakuannya sama seperti Agen C: batas 1 mengeluarkannya, batas 2 memberinya 2,0, dan klaim itu tidak masuk uji konsistensi.
Nilai: rerata atau proporsi [CI 95% bootstrap klaster per article_id, B=2000, seed default]. Brier batas 2 tanpa CI. Tau = 0,7.

## Jumlah klaim dan observasi

| Model | n klaim (items) | n observasi | n klaim uji konsistensi (R1 & R3 valid) | n baris keluaran | parse gagal percobaan 1 | parse gagal final |
|---|---|---|---|---|---|---|
| qwen3.8-flash | 36 | 252 | 36 | 252 | 0 | 0 |
| qwen4-max-preview | 36 | 252 | 36 | 252 | 0 | 0 |
| deepseek-v4.1-flash | 36 | 252 | 35 | 255 | 3 | 1 |
| codex (gpt-6.1-sol, tak terverifikasi) | 36 | 252 | 35 | 252 | 7 | 7 |

## Skor per metrik (nilai [CI 95%])

| Metrik | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash | codex (gpt-6.1-sol, tak terverifikasi) |
|---|---|---|---|---|
| Brier batas 1 own R3 (anchor SUPPORTED) | 0.0765 [0.0004; 0.1985] | 0.0083 [0.0029; 0.0151] | 0.1225 [0.0072; 0.2675] | 0.0339 [0.0003; 0.0988] |
| Brier batas 1 near R1 (anchor NEI) | 0.0589 [0.0048; 0.1524] | 0.0696 [0.0174; 0.1565] | 0.0035 [0.0012; 0.0075] | 0.0009 [0.0001; 0.0026] |
| Brier batas 1 near R3 (anchor NEI) | 0.1388 [0.0209; 0.2866] | 0.1725 [0.0755; 0.2937] | 0.0076 [0.0025; 0.0150] | 0.0048 [0.0001; 0.0139] |
| Brier batas 1 far R1 (anchor NEI) | 0.0541 [0.0018; 0.1551] | 0.0773 [0.0143; 0.1539] | 0.0994 [0.0004; 0.2519] | 0.0005 [0.0000; 0.0014] |
| Brier batas 1 far R3 (anchor NEI) | 0.0900 [0.0053; 0.2112] | 0.2630 [0.1088; 0.4386] | 0.0898 [0.0007; 0.2274] | 0.0011 [0.0000; 0.0031] |
| Brier batas 2 own R3 (gagal = 2,0) | 0.0765 | 0.0083 | 0.1746 | 0.0885 |
| Brier batas 2 near R1 (gagal = 2,0) | 0.0589 | 0.0696 | 0.0035 | 0.0564 |
| Brier batas 2 near R3 (gagal = 2,0) | 0.1388 | 0.1725 | 0.0076 | 0.0602 |
| Brier batas 2 far R1 (gagal = 2,0) | 0.0541 | 0.0773 | 0.0994 | 0.0561 |
| Brier batas 2 far R3 (gagal = 2,0) | 0.0900 | 0.2630 | 0.0898 | 0.0567 |
| Sesuai (label R1 = R3) | 0.5278 [0.3611; 0.6944] | 0.5556 [0.3889; 0.7222] | 0.4286 [0.2571; 0.6000] | 0.5143 [0.3429; 0.6857] |
| Pergeseran dS | 0.4689 [0.3396; 0.6075] | 0.4119 [0.2899; 0.5447] | 0.4449 [0.2923; 0.5977] | 0.4301 [0.2909; 0.5639] |
| Pergeseran dN | 0.4443 [0.3182; 0.5809] | 0.3749 [0.2595; 0.4975] | 0.4359 [0.2847; 0.5870] | 0.4385 [0.2993; 0.5706] |
| Overkomit (tau 0,7) | 0.0000 [0.0000; 0.0000] | 0.0000 [0.0000; 0.0000] | 0.0286 [0.0000; 0.0857] | 0.0000 [0.0000; 0.0000] |
| False-support near R1 | 0.0711 [0.0286; 0.1308] | 0.1217 [0.0808; 0.1736] | 0.0289 [0.0183; 0.0417] | 0.0092 [0.0043; 0.0175] |
| False-support far R1 | 0.0508 [0.0153; 0.1075] | 0.1100 [0.0603; 0.1694] | 0.0631 [0.0089; 0.1408] | 0.0056 [0.0022; 0.0110] |
| Selisih FS near-far R1 | 0.0203 [-0.0072; 0.0511] | 0.0117 [-0.0283; 0.0467] | -0.0342 [-0.1117; 0.0217] | 0.0036 [-0.0032; 0.0127] |
| False-support near R3 | 0.1336 [0.0650; 0.2153] | 0.2122 [0.1475; 0.2842] | 0.0394 [0.0228; 0.0592] | 0.0160 [0.0055; 0.0343] |
| False-support far R3 | 0.0814 [0.0242; 0.1511] | 0.2200 [0.1308; 0.3200] | 0.0611 [0.0083; 0.1375] | 0.0086 [0.0028; 0.0170] |
| Selisih FS near-far R3 | 0.0522 [-0.0344; 0.1411] | -0.0078 [-0.0744; 0.0539] | -0.0217 [-0.0942; 0.0317] | 0.0074 [-0.0056; 0.0273] |
