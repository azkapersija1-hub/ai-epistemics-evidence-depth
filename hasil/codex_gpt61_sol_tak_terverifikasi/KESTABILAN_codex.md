# Kestabilan Codex: sesi 40 vs sesi 19 (19 klaim lapis 19)

Status: HASIL MODEL (BELUM DIVERIFIKASI). Sesi 19 adalah putaran uji ulang kestabilan, BUKAN penambah data hasil utama. Keduanya memakai provider dan model_id yang sama; perbandingan per observasi lewat obs_id.
Observasi lapis 19: 133. Pasangan yang valid di kedua sesi dipakai; pasangan yang gagal (SKIP/gagal parse) dicatat di bawah dan TIDAK dibuang diam-diam.
Observasi dengan SKIP/gagal parse di salah satu sesi: 0.
Argmax = label terpilih (aturan seri NEI menang). Selisih Brier = BS(sesi 19) - BS(sesi 40), hanya observasi berlabel; per klaim = rerata selisih di atas observasi berlabel klaim itu pada tingkat tersebut (tingkat semua = seluruh tingkat). R2 tidak berlabel, jadi Brier tidak dihitung.
CI: bootstrap klaster per article_id, B=2000, seed tetap.

| Tingkat bukti | n obs (kedua sesi valid) | Argmax sama (%) [CI] | Rerata abs selisih p(SUPPORTED) [CI] | n obs berlabel | Selisih Brier per obs [CI] | n klaim berlabel | Rerata selisih Brier per klaim | Min | Max | Klaim selisih > 0 | Klaim selisih < 0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | 57 | 98.2% [94.7; 100.0] | 0.0223 [0.0045; 0.0512] | 38 | -0.0005 [-0.0017; 0.0002] | 19 | -0.0005 | -0.0113 | +0.0012 | 16 | 2 |
| R2 | 19 | 100.0% [100.0; 100.0] | 0.0210 [0.0041; 0.0441] | 0 | - | - | - | - | - | - | - |
| R3 | 57 | 100.0% [100.0; 100.0] | 0.0043 [0.0012; 0.0084] | 57 | 0.0014 [-0.0026; 0.0057] | 19 | +0.0014 | -0.0230 | +0.0298 | 14 | 5 |
| semua | 133 | 99.2% [97.7; 100.0] | 0.0144 [0.0044; 0.0277] | 95 | 0.0007 [-0.0022; 0.0035] | 19 | +0.0007 | -0.0183 | +0.0184 | 16 | 3 |
