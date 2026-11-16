# Ringkasan Katalog Sumber Artikel (S1)

Tanggal: 2026-11-15. Hanya metadata bibliografis (judul, penulis, tahun, jurnal, volume, issue, halaman, DOI). Tidak ada teks klaim, abstrak, atau teks bukti yang disalin.

## 1. Jumlah artikel unik

| Kelompok | Jumlah unik | Keterangan |
|---|---|---|
| A. Artikel asal klaim | 294 | article_id dari pasangan_v2_1.jsonl; pool_v2.jsonl berisi 300 baris, 6 sisanya (B0295, B0296, B0297, B0298, B0299, B0300) tidak punya pasangan dan tidak dimasukkan |
| B. Artikel bukti (near dan far) | 357 | ev_id unik dari near_ev dan far_ev; dari 595 baris kolam, 238 tidak dipakai pasangan |

Peran pada B: bukti_near saja 150, bukti_far saja 150, dan keduanya 57.

## 2. Status metadata

| Status | A (asal klaim) | B (bukti) |
|---|---|---|
| LENGKAP (penulis, tahun, judul, jurnal terisi) | 181 | 208 |
| SEBAGIAN | 113 | 149 |
| TANPA_DOI | 0 | 0 |

Semua artikel punya DOI di berkas bahan, sehingga tidak ada yang berstatus TANPA_DOI.

## 3. Pencocokan dengan katalog internal (lewat DOI)

| Metode | A | B |
|---|---|---|
| DOI (tepat satu baris katalog) | 197 | 252 |
| DOI+judul (DOI cocok dan judul ternormalisasi sama) | 95 | 104 |
| DOI ganda di katalog (tidak diisi, ditandai) | 2 | 1 |
| Tidak cocok | 0 | 0 |

Pencocokan judul hanya dipakai bila DOI kosong, dan semua artikel punya DOI, sehingga tidak ada yang dicocokkan lewat judul.

## 4. Lengkapan dari Crossref

- DOI unik yang perlu dicek Crossref (ada celah penulis, tahun, atau jurnal setelah katalog): 626.
- Rekaman ditemukan di Crossref: 593. Tidak ditemukan (404, ditandai TIDAK_DITEMUKAN_CROSSREF): 33. Gagal: 0 (tidak ada).
- Artikel yang mendapat minimal satu kolom dari Crossref: A 169, B 197.
- Crossref tidak dipakai untuk mengisi bila judulnya tidak sesuai dengan judul berkas bahan (kemiripan di bawah 0,6). Kasus ini dicatat di kolom catatan: A 95, B 132. Sebagian besar karena judul di berkas bahan memang keliru (misalnya berisi nama jurnal atau teks halaman), sehingga perlu diperiksa manusia.
- Konflik tahun antara katalog dan Crossref (katalog dipertahankan): A 39, B 47. Konflik jurnal: 0.

## 5. Judul

- Beda judul berkas bahan dengan katalog: A 197, B 252. Judul tidak dipilih dan tidak diubah; kedua kolom disimpan.
- Beda judul berkas bahan dengan Crossref: A 119, B 169.

Daftar article_id A dengan beda judul katalog: B0001, B0003, B0004, B0005, B0006, B0008, B0009, B0010, B0011, B0012, B0013, B0014, B0015, B0019, B0020, B0021, B0024, B0025, B0026, B0028, B0029, B0030, B0031, B0034, B0036, B0038, B0039, B0040, B0041, B0042, B0043, B0044, B0045, B0046, B0048, B0049, B0050, B0051, B0052, B0053, B0054, B0055, B0056, B0057, B0058, B0059, B0060, B0061, B0063, B0065, B0066, B0067, B0071, B0072, B0077, B0078, B0080, B0081, B0082, B0084, B0085, B0086, B0088, B0089, B0090, B0091, B0092, B0093, B0094, B0097, B0099, B0101, B0102, B0103, B0104, B0105, B0107, B0108, B0109, B0110, B0112, B0113, B0114, B0115, B0116, B0117, B0118, B0121, B0125, B0127, B0129, B0130, B0131, B0132, B0135, B0138, B0140, B0141, B0142, B0143, B0144, B0145, B0146, B0147, B0148, B0149, B0151, B0152, B0153, B0154, B0155, B0156, B0157, B0158, B0159, B0160, B0161, B0162, B0165, B0166, B0168, B0169, B0170, B0171, B0172, B0173, B0175, B0176, B0177, B0178, B0179, B0180, B0181, B0184, B0188, B0189, B0190, B0193, B0194, B0196, B0197, B0198, B0199, B0200, B0201, B0203, B0204, B0206, B0207, B0208, B0209, B0211, B0212, B0215, B0217, B0218, B0219, B0221, B0224, B0227, B0230, B0234, B0237, B0239, B0242, B0243, B0245, B0246, B0247, B0248, B0249, B0250, B0251, B0252, B0253, B0254, B0256, B0257, B0258, B0259, B0260, B0261, B0262, B0263, B0264, B0266, B0267, B0268, B0269, B0270, B0272, B0273, B0274, B0277, B0278, B0280, B0284

Daftar ev_id B dengan beda judul katalog: E0001, E0008, E0009, E0015, E0021, E0024, E0026, E0028, E0029, E0030, E0031, E0032, E0034, E0035, E0037, E0038, E0040, E0042, E0043, E0046, E0047, E0055, E0056, E0058, E0060, E0062, E0064, E0067, E0068, E0069, E0071, E0073, E0077, E0078, E0083, E0085, E0088, E0090, E0091, E0093, E0106, E0107, E0108, E0109, E0110, E0111, E0112, E0113, E0116, E0117, E0120, E0124, E0125, E0126, E0129, E0130, E0133, E0134, E0138, E0139, E0141, E0142, E0144, E0147, E0150, E0152, E0153, E0154, E0156, E0159, E0160, E0161, E0163, E0164, E0170, E0171, E0172, E0173, E0180, E0181, E0182, E0184, E0186, E0188, E0189, E0190, E0191, E0192, E0193, E0194, E0198, E0200, E0202, E0203, E0207, E0210, E0211, E0214, E0215, E0216, E0217, E0218, E0222, E0223, E0224, E0226, E0228, E0229, E0231, E0234, E0235, E0236, E0237, E0238, E0241, E0242, E0247, E0248, E0250, E0251, E0253, E0256, E0257, E0258, E0259, E0260, E0263, E0264, E0265, E0266, E0267, E0269, E0270, E0272, E0274, E0276, E0277, E0280, E0283, E0291, E0293, E0294, E0295, E0298, E0299, E0300, E0302, E0303, E0304, E0305, E0312, E0314, E0315, E0316, E0318, E0331, E0336, E0339, E0342, E0343, E0345, E0347, E0348, E0352, E0353, E0354, E0357, E0358, E0359, E0361, E0362, E0363, E0366, E0367, E0369, E0373, E0376, E0377, E0378, E0379, E0380, E0381, E0382, E0383, E0385, E0386, E0387, E0393, E0395, E0396, E0397, E0398, E0401, E0402, E0406, E0410, E0411, E0414, E0427, E0435, E0438, E0453, E0454, E0456, E0458, E0460, E0465, E0466, E0468, E0476, E0477, E0478, E0480, E0482, E0486, E0490, E0491, E0495, E0496, E0499, E0500, E0503, E0505, E0507, E0508, E0510, E0513, E0514, E0515, E0516, E0517, E0519, E0520, E0521, E0522, E0523, E0525, E0526, E0532, E0535, E0537, E0538, E0540, E0544, E0552, E0557, E0559, E0567, E0568, E0578, E0582, E0588

Daftar article_id A dengan beda judul Crossref: B0003, B0005, B0008, B0009, B0010, B0011, B0012, B0013, B0018, B0019, B0020, B0021, B0025, B0026, B0027, B0028, B0030, B0034, B0038, B0041, B0043, B0044, B0046, B0050, B0053, B0055, B0057, B0058, B0061, B0063, B0071, B0072, B0078, B0080, B0082, B0084, B0086, B0089, B0090, B0091, B0093, B0097, B0099, B0102, B0104, B0105, B0107, B0108, B0114, B0115, B0116, B0117, B0120, B0125, B0127, B0129, B0130, B0131, B0132, B0134, B0138, B0145, B0147, B0149, B0151, B0153, B0154, B0155, B0156, B0158, B0159, B0160, B0169, B0170, B0171, B0172, B0173, B0175, B0176, B0177, B0179, B0180, B0184, B0185, B0192, B0198, B0201, B0202, B0204, B0205, B0206, B0209, B0211, B0213, B0214, B0217, B0218, B0225, B0230, B0233, B0234, B0239, B0247, B0250, B0255, B0256, B0257, B0258, B0260, B0262, B0266, B0267, B0272, B0274, B0277, B0278, B0279, B0280, B0288

Daftar ev_id B dengan beda judul Crossref: E0018, E0021, E0024, E0026, E0028, E0029, E0030, E0035, E0037, E0040, E0042, E0043, E0047, E0050, E0051, E0055, E0058, E0062, E0064, E0067, E0068, E0077, E0078, E0083, E0085, E0088, E0090, E0093, E0107, E0108, E0110, E0111, E0112, E0113, E0116, E0117, E0123, E0124, E0130, E0133, E0134, E0139, E0141, E0147, E0150, E0156, E0161, E0163, E0164, E0170, E0171, E0173, E0181, E0182, E0186, E0188, E0189, E0190, E0191, E0192, E0193, E0198, E0200, E0202, E0207, E0215, E0216, E0217, E0218, E0222, E0223, E0224, E0228, E0229, E0234, E0235, E0237, E0238, E0241, E0242, E0247, E0250, E0253, E0256, E0260, E0266, E0267, E0269, E0270, E0274, E0276, E0277, E0283, E0293, E0294, E0295, E0298, E0299, E0300, E0302, E0303, E0304, E0305, E0314, E0315, E0316, E0331, E0342, E0343, E0345, E0348, E0353, E0354, E0358, E0359, E0366, E0369, E0373, E0376, E0377, E0381, E0383, E0386, E0388, E0389, E0391, E0395, E0396, E0397, E0398, E0402, E0411, E0430, E0432, E0438, E0453, E0456, E0458, E0460, E0465, E0468, E0469, E0477, E0478, E0482, E0487, E0489, E0490, E0492, E0495, E0503, E0504, E0508, E0510, E0514, E0516, E0517, E0520, E0523, E0525, E0533, E0535, E0537, E0544, E0552, E0557, E0568, E0582, E0588

## 6. Rentang tahun

- A: 2008 sampai 2026 (293 dari 294 artikel punya tahun)
- B: 2016 sampai 2026 (357 dari 357 artikel punya tahun)

## 7. Bahasa dan domain (dari berkas bahan)

| | A | B |
|---|---|---|
| Bahasa | en 155, id 100, unk 39 | en 196, id 110, unk 51 |
| Domain | Social Sciences 269, Formal Sciences 15, Needs Review 5, Health Sciences 4, Natural Sciences 1 | Social Sciences 306, Formal Sciences 31, Needs Review 11, Health Sciences 9 |

Beda label bahasa antara berkas bahan dan katalog (dicatat, tidak dipilih): A 48, B 55.

## 8. Verifikasi berkas

Hash SHA-256 sebelum dan sesudah pekerjaan: semua identik untuk pool_v2.jsonl, kolam_bukti_v2_1.jsonl, pasangan_v2_1.jsonl, dan KATALOG_METADATA_LENGKAP.xlsx. Rincian ada di LOG_KATALOG_SUMBER.md.

## 9. Keluaran

- katalog_sumber_artikel_asal_294.csv
- katalog_sumber_bukti_near_far.csv
- LAMPIRAN_KATALOG_SUMBER.md
- LOG_KATALOG_SUMBER.md
- crossref_respon_ringkas.json (rekaman Crossref yang dipakai, hanya bidang metadata)
- skrip_bangun_katalog_sumber.py (skrip yang menghasilkan keluaran ini)
