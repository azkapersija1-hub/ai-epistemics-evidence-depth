# Log verifikasi v2

Tanggal akses semua entri baru: 2026-11-15. Cakupan: rujukan yang ditahan (Brier 1950, Cohen 1960, Fleiss 1971), kandidat AURC, pengecekan ulang Guo 2017, Efron 1979, Karger 2024, Kim 2025, Ren 2025, serta konfirmasi status BELUM pada v1.

Alat: curl dari Bash (tanpa WebFetch). Permintaan hanya memuat DOI, ID arXiv, atau kata kunci topik. Tidak ada nama peneliti, data penelitian, email, atau parameter mailto yang dikirim. Pemanggilan dilakukan dengan HTTPS (permintaan HTTP ke export.arxiv.org dialihkan 301). Hasil disimpan sementara di folder scratchpad sesi, tidak di drive D:.

Batasan metode: hanya metadata (judul, penulis, tahun, volume, halaman) dan abstrak yang dibaca. Isi makalah tidak dibaca. Angka pada makalah tidak diperiksa.

## A. Rujukan yang ditahan (inisial penulis)

Sumber yang dibuka, per rujukan:

### A1. Brier 1950 (DOI 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2)

| Sumber | URL dibuka | Hasil |
|---|---|---|
| Crossref | https://api.crossref.org/works/10.1175/1520-0493(1950)078<0001:vofeit>2.0.co;2 | Penulis: given "GLENN W.", family "BRIER". Judul (huruf kapital): "VERIFICATION OF FORECASTS EXPRESSED IN TERMS OF PROBABILITY". Jurnal Monthly Weather Review; volume 78; issue 1; halaman 1-3; terbit 1950-01. |
| OpenAlex | https://api.openalex.org/works/doi:10.1175/1520-0493(1950)078<0001:vofeit>2.0.co;2 | display_name "Glenn W. Brier"; sumber Monthly Weather Review; tahun 1950. |
| Semantic Scholar | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2?fields=title,authors,year,venue | author "G. Brier"; tahun 1950. Field volume tidak didukung API (error), diganti tanpa volume. |
| Penerbit | https://journals.ametsoc.org (via doi.org) | HTTP 403. Tidak dibaca. (Sama seperti log v1.) |

Hasil: inisial G. W. konsisten di tiga sumber. Status VERIFIED.

### A2. Cohen 1960 (DOI 10.1177/001316446002000104)

| Sumber | URL dibuka | Hasil |
|---|---|---|
| Crossref | https://api.crossref.org/works/10.1177/001316446002000104 | Penulis: given "Jacob", family "Cohen". Judul "A Coefficient of Agreement for Nominal Scales". Educational and Psychological Measurement; volume 20; issue 1; halaman 37-46; terbit 1960-04. |
| OpenAlex | https://api.openalex.org/works/doi:10.1177/001316446002000104 | display_name "Jacob Cohen"; halaman 37-46. |
| Semantic Scholar | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1177/001316446002000104?fields=title,authors,year,venue | author "Jacob Cohen"; tahun 1960. |
| Penerbit | https://doi.org -> journals.sagepub.com | HTTP 403. Tidak dibaca. |

Hasil: inisial J. konsisten. Status VERIFIED.

### A3. Fleiss 1971 (DOI 10.1037/h0031619)

| Sumber | URL dibuka | Hasil |
|---|---|---|
| Crossref | https://api.crossref.org/works/10.1037/h0031619 | Penulis: given "Joseph L.", family "Fleiss". Judul "Measuring nominal scale agreement among many raters." Psychological Bulletin; volume 76; issue 5; halaman 378-382; terbit 1971-11. |
| OpenAlex | https://api.openalex.org/works/doi:10.1037/h0031619 | display_name "Joseph L. Fleiss"; halaman 378-382. |
| Semantic Scholar | https://api.semanticscholar.org/graph/v1/paper/DOI:10.1037/h0031619?fields=title,authors,year,venue | author "J. Fleiss"; tahun 1971. |
| Penerbit | https://doi.apa.org/doi/10.1037/h0031619 | HTTP 403. Tidak dibaca. Log v1 mencatat psycnet "Loading"; sesi ini 403. |

Hasil: inisial J. L. konsisten (S2 tanpa nama tengah). Status VERIFIED.

### A4. Perbedaan dengan log v1

| Butir | Log v1 (2026-11-13) | Sekarang (2026-11-15) |
|---|---|---|
| Brier, Cohen, Fleiss: nama depan | "Crossref hanya nama belakang" | Rekaman Crossref sekarang memuat nama depan (given). Catatan v1 tidak sesuai rekaman saat ini, sehingga catatan v1 dinyatakan usang. |
| Brier: judul | "Verification of forecasts..." | Crossref menulis huruf kapital. Kata-kata sama. Pada APA diubah ke kalimat (sentence case). |
| Efron 1979 | Crossref inisial "B." | Dicek ulang: OpenAlex raw "B. Efron", display "Bradley Efron"; S2 "B. Efron". Inisial B. konsisten. Tetap VERIFIED. |

## B. Kandidat primer AURC

Pencarian dilakukan dengan kata kunci topik, bukan judul dari ingatan:

| Pencarian | URL | Hasil |
|---|---|---|
| Judul memuat "selective classification" | https://export.arxiv.org/api/query?search_query=ti:%22selective%20classification%22&max_results=10 | Beberapa hasil, termasuk 1705.08500 "Selective Classification for Deep Neural Networks" (Geifman, El-Yaniv, 23 Mei 2017). |
| Abstrak memuat "risk-coverage" dan "AURC" | https://export.arxiv.org/api/query?search_query=abs:%22risk-coverage%22%20AND%20abs:%22AURC%22&max_results=10 | 2410.15361 "A Novel Characterization of the Population Area Under the Risk Coverage Curve (AURC) and Rates of Finite Sample Estimators" (Zhou dkk., 20 Okt 2024). |
| Abstrak memuat "area under the risk" | https://export.arxiv.org/api/query?search_query=abs:%22area%20under%20the%20risk%22&max_results=10 | Hasil sama (2410.15361) dan beberapa lain yang tidak relevan. |

### B1. Zhou dkk. 2024 (arXiv 2410.15361): VERIFIED (metadata)

| Sumber | URL dibuka | Hasil |
|---|---|---|
| arXiv API | https://export.arxiv.org/api/query?id_list=2410.15361 | Judul; penulis Han Zhou, Jordy Van Landeghem, Teodora Popordanoska, Matthew B. Blaschko; published 2024-10-20; versi v4 (updated 2025-09-03). Abstrak (ringkasan API) dibaca: menyebut AURC sebagai "foremost evaluation metric" untuk selective classifier. |
| arXiv abstract page | https://arxiv.org/abs/2410.15361 | citation_author: "Zhou, Han", "Van Landeghem, Jordy", "Popordanoska, Teodora", "Blaschko, Matthew B."; citation_date 2024/10/20. |
| Semantic Scholar | https://api.semanticscholar.org/graph/v1/paper/DOI:10.48550/arXiv.2410.15361?fields=title,authors,year | "Han Zhou", "Jordy Van Landeghem", "Teodora Popordanoska", "M. Blaschko"; tahun 2024. |
| OpenAlex | https://api.openalex.org/works/doi:10.48550/arXiv.2410.15361 | display "Han Qing Zhou", "Jordy Van Landeghem", "Teodora Popordanoska", "Matthew B. Blaschko"; terbit 2024-10-20. DOI ini dikenali OpenAlex. |

Perbedaan: nama tengah "Qing" hanya ada di OpenAlex. Arxiv dan S2 menulis "Han Zhou". Inisial H. konsisten. Entri memakai "Zhou, H." dan perbedaan nama tengah dicatat sebagai KONFLIK ringan untuk keputusan peneliti. Blaschko: S2 menulis "M. Blaschko" (inisial konsisten dengan "Matthew B."). Status: VERIFIED (metadata), catatan makalah karakterisasi, bukan sumber asal metrik.

Catatan: makalah ini membahas AURC sebagai metrik. Ia tidak menyatakan sebagai pengenal pertama metrik. Asal metrik belum terverifikasi.

### B2. Geifman dan El-Yaniv 2017 (arXiv 1705.08500): BELUM_TERVERIFIKASI

| Sumber | URL dibuka | Hasil |
|---|---|---|
| arXiv API | https://export.arxiv.org/api/query?id_list=1705.08500 | Judul "Selective Classification for Deep Neural Networks"; penulis Yonatan Geifman, Ran El-Yaniv; published 2017-05-23; v2 updated 2017-06-01. |
| Abstrak (ringkasan API) | sama | Membahas selective classification dan risk level yang diinginkan. Tidak menyebut AURC maupun risk-coverage curve. |

Keputusan: tidak dipakai sebagai sumber AURC karena abstrak tidak menyebut metrik itu. Venue dan DOI belum dicek (tidak dicari dengan ingatan).

### B3. Guo dkk. 2017 (arXiv 1706.04599): diperiksa ulang, tetap VERIFIED

| Sumber | URL dibuka | Hasil |
|---|---|---|
| arXiv API | https://export.arxiv.org/api/query?id_list=1706.04599 | Judul "On Calibration of Modern Neural Networks"; penulis Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger; published 2017-06-14; updated 2017-08-03 (v2); comment "ICML 2017". |

Sesuai dengan entri v1 (Guo, C., Pleiss, G., Sun, Y., & Weinberger, K. Q.). ECE: definisi di isi makalah tidak dibaca.

### B4. Karger dkk. 2024 (arXiv 2409.19839): urutan nama terkonfirmasi

| Sumber | URL dibuka | Hasil |
|---|---|---|
| arXiv API | https://export.arxiv.org/api/query?id_list=2409.19839 | Penulis: Ezra Karger, Houtan Bastani, "Chen Yueh-Han", Zachary Jacobs, Danny Halawi, Fred Zhang, Philip E. Tetlock. Judul "ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities". Published 2024-09-30. |
| arXiv abstract page | https://arxiv.org/abs/2409.19839 | citation_author: "Yueh-Han, Chen" (family Chen, given Yueh-Han). |
| OpenAlex | https://api.openalex.org/works/doi:10.48550/arXiv.2409.19839 | raw_author_name "Yueh-Han, Chen". |

Keputusan: APA "Chen, Y.-H." dikonfirmasi oleh dua sumber (arXiv abstract dan OpenAlex raw). Pertanyaan urutan nama di log v1 ditutup.

### B5. Kim, Kim, Thorne 2025 (arXiv 2504.19622) dan Ren dkk. 2025 (arXiv 2503.03750)

- Kim: arXiv API menulis Minsu Kim, Sangryul Kim, James Thorne; judul "From Evidence to Belief: A Bayesian Epistemology Approach to Language Models"; published 2025-04-28. Sesuai entri v2.
- Ren: tidak diperiksa ulang pada sesi ini (tidak ada perubahan yang diminta); status v1 VERIFIED dipertahankan.

## C. Status BELUM pada v1 yang tidak diubah

- Abdaljalil dkk. 2026 (2602.14189): tetap kandidat, tidak dikutip. Keputusan peneliti.
- Murphy 1973, Naeini 2015: belum dibuka. Tidak dicari pada sesi ini.
- Inspect AI, Forethought, daftar dibatasi brief: tidak dibuka.
- DeepSeek pricing page: tetap DITAHAN_TIDAK_COCOK, tidak dikutip.

## D. Hasil ringkas

| Rujukan | Status v2 | Sumber utama |
|---|---|---|
| Brier 1950 | VERIFIED | Crossref, OpenAlex, S2 |
| Cohen 1960 | VERIFIED | Crossref, OpenAlex, S2 |
| Fleiss 1971 | VERIFIED | Crossref, OpenAlex, S2 |
| Zhou dkk. 2024 (AURC) | VERIFIED (metadata; nama tengah beda, tidak dipilih) | arXiv API, arXiv abs, S2, OpenAlex |
| Geifman dan El-Yaniv 2017 (kandidat AURC) | BELUM_TERVERIFIKASI | arXiv API |
| Guo dkk. 2017 (ECE) | VERIFIED (dicek ulang) | arXiv API |
| Efron 1979 | VERIFIED (inisial dicek ulang) | Crossref, OpenAlex, S2 |
| Karger dkk. 2024 | VERIFIED (urutan nama dikonfirmasi) | arXiv API, arXiv abs, OpenAlex |
| Kim, Kim, Thorne 2025 | VERIFIED (dicek ulang) | arXiv API |

## E. Akses gagal dan catatan

- Halaman penerbit (AMS, SAGE, APA) mengembalikan HTTP 403 pada sesi ini. Tidak dicoba dengan cara lain.
- Semantic Scholar menolak field "volume" (error "Unrecognized or unsupported fields"). Permintaan diulang tanpa field itu.
- OpenAlex dan arXiv API dapat diakses. arXiv API memerlukan HTTPS (HTTP 301).
- Tidak ada konflik inisial pada Brier, Cohen, Fleiss, Efron, Karger. Konflik ringan nama tengah hanya pada Zhou (dicatat).
- Tidak ada rujukan yang diisi dari ingatan. Tidak ada kutipan sekunder yang dipakai.
