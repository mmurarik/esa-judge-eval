"""Loader: one row per human review (WMT24 general task, span-level ESA, English->X).

Filters follow humeval/merge_to_jsonl.py in the source repo: drop rows of type BAD,
doc ids ending #bad / #dup / #incomplete, and any -tutorial doc.
No source or translation text is loaded here; see texts() for that.
"""
import csv
import json
import pathlib
import re

import pandas as pd

DATA = pathlib.Path(__file__).resolve().parents[1] / "data"
LANGS = {"ces": "cs", "spa": "es", "hin": "hi", "isl": "is", "jpn": "ja", "rus": "ru", "ukr": "uk", "zho": "zh"}
NAMES = {"cs": "Czech", "es": "Spanish", "hi": "Hindi", "is": "Icelandic", "ja": "Japanese",
         "ru": "Russian", "uk": "Ukrainian", "zh": "Chinese"}
VENDORS = {"isl": "Arni Magnusson Inst.", "toloka": "Toloka", "ufal": "Charles Univ.", "microsoft": "Microsoft"}
GROUPS = ["no-error", "minor-only", "major"]
HUMAN = {"refA"}          # human reference translations
CHALLENGE = {"MSLC"}      # deliberately simple baseline built for the metrics task (WMT24 findings, app. B.10)
COLS = ["login", "system", "line_id", "type", "src", "tgt", "score", "doc_id", "flag", "spans", "start", "end"]


def group_of(severities):
    """major if any span is major; else minor-only if any span at all; else no-error.

    Severity values other than minor/major (ESA allows 'undecided') count as an error
    of unknown size: they make a translation minor-only, never major. Counted in n_other.
    """
    if "major" in severities:
        return "major"
    return "minor-only" if severities else "no-error"


def reviews(drop_filtered=True):
    amap = {login: name for name, logins in json.load(open(DATA / "humeval/annotator_mapping.json")).items()
            for login in logins}
    docs = {}
    rows = []
    for wave in range(4):
        with open(DATA / f"humeval/esa_generalMT2024_wave{wave}.csv", newline="") as fh:
            for r in csv.reader(fh):
                d = dict(zip(COLS, r))
                if d["src"] != "eng" or d["tgt"] not in LANGS:
                    continue
                bad = (d["type"] == "BAD" or d["doc_id"].endswith(("#bad", "#dup", "#incomplete"))
                       or "-tutorial" in d["doc_id"])
                if bad and drop_filtered:
                    continue
                lang = LANGS[d["tgt"]]
                if lang not in docs:
                    docs[lang] = [x.split("\t") for x in open(DATA / f"txt/documents/en-{lang}.docs").read().splitlines()]
                line = int(d["line_id"])
                sev = [s.get("severity") for s in json.loads(d["spans"])]
                if not bad:
                    assert docs[lang][line][1] == d["doc_id"], (lang, line, d["doc_id"])
                reviewer = amap[d["login"]]
                rows.append(dict(
                    lang=lang, wave=wave, system=d["system"], line_id=line, doc_id=d["doc_id"],
                    text_type=docs[lang][line][0] if not bad else None,
                    reviewer=reviewer, vendor=VENDORS[re.sub(r"^Annotator\d+", "", reviewer)],
                    group=group_of(sev), score=float(d["score"]), n_spans=len(sev),
                    n_major=sev.count("major"), n_minor=sev.count("minor"),
                    n_other=sum(s not in ("minor", "major") for s in sev),
                    start=float(d["start"]), end=float(d["end"]), filtered=bad,
                ))
    df = pd.DataFrame(rows)
    df["kind"] = df["system"].map(lambda s: "human" if s in HUMAN else "challenge" if s in CHALLENGE else "machine")
    df["group"] = pd.Categorical(df["group"], GROUPS, ordered=True)
    # Waves 0-1 are the first pass (disjoint halves of the passages); waves 2-3 are a second
    # pass over the same translations, run only for some languages (WMT24 findings, sec. 6.1).
    df["pass_"] = (df["wave"] >= 2).astype(int) + 1
    return df


KEY = ["lang", "system", "line_id"]


def dedupe(df):
    """One review per translation per pass.

    Within a pass a translation is always reviewed by one reviewer, but 493 reviewer-translation
    pairs appear more than once (task re-submissions; 86% carry an identical score). Keep the latest.
    """
    return df.sort_values("end").drop_duplicates(KEY + ["pass_"], keep="last").sort_values(KEY + ["pass_"]).reset_index(drop=True)


def texts(lang):
    """Source lines and {system: translation lines}. Text stays local; never written to out/."""
    src = open(DATA / f"txt/sources/en-{lang}.txt").read().split("\n")
    tgt = {p.stem: p.read_text().split("\n") for p in (DATA / f"txt/system-outputs/en-{lang}").glob("*.txt")}
    return src, tgt


if __name__ == "__main__":
    df = reviews()
    print(len(df), "reviews kept")
    print(df.groupby("lang").size())
