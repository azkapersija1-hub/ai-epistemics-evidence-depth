# PRAREGISTRASI DIBEKUKAN (sebelum ada jawaban model yang dikumpulkan)

Dibekukan: 2026-11-11 23:08:13 (waktu lokal)

## Pertanyaan
Saat LLM hanya membaca bagian awal artikel ilmiah (R1 abstrak; R2 abstrak+hasil; R3 teks relevan penuh), seberapa terkalibrasi distribusi SUPPORTED/REFUTED/NEI-nya, dan seberapa sering ia terlalu yakin pada R1 dibanding R3, serta mengisi dukungan palsu pada bukti artikel lain (near/far).

## Desain dan label
- 294 klaim x 7 observasi (own R1,R2,R3; near R1,R3; far R1,R3). Split per artikel: {"dev": 78, "holdout": 98, "pilot": 20, "val": 98}.
- LABEL JANGKAR (bukan label ahli): own+R3 = SUPPORTED (kesimpulan penulis); near/far = NEI (bukti artikel lain, bahasa sama); own R1/R2 = tanpa label.
- REFUTED tidak ada pada jangkar; label ahli (lembar_ahli_40, lembar_ahli_jangkar_30) BELUM diisi.

## Primary dan sekunder
- Primary: Brier multikelas pada observasi berjangkar (SUPPORTED own R3 dan NEI near/far), dilaporkan dengan CI bootstrap klaster per article_id.
- Sekunder: akurasi, ECE, AURC, konsistensi R1 vs R3 (sesuai/tidak sesuai), pergeseran dS dan dN, overkomit R1 (tau = 0,7), false-support mass near vs far, per bahasa (en/id/unk).
- Hipotesis dua arah. Tidak ada koreksi p untuk analisis eksploratif; interval dilaporkan apa adanya.

## Aturan
- tau overkomit = 0,7 (dibekukan). Aturan seri argmax: NEI menang.
- Parse gagal: ulang sekali; lalu dicatat. Brier dilaporkan dua batas (butir gagal dikeluarkan / diberi 2,0).
- Temperature tidak dapat diatur lewat model_api (default penyedia); dicatat sebagai keterbatasan. Ulangan 1 utama; stabilitas pada subset dev.
- Urutan: pilot (teknis; tidak dilaporkan sebagai hasil) -> dev -> val -> holdout SEKALI. Tidak ada penyetelan prompt, tau, atau aturan setelah melihat hasil dev/val.
- Model: qwen3.8-flash dan deepseek-v4.1-flash via profil qwen_plan. Model lain (GPT-6.1 Sol, Gemini) menyusul lewat jalur lain dan akan dilaporkan terpisah.
- max_tokens 512, timeout 120 detik. Kutipan artikel jurnal dinyatakan bukan konten pribadi (flag --bukan-konten-pribadi).

## Hash berkas beku (sha256)
- prompt_templates/prompt_v1.txt: `0a12032e7670e0f6a1ba591b86ba7b715500dbd60c8becf8524a6544c8752530`
- bahan/v2/items_model.jsonl: `95d623f031eab9ea5d82fa75ebab65f6460ec84acf44e74d80543ab4effb6e85`
- bahan/v2/RAHASIA/kunci.jsonl: `e71e0148e0f5c97f9d84090c5fd5349395d066da2e463b66c6336b17fc2f297a`
- bahan/v2/pasangan_v2_1.jsonl: `be4b775be985e45beb0e4622458b7e116e6e9a1f67f89719b7ce9543a6487240`
- bahan/v2/pool_manifest.json: `beab654808ab40479d3c30f6d1a2f8fef74718026c0f6cdee075f9cf22fe4966`
- sha256_daftar_article_holdout: `a4d7c0cc882a4d808cf79467995264ac846023166815166f6a207c082da660e0`

## AMANDEMEN 1 (dicatat sebelum dev/val/holdout dibuka; ditulis setelah pilot teknis)
- Temuan pilot (teknis, bukan skor): deepseek-v4.1-flash mengembalikan keluaran KOSONG pada 20 dari 140 observasi pilot (14%) bahkan setelah ulang, dengan max_tokens 512; qwen3.8-flash 140/140 ter-parse. Dugaan: token penalaran tersembunyi menghabiskan batas.
- Tindakan: max_tokens deepseek-v4.1-flash dinaikkan ke 4000 dan pilot DeepSeek dijalankan ulang; keluaran lama diarsipkan (ARSIP_nyata_pilot_deepseek-v4.1-flash_u1_max512.jsonl). qwen3.8-flash tetap 512.
- Tidak ada skor, label, tau, prompt, atau aturan analisis yang diubah. Perubahan hanya parameter keluaran model karena kegagalan teknis; dilaporkan sebagai keterbatasan.

## AMANDEMEN 2 (dicatat sebelum satu pun keluaran qwen4-max-preview dikumpulkan)
- Model tambahan: qwen4-max-preview via profil qwen_plan (akses terbukti dengan ping satu kata; qwen4-max tanpa "-preview" tidak ada, 404).
- Prompt, templat, urutan blok, kunci, tau 0,7, aturan analisis, dan urutan pilot -> dev -> val -> holdout (sekali) SAMA dengan model lain. Tidak ada yang diubah.
- max_tokens 4000 sejak awal (model besar kemungkinan bernalar; alasan sama dengan Amandemen 1) dan timeout 180 detik.
- Holdout belum pernah dijalankan pada model ini. Hasil holdout model lain sudah dilihat; tidak ada penyetelan terhadap hasil itu.
- Penguji luar (GPT-6.1 Sol via Codex, Gemini via Antigravity) memakai paket batch dengan prompt yang sama, satu observasi per klaim per batch, dan dilaporkan terpisah sebagai pembanding eksploratif.

## AMANDEMEN 3 (dicatat sebelum satu pun keluaran glm-5.3 dikumpulkan)
- Model tambahan: glm-5.3 via profil qwen_plan (akses terbukti dengan ping satu kata). glm-5.2 juga dapat diakses tetapi TIDAK dipakai; glm-5 dan glm-5.1 ditolak (403).
- Semua aturan sama seperti model lain: prompt, kunci, tau 0,7, analisis, dan urutan pilot -> dev -> val -> holdout (sekali). max_tokens 4000 sejak awal (kemungkinan bernalar), timeout 180 detik.
- Hasil holdout model lain sudah dilihat; tidak ada penyetelan terhadapnya.

## AMANDEMEN 4 (12 November 2026)
- glm-5.3 dikeluarkan dari desain (alasan biaya token); lihat CATATAN_DEVIASI.md D2. Model dalam perbandingan utama: qwen3.8-flash, deepseek-v4.1-flash, qwen4-max-preview (API), serta Gemini (Antigravity) dan GPT-6.1 Sol (Codex) sebagai pembanding jalur agen. Tidak ada analisis atau aturan lain yang diubah.

## AMANDEMEN 5 (12 November 2026; ditulis SEBELUM ada penilaian kelayakan yang masuk)
Penilaian kelayakan butir oleh tim (BUKAN uji validitas isi CVI).
- Nama dan status: "penilaian kelayakan butir oleh tim penulis". Tidak disebut CVI atau validitas isi oleh panel ahli, karena penilainya adalah penulis laporan dan mengetahui hipotesis. Keterbatasan ini ditulis di laporan.
- Penilai: tiga penulis (peneliti utama/engineering; penulis dengan latar psikometri; penulis bagian penulisan). Latar belakang masing-masing dilaporkan. Pemeriksaan eksternal (satu atau dua ahli di luar penulis) pada sebagian butir bersifat tambahan bila tersedia, dan dilaporkan terpisah.
- Objek: 40 pernyataan (10 pilot + 30 dev; tidak ada butir holdout) dan 5 pernyataan ubahan (draf), serta 30 pasangan bukti.
- Pilihan penilai per butir: LAYAK / PERLU_REVISI / TIDAK_LAYAK. PERLU_REVISI wajib disertai catatan apa yang direvisi. TIDAK_LAYAK wajib disertai alasan.
- Aturan keputusan (suara terbanyak, 3 penilai): >=2 LAYAK -> DIPAKAI; >=2 PERLU_REVISI -> DIREVISI; >=2 TIDAK_LAYAK -> KELUAR. Bila tiga suara berbeda (tidak ada mayoritas): didiskusikan oleh ketiga penilai dan dicatat; bila tetap tidak sepakat -> KELUAR (konservatif) dan jumlahnya dilaporkan. Catatan penilai yang berbeda dari mayoritas tetap disimpan.
- Pelaporan kesepakatan (norma statistik psikologi): persen kesepakatan per pasangan penilai dan keseluruhan, kappa Fleiss untuk tiga penilai, dan proporsi penilai yang menilai LAYAK per butir (dilaporkan sebagai angka deskriptif, bukan I-CVI/S-CVI baku).
- Kebutaan: penilai tidak membuka hasil model per butir untuk 40 butir sebelum selesai menilai. Penilai yang tidak terlibat merancang penelitian tidak diberi tahu hipotesis.
- Dampak pada analisis: analisis utama tetap memakai seluruh 294 klaim seperti praregistrasi. Analisis kepekaan terpisah: (a) tanpa butir berstatus KELUAR; (b) butir DIREVISI diuji ulang hanya pada model API (jalur agen tidak diuji ulang; keterbatasan ditulis) dan dilaporkan sebagai analisis terpisah, bukan digabung ke hasil konfirmatori. Butir holdout tidak tersentuh revisi.
- Penilaian jawaban benar (SUPPORTED/REFUTED/NEI) bertahap pada alat ALAT_VALIDASI_AHLI.html bersifat opsional dan buta; bila dipakai, dilaporkan terpisah dari penilaian kelayakan.

## AMANDEMEN 6 (12 November 2026; penyempurnaan Amandemen 5; ditulis sebelum data penilai kedua dan ketiga masuk)
- Daftar KELUAR untuk analisis kepekaan utama (ID_KELUAR.txt) hanya memuat butir berstatus FINAL (3 penilai, >=2 TIDAK_LAYAK) atau yang diputuskan lewat diskusi. Keputusan SEMENTARA (kurang dari 3 penilai) ditulis di berkas terpisah ID_KELUAR_SEMENTARA.txt dan hanya untuk pratinjau.
- Tiga suara berbeda: status PERLU_DISKUSI, TIDAK masuk ID_KELUAR sampai diskusi selesai. Hasil diskusi dicatat di berkas diskusi.csv (claim_id,jenis,keputusan_final,catatan). Bila setelah diskusi tetap tidak sepakat -> KELUAR (sesuai Amandemen 5).
- Dua penilai berbeda: PERLU_PENILAI_KETIGA, keputusan kosong, tidak masuk ID_KELUAR.
- Analisis kepekaan dua versi: (a) KELUAR FINAL saja; (b) ketat: seluruh butir yang menerima SETIDAKNYA SATU suara TIDAK_LAYAK (ID_KELUAR_KETAT.txt).
- PERLU_REVISI tanpa catatan atau TIDAK_LAYAK tanpa alasan tidak menghentikan perhitungan: suara tetap dihitung dan ditandai 'catatan hilang' di laporan sebagai peringatan.
- Kesepakatan dilaporkan terpisah untuk pernyataan JANGKAR dan UBAHAN, di samping gabungan.
