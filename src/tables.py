"""Phase 1 tables: per-language counts, reviewer and vendor flag rates, reviewer-to-reviewer agreement.

    python3 src/tables.py        # writes out/*.csv and out/tables.md (numbers only, no text)
"""
import pathlib

import numpy as np
import pandas as pd

import load
import stats

OUT = pathlib.Path(__file__).resolve().parents[1] / "out"
OUT.mkdir(exist_ok=True)
ORDER = list(load.NAMES)
md = []


def to_md(df):
    def cell(v):
        if isinstance(v, float):
            return "" if np.isnan(v) else (f"{v:,.0f}" if v == int(v) and abs(v) >= 1000 else f"{v:g}")
        return f"{v:,}" if isinstance(v, (int, np.integer)) else str(v)
    head = "| " + " | ".join(str(c).strip() for c in df.columns) + " |"
    sep = "|" + "|".join("---" if df[c].dtype == object else "---:" for c in df.columns) + "|"
    return "\n".join([head, sep] + ["| " + " | ".join(cell(v) for v in r) + " |" for r in df.itertuples(index=False)])


def emit(title, df, note=""):
    md.append(f"### {title}\n\n{to_md(df)}\n" + (f"\n{note}\n" if note else ""))


def pct(x):
    return round(100 * x, 1)


def shares(d):
    g = d["group"].value_counts()
    n = len(d)
    return {"No-error %": pct(g["no-error"] / n), "Minor-only %": pct(g["minor-only"] / n),
            "Major %": pct(g["major"] / n), "Major n": int(g["major"])}


raw = load.reviews()
allrev = load.dedupe(raw)
allrev["name"] = allrev["lang"].map(load.NAMES)
allrev["flag"] = allrev["group"] != "no-error"
allrev["major"] = allrev["group"] == "major"
allrev["code"] = allrev["group"].cat.codes
m = allrev[allrev["kind"] == "machine"]
p1 = m[m["pass_"] == 1]

# ---- T0 rows in the files ------------------------------------------------------------------
full = load.reviews(drop_filtered=False)
rows = []
for lang in ORDER:
    f = full[full["lang"] == lang]
    a = allrev[allrev["lang"] == lang]
    rows.append({"Language": load.NAMES[lang], "Rows in files": len(f), "Dropped (quality-control, tutorial, #dup, #incomplete)": int(f["filtered"].sum()),
                 "Kept": int((~f["filtered"]).sum()), "Repeat submissions dropped": int((~f["filtered"]).sum()) - len(a), "Reviews used": len(a),
                 "of which human reference": int((a["kind"] == "human").sum()), "of which MSLC": int((a["kind"] == "challenge").sum()),
                 "Spans with severity 'undecided'": int(a["n_other"].sum())})
emit("T0. Rows in the files and what was dropped", pd.DataFrame(rows))

# ---- T1 overview (machine systems) ---------------------------------------------------------
rows = []
for lang in ORDER:
    d, a = p1[p1["lang"] == lang], m[m["lang"] == lang]
    n2 = a.groupby(load.KEY).size()
    rows.append({"Language": load.NAMES[lang], "Vendor": " + ".join(sorted(a["vendor"].unique())), "Source passages": d["line_id"].nunique(),
                 "Documents": d["doc_id"].nunique(), "Machine systems": d["system"].nunique(), "Translations": len(d),
                 "Reviewers": a["reviewer"].nunique(), "Reviews": len(a), "Reviewed twice %": pct((n2 == 2).mean()),
                 "Reviews per translation": round(len(a) / len(d), 2), **shares(d), "Mean score": round(d["score"].mean(), 1)})
t1 = pd.DataFrame(rows)
emit("T1. Per language, machine systems only; group shares from the first review of each translation", t1)
t1.to_csv(OUT / "t1_overview.csv", index=False)

# ---- T1b second pass shares ----------------------------------------------------------------
rows = []
for lang in ["cs", "hi", "ja", "zh"]:
    for ps in (1, 2):
        d = m[(m["lang"] == lang) & (m["pass_"] == ps)]
        both = m[(m["lang"] == lang)].groupby(load.KEY)["pass_"].transform("nunique") == 2
        d2 = m[(m["lang"] == lang)][both]
        d2 = d2[d2["pass_"] == ps]
        rows.append({"Language": load.NAMES[lang], "Review": "first" if ps == 1 else "second", "Translations": len(d), "Reviewers": d["reviewer"].nunique(),
                     **shares(d), "Major % on twice-reviewed only": pct(d2["major"].mean()), "Flagged % on twice-reviewed only": pct(d2["flag"].mean())})
emit("T1b. First and second review, languages reviewed twice", pd.DataFrame(rows))

# ---- T2 excluded systems -------------------------------------------------------------------
rows = []
for lang in ORDER:
    for kind, label in (("human", "human reference (refA)"), ("challenge", "MSLC")):
        d = allrev[(allrev["lang"] == lang) & (allrev["kind"] == kind) & (allrev["pass_"] == 1)]
        if len(d):
            mm = p1[p1["lang"] == lang]
            rows.append({"Language": load.NAMES[lang], "Excluded": label, "Translations": len(d), **shares(d), "Mean score": round(d["score"].mean(), 1),
                         "Machine systems: major %": pct(mm["major"].mean()), "Machine systems: mean score": round(mm["score"].mean(), 1)})
emit("T2. Excluded from the main tables: human references and MSLC (first review)", pd.DataFrame(rows))

# ---- T3 text type --------------------------------------------------------------------------
rows = []
for lang in ORDER:
    for tt in ["literary", "news", "social", "speech"]:
        d = p1[(p1["lang"] == lang) & (p1["text_type"] == tt)]
        rows.append({"Language": load.NAMES[lang], "Text type": tt, "Source passages": d["line_id"].nunique(), "Translations": len(d), **shares(d)})
t3 = pd.DataFrame(rows)
t3.to_csv(OUT / "t3_text_type.csv", index=False)
w = t3.pivot(index="Language", columns="Text type", values="Major %").reindex([load.NAMES[l] for l in ORDER]).reset_index()
emit("T3a. Major % by text type (first review)", w)
w = t3.assign(f=100 - t3["No-error %"]).pivot(index="Language", columns="Text type", values="f").round(1).reindex([load.NAMES[l] for l in ORDER]).reset_index()
emit("T3b. Flagged % (any error) by text type (first review)", w)
w = t3.pivot(index="Language", columns="Text type", values="Major n").reindex([load.NAMES[l] for l in ORDER]).reset_index()
emit("T3c. Major-error translations by text type (first review)", w)
w = t3[t3["Language"] == "Spanish"][["Text type", "Source passages"]]
emit("T3d. Source passages by text type (same in every language)", w)

# ---- T4 reviewer and vendor flag rates -----------------------------------------------------
def doc_boot(d, col, B=1000, seed=20261112):
    g = d.groupby("doc_id")[col].agg(["sum", "size"]).to_numpy()
    lo, hi = stats.cluster_boot(g, lambda s: s[0] / s[1], B=B, seed=seed)
    return pct(lo), pct(hi)


rows = []
for (lang, vendor, rev), d in m.groupby(["lang", "vendor", "reviewer"]):
    ns = d[d["text_type"] != "speech"]
    lo, hi = doc_boot(d, "flag")
    # the same translations as seen by the other review (twice-reviewed languages only)
    other = m[(m["lang"] == lang) & (m["reviewer"] != rev)].merge(d[load.KEY], on=load.KEY)
    rows.append({"lang": lang, "Language": load.NAMES[lang], "Vendor": vendor, "Reviewer": rev, "Reviews": len(d), "Documents": d["doc_id"].nunique(),
                 "Flagged %": pct(d["flag"].mean()), "Flagged % low": lo, "Flagged % high": hi, "Major %": pct(d["major"].mean()),
                 "Flagged %, no speech": pct(ns["flag"].mean()) if len(ns) else np.nan, "Mean score": round(d["score"].mean(), 1),
                 "Same translations, other reviewer: n": len(other), "Same translations, other reviewer: flagged %": pct(other["flag"].mean()) if len(other) else np.nan,
                 "Own flagged % on those": pct(d.merge(other[load.KEY].drop_duplicates(), on=load.KEY)["flag"].mean()) if len(other) else np.nan})
t4 = pd.DataFrame(rows)
t4.to_csv(OUT / "t4_reviewers.csv", index=False)

rows = []
for (lang, vendor), d in m.groupby(["lang", "vendor"]):
    r = t4[(t4["lang"] == lang) & (t4["Vendor"] == vendor) & (t4["Reviews"] >= 100)]
    lo, hi = doc_boot(d, "flag")
    rows.append({"lang": lang, "Language": load.NAMES[lang], "Vendor": vendor, "Reviewers": d["reviewer"].nunique(), "Reviews": len(d),
                 "Flagged %": pct(d["flag"].mean()), "95% range": f"{lo}-{hi}", "Major %": pct(d["major"].mean()),
                 "Reviewer flagged %: lowest": r["Flagged %"].min(), "median": r["Flagged %"].median(), "highest": r["Flagged %"].max(),
                 "Reviewers with 100+ reviews": len(r), "Share of reviews by the 2 busiest %": pct(d["reviewer"].value_counts().head(2).sum() / len(d))})
t4v = pd.DataFrame(rows).set_index("lang").loc[ORDER].reset_index(drop=True)
emit("T4. Flag rate (any error) by vendor, and the spread across that vendor's reviewers (all reviews, machine systems)", t4v,
     "95% range: percentile bootstrap, 1,000 resamples of documents. Reviewer spread uses reviewers with 100 or more reviews.")
t4v.to_csv(OUT / "t4_vendors.csv", index=False)

for lang in ["es", "ru", "uk", "is"]:
    r = t4[t4["lang"] == lang].sort_values(["Vendor", "Flagged %"])
    r = r.assign(**{"Flagged % (95% range)": [f"{a} ({b}-{c})" for a, b, c in zip(r["Flagged %"], r["Flagged % low"], r["Flagged % high"])]})
    emit(f"T4-{lang}. {load.NAMES[lang]}: each reviewer", r[["Vendor", "Reviewer", "Reviews", "Documents", "Flagged % (95% range)", "Major %", "Flagged %, no speech", "Mean score"]])
for lang in ["cs", "hi", "ja", "zh"]:
    r = t4[(t4["lang"] == lang)].sort_values("Flagged %")
    emit(f"T4-{lang}. {load.NAMES[lang]}: each reviewer, with the other reviewer's rate on the same translations",
         r[["Reviewer", "Reviews", "Flagged %", "Major %", "Mean score", "Same translations, other reviewer: n", "Own flagged % on those", "Same translations, other reviewer: flagged %"]])

# vendor x text type, Spanish
d = p1[p1["lang"] == "es"]
w = (d.pivot_table(index="vendor", columns="text_type", values="flag", aggfunc="mean") * 100).round(1).reset_index()
emit("T4-es-b. Spanish: flagged % by vendor and text type", w)
w = d.pivot_table(index="vendor", columns="text_type", values="flag", aggfunc="size").reset_index()
emit("T4-es-c. Spanish: translations by vendor and text type", w)

# ---- T5 agreement between first and second review ------------------------------------------
def agreement(d):
    """d: twice-reviewed translations, one row each, columns line_id, c1, c2 (group codes)."""
    per = np.stack([stats.coincidence(g["c1"].to_numpy(), g["c2"].to_numpy()) for _, g in d.groupby("line_id")])
    o = per.sum(0)
    fns = {"alpha, 3 groups (ordinal)": lambda o: stats.alpha(o, "ordinal"),
           "alpha, 3 groups (nominal)": lambda o: stats.alpha(o, "nominal"),
           "alpha, any error yes/no": lambda o: stats.alpha(stats.binary(o, [1, 2])),
           "alpha, major yes/no": lambda o: stats.alpha(stats.binary(o, [2]))}
    out = {"Translations": len(d), "Source passages": d["line_id"].nunique(), "Same group %": pct((d["c1"] == d["c2"]).mean())}
    for name, fn in fns.items():
        lo, hi = stats.cluster_boot(per, fn)
        out[name] = f"{fn(o):.2f} ({lo:.2f}-{hi:.2f})"
    return out


rows, rows_tt, rows_same, cond = [], [], [], []
pairs_all = {}
for lang in ["cs", "hi", "ja", "zh"]:
    a = m[(m["lang"] == lang)]
    w = a[a["pass_"] == 1].merge(a[a["pass_"] == 2], on=load.KEY, suffixes=("1", "2"))
    w = w.rename(columns={"code1": "c1", "code2": "c2", "text_type1": "text_type"})
    diff, same = w[w["reviewer1"] != w["reviewer2"]], w[w["reviewer1"] == w["reviewer2"]]
    pairs_all[lang] = diff
    rows.append({"Language": load.NAMES[lang], "Reviewer pairs": diff.groupby(["reviewer1", "reviewer2"]).ngroups, **agreement(diff)})
    rows_same.append({"Language": load.NAMES[lang], **agreement(same)})
    rows_tt.append({"Language": load.NAMES[lang], "Cut": "no speech", **agreement(diff[diff["text_type"] != "speech"])})
    rows_tt.append({"Language": load.NAMES[lang], "Cut": "speech only", **agreement(diff[diff["text_type"] == "speech"])})
    # what the other reviewer said, in both directions (each translation counted twice)
    lab = pd.concat([diff[["c1", "c2"]].rename(columns={"c1": "a", "c2": "b"}), diff[["c1", "c2"]].rename(columns={"c2": "a", "c1": "b"})])
    for code, gname in enumerate(load.GROUPS):
        s = lab[lab["a"] == code]["b"]
        cond.append({"Language": load.NAMES[lang], "One reviewer said": gname, "Reviews": len(s), "Other said no-error %": pct((s == 0).mean()),
                     "minor-only %": pct((s == 1).mean()), "major %": pct((s == 2).mean())})
    ct = pd.crosstab(diff["c1"], diff["c2"]).reindex(index=[0, 1, 2], columns=[0, 1, 2], fill_value=0)
    ct.index = [f"first: {g}" for g in load.GROUPS]; ct.columns = [f"second: {g}" for g in load.GROUPS]
    ct.to_csv(OUT / f"t5_crosstab_{lang}.csv")
emit("T5. Agreement between the first and second review, different reviewers (Krippendorff's alpha, 95% range from resampling source passages)", pd.DataFrame(rows))
emit("T5b. Same cut, speech separated", pd.DataFrame(rows_tt))
emit("T5c. Same reviewer reviewing the same translation twice (first and second pass)", pd.DataFrame(rows_same))
emit("T5d. When one reviewer put a translation in a group, what the other reviewer said", pd.DataFrame(cond))
rows_e = []
for lang, diff in pairs_all.items():
    for cut, d in (("all", diff), ("no speech", diff[diff["text_type"] != "speech"])):
        rows_e.append({"Language": load.NAMES[lang], "Cut": cut, "Translations with two reviewers": len(d),
                       "Both no-error": int(((d["c1"] == 0) & (d["c2"] == 0)).sum()), "Both major": int(((d["c1"] == 2) & (d["c2"] == 2)).sum()),
                       "Exactly one major": int(((d["c1"] == 2) != (d["c2"] == 2)).sum()),
                       "One major, other no-error": int((((d["c1"] == 2) & (d["c2"] == 0)) | ((d["c1"] == 0) & (d["c2"] == 2))).sum()),
                       "Source passages with a both-major translation": d[(d["c1"] == 2) & (d["c2"] == 2)]["line_id"].nunique()})
emit("T5e. Translations where two different reviewers gave the same verdict", pd.DataFrame(rows_e))
pd.DataFrame(rows_e).to_csv(OUT / "t5_two_reviewer_labels.csv", index=False)
pd.DataFrame(rows).to_csv(OUT / "t5_agreement.csv", index=False)
pd.DataFrame(cond).to_csv(OUT / "t5_conditional.csv", index=False)

# ---- T6 paper vs files ---------------------------------------------------------------------
paper = {"cs": (15, 1.3, 20, 751), "es": (13, 1.0, 14, 370), "hi": (10, 1.3, 15, 775), "is": (10, 1.0, 4, 376),
         "ja": (12, 1.5, 14, 1212), "ru": (13, 1.0, 7, 370), "uk": (10, 1.0, 8, 376), "zh": (12, 1.5, 12, 1217)}
rows = []
for lang in ORDER:
    a = allrev[(allrev["lang"] == lang) & (allrev["kind"] != "human")]
    r = raw[(raw["lang"] == lang)]
    ps, pd_, pa, pn = paper[lang]
    rows.append({"Language": load.NAMES[lang], "Systems: paper": ps, "files": a["system"].nunique(),
                 "Reviewers: paper": pa, "files ": allrev[allrev["lang"] == lang]["reviewer"].nunique(),
                 "Reviews per translation: paper": pd_, "files  ": round(len(a) / a.drop_duplicates(load.KEY).shape[0], 2),
                 "Reviews per system: paper": pn, "files, incl. refA, before de-duplication": round(len(r) / r["system"].nunique()),
                 "Source passages: paper": 649, "files   ": a["line_id"].nunique(), "Documents: paper": 170, "files    ": a["doc_id"].nunique()})
emit("T6. WMT24 findings paper (Table 6) against the files", pd.DataFrame(rows))

(OUT / "tables.md").write_text("\n".join(md))
print("\n".join(md))
