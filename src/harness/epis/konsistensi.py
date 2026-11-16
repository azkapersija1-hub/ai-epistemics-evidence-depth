"""Konsistensi jawaban per klaim dan false-support mass (skema JANGKAR v2).

Setiap record: dict dengan kunci claim_id, article_id, pair_type (own|near|far),
rung (R1|R2|R3), lang, label (SUPPORTED|REFUTED|NEI|None), ok (bool), p (dict|None).
Hanya observasi ok yang dipakai. Semua CI memakai bootstrap klaster per article_id.

Definisi (dibekukan di praregistrasi):
  (a) sesuai      : label terpilih R1 == label terpilih R3 (seri: NEI menang).
  (b) pergeseran  : dS = p_S(R3) - p_S(R1) ; dN = p_N(R1) - p_N(R3).
  (c) overkomit   : max(p_S(R1), p_R(R1)) >= tau  DAN  label terpilih R3 != label terpilih R1.
  (d) false-support mass : p_S + p_R pada observasi near/far yang label-nya NEI,
      dipisah per pair_type dan rung; selisih near - far per rung.
"""
from epis import skor, stats

DEFAULT_TAU = 0.7
BAHASA = ("id", "en", "unk")
RUNG_FS = ("R1", "R3")


def _saring_bahasa(records, bahasa):
    if bahasa is None:
        return records
    return [r for r in records if r["lang"] == bahasa]


def _indeks_own(records):
    """Per klaim own: {claim_id: {article_id, lang, R1: p, R3: p}} (hanya observasi ok)."""
    per = {}
    for r in records:
        if r["pair_type"] != "own" or not r["ok"]:
            continue
        isi = per.setdefault(r["claim_id"], {"article_id": r["article_id"], "lang": r["lang"]})
        isi[r["rung"]] = r["p"]
    return per


def indikator_own(records, tau=DEFAULT_TAU):
    """Satu baris per klaim own yang punya R1 dan R3 valid."""
    hasil = []
    for claim, isi in _indeks_own(records).items():
        if "R1" not in isi or "R3" not in isi:
            continue
        p1, p3 = isi["R1"], isi["R3"]
        l1, l3 = skor.label_terpilih(p1), skor.label_terpilih(p3)
        hasil.append({
            "claim_id": claim,
            "article_id": isi["article_id"],
            "lang": isi["lang"],
            "sesuai": 1.0 if l1 == l3 else 0.0,
            "dS": p3["SUPPORTED"] - p1["SUPPORTED"],
            "dN": p1["NEI"] - p3["NEI"],
            "overkomit": 1.0 if (max(p1["SUPPORTED"], p1["REFUTED"]) >= tau and l3 != l1) else 0.0,
        })
    return hasil


def mass_false_support(records):
    """Observasi near/far berjangkar NEI: massa p_S + p_R, dengan pair_type dan rung."""
    hasil = []
    for r in records:
        if r["ok"] and r["pair_type"] in ("near", "far") and r["label"] == "NEI":
            hasil.append({
                "pair_type": r["pair_type"], "rung": r["rung"],
                "article_id": r["article_id"], "lang": r["lang"],
                "massa": r["p"]["SUPPORTED"] + r["p"]["REFUTED"],
            })
    return hasil


def _ci(nilai, klaster, b):
    if not nilai:
        return None
    h = stats.bootstrap_klaster(nilai, klaster, b=b)
    return {"n": len(nilai), "rerata": h["rerata"], "lo": h["lo"], "hi": h["hi"]}


def _false_support_per_rung(masses, b):
    hasil = {}
    for rung in RUNG_FS:
        near = [m for m in masses if m["rung"] == rung and m["pair_type"] == "near"]
        far = [m for m in masses if m["rung"] == rung and m["pair_type"] == "far"]
        entri = {
            "near": _ci([m["massa"] for m in near], [m["article_id"] for m in near], b),
            "far": _ci([m["massa"] for m in far], [m["article_id"] for m in far], b),
            "selisih": None,
        }
        if near and far:
            sel = stats.bootstrap_selisih_klaster(
                [m["massa"] for m in near], [m["article_id"] for m in near],
                [m["massa"] for m in far], [m["article_id"] for m in far], b=b)
            entri["selisih"] = sel
        hasil[rung] = entri
    return hasil


def ringkas(records, tau=DEFAULT_TAU, b=stats.B_BOOTSTRAP, bahasa=None):
    """Semua metrik konsistensi dan false-support, opsional dibatasi satu bahasa."""
    rec = _saring_bahasa(records, bahasa)
    ind = indikator_own(rec, tau)
    klaster = [x["article_id"] for x in ind]
    out = {"n_klaim": len(ind), "tau": tau}
    for kunci in ("sesuai", "dS", "dN", "overkomit"):
        out[kunci] = _ci([x[kunci] for x in ind], klaster, b)
    out["false_support"] = _false_support_per_rung(mass_false_support(rec), b)
    return out


def ringkas_per_bahasa(records, tau=DEFAULT_TAU, b=stats.B_BOOTSTRAP):
    """Ringkasan per bahasa (id, en, unk) untuk bahasa yang muncul di data."""
    ada = {r["lang"] for r in records}
    return {lang: ringkas(records, tau=tau, b=b, bahasa=lang) for lang in BAHASA if lang in ada}
