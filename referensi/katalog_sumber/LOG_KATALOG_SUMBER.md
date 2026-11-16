# Log Katalog Sumber (S1)

Tanggal: 2026-11-15.

## 1. Berkas dan hash

| Berkas | SHA-256 sebelum | SHA-256 sesudah | Sama |
|---|---|---|---|
| pool_v2.jsonl | bfe5afef1c6334edbeed68447aba4835160b99652d6f15bb5c128b5d676bbeb8 | bfe5afef1c6334edbeed68447aba4835160b99652d6f15bb5c128b5d676bbeb8 | ya |
| kolam_bukti_v2_1.jsonl | b0b7ff8d17b7e236f76765ec390f101dccc0f7ac4e9e4578ce97ce43cf555b03 | b0b7ff8d17b7e236f76765ec390f101dccc0f7ac4e9e4578ce97ce43cf555b03 | ya |
| pasangan_v2_1.jsonl | be4b775be985e45beb0e4622458b7e116e6e9a1f67f89719b7ce9543a6487240 | be4b775be985e45beb0e4622458b7e116e6e9a1f67f89719b7ce9543a6487240 | ya |
| KATALOG_METADATA_LENGKAP.xlsx | 6312528964d264e0642586fa197c2bbe4d503d49cbd3cb01f59c33f20db2ea93 | 6312528964d264e0642586fa197c2bbe4d503d49cbd3cb01f59c33f20db2ea93 | ya |

Salinan katalog xlsx dibuat sekali ke folder _tmp dan dibaca dari salinan. Berkas asli di D: hanya dibaca dan tidak ditulis.

## 2. Masukan dan cakupan

- pool_v2.jsonl: 300 baris. Dipakai hanya field article_id, doi, title, lang_guess, domain, split, doc_id. Field sections, ladder, claim_original, claim_altered_draft tidak dibaca.
- pasangan_v2_1.jsonl: 294 baris. Kolom near_ev dan far_ev berisi ev_id dan semuanya ada di kolam (0 dan 0 yang tidak ditemukan).
- Artikel A: 294 article_id dari claim_article_id. Enam artikel di pool tanpa pasangan (B0295, B0296, B0297, B0298, B0299, B0300) tidak dimasukkan. Pemisahan split pool dan pasangan: 0 selisih.
- kolam_bukti_v2_1.jsonl: 595 baris. Dipakai field ev_id, doc_id, doi, title, lang_guess, domain. Field ladder dan abstrak tidak dibaca.
- Katalog: lembar 'Katalog Lengkap', 6090 baris data, 4195 DOI unik. Dibaca lewat XML bawaan Python (zipfile dan ElementTree), tanpa memasang paket tambahan. Kolom yang dipakai: Judul, Penulis, Tahun, Jurnal, Volume, Issue, DOI, Bahasa.

## 3. Metode

1. Normalisasi DOI: huruf kecil, awalan https://doi.org/, dx.doi.org, dan doi: dibuang.
2. Pencocokan katalog lewat DOI. Judul ternormalisasi hanya dipakai bila DOI kosong (tidak terjadi). DOI yang cocok dengan lebih dari satu baris katalog ditandai DOI_GANDA_KATALOG dan tidak diisi.
3. Kolom katalog diisi hanya bila sel katalog terisi. Tahun dinormalisasi dari bentuk 2023.0 menjadi 2023.
4. Crossref dipanggil hanya untuk DOI yang masih punya celah penulis, tahun, atau jurnal setelah katalog (626 DOI unik). Endpoint https://api.crossref.org/works/<DOI>, User-Agent 'research-reference-check', jeda 0,2 detik antar permintaan, tanpa mailto dan tanpa data pribadi. Bidang yang diambil: title, container-title, author (family, given atau name), tanggal terbit (issued, lalu published-print, published-online, published), volume, issue, page.
5. Gerbang judul: rekaman Crossref dipakai untuk mengisi celah hanya bila kemiripan judul dengan berkas bahan minimal 0,6 (difflib SequenceMatcher pada judul ternormalisasi). Bila tidak, rekaman dicatat tapi tidak dipakai.
6. Sumber tiap sel dicatat di kolom sumber_metadata (katalog, crossref, atau kosong).
7. Status: TANPA_DOI bila DOI kosong; LENGKAP bila penulis, tahun, judul, dan jurnal terisi; selain itu SEBAGIAN.
8. Judul tidak diubah. Judul katalog dan judul Crossref disimpan di kolom terpisah.

## 4. Permintaan Crossref

- DOI unik yang diperiksa: 626.
- Hasil di cache akhir: ok 593, TIDAK_DITEMUKAN_CROSSREF (404) 33, gagal 0.
- Kegagalan jaringan atau HTTP: 0 pada seluruh jalan. Batas 20 kegagalan beruntun tidak pernah tercapai.
- Skrip berjalan bertahap dengan batas waktu per jalan dan melanjutkan dari cache (crossref_cache.json). Jalan pertama dan kedua selesai sebagian, jalan ketiga menyelesaikan sisanya. Karena itu jumlah HTTP yang tepat lintas jalan tidak tercatat utuh di satu angka. Minimal 626 permintaan dilakukan, sesuai jumlah DOI unik.
- Permintaan 429 (rate limit) tidak tercatat. Bila terjadi, skrip menunggu 5 detik dan mengulang sekali.

## 5. Kejadian operasional

- Satu proses latar dihentikan secara manual setelah jalannya selesai. Cache diperiksa dan sah (626 entri), sehingga tidak ada data hilang.
- Skrip dijalankan ulang tiga kali untuk menyelesaikan sisa permintaan. Tidak ada keluaran yang ditulis sebelum semua DOI punya status final.
- Kesalahan kolom saat menulis CSV diperbaiki dan CSV dibangun ulang dari cache, tanpa memanggil Crossref lagi.

## 6. Hasil katalog dan Crossref

- Artikel A: DOI cocok 292, ganda 2, tidak cocok 0.
- Artikel B: DOI cocok 356, ganda 1, tidak cocok 0.
- Gerbang judul Crossref menolak pengisian: A 95, B 132.
- Konflik tahun katalog dan Crossref: A 39, B 47. Katalog dipertahankan.
- Konflik bahasa berkas bahan dan katalog: A 48, B 55. Dicatat, tidak dipilih.

## 7. Masalah dan batasan

- Judul berkas bahan sebagian keliru: berisi nama jurnal (misalnya satu judul hanya berbunyi nama jurnal) atau teks halaman. Judul seperti ini membuat gerbang Crossref menolak pengisian. Perlu dicek manusia.
- Katalog internal punya judul berbeda untuk 197 artikel A dan 252 artikel B. Semua dicatat, tidak dipilih.
- DOI di berkas bahan belum diverifikasi selain lewat Crossref. DOI yang tidak ditemukan Crossref (33 DOI) perlu dicek manual.
- Metadata tidak diverifikasi langsung ke penerbit.
