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

## Background: the data and the literature

### Where the data come from

| | |
|---|---|
| Event | WMT24, the Ninth Conference on Machine Translation, November 2024. Its general translation task asks teams to submit translation systems, then has people review the output |
| What was collected | Translations of the same English passages (news, literary, social media, speech) by 10-15 machine systems per language plus a human reference, each reviewed by paid bilingual reviewers (professional translators in most languages; linguists, researchers and students for Czech) |
| Why it was collected | To rank translation systems against each other and against human translators |
| Where it is | [github.com/wmt-conference/wmt24-news-systems](https://github.com/wmt-conference/wmt24-news-systems), pinned here at commit `fabe1f8`. The repo states no license |
| Paper that describes it | Kocmi et al. 2024a, section 6 and appendix B |

### How this project uses the data differently

The organisers collected the reviews to answer "which translation system is best?". This project reuses the same reviews to answer a different question: **how far can an LLM be trusted to judge translations, measured against those human reviews, language by language?**

That reuse has consequences, because the collection was not designed for it:

| Design choice made for ranking systems | What it means for judging a judge |
|---|---|
| Most translations were reviewed once | No way to tell a reviewer's strictness from a translation's quality in four of the eight languages |
| Reviewers were assigned by passage, and Spanish was split between two vendors | Labels in Spanish depend on which vendor reviewed the passage (finding 4) |
| Speech reviewers watched the video | A text-only judge sees less than the reviewer did (finding 5) |

### What ESA is, and how it differs from MQM

Both are ways for a person to review a translation by marking the errors in it.

| | MQM (Multidimensional Quality Metrics) | ESA (Error Span Annotation) |
|---|---|---|
| Introduced | Lommel et al. 2014; adapted for machine translation research by Freitag et al. 2021 | Kocmi et al. 2024b; first used as WMT's main human review method in 2024 |
| What the reviewer marks | Each error span, its category (for example mistranslation, omission, grammar) and its severity (minor, major, sometimes critical) | Each error span and its severity (minor or major). No category |
| Where the score comes from | Computed from the errors with fixed weights (Freitag et al. 2021: minor 1, major 5, non-translation 25) | Given directly by the reviewer, 0-100, after marking the errors |
| Who reviews | Reviewers trained in the error typology | In WMT24: "professional translators but not experts in MQM/ESA-style annotations" (Kocmi et al. 2024a) |
| Cost | Slower and more expensive per translation | Designed to be cheaper: Kocmi et al. 2024a report it was more efficient to collect than MQM |
| In WMT24 | English→German and Japanese→Chinese in the general task; the metrics task also released English→Spanish MQM reviews (Freitag et al. 2024) | The eight English→X languages studied here, plus Czech→Ukrainian |

ESA sits between two older methods: giving one overall score with no error marking (direct assessment, Graham et al. 2013) and full MQM. The judge in this project marks errors the MQM way (with categories) because its instructions are carried over unchanged from an earlier project on the English→Spanish MQM data; it is then compared with ESA reviews at the level both share, whether a translation has no error, minor errors only, or a major error.

### Literature

| Topic | Reference | Link |
|---|---|---|
| The dataset | Kocmi et al. 2024a. Findings of the WMT24 General Machine Translation Shared Task: The LLM Era Is Here but MT Is Not Solved Yet. WMT 2024 | [aclanthology.org/2024.wmt-1.1](https://aclanthology.org/2024.wmt-1.1/) |
| ESA | Kocmi et al. 2024b. Error Span Annotation: A Balanced Approach for Human Evaluation of Machine Translation. WMT 2024 | [aclanthology.org/2024.wmt-1.131](https://aclanthology.org/2024.wmt-1.131/) |
| MQM, original framework | Lommel, Uszkoreit, Burchardt 2014. Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics. Tradumàtica 12 | Cited as in Kocmi et al. 2024a; not read for this project |
| MQM for machine translation | Freitag et al. 2021. Experts, Errors, and Context: A Large-Scale Study of Human Evaluation for Machine Translation. TACL | [aclanthology.org/2021.tacl-1.87](https://aclanthology.org/2021.tacl-1.87/) |
| MQM reviews in WMT24 | Freitag et al. 2024. Are LLMs Breaking MT Metrics? Results of the WMT24 Metrics Shared Task. WMT 2024 | [aclanthology.org/2024.wmt-1.2](https://aclanthology.org/2024.wmt-1.2/) |
| Direct assessment | Graham et al. 2013. Continuous Measurement Scales in Human Evaluation of Machine Translation | [aclanthology.org/W13-2305](https://aclanthology.org/W13-2305/) |
| An LLM marking MQM errors | Kocmi and Federmann 2023. GEMBA-MQM: Detecting Translation Quality Error Spans with GPT-4. WMT 2023 | [aclanthology.org/2023.wmt-1.64](https://aclanthology.org/2023.wmt-1.64/) |
| Clearing with a guarantee | Jung, Brahman, Choi 2024. Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement | [arxiv.org/abs/2407.18370](https://arxiv.org/abs/2407.18370) |
| The statistics behind the guarantee | Angelopoulos et al. 2021. Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control | [arxiv.org/abs/2110.01052](https://arxiv.org/abs/2110.01052) |
| Reviewer agreement | Krippendorff 2004. Content Analysis: An Introduction to Its Methodology, 2nd ed. | Book; source of alpha and the 0.667 floor |

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
