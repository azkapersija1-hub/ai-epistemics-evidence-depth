# How Much Evidence Is Enough?
## Calibration of LLM verdicts across evidence depth on academic claims

> **Status: preparation and preliminary results.** Model outputs in `results/` are labelled by the harness as "HASIL MODEL (BELUM DIVERIFIKASI)" (model results, not yet verified) and are valid only under the frozen preregistration. This repository is not a set of conclusions.
>
> Context: Apart Research AI x Epistemics sprint. License: MIT for code, CC BY 4.0 for text and reports (see `LICENSE` and `LICENSE-DOCS.md`). The README in Indonesian (`README.md`) is the main document.

## Summary

Language models are often asked whether a scientific claim is supported, refuted, or not enough evidence (SUPPORTED, REFUTED, NEI). This study asks whether those verdicts stay calibrated when the model reads only the start of an article (R1: abstract; R2: abstract and results) compared with the full relevant text (R3). The design was frozen before model answers were collected and uses mechanical anchor labels rather than full expert labels. The main analysis (UTAMA-294) uses all 294 claims for three API models. Layers 40, 36, 26 and 19 (team-validated subsets) and two sensitivity sets (290 and 280 claims) are sensitivity analyses, not the main analysis. Results are descriptive and not yet re-verified.

## Research questions

1. How calibrated is the distribution of SUPPORTED, REFUTED, and NEI outputs at each evidence depth (R1, R2, R3)?
2. How often does the model become overconfident at R1 relative to R3 (tau = 0.7)?
3. How large is the false-support mass on evidence from other articles (near and far)?

## Main results

The main analysis (UTAMA-294) uses 294 claims and 2058 observations for three API models: qwen3.8-flash, qwen4-max-preview and deepseek-v4.1-flash. This set includes the 20 pilot claims, as allowed by Amendment 5. A variant without the pilot (UTAMA-274) is provided for comparison. No rule, tau parameter or prompt was tuned after seeing results.

Team-validated layers and two sensitivity sets (KEPEKAAN-A with 290 claims, KEPEKAAN-B with 280 claims) are sensitivity analyses and do not replace the main analysis. GPT-6.1 Sol (identity and configuration not verified) and Gemini 3.8 Flash (Antigravity) were run only through the agent path on subsets and are not part of the main analysis. glm-5.3 was stopped (see Limitations).

Selected values (means or proportions, no tuning):

| Metric (UTAMA-294) | qwen3.8-flash | qwen4-max-preview | deepseek-v4.1-flash |
|---|---|---|---|
| Brier bound 1, own R3 | 0.0322 | 0.0222 | 0.0919 |
| Overconfidence (tau 0.7) | 0.0068 | 0.0068 | 0.0208 |
| False-support near R1 | 0.0718 | 0.1473 | 0.0446 |
| Agreement (R1 label = R3 label) | 0.5034 | 0.5306 | 0.4896 |

The full table with bootstrap confidence intervals is in `results/utama294/tabel_utama294_3model.md`. Other sets and per-split results are in `results/utama294/` (`analisis_*.md`, `results/utama294/tabel_kepekaan.md`, `results/utama294/tabel_per_split.md`). Figures H1 to H5 (English and Indonesian versions) are in `figures_294/`, with an index at `figures_294/INDEKS294.md`.

Status: MODEL RESULTS (NOT YET VERIFIED). These numbers do not show which model is more correct.

## Layout

```
repo/
  .gitignore
  CITATION.cff
  EXCLUDED.md
  README.md
  README_ID.md
  data/  (1 berkas langsung)
    claim_id/  (4 berkas)
    kelayakan/  (12 berkas)
  docs/  (3 berkas langsung)
    fase1_riset/  (21 berkas)
    panduan_penilai/  (2 berkas)
    prareg/  (2 berkas)
  figures/  (29 berkas langsung)
  figures_294/  (22 berkas)
  results/  (0 berkas langsung)
    codex_gpt61_sol_tak_terverifikasi/  (16 berkas)
    deepseek_v4_1_flash/  (9 berkas)
    gemini_antigravity/  (38 berkas)
    glm_dihentikan/  (1 berkas)
    lapis36/  (5 berkas)
    perbandingan_lapis/  (5 berkas)
    qwen3_8_flash/  (7 berkas)
    qwen4_max_preview/  (7 berkas)
    retest_lapis19/  (12 berkas)
    utama294/  (18 berkas)
  report/  (2 berkas langsung)
  references/  (6 berkas langsung)
  external_sessions/  (5 berkas langsung)
  src/  (0 berkas langsung)
    analisis/  (6 berkas)
    harness/  (35 berkas)
  video/  (summary video, 294-claim main analysis, two languages)
```

## Preexisting work (mandatory)

See `docs/PEKERJAAN_PREEXISTING.md` and the Indonesian README for the full list and the dated facts. Every asset used or mentioned must be marked "preexisting". Whether a given asset counts as preexisting is **DECIDED BY THE AUTHORS**.

## Reproducing

Windows and Python 3.12. Runnable from this repository:

- Harness unit tests: `py -3.12 -I -X utf8 -m unittest discover -s src/harness/tests -v` (135 of 152 pass; 17 errors need the fixture that is not included)
- Main 294 analysis outputs are in `results/utama294/`. The script `results/utama294/skrip_analisis_utama294.py` needs the answer key (not included) and hard-coded paths (see `docs/PATH_MAP.md`), so it is not runnable here.
- Feasibility tests on synthetic data: `py -3.12 -I -X utf8 src/analisis/test_hitung_kelayakan.py` (32 of 32 pass)

Not runnable from this repository, because inputs are not included: the analysis scripts that read the answer keys, the feasibility aggregation from per-rater files, live model calls, and figure and video builders with hard-coded paths. See `docs/PATH_MAP.md` and `EXCLUDED.md`. The answer key is not included; access is decided by the authors.

## Limitations

- The main analysis has 294 claims, but layer subsets (40, 36, 26, 19) and sensitivity sets are smaller, so statistical power per subset is limited.
- The 20 pilot claims are included in the main 294 analysis under Amendment 5 (see D3 in `docs/prareg/CATATAN_DEVIASI.md`). How the pilot is reported is for the authors to decide.
- The holdout, which was run once, has not been re-verified from the harness logs.
- Anchor labels are mechanical, not per-item expert judgements.
- Raters are the author team, not independent raters.
- GPT-6.1 Sol outputs via Codex are not verified.
- glm-5.3 was stopped for token cost; its partial holdout is not analysed.
- Temperature cannot be set on the model_api path.
- deepseek-v4.1-flash max_tokens was raised from 512 to 4000 after a technical pilot (Amendment 1).

## Warning: figures G3 to G7

Figures G3 to G7 in `figures/` were built from the tier-36 subset, not from the main 294 analysis, so their numbers do not match `results/utama294/`; use `figures_294/` for main results. The summary video has been rebuilt from the main 294 analysis (`video/ringkasan294_en.mp4` and `video/ringkasan294_id.mp4`).

## Manuscript status

The report is being edited by the authors and is not final. The final report will be placed in `report/`. This repository does not contain a draft of the report.

## License

Code (`src/`) is MIT licensed (`LICENSE`). Text, figures and reports are CC BY 4.0 (`LICENSE-DOCS.md`).

## Authors

- [Penulis 1]
- [Penulis 2]
- [Penulis 3]
