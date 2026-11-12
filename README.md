# esa-judge-eval

An LLM translation judge against human reviews in eight English→X languages (WMT24 general task, span-level ESA reviews: Czech, Spanish, Hindi, Icelandic, Japanese, Russian, Ukrainian, Chinese).

| File | What |
|---|---|
| [REPORT.md](REPORT.md) | Phase 1: what the human reviews look like, reviewer agreement, which languages can carry a conclusion |
| [DESIGN.md](DESIGN.md) | Phase 2: proposed judge study ("clearing with a guarantee"). Not yet run |
| `scripts/download.sh` | Fetches the public data at a pinned commit into `data/` (git-ignored) |
| `src/load.py` | One row per human review |
| `src/tables.py` | Phase 1 tables → `out/` |
| `src/design.py` | Sample sizes, passage splits, call and cost estimates → `out/design_tables.md`, `ids/` |

```bash
sh scripts/download.sh
```

```bash
python3 src/tables.py
```

```bash
python3 src/design.py
```

The data repo (`wmt-conference/wmt24-news-systems`) states no license, so no source or translation text is committed here: only code, ids, counts and derived numbers. No LLM has been called.
