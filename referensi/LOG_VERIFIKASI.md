# Log verifikasi rujukan

Tanggal akses semua entri: 2026-11-13. Alat: WebFetch (halaman arXiv, halaman sprint, dokumentasi model), Crossref API (api.crossref.org/works?query.bibliographic=...), dan pengalihan DOI penerbit.

**Batasan metode.** WebFetch mengembalikan ringkasan yang dibuat model kecil, bukan HTML mentah. Daftar penulis dan judul dibaca dari ringkasan itu. Pemeriksaan ulang manual di halaman arXiv disarankan untuk entri berikut: Kadavath (36 penulis), MASK (16 penulis), dan ForecastBench (penulis "Chen Yueh-Han"). Isi makalah (angka, definisi, kesimpulan) TIDAK dibaca; log ini hanya memverifikasi identitas dan metadata.

## A. Rujukan boleh dikutip (bagian 1a)

| Kunci | URL dibuka | Hasil | Cocok dengan berkas lama? | Perbedaan / catatan |
|---|---|---|---|---|
| FEVER (1803.05355) | https://arxiv.org/abs/1803.05355 | Thorne, Vlachos, Christodoulopoulos, Mittal; judul "FEVER: a large-scale dataset for Fact Extraction and VERification"; v3 18 Des 2018 | Ya (penulis, tahun, ID) | Komentar "Updated version of NAACL2018 paper"; venue NAACL tidak tertulis eksplisit. Versi v3. |
| FEVEROUS (2106.05707) | https://arxiv.org/abs/2106.05707 | Aly, Guo, Schlichtkrull, Thorne, Vlachos, Christodoulopoulos, Cocarascu, Mittal; v3 12 Okt 2021 | Ya | Komentar: accepted NeurIPS 2021 D&B. Berkas lama hanya menulis "Aly et al.". |
| SciFact (2004.14974) | https://arxiv.org/abs/2004.14974 | Wadden, Lin, Lo, Wang, van Zuylen, Cohan, Hajishirzi; judul "Fact or Fiction: Verifying Scientific Claims"; v6 3 Okt 2020 | Ya | Komentar EMNLP 2020. Label NEI tidak diperiksa. |
| MASK (2503.03750) | https://arxiv.org/abs/2503.03750 | 16 penulis (Ren ... Hendrycks); judul "The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems"; v3 5 Jan 2026 | Ya (penulis pertama, tahun) | Versi terakhir 2026; tahun pengajuan pertama 2025 dipakai. |
| SycEval (2502.08177) | https://arxiv.org/abs/2502.08177 | Fanous, Goldberg, Agarwal, Lin, Zhou, Daneshjou, Koyejo; v4 19 Sep 2025 | Ya | Komentar AIES 2025. |
| ELEPHANT (2505.13995) | https://arxiv.org/abs/2505.13995 | Cheng, Yu, Lee, Khadpe, Ibrahim, Jurafsky; v2 29 Sep 2025 ditampilkan; v1 20 Mei 2025 | Ya; versi dikonfirmasi | Halaman memuat DOI Science 10.1126/science.aec8352 (tidak dibuka). Angka "~45 poin persen" tidak diperiksa. |
| Kalai et al. (2509.04664) | https://arxiv.org/abs/2509.04664 | Kalai, Nachum, Vempala, Zhang; 4 Sep 2025; v1 saja | Ya | Tidak ada venue. |
| ForecastBench (2409.19839) | https://arxiv.org/abs/2409.19839 | Karger, Bastani, "Chen Yueh-Han", Jacobs, Halawi, Zhang, Tetlock; v5 28 Feb 2025; v1 30 Sep 2024 | Ya (Karger pertama) | Nama "Chen Yueh-Han" perlu konfirmasi urutan nama. Judul lengkap: "ForecastBench: A Dynamic Benchmark of AI Forecasting Capabilities". |
| Kim, Kim, Thorne (2504.19622) | https://arxiv.org/abs/2504.19622 | Minsu Kim, Sangryul Kim, James Thorne; judul "From Evidence to Belief: A Bayesian Epistemology Approach to Language Models"; 28 Apr 2025 | Penulis ya; JUDUL TIDAK | Berkas lama: "Belief updating of LLMs with evidence". Judul halaman dipakai. |

## B. Rujukan perlu dibuka dulu (bagian 1b)

| Kunci | URL dibuka | Hasil | Cocok dengan berkas lama? | Perbedaan / catatan |
|---|---|---|---|---|
| Kadavath (2207.05221) | https://arxiv.org/abs/2207.05221 | 36 penulis; Kadavath pertama, Kaplan terakhir; v4 21 Nov 2022 | Ya (urutan penulis pertama sesuai) | Berkas menyebut urutan penulis berbeda antar sumber; halaman arXiv dipakai. Format APA: 19 pertama, elipsis, penulis terakhir. |
| Xiong (2306.13063) | https://arxiv.org/abs/2306.13063 | Xiong, Hu, Lu, Li, Fu, He, Hooi; v2 17 Mar 2024; v1 22 Jun 2023 | Ya | Komentar ICLR 2024. Judul lengkap: "Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs". |
| Tian (2305.14975) | https://arxiv.org/abs/2305.14975 | Tian, Mitchell, Zhou, Sharma, Rafailov, Yao, Finn, Manning; v2 24 Okt 2023 | Ya | Judul lengkap: "Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback". Komentar EMNLP 2023 camera ready. |
| Guo (1706.04599) | https://arxiv.org/abs/1706.04599 | Guo, Pleiss, Sun, Weinberger; v2 3 Agu 2017; v1 14 Jun 2017 | Ya | Komentar ICML 2017. |
| HoVer (2011.03088) | https://arxiv.org/abs/2011.03088 | Jiang, Bordia, Zhong, Dognin, Singh, Bansal; v2 16 Nov 2020 | Penulis ya; JUDUL BEDA | Berkas: "HoVer: multi-hop fact extraction and claim verification". Halaman: "HoVer: A Dataset for Many-Hop Fact Extraction And Claim Verification". Komentar: Findings of EMNLP 2020. |
| CLIMATE-FEVER (2012.00614) | https://arxiv.org/abs/2012.00614 | Diggelmann, Boyd-Graber, Bulian, Ciaramita, Leippold; v2 2 Jan 2021 | Ya | Komentar: workshop NeurIPS 2020. Angka 1.535 klaim tidak diperiksa. |
| AVeriTeC (2305.13117) | https://arxiv.org/abs/2305.13117 | Schlichtkrull, Guo, Vlachos; v3 8 Nov 2023 | Ya | Komentar NeurIPS 2023 D&B. Angka 4.568 dan kappa 0,619 tidak diperiksa. |
| FEVER Shared Task (1811.10971) | https://arxiv.org/abs/1811.10971 | Thorne, Vlachos, Cocarascu, Christodoulopoulos, Mittal; v2 30 Nov 2018 | Penulis ya; JUDUL BEDA | Berkas: "The FEVER2.0/Shared Task findings". Halaman: "The Fact Extraction and VERification (FEVER) Shared Task". Komentar: revisi dari versi prosiding FEVER workshop EMNLP 2018 (prosiding tidak dibuka). |

## C. Identitas 2602.14189 (bagian 1c)

| URL dibuka | Hasil | Catatan |
|---|---|---|
| https://arxiv.org/abs/2602.14189 | "Knowing When Not to Answer: Abstention-Aware Scientific Reasoning"; Abdaljalil, Serpedin, Kurban; 15 Feb 2026 (v1) | Identitas jelas; kandidat ditahan. Dua kalimat pertama abstrak tidak menyebut SciFact/PubMedQA seperti berkas lama. Tidak dimasukkan ke daftar final. |

Tidak ada rujukan lain di kelompok "tidak boleh dikutip" yang dibuka.

## D. Rujukan metode (bagian 1d, Crossref)

| Rujukan | Sumber | Hasil | Status |
|---|---|---|---|
| Brier 1950, Monthly Weather Review 78(1), 1-3, DOI 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 | Crossref (judul, jurnal, volume, halaman, DOI, tahun cocok); doi.org -> journals.ametsoc.org (HTTP 403) | Crossref hanya nama belakang "Brier" | BELUM_TERVERIFIKASI (inisial) |
| Cohen 1960, Educational and Psychological Measurement 20(1), 37-46, DOI 10.1177/001316446002000104 | Crossref; doi.org -> journals.sagepub.com (HTTP 403) | Crossref hanya nama belakang "Cohen" | BELUM_TERVERIFIKASI (inisial) |
| Fleiss 1971, Psychological Bulletin 76(5), 378-382, DOI 10.1037/h0031619 | Crossref; doi.org -> doi.apa.org -> psycnet.apa.org (halaman "Loading", tidak termuat) | Crossref hanya nama belakang "Fleiss" | BELUM_TERVERIFIKASI (inisial) |
| Efron 1979, The Annals of Statistics 7(1), 1-26, DOI 10.1214/aos/1176344552 | Crossref | Judul "Bootstrap Methods: Another Look at the Jackknife"; nama "B. Efron" | TERVERIFIKASI |
| Guo 2017 (ECE) | arXiv (lihat bagian B) | | TERVERIFIKASI |

## E. Dokumentasi resmi (bagian 1e)

| Dokumen | URL | Hasil | Status |
|---|---|---|---|
| Halaman sprint Apart Research | https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15 | Judul "AI x Epistemics Research Sprint | Apart Research"; PDF maks. 8 halaman di luar referensi dan lampiran; Track 1 sesuai berkas | TERVERIFIKASI |
| Alibaba Cloud Model Studio, daftar model | https://www.alibabacloud.com/help/en/model-studio/models | Judul "Supported Models and Capabilities Overview - Model Studio - Alibaba Cloud"; last updated 12 Nov 2026; memuat qwen3.8-flash, qwen4-max-preview, deepseek-v4.1-flash | TERVERIFIKASI |
| Alibaba Cloud, halaman qwen3.8-max | https://www.alibabacloud.com/help/en/model-studio/qwen3-8-max | Last updated 5 Nov 2026; ID qwen3.8-max (dan snapshot qwen3.8-max-0902); tidak memuat qwen3.8-flash atau qwen4-max-preview | Dibuka, tidak dipakai |
| DeepSeek, Models & Pricing | https://api-docs.deepseek.com/quick_start/pricing/ | Memuat deepseek-flash, deepseek-v4-pro; versi string DeepSeek-V4.1-Flash-1017; TIDAK memuat deepseek-v4.1-flash; tanpa tanggal | DITAHAN_TIDAK_COCOK |

Catatan tanggal pengujian model: 11 sampai 13 November 2026 berasal dari brief dan tidak diverifikasi di sini. Tidak ada pemanggilan model yang dilakukan.

Codex (GPT-6.1 Sol) dan Gemini (Antigravity): tidak diverifikasi, tidak dibuat rujukan, hanya catatan.

## F. Ketidaksesuaian dengan berkas lama (ringkas)

1. Kim, Kim, Thorne: judul berbeda total (berkas: "Belief updating of LLMs with evidence"; halaman: "From Evidence to Belief: A Bayesian Epistemology Approach to Language Models"). Halaman dipakai.
2. HoVer: judul berbeda (berkas: "multi-hop fact extraction and claim verification"; halaman: "A Dataset for Many-Hop Fact Extraction And Claim Verification").
3. FEVER Shared Task (1811.10971): judul berbeda (berkas: "The FEVER2.0/Shared Task findings"; halaman: "The Fact Extraction and VERification (FEVER) Shared Task").
4. ELEPHANT: berkas menyebut v1 dan v2 berbeda angka; halaman hanya menampilkan v2 (29 Sep 2025) dan v1 (20 Mei 2025) tanpa rincian perubahan. Versi yang dicatat: v2.
5. Kadavath: urutan penulis di berkas berbeda antar sumber; halaman arXiv: Kadavath pertama, 36 penulis.
6. ForecastBench: nama "Chen Yueh-Han" pada halaman; urutan nama perlu konfirmasi.
7. Brier, Cohen, Fleiss: inisial tidak terlihat (lihat bagian D).
8. Angka statistik dalam berkas (FEVER, FEVEROUS, CLIMATE-FEVER, AVeriTeC, ELEPHANT, SycEval, dsb.) TIDAK diperiksa; hanya identitas dan metadata yang diperiksa.
