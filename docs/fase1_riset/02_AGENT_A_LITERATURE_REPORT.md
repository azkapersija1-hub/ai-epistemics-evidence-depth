# AGENT A: Laporan Literatur (AI x Epistemics Research Sprint 2026)

Tanggal akses: 2026-11-11. Peran: peneliti literatur, bukan subjek eksperimen. Tidak ada model yang dijalankan, tidak ada API uji, tidak ada Brier dari uji, tidak ada dataset final. Folder Agent B tidak dibuka.

Catatan akses: WebFetch ke apartresearch.com ditolak oleh tool (domain dianggap tidak terverifikasi), sehingga halaman sprint dibaca lewat Browser pane. Seluruh teks halaman sprint (Overview, Resources, Guidelines) terbaca penuh, sehingga tingkat kepastiannya TEKS_LENGKAP. Tab Schedule dan daftar pembicara tidak dibuka lebih lanjut.

Tingkat kepastian pada laporan ini: TEKS_LENGKAP (halaman sprint), ABSTRAK_SAJA (halaman arXiv yang dibuka, teks lengkap tidak dibaca), RINGKASAN_WEB (hanya hasil pencarian atau ringkasan pihak ketiga). Matriks lengkap ada di LITERATURE_EVIDENCE_MATRIX_AGENT_A.csv.

## 1. Persyaratan resmi sprint (TEKS_LENGKAP)

- Jadwal: online, 13-15 November 2026. Batas submisi Minggu 15 November 2026 pukul 23.59 AoE. Pemenang diumumkan sekitar 1-2 minggu setelah batas penilaian.
- Hadiah: total $2,000 (juara 1 $1,000; juara 2 $500; juara 3 $300; juara 4 dan 5 masing-masing $100).
- Tim 1-5 orang dianjurkan. Tiap orang maksimal dua proyek. Pekerjaan sebelum sprint boleh dibangun di atasnya, tetapi wajib diberi tanda preexisting di README dan laporan. Pengungkapan pekerjaan terdahulu yang tidak jelas dapat berujung diskualifikasi.
- Format wajib: laporan PDF memakai template resmi (tautan di tab Guidelines; template di email penerimaan bisa usang). Maksimal 8 halaman, tidak termasuk referensi dan lampiran. Judul dan abstrak 150-250 kata. Nama penulis dan afiliasi. Lampiran wajib "Limitations and Dual-Use / Ethical Considerations". Opsional: repo GitHub publik, video demo 3-5 menit.
- Struktur yang disarankan: Introduction, Related Work, Methodology (cukup detail untuk direplikasi), Results (kuantitatif, dengan varians dan baseline), Discussion, lampiran Limitations/Dual-Use, References.
- Penggunaan AI diizinkan. Tim bertanggung jawab penuh; hasil atau referensi yang dibuat-buat dapat mendiskualifikasi proyek.
- Submisi ulang dengan judul yang sama menggantikan versi lama, dilakukan lewat formulir sebelum batas, bukan lewat email.
- Proyek belum tampil di situs sebelum penjurian karena alasan infohazard. Konfirmasi lewat email.
- Rubrik (tiga dimensi, skor 1-5, tanpa bobot yang dinyatakan):
  - Impact Potential & Innovation: seberapa penting bila berhasil dan seberapa baru. Skor 4-5 mensyaratkan kebaruan nyata, bukan replikasi karya terbaru.
  - Execution Quality: metodologi, implementasi, dan temuan. Skor 3 mensyaratkan metodologi masuk akal, hasil dapat ditafsirkan, dan keterbatasan diakui. Skor 4 mensyaratkan validasi yang meyakinkan.
  - Presentation & Clarity: kejelasan masalah, metode, temuan, dan keterbatasan.
- Masalah yang didorong penyelenggara untuk Track 1 (Model Epistemics & Decision-Making Evals): apakah model mengetahui seberapa kuat klaimnya; apakah keyakinan dapat diukur dan diverifikasi terhadap kenyataan; celah antara yang tersirat dan yang bisa dipertahankan (overselling, flip-flopping, salah menyajikan bukti); apakah peringkat pada benchmark kejujuran memprediksi kualitas keputusan; bagaimana benchmark tetap bermakna dan bagaimana celah yang membuatnya bisa diakali bisa ditunjukkan dan ditutup.
- Contoh proyek Track 1 dari halaman sprint: MisleadBench (benchmark multi-giliran untuk gap antara yang tersirat dan yang dipertahankan); Confidence Audit (kalibrasi keyakinan rekomendasi pada hasil yang datang belakangan); FlipRate (kurva perubahan jawaban di bawah sanggahan bertingkat, memisahkan pembaruan yang sah dari menyerah); Epistemic virtue eval suite (dibangun sebagai Inspect tasks); protokol Pasal 5 EU AI Act.

Implikasi: Confidence Audit dan FlipRate sudah ada sebagai contoh proyek resmi. Judul apa pun yang memakai kalibrasi dan sanggahan akan tampak tumpang tindih kecuali ada sudut yang jelas (lihat bagian 4).

Rujukan halaman: https://apartresearch.com/sprints/ai-x-epistemics-research-sprint-2026-11-13-to-2026-11-15 (dibuka 2026-11-11, Overview, Resources, Guidelines).

## 2. Telaah sumber Track 1 dan Resources

Dibuka sebagai arXiv abstrak; teks lengkap tidak dibaca, sehingga desain eksperimen dinyatakan dengan tingkat kepastian ABSTRAK_SAJA.

- MASK (Ren et al., arXiv 2503.03750). Pertanyaan: apakah kejujuran dapat diukur terpisah dari akurasi. Hasil utama: model akurat di benchmark kebenaran tetap sering berbohong di bawah tekanan; skala menaikkan akurasi tetapi tidak kejujuran; representation engineering membantu sebagian. Keterbatasan dan rumus skor belum saya baca. Hubungan: kerangka pemisahan keyakinan dan ucapan. Kepastian: ABSTRAK_SAJA.
- SycEval (Fanous et al., arXiv 2502.08177). Dataset: AMPS dan MedQuad. Model: ChatGPT-4o, Claude-Sonnet, Gemini-1.5-Pro. Hasil di abstrak: sikofansi keseluruhan 58,19 persen; progresif 43,52 persen; regresif 14,66 persen. Sanggahan preemptif lebih sering memicu sikofansi. Keterbatasan dan metode judge belum dibaca. Angka pihak ketiga yang berbeda belum saya cek. Hubungan: regresif (benar menjadi salah) harus dipisahkan dari pembaruan yang sah. Kepastian: ABSTRAK_SAJA.
- ELEPHANT (Cheng et al., arXiv 2505.13995). Fokus pada sikofansi sosial (mempertahankan muka pengguna), bukan kebenaran fakta. Dataset: OEQ dan r/AmITheAsshole. Versi 2 menyebut 11 model dan sekitar 45 poin persen lebih banyak mempertahankan muka dibanding manusia. Versi 1 memberi angka berbeda (47 persen dan 42 persen). Kepastian: ABSTRAK_SAJA.
- Why Language Models Hallucinate (Kalai, Nachum, Vempala, Zhang, arXiv 2509.04664). Argumen: evaluasi biner memberi ganjaran pada tebakan dibanding abstensi. Usul: menilai ulang benchmark yang ada. Implikasi desain: bila skor menghukum "not enough information", hasilnya sudah bias. Bukti formal dan eksperimen belum dibaca. Kepastian: ABSTRAK_SAJA.
- ForecastBench (Karger et al., arXiv 2409.19839, ICLR 2025). Sekitar 1.000 pertanyaan yang diperbarui otomatis; 200 pertanyaan sampel untuk perbandingan manusia dan LLM. Pakar mengungguli LLM terbaik (p < 0,001 menurut abstrak). Metrik belum saya pastikan (Brier atau bukan). Kepastian: ABSTRAK_SAJA.
- Epistemic virtue evals (Forethought, Design Sketches for Collective Epistemics, 2025). Usulan suite untuk kalibrasi, honest uncertainty, dan ketahanan manipulasi. Sumber primer belum dibuka; hanya wiki sekunder. Kepastian: RINGKASAN_WEB. Status TIDAK_TERVERIFIKASI untuk isi primer.
- Inspect AI (UK AI Security Institute). Kerangka kerja evaluasi open source, MIT, Python 3.10+. Homepage tidak dibuka; fakta hanya dari PyPI dan pihak ketiga. Status: TIDAK_TERVERIFIKASI penuh.
- Benchmark lain di daftar Resources (DarkBench, Petri dan Bloom, Community Notes, C2PA, EU AI Act Pasal 5) tidak saya buka. Tidak dimasukkan ke matriks sebagai sumber terverifikasi.

## 3. FEVER dan benchmark pendukung, serta literatur 2023-2026

Verifikasi FEVER:
- FEVER (Thorne, Vlachos, Christodoulopoulos, Mittal; arXiv 1803.05355; NAACL 2018). 185.445 klaim, label SUPPORTED / REFUTED / NOTENOUGHINFO, klaim dibuat dengan mengubah kalimat Wikipedia. Baseline 31,87 persen dengan bukti benar dan 50,91 persen tanpa bukti (abstrak). Kepastian ABSTRAK_SAJA.
- FEVER Shared Task (arXiv 1811.10971): 23 tim, 19 melampaui baseline (RINGKASAN_WEB, daftar sudah terlihat di hasil pencarian).
- FEVEROUS (Aly et al., arXiv 2106.05707; NeurIPS 2021 Datasets and Benchmarks). 87.026 klaim, label termasuk NOT ENOUGH INFO, bukti dari teks dan sel tabel Wikipedia. Baseline mendapat bukti dan verdict benar untuk 18 persen klaim (abstrak).

Benchmark pendukung:
- SciFact (Wadden et al., arXiv 2004.14974; EMNLP 2020): sekitar 1,4 ribu klaim ilmiah yang ditulis pakar, dengan abstrak, label, dan rasionalisasi. Relevan untuk domain akademik. Catatan penting: label NEI belum saya konfirmasi dari halaman yang dibuka; perlu dicek sebelum dipakai.
- HoVer (Jiang et al., arXiv 2011.03088; Findings of EMNLP 2020): klaim multi-hop dengan bukti dari hingga empat artikel Wikipedia, label Supported / Not-Supported. Kinerja turun saat jumlah hop naik (RINGKASAN_WEB dari hasil pencarian).
- CLIMATE-FEVER (Diggelmann et al., arXiv 2012.00614): 1.535 klaim iklim nyata; klaim nyata lebih sulit dibanding klaim sintetis (RINGKASAN_WEB).
- AVeriTeC (Schlichtkrull, Guo, Vlachos; arXiv 2305.13117; NeurIPS 2023): 4.568 klaim nyata dari 50 organisasi pengecek fakta, dengan bukti web dan justifikasi. Kappa verdict 0,619 (RINGKASAN_WEB).

Kalibrasi dan kepercayaan LLM (sumber primer tidak sepenuhnya dibuka):
- Kadavath et al. (arXiv 2207.05221): model kalibrasi cukup baik pada pilihan ganda; P(IK) generalisasi antar-tugas tetapi kurang kalibrasi di tugas baru. Urutan penulis berbeda antar sumber.
- Xiong et al. (arXiv 2306.13063; ICLR 2024): confidence verbal cenderung terlalu tinggi; metode berbasis konsistensi dan hibrida lebih baik. Versi berbeda menyebut daftar model yang berbeda.
- Tian et al. (arXiv 2305.14975; EMNLP 2023): confidence verbal sering lebih terkalibrasi dibanding probabilitas token; menghasilkan beberapa jawaban dulu lalu temperature scaling membantu. Detail eksperimen belum saya periksa langsung.

Bukti dan pembaruan keyakinan (2025):
- Kim, Kim, Thorne (arXiv 2504.19622, 2025): model mengikuti Bayes untuk bukti benar, tetapi melanggar asumsi Bayes pada jenis bukti lain. Keyakinan bisa tinggi setelah bukti kuat tanpa akurasi yang andal. Daftar model dan taksonomi bukti belum dibaca penuh.

Pencarian literatur 2023-2026 yang belum terverifikasi penuh (hanya RINGKASAN_WEB):
- Abstention dan kalibrasi dalam verifikasi klaim ilmiah: arXiv 2602.14189 (Feb 2026), memakai SciFact dan PubMedQA, menyatakan abstensi berbasis confidence menurunkan risiko pada cakupan sedang. Ini tumpang tindih kuat dengan usul ketiga.
- Atomic+Search (uncertainty-aware web-conditioned fact-checking) dengan label NEI pada PubMedFact1k, BIONLI-300, CLIMATE-FEVER; hanya dari ulasan pihak ketiga.
- DeepSciVerify (arXiv 2605.27710), CalBrief (arXiv 2606.27383), dan survei arXiv 2608.05179 tentang verification gap pada agen riset: hanya dari ringkasan.
- Belief revision: AGM-Bench (halaman ICLR 2026, bukan arXiv), arXiv 2507.03120 (choice-supportive bias dan bobot tidak simetris pada saran), arXiv 2511.13240 (koherensi keyakinan dan tindakan). Semua hanya dari cuplikan.

Tidak ditemukan paket literatur 2025 yang langsung menguji calibration plus NEI plus counterevidence pada klaim akademik dengan Brier multikelas. Ini bukan bukti bahwa celahnya kosong, karena pencarian saya terbatas.

## 4. Research gap yang nyata dan batasannya

Jawaban singkat per pertanyaan:

- Apa yang belum diketahui tentang kualitas penilaian bukti LLM: cukup banyak sudah diketahui untuk fakta umum dan pilihan ganda (Kadavath, Xiong, Tian). Yang kurang: penilaian tiga-label pada klaim akademik dengan bukti yang bisa kontradiktif, dibandingkan lintas model, dengan skor probabilistik multikelas.
- Apakah evaluasi keyakinan pada klaim akademik sudah banyak: belum terlihat banyak dari pencarian saya. Namun abstention berbasis confidence pada SciFact (2602.14189) sudah ada, sehingga gap harus dinyatakan dengan tepat, bukan "belum pernah".
- Kelemahan benchmark verifikasi bukti: FEVER dan FEVEROUS bersifat sintetis atau berbasis Wikipedia. Label NEI sering memuat campuran "tidak ada bukti" dan "bukti tidak cukup untuk klaim yang kompleks". Benchmark berbasis skor biner (HoVer, Kalai) menghukum abstensi.
- Apakah evaluasi berbasis sumber akademik berbeda dari fact-checking umum: ya secara substansi, karena klaim ilmiah sering bergantung pada kondisi, ukuran sampel, dan batasan metode, sehingga "bukti tidak cukup" lebih sering dan bersifat metodologis. Ini perlu dikonfirmasi pada data, bukan diasumsikan.
- Apakah sinyal tambahan seperti F11x dapat memberi kontribusi yang belum ditunjukkan metode lain: saya tidak menemukan literatur tentang F11x di sumber yang saya periksa. Status: TIDAK_TERVERIFIKASI. Tidak boleh diasumsikan valid. Kontribusinya hanya bisa diklaim bila ada baseline tanpa F11x yang didefinisikan sebelum pengujian dan ablasi yang jelas.
- Menghindari benchmark yang mengulang eksperimen terdahulu: pakai SciFact atau sumber yang sudah ada sebagai data, tetapi tambahkan dimensi yang belum diukur (probabilitas multikelas, kondisi bukti kontradiktif yang dikontrol, lintas model). Hindari klaim "pertama kali" tanpa pencarian ulang.

Celah yang paling defensif menurut saya: kalibrasi multikelas (Brier) pada klaim akademik dengan tiga label, dengan kondisi bukti yang dikontrol (dukung, bantah, tidak cukup, dan bukti kontradiktif), lalu membandingkan keyakinan verbal dengan probabilitas yang diturunkan dari sampel. Ini mengikuti jalur Xiong dan Tian, memakai label FEVER, dan membedakan NEI dari salah. Cakupan harus sempit agar selesai dalam tiga hari.

## 5. Alternatif judul dan penilaian analitis

Penilaian: kebaruan (K), keselarasan Track 1 (T1), keterukuran (U), ketersediaan data (D), kelayakan tiga hari (L), risiko tumpang tindih (R). Ini penilaian kualitatif dan bukan skor resmi.

(1) When Evidence Disagrees: Evaluating LLM Evidence Judgment, Confidence Calibration, and Response to Counterevidence
- K: sedang. Kombinasi tiga dimensi sudah ada secara terpisah (Kim et al. untuk belief; Kalai untuk abstensi; Xiong untuk kalibrasi). Kombinasi itu sendiri bisa menjadi kontribusi bila ada desain yang jelas.
- T1: baik (cocok dengan "belief updating" dan "decision quality").
- U: baik bila bukti kontradiktif dibuat dengan kontrol (tiga level pengaruh).
- D: FEVER, SciFact, atau AVeriTeC dapat dipakai; perlu dicek apakah kontradiksi terkontrol tersedia.
- L: berisiko. Tiga dimensi dalam tiga hari terlalu banyak. Perlu dipangkas menjadi dua.
- R: sedang-tinggi, karena Confidence Audit dan FlipRate mengarah ke sini.
- Pendapat: judul ini layak dipertahankan sebagai payung, tetapi lingkup perlu dibatasi ke satu dimensi utama.

(2) Does External Evidence Verification Improve LLM Calibration? A Controlled Comparison With and Without F11x
- K: belum bisa dinilai, karena F11x belum terdefinisi di sumber yang saya periksa.
- T1: sedang (lebih ke Track 2, trust infrastructure, daripada Track 1 murni).
- U: hanya bila F11x punya definisi, fitur, dan cara evaluasi yang dibekukan sebelum uji. Tanpa itu, hasilnya tidak bisa diukur dengan jujur.
- D: bergantung pada F11x. Fitur 15 dimensi harus tersedia dan tidak boleh dilatih pada data uji.
- L: sulit. Perlu ansambel logistik dilatih di luar data uji dan dicocokkan dengan baseline tanpa F11x.
- R: rendah terhadap literatur, tetapi tinggi terhadap kebocoran data bila F11x dibangun dari penelitian yang sama.
- Pendapat: hanya layak bila F11x dapat dioperasionalkan, sesuai syarat yang Anda tulis. Sebagai judul kedua atau cadangan, bukan judul utama. Bila F11x belum jelas, jangan dipakai.

(3) Knowing When Evidence Is Insufficient: A Cross-Model Evaluation of Academic Evidence Judgment and Confidence
- K: sedang. Abstensi pada SciFact sudah diteliti (2602.14189), sehingga kebaruan ada di perbandingan lintas model dan skor Brier multikelas, bukan di gagasan abstensi.
- T1: sangat baik. Cocok dengan "knowing how solid its claims are".
- U: baik. NEI dapat diukur dengan label dan Brier multikelas.
- D: SciFact dan FEVER tersedia. Perlu dicek apakah SciFact memiliki label NEI; bila tidak, NEI harus dibangun dari klaim yang abstraknya tidak menjawab.
- L: layak bila lingkupnya dua atau tiga model dan satu benchmark.
- R: sedang-tinggi terhadap 2602.14189 dan Track 1 contoh.
- Pendapat: menurut saya ini kandidat paling kuat dari tiga, dengan syarat diperjelas sebagai perbandingan lintas model plus skor multikelas, dan NEI dibangun secara eksplisit.

(4) Alternatif yang saya usulkan: Calibration Under Controlled Evidence Strength: Brier Scores for Three-Label Academic Claim Verification
- K: sedang-tinggi bila dibandingkan dengan Confidence Audit yang mengukur hasil belakangan.
- T1: baik.
- U: sangat baik karena bukti dikontrol berjenjang.
- D: SciFact atau data terkontrol sendiri; perlu dicek lisensi.
- L: layak.
- R: sedang.

(5) Alternatif kedua: Does Verbalised Confidence Track Evidence Strength? A Flip-Curve Study on Academic Claims
- K: rendah-sedang; sangat dekat dengan FlipRate.
- Pendapat: tidak disarankan kecuali sudut akademik kuat.

## 6. Teori yang benar-benar dibutuhkan dan variabel utama

Teori yang relevan:
- Evidence-based judgment: label dan rasionalisasi, dengan kondisi bukti yang eksplisit (FEVER, SciFact).
- Confidence calibration: Brier multikelas dan ECE, dengan confidence verbal dan probabilitas token dibandingkan secara terpisah (Xiong, Tian, Kadavath).
- Appropriate abstention: NEI dan abstensi selektif. Perhatikan bahwa penilaian skor biner dapat menghukum abstensi (Kalai).
- Evidence sensitivity: apakah jawaban berubah sebanding dengan kekuatan bukti. Ini adalah kebutuhan untuk membedakan pembaruan yang sah dari sikofansi.
- Belief updating: Bayes adalah rujukan normatif, tetapi Kim et al. menunjukkan model tidak selalu mengikutinya. Gunakan Bayes sebagai pembanding, bukan sebagai kebenaran.
- Resistance to misleading counterevidence: bukti yang menyesatkan harus dibedakan dari bukti benar yang kontradiktif (SycEval, MASK).

Variabel utama yang disarankan untuk proyek tiga hari (maksimal dua):
1. Label (dukung, bantah, tidak cukup) sebagai variabel respons utama, dengan Brier multikelas dan akurasi sebagai pendukung.
2. Kekuatan dan arah bukti kontradiktif sebagai variabel manipulasi, dengan tiga level terkontrol.
Variabel sekunder: jenis confidence (verbal vs token) dan model. Hindari terlalu banyak variabel.

Peringatan konseptual: keluaran teks model tentang keyakinan bukan keyakinan internal manusia. Confidence verbal adalah laporan, bukan probabilitas bayesian yang dimiliki model. Istilah "keyakinan model" dalam laporan harus diberi tanda kutip atau didefinisikan sebagai keluaran terukur.

## 7. Daftar yang tidak sempat atau tidak bisa diverifikasi

- Teks lengkap FEVER, FEVEROUS, SciFact, HoVer, CLIMATE-FEVER, AVeriTeC, Kadavath, Xiong, Tian, MASK, SycEval, ELEPHANT, Kalai, ForecastBench, Kim et al. belum dibaca penuh. Yang dibaca adalah abstrak arXiv atau ringkasan hasil pencarian.
- Label NEI pada SciFact belum dikonfirmasi.
- Epistemic virtue evals (Forethought) dan dokumen primer Design Sketches belum dibuka. Hanya wiki sekunder.
- Inspect AI: homepage belum dibuka. Klaim adopsi (METR, Apollo) hanya dari pihak ketiga, tidak diverifikasi.
- DarkBench, Petri dan Bloom, Community Notes, C2PA, Pasal 5 EU AI Act, MisleadBench, FlipRate, dan Confidence Audit belum dibuka sebagai karya asli, kecuali sebagai judul di halaman sprint.
- Angka sikofansi pada SycEval versi pihak ketiga (58,19 persen dan lainnya) berbeda antara sumber. Hanya angka di abstrak arXiv yang saya sebut.
- ELEPHANT v1 dan v2 memberi angka berbeda. Saya hanya melaporkan v2 dan menyebutkan perbedaan.
- arXiv 2602.14189, 2605.27710, 2606.27383, 2608.05179, 2507.03120, 2511.13240, AGM-Bench, Atomic+Search, dan Belief-R: hanya RINGKASAN_WEB, tidak dibuka. Jangan dikutip sebelum diperiksa langsung.
- F11x: tidak ditemukan di literatur yang saya periksa. Status TIDAK_TERVERIFIKASI. Asal, definisi, dan validitasnya tidak dapat saya nilai.
- Metrik ForecastBench (Brier atau bukan) belum dipastikan.

## 8. Pernyataan jujur tentang model yang saya gunakan

Saya adalah Haiku 5.5 dengan ID model claude-haiku-5-5 (sesuai konteks sistem saya). Saya tidak menjalankan model apa pun untuk menjawab uji, tidak memanggil API model untuk uji, dan tidak menghitung Brier dari eksperimen. Ringkasan dan penilaian di atas berasal dari teks yang saya baca dan dari ringkasan pihak ketiga yang saya tandai. Penilaian kebaruan bersifat analitis dan tidak menggantikan pencarian ulang yang lebih lengkap sebelum submisi. Pemakaian sumber pihak ketiga tidak dikutip sebagai sumber primer.

## 9. Ringkasan 12 baris

1. Entri dalam matriks: 19 (17 sumber akademik dan dokumen sprint, plus Inspect AI dan Epistemic virtue evals).
2. Terverifikasi dengan membuka halaman primer (abstrak arXiv atau halaman resmi): 10 (FEVER, SciFact, FEVEROUS, MASK, SycEval, ELEPHANT, Kalai, ForecastBench, Kim et al., halaman sprint Apart).
3. Terverifikasi lewat hasil pencarian yang menampilkan halaman primer tetapi tidak dibuka penuh: 7 (FEVER Shared Task, HoVer, CLIMATE-FEVER, AVeriTeC, Kadavath, Xiong, Tian). Status TERVERIFIKASI_SEARCH.
4. Tidak terverifikasi: 2 (Inspect AI homepage; Epistemic virtue evals primer). Status TIDAK_TERVERIFIKASI.
5. Halaman sprint dibaca penuh lewat Browser pane (WebFetch diblokir). Persyaratan: PDF, 8 halaman, abstrak 150-250 kata, lampiran Limitations dan Dual-Use wajib.
6. Rubrik: tiga dimensi 1-5 (Impact, Execution, Presentation), tanpa bobot yang dinyatakan.
7. Track 1 memiliki empat masalah dan lima contoh proyek. Confidence Audit dan FlipRate tumpang tindih kuat dengan usulan judul.
8. Gap paling defensif: kalibrasi Brier multikelas tiga label pada klaim akademik, lintas model, dengan bukti kontradiktif terkontrol.
9. Judul ketiga (Knowing When Evidence Is Insufficient) menurut analisis saya paling kuat, dengan risiko tumpang tindih dengan arXiv 2602.14189 yang harus diperiksa.
10. Judul kedua (F11x) hanya layak bila F11x didefinisikan dan dibekukan sebelum uji. Saat ini status TIDAK_TERVERIFIKASI.
11. Teori utama: kalibrasi, abstensi, sensitivitas bukti, pembaruan keyakinan, ketahanan terhadap bukti menyesatkan. Maksimal dua variabel utama.
12. Keterbatasan terbesar: sebagian besar sumber dibaca dari abstrak, bukan teks penuh; label NEI SciFact belum dikonfirmasi; F11x belum dapat dinilai dari literatur.
