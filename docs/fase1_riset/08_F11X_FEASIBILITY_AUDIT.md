# 08 Audit kelayakan F11x

Sumber kode: `D:\kerjaan baru\SWARM_ALIGNMENT_2026_FINAL\retest_v2\src\stats_v2.py` (`f11x_design`, `f9b_design`, `_std_logit`), `evaluate_v2.py`, `prereg\candidate_formulas.py`. Baca-saja; tidak ada pelatihan ulang atau eksekusi. Milik Swarm Alignment Hackathon (6-8 Nov) = **pekerjaan terdahulu**.

## Apa F11x (dari kode)
- "F11x candidate ensemble", jenis `logit`: regresi logistik sklearn (C=1,0, fitur distandarkan), dilatih di *calibration split*, dinilai sekali di *test split*.
- **15 fitur** = `f9b_design` (11) + 4 tambahan:
  - 8 fitur artefak: `lex, cos, stp, stpar, stpar_moi, rcc_ar_moi, argon_mmd, argon_claim_overlap`;
  - 3 fitur sumber: `unsup_own, src_cont, sup_in_a_src`;
  - 4 tambahan: `E_sup` (skor H1, NaN→0), `has_src`, `S_disguise`, `F_omit`.
- Bukan rumus baru: **ansambel fitur + regresi logistik**. Kebaruan hanya pada fitur-fiturnya.
- "Argon F11" di `candidate_formulas.py` (agregator posterior Bayes) berbeda dari F11x.

## Target yang dilatih
`A_primary` (`copy_u`), `A_secondary` (`copying_occurred`), `B` (`evidence_nonindependent`), `C` (`provenance_claim_false`): label **perilaku antaragen** (penyalinan tak diungkap, bukti tak independen, klaim asal-usul palsu). **Bukan** kebenaran klaim akademik.

## Ketergantungan data
Fitur dihitung dari pasangan laporan agen, artefak, dan *ledger* sumber. Pada butir "klaim + bukti" tunggal yang dijawab satu model, sebagian besar fitur **tidak terdefinisi**.

## Pemisahan komponen
| Komponen | Isi |
|---|---|
| Formula asli | Kemiripan dan rumus STP/RCC/MOI (penelitian lain) |
| Feature engineering | 15 fitur, imputasi NaN, `has_src` |
| Model | Regresi logistik L2 |
| Keluaran | P(label pengawasan antaragen) |
| Ambang | Kuantil Q_LO=0,80, Q_HI=0,95 pada jalur H8; bukan ambang FEVER |

## Kalibrasi, bocoran, domain
- Fitting pada data sintetis hackathon; kalibrasi untuk klaim akademik: **tidak ada**.
- Risiko kebocoran bila dilatih ulang pada butir dari artikel yang sama dengan uji: split harus berbasis artikel.
- Kesesuaian domain **rendah**; probabilitas F11x bukan probabilitas kebenaran klaim.

## Adaptasi (hipotesis, belum teruji)
Satu komponen bermakna: **non-independensi antar-potongan bukti** (potongan bukti sebenarnya satu sumber/saling menyalin), sebagai fitur "redundansi bukti". Ini desain baru; perlu definisi beku, validasi di development split, dan prareg. Retraining tidak dilakukan di fase ini.

## Sebagai sinyal bagi LLM
Skor di prompt (Kondisi B) adalah **intervensi** (anchoring, otoritas angka), bukan validasi skor. Kontrol plasebo (Kondisi D: angka acak, format sama) wajib.

## Kesimpulan
1. F11x tidak boleh diklaim mengukur kebenaran/kualitas bukti akademik.
2. Hanya layak sebagai **eksplorasi sekunder** dengan definisi beku dan plasebo.
3. Nyatakan jujur: ansambel logistik, bukan rumus baru, dan preexisting.
4. Kontribusi inti harus berdiri tanpa F11x (lihat `20_FINAL_RESEARCH_RECOMMENDATION.md`).
