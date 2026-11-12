"""Phase 2 numbers for DESIGN.md: exact-binomial sample sizes, label counts, a passage split, call counts.

    python3 src/design.py        # writes out/design_tables.md and ids/split_<lang>.csv (ids only)

No LLM is called. Text is read only to count characters and identical outputs.
"""
import pathlib

import numpy as np
import pandas as pd
from scipy import stats as st

import load
import stats

ROOT = pathlib.Path(__file__).resolve().parents[1]
SEED = 20261112
TWICE = ["cs", "hi", "ja", "zh"]
ONCE = ["es", "is", "ru", "uk"]
md = []


def emit(title, df, note=""):
    md.append(f"### {title}\n\n{stats.to_md(df)}\n" + (f"\n{note}\n" if note else ""))


# ---- D1 exact binomial: how many major-error translations a limit needs ---------------------
def n_needed(k, limit, conf=0.95):
    n = k + 1
    while stats.cp_upper(k, n, conf) > limit:
        n += 1
    return n


def k_max(n, limit, conf=0.95):
    k = -1
    while k + 1 < n and stats.cp_upper(k + 1, n, conf) <= limit:
        k += 1
    return k


rows = [{"Misses allowed": k, "Majors needed, limit 5%": n_needed(k, 0.05), "Majors needed, limit 10%": n_needed(k, 0.10)} for k in range(6)]
emit("D1. Major-error translations needed so the one-sided 95% exact-binomial upper bound on the miss rate is under the limit", pd.DataFrame(rows))

rows = []
for n in (100, 150, 200):
    for p in (0.25, 0.35, 0.5):
        lo, hi = stats.cp(round(n * p), n)
        rows.append({"No-error translations": n, "Cleared share": f"{p:.0%}", "95% range": f"{lo:.1%} to {hi:.1%}", "Half-width, points": round(100 * (hi - lo) / 2, 1)})
emit("D2. Two-sided 95% exact-binomial range for a cleared share", pd.DataFrame(rows))

# ---- labels ---------------------------------------------------------------------------------
a = load.dedupe(load.reviews())
m = a[a["kind"] == "machine"].copy()
m["code"] = m["group"].cat.codes
spent = pd.read_csv(ROOT / "ids/spent_enes.csv")


def two_reviewer(lang):
    d = m[m["lang"] == lang]
    w = d[d["pass_"] == 1].merge(d[d["pass_"] == 2], on=load.KEY, suffixes=("1", "2"))
    w = w[w["reviewer1"] != w["reviewer2"]].rename(columns={"text_type1": "text_type", "doc_id1": "doc_id"})
    lo, hi = w[["code1", "code2"]].min(axis=1), w[["code1", "code2"]].max(axis=1)
    w["label"] = np.select([lo == 2, hi == 0, (hi == 2) & (lo == 1), (hi == 2) & (lo == 0)],
                           ["confirmed major", "confirmed clean", "major + minor", "major + no-error"], "minor involved, no major")
    return w[load.KEY + ["doc_id", "text_type", "label"]]


def one_reviewer(lang):
    d = m[(m["lang"] == lang) & (m["pass_"] == 1)]
    if lang == "es":
        d = d[(d["vendor"] == "Microsoft") & ~d["line_id"].isin(spent["line_id"])]
    return d.assign(label=d["group"].astype(str))[load.KEY + ["doc_id", "text_type", "label"]]


def add_text(d, lang):
    _, tgt = load.texts(lang)
    return d.assign(_t=[tgt[s][i] for s, i in zip(d["system"], d["line_id"])])


labels = {l: two_reviewer(l) for l in TWICE} | {l: one_reviewer(l) for l in ONCE}

rows = []
for lang in TWICE:
    w = add_text(labels[lang], lang)
    for cut, d in (("no speech", w[w["text_type"] != "speech"]), ("speech", w[w["text_type"] == "speech"])):
        c = d["label"].value_counts()
        cm = d[d["label"] == "confirmed major"]
        rows.append({"Language": load.NAMES[lang], "Cut": cut, "Translations": len(d), "Confirmed clean": c.get("confirmed clean", 0),
                     "Confirmed major": len(cm), "on source passages": cm["line_id"].nunique(),
                     "distinct texts": cm.drop_duplicates(["line_id", "_t"]).shape[0],
                     "Major + minor": c.get("major + minor", 0), "Major + no-error": c.get("major + no-error", 0),
                     "Minor involved, no major": c.get("minor involved, no major", 0)})
emit("D3. Two-reviewer labels (two different reviewers), twice-reviewed languages", pd.DataFrame(rows))

rows = []
for lang in ONCE:
    w = labels[lang]
    d = w[w["text_type"] != "speech"]
    c = d["label"].value_counts()
    rows.append({"Language": load.NAMES[lang] + (" (Microsoft half, spent passages removed)" if lang == "es" else ""), "Translations, no speech": len(d),
                 "Source passages": d["line_id"].nunique(), "No-error": c.get("no-error", 0), "Minor-only": c.get("minor-only", 0), "Major": c.get("major", 0),
                 "Major on source passages": d[d["label"] == "major"]["line_id"].nunique()})
emit("D4. One-reviewer labels, once-reviewed languages", pd.DataFrame(rows))

# ---- split by source passage ----------------------------------------------------------------
CAL_SHARE = 0.6
N_DEV_PASSAGES = 20
N_CLEAN_TEST, N_OTHER_TEST, N_DEV = 200, 150, 60
N_MAJOR_ONCE = 150      # per set, once-reviewed languages
rows, calls = [], []
for lang in TWICE + ONCE:
    rng = np.random.default_rng(SEED + list(load.NAMES).index(lang))
    w = labels[lang]
    major = "confirmed major" if lang in TWICE else "major"
    clean = "confirmed clean" if lang in TWICE else "no-error"
    ns = w[w["text_type"] != "speech"]
    passages = pd.DataFrame({"line_id": sorted(ns["line_id"].unique())})
    passages["text_type"] = passages["line_id"].map(ns.drop_duplicates("line_id").set_index("line_id")["text_type"])
    passages["has_major"] = passages["line_id"].isin(ns[ns["label"] == major]["line_id"])
    passages["set"] = ""
    # dev: passages without a (confirmed) major in twice-reviewed languages, so no scarce major is spent on it
    pool = passages[~passages["has_major"]] if lang in TWICE else passages
    dev = rng.choice(pool["line_id"].to_numpy(), N_DEV_PASSAGES, replace=False)
    passages.loc[passages["line_id"].isin(dev), "set"] = "dev"
    for _, g in passages[passages["set"] == ""].groupby(["text_type", "has_major"]):
        ids = rng.permutation(g["line_id"].to_numpy())
        n_cal = int(round(CAL_SHARE * len(ids)))
        passages.loc[passages["line_id"].isin(ids[:n_cal]), "set"] = "calibration"
        passages.loc[passages["line_id"].isin(ids[n_cal:]), "set"] = "test"
    passages.assign(lang=lang)[["lang", "line_id", "text_type", "set"]].to_csv(ROOT / f"ids/split_{lang}.csv", index=False)
    ns = ns.merge(passages[["line_id", "set"]], on="line_id")
    n = {s: (ns[(ns["set"] == s) & (ns["label"] == major)].shape[0], ns[(ns["set"] == s) & (ns["label"] == clean)].shape[0],
             ns[(ns["set"] == s) & ~ns["label"].isin([major, clean])].shape[0]) for s in ("dev", "calibration", "test")}
    cal_major = n["calibration"][0] if lang in TWICE else min(N_MAJOR_ONCE, n["calibration"][0])
    test_major = n["test"][0] if lang in TWICE else min(N_MAJOR_ONCE, n["test"][0])
    row = {"Language": load.NAMES[lang], "Label": "two reviewers" if lang in TWICE else "one reviewer",
           "Passages dev / cal / test": " / ".join(str((passages["set"] == s).sum()) for s in ("dev", "calibration", "test")),
           "Majors available cal / test": f"{n['calibration'][0]} / {n['test'][0]}", "Majors used cal": cal_major, "Majors used test": test_major}
    for limit in (0.05, 0.10):
        k = k_max(cal_major, limit)
        row[f"Limit {limit:.0%}: misses allowed"] = "cannot certify" if k < 0 else k
        for p in (0.01, 0.03):
            row[f"Limit {limit:.0%}: chance to certify if true miss rate is {p:.0%}"] = "0%" if k < 0 else f"{st.binom.cdf(k, cal_major, p):.0%}"
    row["Test: upper bound if 0 missed"] = f"{stats.cp_upper(0, test_major):.1%}"
    rows.append(row)
    n_speech = 0
    if lang in TWICE:
        sp = w[w["text_type"] == "speech"]
        n_speech = (sp["label"] == major).sum() + 60
    calls.append({"lang": lang, "Language": load.NAMES[lang], "Dev": N_DEV, "Calibration (majors)": cal_major,
                  "Test majors": test_major, "Test clean": min(N_CLEAN_TEST, n["test"][1]), "Test other": min(N_OTHER_TEST, n["test"][2]),
                  "Speech arm (test only)": int(n_speech)})
emit("D5. Proposed split by source passage (no speech) and what the calibration set can certify, 95% confidence", pd.DataFrame(rows),
     "Split: 20 dev passages; the rest 60% calibration / 40% test, stratified by text type and by whether the passage has a major-error translation. Seeded; ids in ids/split_<lang>.csv.")

# ---- calls and cost -------------------------------------------------------------------------
# Measured in mqm-judge-eval (Spanish, 108 calls, Claude Opus 5.5, effort medium, 5 neighbours each side):
# mean 3,215 input and 371 output tokens per call.
# Fixed part of the input (system prompt + answer schema + request overhead): least-squares fit of input tokens on
# the characters of the per-translation message, rebuilt from local data for the same 108 calls.
# Intercept 2,063 tokens (95% range 2,042-2,086, bootstrap over calls), slope 0.362 tokens per character, R2 0.99.
# Other scripts cost more tokens per character; the multipliers below are planning assumptions, not measurements.
TOK_PER_CHAR = {"cs": 0.40, "es": 0.30, "hi": 0.80, "is": 0.45, "ja": 1.0, "ru": 0.50, "uk": 0.55, "zh": 1.1}
# Claude Opus 5.5, $ per million tokens (claude-api skill, cached 2026-11-03). Cache read 0.05x input, 5-minute cache write 1.25x.
PRICE_IN, PRICE_OUT, PRICE_READ, PRICE_WRITE = 4.00, 20.00, 0.20, 5.00
BATCH = 0.5                             # Message Batches API: half price on every token type
FIXED_TOKENS, OUT_TOKENS, OUT_HIGH = 2063, 450, 800
SCAFFOLD_CHARS = 450                    # labels and headings in the per-translation message
VAR_SCALE = 0.362 / 0.275               # measured tokens per character over the assumed English/Spanish mix
c = pd.DataFrame(calls)
c["Calls"] = c[["Dev", "Calibration (majors)", "Test majors", "Test clean", "Test other", "Speech arm (test only)"]].sum(axis=1)
est = []
for lang in c["lang"]:
    src, tgt = load.texts(lang)
    d = m[(m["lang"] == lang) & (m["pass_"] == 1) & (m["text_type"] != "speech")]
    docs = d.drop_duplicates("line_id").sort_values("line_id")
    pos = {doc: g["line_id"].tolist() for doc, g in docs.groupby("doc_id")}
    sample = d.sample(400, random_state=SEED)
    toks = []
    for r in sample.itertuples():
        ids = pos[r.doc_id]
        i = ids.index(r.line_id)
        near = ids[max(0, i - 5):i + 6]
        en = sum(len(src[j]) for j in near)
        tg = sum(len(tgt[r.system][j]) for j in near)
        toks.append(VAR_SCALE * (SCAFFOLD_CHARS * 0.275 + en * 0.25 + tg * TOK_PER_CHAR[lang]))
    est.append(np.mean(toks))
c["Fixed tokens per call"] = FIXED_TOKENS
c["Variable tokens per call (est.)"] = np.round(est, -1).astype(int)


def cost(row, hit=None, high=False, batch=False):
    """Dollars for one language. hit=None: no caching. hit=h: share of calls that read the fixed part from cache;
    the rest pay the cache-write price for it. high: fixed x 1.1, variable x 1.5, 800 output tokens."""
    fixed = row["Fixed tokens per call"] * (1.1 if high else 1)
    var = row["Variable tokens per call (est.)"] * (1.5 if high else 1)
    out = OUT_HIGH if high else OUT_TOKENS
    fixed_price = PRICE_IN if hit is None else hit * PRICE_READ + (1 - hit) * PRICE_WRITE
    return row["Calls"] * (fixed * fixed_price + var * PRICE_IN + out * PRICE_OUT) / 1e6 * (BATCH if batch else 1)


c["Standard, expected $"] = c.apply(cost, axis=1).round(2)
c["Standard, high $"] = c.apply(cost, axis=1, high=True).round(2)
c["Batch, expected $"] = c.apply(cost, axis=1, batch=True).round(2)
c["Batch, high $"] = c.apply(cost, axis=1, batch=True, high=True).round(2)
tot = {"Language": "Total", **{k: c[k].sum() for k in c.columns if k not in ("lang", "Language", "Fixed tokens per call", "Variable tokens per call (est.)")}}
c2 = pd.concat([c.drop(columns="lang"), pd.DataFrame([tot])], ignore_index=True)
for k in ("Fixed tokens per call", "Variable tokens per call (est.)"):
    c2[k] = c2[k].map(lambda v: "" if pd.isna(v) else f"{int(v):,}")
emit("D6. Judge calls and API cost without caching (Claude Opus 5.5 at $4 input / $20 output per million tokens)", c2,
     "Fixed tokens: measured (see D7 note). Variable tokens: estimated from character counts. Expected: 450 output tokens per call. "
     "High: fixed x 1.1, variable x 1.5, 800 output tokens. Batch is half the standard price.")

OPTIONS = [("A. Pilot", ["zh"]), ("B. Twice-reviewed", TWICE), ("C. All eight", TWICE + ONCE)]
rows = []
for name, langs in OPTIONS:
    a = c[c["lang"].isin(langs)]
    s = lambda **k: a.apply(cost, axis=1, **k).sum()
    rows.append({"Option": name, "Calls": int(a["Calls"].sum()),
                 "Standard, no cache $": round(s(), 2),
                 "Standard + cache, all hits $": round(s(hit=1.0), 2),
                 "Batch, no cache $": round(s(batch=True), 2),
                 "Batch + cache, half hits $": round(s(batch=True, hit=0.5), 2),
                 "Batch + cache, all hits $": round(s(batch=True, hit=1.0), 2),
                 "Batch, no cache, high $": round(s(batch=True, high=True), 2),
                 "Batch + cache, all hits, high $": round(s(batch=True, hit=1.0, high=True), 2)})
emit("D7. Cost with prompt caching of the fixed part (expected unless marked high)", pd.DataFrame(rows),
     "Fixed part: 2,063 input tokens per call (95% range 2,042-2,086), from a least-squares fit of project 1's 108 measured calls "
     "on message length (R2 0.99). Cache read $0.20 and 5-minute cache write $5.00 per million tokens; batch halves both. "
     "A call that misses the cache pays the write price, so caching only pays above a 21% hit rate. "
     "Hit rate inside a batch is not guaranteed; half hits and all hits are shown as assumptions, not forecasts.")
a4 = c[c["lang"].isin(TWICE)]
ns4 = a4["Calls"].sum() - a4["Speech arm (test only)"].sum()
md.append(f"Twice-reviewed languages without the speech arm: {ns4:,} calls.\n")

(ROOT / "out/design_tables.md").write_text("\n".join(md))
print("\n".join(md[-4:]))
