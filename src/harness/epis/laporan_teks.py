"""Format teks (Markdown) untuk laporan skema JANGKAR v2. Semua keluaran diberi header SIMULASI."""
from epis.laporan import HEADER_SIMULASI, URUTAN_PAIR, URUTAN_RUNG


def _f(x, digit=4):
    if x is None:
        return "-"
    if isinstance(x, float):
        return f"{x:.{digit}f}"
    return str(x)


def _ci(ci):
    if ci is None:
        return "-"
    return f"{_f(ci['rerata'])} [{_f(ci['lo'])}; {_f(ci['hi'])}]"


def _tabel_skor(skor_map):
    baris = [
        "| Pasangan | Anak tangga | Label | n | gagal | Brier (batas 1) | Brier (batas 2) "
        "| Brier 95% CI klaster | Akurasi | ECE | AURC | Recall NEI | Presisi NEI | n kunci NEI |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for pair in URUTAN_PAIR:
        for rung in URUTAN_RUNG:
            g = skor_map.get((pair, rung))
            if g is None:
                continue
            for tipe in ("anchor", "expert"):
                s = g["per_tipe"][tipe]
                if s["n"] == 0:
                    continue
                nei = s["nei"]
                baris.append(
                    f"| {pair} | {rung} | {tipe} | {s['n']} | {g['n_gagal']} | "
                    f"{_f(g['brier_batas1'])} | {_f(g['brier_batas2'])} | {_ci(g['ci_brier'])} | "
                    f"{_f(s['akurasi'])} | {_f(s['ece'])} | {_f(s['aurc'])} | "
                    f"{_f(nei['recall_nei'])} | {_f(nei['presisi_nei'])} | {nei['n_kunci_nei']} |")
    return baris


def _tabel_konsistensi(k):
    return [
        "| Metrik (pasangan own, R1 vs R3) | n klaim | Rerata [95% CI klaster] |",
        "|---|---|---|",
        f"| Sesuai (label R1 = label R3) | {k['n_klaim']} | {_ci(k['sesuai'])} |",
        f"| Pergeseran dS = p_S(R3) - p_S(R1) | {k['n_klaim']} | {_ci(k['dS'])} |",
        f"| Pergeseran dN = p_N(R1) - p_N(R3) | {k['n_klaim']} | {_ci(k['dN'])} |",
        f"| Overkomit (max p_S,p_R di R1 >= tau={k['tau']}, label R3 berbeda) | {k['n_klaim']} | {_ci(k['overkomit'])} |",
    ]


def _tabel_false_support(fs):
    baris = [
        "| Anak tangga (berjangkar NEI) | False-support mass near | far | selisih near - far |",
        "|---|---|---|---|",
    ]
    for rung in ("R1", "R3"):
        e = fs[rung]
        sel = e["selisih"]
        selisih_txt = "-" if sel is None else f"{_f(sel['rerata'])} [{_f(sel['lo'])}; {_f(sel['hi'])}]"
        baris.append(f"| {rung} | {_ci(e['near'])} | {_ci(e['far'])} | {selisih_txt} |")
    return baris


def _tabel_bahasa(per_bahasa):
    baris = [
        "| Bahasa | n klaim | Sesuai | Overkomit | Selisih FS near-far R1 | Selisih FS near-far R3 |",
        "|---|---|---|---|---|---|",
    ]
    for lang, k in per_bahasa.items():
        s1 = k["false_support"]["R1"]["selisih"]
        s3 = k["false_support"]["R3"]["selisih"]
        baris.append(
            f"| {lang} | {k['n_klaim']} | {_f(k['sesuai'] and k['sesuai']['rerata'])} | "
            f"{_f(k['overkomit'] and k['overkomit']['rerata'])} | "
            f"{_f(s1 and s1['rerata'])} | {_f(s3 and s3['rerata'])} |")
    return baris


def format_provider(provider_id, n_observasi, ringkasan, prompt_hash, gagal_percobaan_1=None):
    """Bagian laporan untuk satu provider (mock)."""
    k = ringkasan["konsistensi"]
    baris = [
        f"## Provider: {provider_id}",
        f"- Jumlah observasi: {n_observasi}; prompt_hash: {prompt_hash}",
        f"- Parse gagal percobaan pertama: {_f(gagal_percobaan_1, 0)}; "
        f"gagal setelah ulang (dicatat): {ringkasan['n_gagal_total']}",
        "",
        "### A. Skor berjangkar (hanya observasi berlabel; label null dikecualikan)",
        *_tabel_skor(ringkasan["skor"]),
        "",
        "### B. Konsistensi per klaim (own R1 vs R3)",
        *_tabel_konsistensi(k),
        "",
        "### C. Near vs far (false-support mass pada observasi berjangkar NEI)",
        *_tabel_false_support(k["false_support"]),
        "",
        "### D. Per bahasa",
        *_tabel_bahasa(ringkasan["per_bahasa"]),
        "",
    ]
    return "\n".join(baris)


HEADER_MODEL_NYATA = "HASIL MODEL (BELUM DIVERIFIKASI; hanya sah bila sesuai praregistrasi)"


def format_laporan(bagian, nyata=False):
    """Gabungkan bagian dengan header di baris pertama.

    nyata=False (default): header SIMULASI, untuk keluaran MockProvider.
    nyata=True: header HASIL MODEL dengan catatan belum diverifikasi.
    """
    if nyata:
        judul = f"# {HEADER_MODEL_NYATA}\n\nAnalisis otomatis dari keluaran model. Ikuti PREREG; bukan kesimpulan."
    else:
        judul = f"# {HEADER_SIMULASI}\n\nSemua angka di bawah berasal dari MockProvider. Bukan hasil model."
    return judul + "\n\n" + "\n".join(bagian)
