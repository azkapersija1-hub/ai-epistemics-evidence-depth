import json, re, zipfile, csv, time, urllib.request, urllib.error, urllib.parse, difflib, hashlib, sys, collections, os
import xml.etree.ElementTree as ET

B = "C:/EPIS_KERJA/AI_EPISTEMICS_2026_PHASE_2_PREP/bahan/v2/"
O = "C:/EPIS_KERJA/REFERENSI/katalog_sumber/"
T = O + "_tmp/"
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
BUDGET = float(sys.argv[1]) if len(sys.argv) > 1 else 480.0
T0 = time.time()
CACHE_P = T + "crossref_cache.json"
UA = "research-reference-check"
FIELDS_CR = ["penulis", "tahun", "jurnal", "volume", "issue", "halaman"]


def jl(p):
    with open(B + p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def ndoi(x):
    x = (x or "").strip().lower()
    x = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", x)
    x = re.sub(r"^doi:\s*", "", x)
    return x.strip()


def ntitle(x):
    x = (x or "").lower()
    x = re.sub(r"[\W_]+", " ", x)
    return re.sub(r"\s+", " ", x).strip()


def clean_year(s):
    s = (s or "").strip()
    s = re.sub(r"^(\d{4})\.0$", r"\1", s)
    return s


def col(ref):
    return re.match(r"[A-Z]+", ref).group(0)


def read_cat():
    z = zipfile.ZipFile(T + "katalog.xlsx")
    hdr = None
    recs = []
    with z.open("xl/worksheets/sheet2.xml") as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if el.tag != NS + "row":
                continue
            d = {}
            for c in el.findall(NS + "c"):
                if c.get("t") == "inlineStr":
                    v = "".join((x.text or "") for x in c.iter(NS + "t"))
                else:
                    ve = c.find(NS + "v")
                    v = ve.text if ve is not None and ve.text else ""
                d[col(c.get("r"))] = v
            if hdr is None:
                hdr = d
            else:
                recs.append((int(el.get("r")), d))
            el.clear()
    names = {k: v.strip() for k, v in hdr.items()}
    out = []
    for r, d in recs:
        row = {names[k]: d.get(k, "").strip() for k in names if names[k]}
        row["_baris"] = r
        out.append(row)
    return out


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- 1. Muat masukan (hanya field yang dibutuhkan) ----------
pool = {p["article_id"]: p for p in jl("pool_v2.jsonl")}
kolam = {e["ev_id"]: e for e in jl("kolam_bukti_v2_1.jsonl")}
pas = jl("pasangan_v2_1.jsonl")
A_ids = [p["claim_article_id"] for p in pas]
assert len(set(A_ids)) == 294, len(set(A_ids))
pool_tanpa_pasangan = sorted(set(pool) - set(A_ids))
near_use = collections.Counter(p["near_ev"] for p in pas)
far_use = collections.Counter(p["far_ev"] for p in pas)
B_ids = sorted(set(near_use) | set(far_use))
split_mismatch = sum(1 for p in pas if pool[p["claim_article_id"]]["split"] != p["split"])
near_bukan_ev = sum(1 for p in pas if p["near_ev"] not in kolam)
far_bukan_ev = sum(1 for p in pas if p["far_ev"] not in kolam)

# ---------- 2. Katalog internal ----------
cat = read_cat()
cat_doi = collections.defaultdict(list)
cat_t = collections.defaultdict(list)
for r in cat:
    d = ndoi(r.get("DOI", ""))
    if d:
        cat_doi[d].append(r)
    t = ntitle(r.get("Judul", ""))
    if t:
        cat_t[t].append(r)
print("katalog baris data:", len(cat), "doi unik:", len(cat_doi))


def cocokkan(doi_n, judul):
    """Kembalikan (metode, rekaman_katalog_atau_None)."""
    if doi_n:
        kand = cat_doi.get(doi_n, [])
        if len(kand) == 1:
            rec = kand[0]
            metode = "DOI+judul" if ntitle(rec.get("Judul", "")) == ntitle(judul) else "DOI"
            return metode, rec
        if len(kand) > 1:
            return "DOI_GANDA_KATALOG", None
        return "tidak_cocok", None
    kand = cat_t.get(ntitle(judul), [])
    if len(kand) == 1:
        return "judul", kand[0]
    if len(kand) > 1:
        return "judul_ganda_katalog", None
    return "tidak_cocok", None


# ---------- 3. Susun item ----------
items = []
for aid in A_ids:
    p = pool[aid]
    items.append({
        "id": aid, "peran": "asal_klaim", "split": p["split"], "doc_id": p["doc_id"],
        "doi_raw": p["doi"], "judul": p["title"], "lang": p["lang_guess"], "domain": p["domain"],
        "jumlah_pasangan": "",
    })
for eid in B_ids:
    e = kolam[eid]
    nr = near_use.get(eid, 0)
    fr = far_use.get(eid, 0)
    peran = "bukti_near+far" if nr and fr else ("bukti_near" if nr else "bukti_far")
    items.append({
        "id": eid, "peran": peran, "split": "", "doc_id": e["doc_id"],
        "doi_raw": e["doi"], "judul": e["title"], "lang": e["lang_guess"], "domain": e["domain"],
        "jumlah_pasangan": nr + fr,
    })

for it in items:
    it["doi"] = ndoi(it["doi_raw"])
    it["metode"], it["rec"] = cocokkan(it["doi"], it["judul"])
    rec = it["rec"]
    if rec:
        it["cur"] = {
            "penulis": rec.get("Penulis", "").strip(),
            "tahun": clean_year(rec.get("Tahun", "")),
            "jurnal": rec.get("Jurnal", "").strip(),
            "volume": rec.get("Volume", "").strip(),
            "issue": rec.get("Issue", "").strip(),
            "halaman": "",
        }
        it["judul_katalog"] = rec.get("Judul", "").strip()
        it["bahasa_katalog"] = rec.get("Bahasa", "").strip()
    else:
        it["cur"] = {k: "" for k in ["penulis", "tahun", "jurnal", "volume", "issue", "halaman"]}
        it["judul_katalog"] = ""
        it["bahasa_katalog"] = ""
    it["src"] = {k: ("katalog" if v else "") for k, v in it["cur"].items()}

# ---------- 4. Crossref (hanya bila ada celah dan DOI tersedia) ----------
need = sorted({it["doi"] for it in items
               if it["doi"] and (not it["cur"]["penulis"] or not it["cur"]["tahun"] or not it["cur"]["jurnal"])})
cache = {}
if os.path.exists(CACHE_P):
    with open(CACHE_P, encoding="utf-8") as f:
        cache = json.load(f)


def ekstrak(m):
    t = (m.get("title") or [""])[0]
    ct = (m.get("container-title") or [""])[0]
    au = []
    for a in m.get("author") or []:
        if a.get("family"):
            au.append((a.get("family", "") + ", " + a.get("given", "")).strip(", "))
        elif a.get("name"):
            au.append(a["name"])
    yr = ""
    for k in ("issued", "published-print", "published-online", "published"):
        dp = (m.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            yr = str(dp[0][0])
            break
    return {"judul": t, "jurnal": ct, "penulis": "; ".join(au), "tahun": yr,
            "volume": str(m.get("volume", "") or ""), "issue": str(m.get("issue", "") or ""),
            "halaman": str(m.get("page", "") or "")}


def ambil(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/()[]:;<>.-_")
    for percobaan in range(2):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                js = json.loads(r.read().decode("utf-8"))
                return "ok", ekstrak(js.get("message", {}))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "TIDAK_DITEMUKAN_CROSSREF", None
            if e.code == 429 and percobaan == 0:
                time.sleep(5)
                continue
            return "gagal_http_%d" % e.code, None
        except Exception as e:
            if percobaan == 0:
                time.sleep(2)
                continue
            return "gagal_" + type(e).__name__, None
    return "gagal", None


def final_status(s):
    return s in ("ok", "TIDAK_DITEMUKAN_CROSSREF")


req_n = 0
gagal_n = 0
gagal_beruntun = 0
maks_beruntun = 0
berhenti_karena = ""
pending = 0
for doi in need:
    if doi in cache and final_status(cache[doi]["status"]):
        continue
    if time.time() - T0 > BUDGET:
        pending += 1
        continue
    if gagal_beruntun > 20:
        berhenti_karena = "lebih dari 20 kegagalan beruntun"
        break
    st, msg = ambil(doi)
    req_n += 1
    if st.startswith("gagal"):
        gagal_n += 1
        gagal_beruntun += 1
        maks_beruntun = max(maks_beruntun, gagal_beruntun)
    else:
        gagal_beruntun = 0
    cache[doi] = {"status": st, "msg": msg}
    if req_n % 25 == 0:
        with open(CACHE_P, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    time.sleep(0.2)
with open(CACHE_P, "w", encoding="utf-8") as f:
    json.dump(cache, f, ensure_ascii=False)

selesai = (pending == 0 and not berhenti_karena)
print("crossref perlu:", len(need), "permintaan:", req_n, "gagal:", gagal_n,
      "maks gagal beruntun:", maks_beruntun, "pending:", pending, "berhenti:", berhenti_karena or "-",
      "waktu:", round(time.time() - T0, 1))
if not selesai:
    print("BELUM SELESAI. Jalankan ulang skrip untuk melanjutkan dari cache.")
    sys.exit(0)

# ---------- 5. Gabung metadata ----------
for it in items:
    cur, src = it["cur"], it["src"]
    it["cr_status"] = ""
    it["cr"] = {}
    it["catatan"] = []
    if it["metode"] == "DOI_GANDA_KATALOG":
        it["catatan"].append("DOI_GANDA_KATALOG")
    if it["metode"] in ("judul_ganda_katalog",):
        it["catatan"].append("JUDUL_GANDA_KATALOG")
    if it["metode"] == "tidak_cocok" and it["doi"]:
        it["catatan"].append("TIDAK_ADA_DI_KATALOG")
    if not it["doi"]:
        it["catatan"].append("DOI_KOSONG")
    if it["doi"]:
        c = cache.get(it["doi"])
        if c is None:
            it["cr_status"] = "tidak_perlu" if it["doi"] not in need else "belum_dicoba"
        elif c["status"] == "ok":
            it["cr_status"] = "ok"
            it["cr"] = c["msg"]
        elif c["status"] == "TIDAK_DITEMUKAN_CROSSREF":
            it["cr_status"] = "TIDAK_DITEMUKAN_CROSSREF"
        else:
            it["cr_status"] = "CROSSREF_GAGAL"
            it["catatan"].append("CROSSREF_GAGAL")
    if it["cr_status"] == "TIDAK_DITEMUKAN_CROSSREF":
        it["catatan"].append("TIDAK_DITEMUKAN_CROSSREF")
    cr = it["cr"]
    it["judul_crossref"] = cr.get("judul", "") if cr else ""
    it["cr_tahun"] = cr.get("tahun", "") if cr else ""
    it["cr_jurnal"] = cr.get("jurnal", "") if cr else ""
    it["beda_judul_crossref"] = ""
    if cr:
        if ntitle(cr.get("judul", "")) != ntitle(it["judul"]):
            it["beda_judul_crossref"] = "ya"
        sim = difflib.SequenceMatcher(None, ntitle(it["judul"]), ntitle(cr.get("judul", ""))).ratio() if cr.get("judul") else 0.0
        it["sim_crossref"] = sim
        gerbang = sim >= 0.6
        if not gerbang:
            it["catatan"].append("CROSSREF_JUDUL_TIDAK_COCOK_TIDAK_DIPAKAI")
        else:
            for k in FIELDS_CR:
                if not cur.get(k) and cr.get(k):
                    cur[k] = cr[k]
                    src[k] = "crossref"
        if it["src"]["tahun"] == "katalog" and cr.get("tahun") and cr["tahun"] != it["cur"]["tahun"]:
            it["catatan"].append("TAHUN_BEDA_KATALOG_CROSSREF")
        if it["src"]["jurnal"] == "katalog" and cr.get("jurnal") and cr["jurnal"].strip().lower() != it["cur"]["jurnal"].strip().lower():
            it["catatan"].append("JURNAL_BEDA_KATALOG_CROSSREF")
    if it["judul_katalog"] and ntitle(it["judul_katalog"]) != ntitle(it["judul"]):
        it["beda_judul_katalog"] = "ya"
        it["catatan"].append("BEDA_JUDUL_KATALOG")
    else:
        it["beda_judul_katalog"] = "tidak" if it["judul_katalog"] else ""
    bk = it["bahasa_katalog"].lower()
    if bk and it["lang"] and bk != it["lang"].lower():
        it["catatan"].append("BEDA_BAHASA_KATALOG")
    if it["cr"] and it["beda_judul_crossref"] == "ya":
        it["catatan"].append("BEDA_JUDUL_CROSSREF")
    if not it["doi"]:
        it["status"] = "TANPA_DOI"
    elif cur["penulis"] and cur["tahun"] and it["judul"].strip() and cur["jurnal"]:
        it["status"] = "LENGKAP"
    else:
        it["status"] = "SEBAGIAN"
    it["sumber_metadata"] = ";".join(
        "%s=%s" % (k, src[k] or "kosong") for k in ["penulis", "tahun", "jurnal", "volume", "issue", "halaman"])
    it["dilengkapi_crossref"] = "ya" if any(src[k] == "crossref" for k in src) else "tidak"
    it["dicoba_crossref"] = "ya" if it["doi"] in need else "tidak"

# ---------- 6. Tulis CSV ----------
COLS_A = ["article_id", "peran", "split", "doc_id", "doi", "judul_bahan", "lang_bahan", "domain_bahan",
          "metode_cocok", "judul_katalog", "beda_judul_katalog", "bahasa_katalog",
          "penulis", "tahun", "jurnal", "volume", "issue", "halaman",
          "judul_crossref", "cr_tahun", "cr_jurnal", "beda_judul_crossref", "cr_status",
          "sumber_metadata", "dilengkapi_crossref", "status", "jumlah_pasangan", "catatan"]
COLS_B = [c if c != "article_id" else "ev_id" for c in COLS_A]


def baris(it):
    cur = it["cur"]
    return {
        "id": it["id"], "peran": it["peran"], "split": it["split"], "doc_id": it["doc_id"],
        "doi": it["doi"], "judul_bahan": it["judul"], "lang_bahan": it["lang"], "domain_bahan": it["domain"],
        "metode_cocok": it["metode"], "judul_katalog": it["judul_katalog"],
        "beda_judul_katalog": it["beda_judul_katalog"], "bahasa_katalog": it["bahasa_katalog"],
        "penulis": cur["penulis"], "tahun": cur["tahun"], "jurnal": cur["jurnal"],
        "volume": cur["volume"], "issue": cur["issue"], "halaman": cur["halaman"],
        "judul_crossref": it["judul_crossref"], "cr_tahun": it["cr_tahun"], "cr_jurnal": it["cr_jurnal"],
        "beda_judul_crossref": it["beda_judul_crossref"], "cr_status": it["cr_status"],
        "sumber_metadata": it["sumber_metadata"], "dilengkapi_crossref": it["dilengkapi_crossref"],
        "status": it["status"], "jumlah_pasangan": it["jumlah_pasangan"],
        "catatan": "|".join(it["catatan"]),
    }


itA = [it for it in items if it["peran"] == "asal_klaim"]
itB = [it for it in items if it["peran"] != "asal_klaim"]
with open(O + "katalog_sumber_artikel_asal_294.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS_A)
    w.writeheader()
    for it in itA:
        r = baris(it)
        r["article_id"] = r.pop("id")
        w.writerow(r)
with open(O + "katalog_sumber_bukti_near_far.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=COLS_B)
    w.writeheader()
    for it in itB:
        r = baris(it)
        r["ev_id"] = r.pop("id")
        w.writerow(r)

# ---------- 7. Statistik ----------
def stat(lst):
    s = {}
    s["n"] = len(lst)
    s["status"] = collections.Counter(it["status"] for it in lst)
    s["metode"] = collections.Counter(it["metode"] for it in lst)
    s["lang"] = collections.Counter(it["lang"] for it in lst)
    s["domain"] = collections.Counter(it["domain"] for it in lst)
    s["cr_ok"] = sum(1 for it in lst if it["dilengkapi_crossref"] == "ya")
    s["dicoba"] = sum(1 for it in lst if it["dicoba_crossref"] == "ya")
    s["cr_404"] = sum(1 for it in lst if it["cr_status"] == "TIDAK_DITEMUKAN_CROSSREF")
    s["cr_gagal"] = sum(1 for it in lst if it["cr_status"] == "CROSSREF_GAGAL")
    s["beda_judul_katalog"] = [it["id"] for it in lst if it["beda_judul_katalog"] == "ya"]
    s["beda_judul_crossref"] = [it["id"] for it in lst if it["beda_judul_crossref"] == "ya"]
    s["tahun"] = sorted(int(it["cur"]["tahun"]) for it in lst if it["cur"]["tahun"].isdigit())
    s["doi_kosong"] = sum(1 for it in lst if not it["doi"])
    s["peran"] = collections.Counter(it["peran"] for it in lst)
    s["judul_cr_tidak_dipakai"] = sum(1 for it in lst if "CROSSREF_JUDUL_TIDAK_COCOK_TIDAK_DIPAKAI" in it["catatan"])
    s["tahun_beda"] = sum(1 for it in lst if "TAHUN_BEDA_KATALOG_CROSSREF" in it["catatan"])
    s["jurnal_beda"] = sum(1 for it in lst if "JURNAL_BEDA_KATALOG_CROSSREF" in it["catatan"])
    s["beda_bahasa"] = sum(1 for it in lst if "BEDA_BAHASA_KATALOG" in it["catatan"])
    s["dari_katalog"] = sum(1 for it in lst if it["metode"] in ("DOI", "DOI+judul", "judul"))
    return s


SA = stat(itA)
SB = stat(itB)
hash_skrg = {
    "pool_v2.jsonl": sha(B + "pool_v2.jsonl"),
    "kolam_bukti_v2_1.jsonl": sha(B + "kolam_bukti_v2_1.jsonl"),
    "pasangan_v2_1.jsonl": sha(B + "pasangan_v2_1.jsonl"),
    "KATALOG_METADATA_LENGKAP.xlsx": sha("D:/BISMILLAH TEMBUS ARTIKEL/KATALOG_METADATA_LENGKAP.xlsx"),
}
hash_awal = {}
with open(T + "hash_sebelum.txt", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(None, 1)
        if len(parts) == 2:
            nama_penuh = parts[1].lstrip("*").strip()
            nama = "KATALOG_METADATA_LENGKAP.xlsx" if nama_penuh.endswith(".xlsx") else os.path.basename(nama_penuh)
            hash_awal[nama] = parts[0]
hash_cocok = {k: (hash_awal.get(k) == hash_skrg[k]) for k in hash_skrg}

stat_out = {
    "A": {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in SA.items()},
    "B": {k: (dict(v) if isinstance(v, collections.Counter) else v) for k, v in SB.items()},
    "req": req_n, "gagal": gagal_n, "maks_beruntun": maks_beruntun,
    "crossref_perlu": len(need), "pool_tanpa_pasangan": pool_tanpa_pasangan,
    "split_mismatch": split_mismatch, "near_bukan_ev": near_bukan_ev, "far_bukan_ev": far_bukan_ev,
    "hash_awal": hash_awal, "hash_skrg": hash_skrg, "hash_cocok": hash_cocok,
    "kolam_n": len(kolam), "pas_n": len(pas), "cat_n": len(cat), "cat_doi_unik": len(cat_doi),
    "ev_tidak_dipakai": len(kolam) - len(B_ids),
}
with open(T + "stat.json", "w", encoding="utf-8") as f:
    json.dump(stat_out, f, ensure_ascii=False, indent=1, default=str)
print("selesai tulis CSV dan stat.json")
print(json.dumps({"A_status": stat_out["A"]["status"], "B_status": stat_out["B"]["status"],
                  "A_n": SA["n"], "B_n": SB["n"], "A_cr": SA["cr_ok"], "B_cr": SB["cr_ok"],
                  "hash_cocok": hash_cocok}, ensure_ascii=False))
