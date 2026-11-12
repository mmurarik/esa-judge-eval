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

## Findings so far

Counted from the public files, not taken from the paper. Detail and method are in [REPORT.md](REPORT.md).

| # | Finding | Numbers |
|---|---|---|
| 1 | Human reviewers barely agree with each other | Krippendorff's alpha on three groups (no error / minor only / major), two different reviewers: Czech 0.30, Hindi 0.27, Japanese 0.17, Chinese 0.18. The usual floor for usable labels is 0.667 (convention, Krippendorff 2004) |
| 2 | A second reviewer often marks nothing where the first marked a major error | Czech 34%, Hindi 36%, Japanese 59%, Chinese 57%. A judge scored against a single review inherits this noise |
| 3 | Only four languages were reviewed twice, and translations where both reviewers marked a major error are scarce | Without speech: Czech 135, Hindi 101, Chinese 96, Japanese 61. This caps how strong a guarantee the study can give |
| 4 | Spanish labels depend on the vendor | Microsoft's 12 reviewers flagged 15% of translations; Toloka's 2 reviewers flagged 66% (83% and 44% individually). The split is by passage, so the two vendors never reviewed the same translations |
| 5 | Speech passages carry about twice the major-error rate of other text | True in all eight languages. Reviewers saw the video; a judge would see only the transcript |

Where the files differ from the paper: 634 source passages per language (paper: 649); Czech 19 reviewers (paper: 20); Chinese 14 (paper: 12); Japanese and Chinese have 2.0 reviews per translation (paper: 1.5), Czech and Hindi about 1.47 (paper: 1.3).

## What we would do next

Proposal only; nothing below has been run. Detail and the basis for each choice are in [DESIGN.md](DESIGN.md).

**Question:** in each language, can the judge clear a share of translations as "no major error" while missing at most a stated share of real major errors, with a statistical guarantee? (Trust or Escalate, Jung et al. 2024, arXiv 2407.18370.)

| Choice | Proposal | Why |
|---|---|---|
| Languages | Czech, Hindi, Japanese, Chinese, each reported on its own | The only four with two reviews per translation. The other four can be described but not certified |
| What counts as a major error | Two different reviewers both marked one | Finding 2: a single review is too noisy to score against |
| Guarantee | Miss rate at most 10%, with 95% confidence; 5% reported as a stretch line | Exact binomial limit. 5% needs 59 confirmed majors with zero misses in the calibration set; Japanese has 36 |
| Splits | Development / calibration / test, split by source passage | No passage appears on both sides, so the test is not leaked |
| Speech | Separate test-only arm, outside the guarantee | Finding 5 |
| Judge | Claude Opus 5.5, medium effort, instructions frozen from the first project; only language and locale wording change | Keeps the two projects comparable |

Steps, in order:

| Step | Calls | What it settles |
|---|---:|---|
| 1. Development run | 240 | Locale wording works, answers parse, real token counts and cache hit rate |
| 2. Calibration run | 246 major-error translations | The confidence cut-off per language |
| 3. Test run | 2,047 | Miss rate and cleared share at that cut-off, with ranges |

Cost for all three steps, four languages, 2,533 calls (estimates; only the fixed 2,063 tokens of instructions per call are measured):

| Way of running | Expected | High |
|---|---:|---:|
| Standard API | $59.51 | $87.24 |
| Batch API | $29.76 | $43.62 |
| Batch API with prompt caching, every call hitting the cache | $19.83 | $32.70 |

Open decisions: the miss-rate limit (10% or 5%), the locale wording (DESIGN section 8), and the spend (recommended: Batch API with caching, hard cap $50).
