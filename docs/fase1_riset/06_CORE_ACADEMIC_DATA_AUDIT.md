# 06 Audit data: core_academic (baca-saja)

Metode: SQLite `mode=ro&immutable=1` (tidak membuat -shm/-wal). Skrip: `_data_audit/profil_core_academic.py`; keluaran mentah: `_data_audit/core_academic_profile.json` dan `core_academic_profile_tambahan.json`. Tidak ada embedding dibangun ulang, tidak ada inferensi, tidak ada perubahan DB.

## Lokasi dan versi
- **Kanonik (dipakai):** `D:\PELATIHAN AI ART\implementation\art_python\core_academic_db\core_academic.db` (2,24 GB, 14 Agustus 2026), bersama cadangan `.bak_preclassify_20260814` dan `similarity_engine/similarity_engine.db`.
- **Salinan lama JANGAN dipakai:** `...\RND_Formula_Discovery\raw_material\academic_knowledge\core_academic.db` (1,6 GB, 9 Agustus; embedding belum lengkap, 219.256 vektor).
- Catatan peringatan di folder lama menunjuk `D:/proyek baru/implementation/art_python/...`; yang ada di disk kini di `D:\PELATIHAN AI ART\implementation\art_python\...`.

## Angka utama (dihitung)
| Ukuran | Nilai |
|---|---|
| Dokumen | **24.054** (bukan 20.000) |
| Judul unik (dinormalisasi) | 21.875 |
| Dokumen berDOI | 13.367 (55,6%); DOI unik 12.135 |
| Kelompok DOI ganda | 187 kelompok, 1.232 dokumen kelebihan |
| Asal DOI | text-scan 12.116; arxiv-inferred 1.251; kosong 10.687 |
| Genre | article 23.656; policy-brief 237; book 161 |
| Chunk | 319.032 (rata-rata 798 karakter, maks 1.200); dokumen punya chunk 23.911 |
| Embedding | 306.821 vektor `mxbai-embed-large`, 1.024-d, cakupan chunk 96,2% |

## Ketersediaan bagian teks (dokumen yang punya chunk bagian itu)
abstract 23.344; conclusion 23.216; results 10.555; methodology 9.179; discussion 7.782; limitations 1.115. Punya abstract + results + conclusion sekaligus: **10.180**; di antaranya berDOI: **5.450** (4.800 DOI unik). Ini kandidat realistis untuk klaim yang bukti dan hasilnya dapat diverifikasi.

## Domain (taksonomi internal)
Social Sciences 10.397; Formal Sciences 6.040; Natural Sciences 3.111; Health Sciences 1.911; Needs Review 1.520; null 588; Engineering 487.

## Bahasa dan tahun
- Bahasa (heuristik kata fungsi, 20.000 dokumen pertama): Inggris 8.326; Indonesia 7.511; tak pasti 4.163. Kasar, bukan deteksi terverifikasi.
- Tahun: kolom TIDAK ADA. Heuristik nama berkas hanya menangkap ~22% dan menunjukkan lonjakan mencurigakan (2016: 2.068; 2018: 1.929), kemungkinan artefak penamaan. **Metadata tahun tidak layak dipakai** tanpa pengayaan (mis. Crossref), yang belum dilakukan.

## Kualitas metadata
44% dokumen tanpa DOI; penulis dan tahun bukan kolom; 187 kelompok DOI ganda perlu dedupe sebelum split berbasis artikel; 1.520 dokumen berlabel "Needs Review".

## Retrieval embedding
Layak teknis, tetapi `mxbai-embed-large` berbeda dari `embeddinggemma-2:740m` (184 buku TLS); jangan campur ruang vektor.

## Hak cipta dan redistribusi
Korpus adalah PDF artikel koleksi pribadi. Teks penuh tidak boleh didistribusikan ulang; repo publik hanya memuat DOI, ID dokumen, dan kutipan pendek wajar. Lisensi per artikel belum diperiksa.

## Kesimpulan
- Korpus adalah **sumber bahan, bukan 24 ribu item uji**. Kandidat realistis: ~5.450 dokumen berDOI dengan abstract+results+conclusion.
- Label SUPPORTED/REFUTED/NEI tidak ada bawaan; perlu kerja manusia atau aturan penyusunan yang dipraregistrasi.
- Sebelum dipakai: dedupe DOI, pengayaan tahun, split berbasis artikel, pemeriksaan lisensi.
