# Phase 1 report: the human reviews

What the WMT24 span-level human reviews look like for the eight English→X languages, and which of them can carry a judge study. No LLM was called for anything here.

All numbers were counted from the files (`python3 src/tables.py`; full tables in [out/tables.md](out/tables.md)). Where the paper and the files differ, section 7 says so.

## 1. Source

| Item | Value |
|---|---|
| Data | `wmt-conference/wmt24-news-systems`, folder `humeval/`, commit `fabe1f8` (2025-11-20) |
| License | None stated. Data is downloaded by `scripts/download.sh` and never committed; no source or translation text is in this repo |
| Paper | Kocmi et al., WMT24 findings, section 6 (https://aclanthology.org/2024.wmt-1.1.pdf) |
| Review method | Error Span Annotation (ESA): the reviewer marks error spans as minor or major, with no error category, then gives a 0-100 score (Kocmi et al. 2024b, https://aclanthology.org/2024.wmt-1.131) |
| Unit | One translation = one system's output for one source passage |
| Group | major = at least one major span; minor-only = spans but none major; no-error = no spans. Same three groups as `mqm-judge-eval` |

Terms: "flagged" = any error marked. "First review" = waves 0-1 in the files; "second review" = waves 2-3, which exist only for Czech, Hindi, Japanese and Chinese.

## 2. Rows kept

| Language | Rows in files | Dropped by the repo's own filters | Repeat submissions dropped | Reviews used | Human reference | MSLC |
|---|---:|---:|---:|---:|---:|---:|
| Czech | 19,086 | 4,065 | 364 | 14,657 | 919 | 0 |
| Spanish | 11,443 | 2,534 | 33 | 8,876 | 634 | 634 |
| Hindi | 13,175 | 2,879 | 55 | 10,241 | 931 | 0 |
| Icelandic | 8,918 | 1,928 | 16 | 6,974 | 634 | 0 |
| Japanese | 21,341 | 4,768 | 89 | 16,484 | 1,268 | 0 |
| Russian | 11,426 | 2,526 | 24 | 8,876 | 634 | 0 |
| Ukrainian | 8,933 | 1,929 | 30 | 6,974 | 634 | 0 |
| Chinese | 21,402 | 4,751 | 167 | 16,484 | 1,268 | 0 |

- Repo filters (from `humeval/merge_to_jsonl.py`): type `BAD` (quality-control items with planted errors), doc ids ending `#bad`, `#dup`, `#incomplete`, and tutorial documents.
- Repeat submissions: the same reviewer reviewing the same translation more than once within one pass (86% carry an identical score). The latest is kept. This rule is mine, not the repo's.
- 73 spans carry the severity `undecided`. They count as an error of unknown size: they can make a translation minor-only, never major. This decides the group of 11 translations.

## 3. Per language (machine systems, first review of each translation)

| Language | Vendor | Systems | Translations | Reviewers | Reviewed twice | No-error % | Minor-only % | Major % | Major n |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | Charles Univ. | 15 | 9,283 | 19 | 46% | 55.1 | 27.6 | 17.4 | 1,612 |
| Spanish | Microsoft + Toloka | 12 | 7,608 | 14 | 0% | 62.0 | 19.5 | 18.5 | 1,411 |
| Hindi | Microsoft | 10 | 6,340 | 15 | 47% | 65.2 | 20.8 | 14.0 | 890 |
| Icelandic | Árni Magnússon Inst. | 10 | 6,340 | 4 | 0% | 21.5 | 35.2 | 43.3 | 2,748 |
| Japanese | Microsoft | 12 | 7,608 | 14 | 100% | 82.1 | 11.9 | 6.0 | 456 |
| Russian | Toloka | 13 | 8,242 | 7 | 0% | 54.1 | 24.9 | 21.0 | 1,732 |
| Ukrainian | Toloka | 10 | 6,340 | 8 | 0% | 66.4 | 14.1 | 19.5 | 1,234 |
| Chinese | Microsoft | 12 | 7,608 | 14 | 100% | 77.6 | 12.2 | 10.2 | 778 |

- Every language has the same 634 source passages in 170 documents: 80 literary, 138 news, 305 social, 111 speech.
- Czech has 9,283 translations, not 634 × 15 = 9,510: some passages were reviewed for 13 or 14 of the 15 systems.
- The Spanish row blends two vendors with very different flag rates (section 5). Do not read 18.5% as one number.

### Text type: major %

| Language | Literary | News | Social | Speech |
|---|---:|---:|---:|---:|
| Czech | 19.6 | 10.9 | 15.8 | 28.3 |
| Spanish | 14.7 | 14.6 | 15.2 | 35.6 |
| Hindi | 11.0 | 14.8 | 10.6 | 24.7 |
| Icelandic | 45.4 | 48.8 | 33.4 | 62.3 |
| Japanese | 5.6 | 2.7 | 5.5 | 11.6 |
| Russian | 18.5 | 16.5 | 17.4 | 38.5 |
| Ukrainian | 21.2 | 14.0 | 16.2 | 34.1 |
| Chinese | 11.7 | 4.8 | 9.2 | 18.8 |

Speech has roughly twice the major rate of the other types in every language. The source text for speech is a machine transcript; reviewers saw the video (paper, section 6). The paper attributes the low speech scores to that transcript.

## 4. Excluded from the main tables

| Language | Excluded | Translations | Major % | Machine systems: major % |
|---|---|---:|---:|---:|
| Czech | human reference | 622 | 8.0 | 17.4 |
| Spanish | human reference | 634 | 6.6 | 18.5 |
| Spanish | MSLC | 634 | 54.4 | 18.5 |
| Hindi | human reference | 634 | 8.5 | 14.0 |
| Icelandic | human reference | 634 | 4.3 | 43.3 |
| Japanese | human reference | 634 | 3.6 | 6.0 |
| Russian | human reference | 634 | 11.4 | 21.0 |
| Ukrainian | human reference | 634 | 15.3 | 19.5 |
| Chinese | human reference | 634 | 6.2 | 10.2 |

- MSLC appears only in Spanish. The paper (appendix B.10) describes it as a deliberately simple baseline built for the metrics task, not as a broken system. It is excluded because it is an outlier by design (54% major against 18.5%).
- Russian and Ukrainian reviewers marked a major error in 11% and 15% of human reference translations, the two highest rates. The files cannot say whether the references are weaker or the reviewers stricter.

## 5. Reviewers and vendors

Flag rate = share of a reviewer's reviews with any error marked. 95% ranges: percentile bootstrap, 1,000 resamples of documents (a reviewer works through whole documents, so documents are the independent unit; resampling the clustering unit is convention).

| Language | Vendor | Reviewers | Reviews | Flagged % (95% range) | Major % | Reviewer flag rate: lowest / median / highest | Reviews done by the 2 busiest |
|---|---|---:|---:|---|---:|---|---:|
| Czech | Charles Univ. | 19 | 13,738 | 42.5 (39.7-45.8) | 16.2 | 20 / 44 / 82 | 22% |
| Spanish | Microsoft | 12 | 4,188 | 15.3 (13.4-17.6) | 4.5 | 8 / 14 / 27 | 29% |
| Spanish | Toloka | 2 | 3,420 | 65.9 (61.8-70.1) | 35.7 | 44 / 64 / 83 | 100% |
| Hindi | Microsoft | 15 | 9,310 | 34.5 (32.4-36.9) | 13.7 | 10 / 38 / 57 | 18% |
| Icelandic | Árni Magnússon Inst. | 4 | 6,340 | 78.5 (75.8-81.6) | 43.3 | 73 / 79 / 83 | 50% |
| Japanese | Microsoft | 14 | 15,216 | 18.1 (16.6-19.9) | 6.6 | 3 / 19 / 57 | 20% |
| Russian | Toloka | 7 | 8,242 | 45.9 (43.1-49.2) | 21.0 | 23 / 46 / 60 | 51% |
| Ukrainian | Toloka | 8 | 6,340 | 33.6 (30.8-36.7) | 19.5 | 18 / 33 / 51 | 63% |
| Chinese | Microsoft | 14 | 15,216 | 21.2 (19.4-23.3) | 9.6 | 3 / 18 / 58 | 24% |

Reviewer spread uses reviewers with 100 or more reviews. Per-reviewer rows: [out/t4_reviewers.csv](out/t4_reviewers.csv).

**Spanish.** Each source passage went to exactly one vendor (297 + 52 speech passages to Microsoft, 226 + 59 to Toloka). On every text type Toloka flagged far more:

| Vendor | Literary | News | Social | Speech |
|---|---:|---:|---:|---:|
| Microsoft flagged % | 10.4 | 11.1 | 13.5 | 32.5 |
| Toloka flagged % | 75.4 | 67.2 | 57.1 | 83.1 |

The two Toloka reviewers flagged 83.4% (1,911 reviews) and 43.7% (1,509). This matches the earlier finding from the Unbabel comparison (85% and 45% on the overlapping subset).

**Russian and Ukrainian (Toloka only).** No reviewer with 100+ reviews flags "almost everything": the range is 23-60% (Russian) and 18-51% (Ukrainian). But two reviewers did 51% and 63% of the work, and there is no second vendor and no second review, so reviewer strictness cannot be separated from translation quality in these two languages.

**The minor/major line is personal.** Among reviewers with 100+ reviews, the share of a reviewer's flagged translations that they called major ranges:

| Language | Lowest | Median | Highest |
|---|---:|---:|---:|
| Czech | 12% | 41% | 64% |
| Spanish, Microsoft | 10% | 31% | 45% |
| Hindi | 15% | 37% | 88% |
| Icelandic | 51% | 55% | 60% |
| Japanese | 7% | 41% | 72% |
| Russian | 26% | 47% | 93% |
| Ukrainian | 41% | 55% | 89% |
| Chinese | 6% | 32% | 87% |

One Russian reviewer called 93% of the translations they flagged major; one Chinese reviewer 6%.

**Same translations, different reviewer.** In the twice-reviewed languages a reviewer's flag rate can be set against what the other reviewer said about the same translations. The strictest Japanese reviewer flagged 57.9% where the others flagged 15.3%; the most lenient flagged 2.6% where the others flagged 19.8%. Chinese: 58.1% against 14.5%, and 2.6% against 22.2%. So the spread is the reviewer, not the material.

## 6. Reviewer-to-reviewer agreement

Only Czech, Hindi, Japanese and Chinese have a second review. Japanese and Chinese: every translation. Czech and Hindi: 297 of the 634 source passages.

**Statistic: Krippendorff's alpha.** Why: the two reviews of a translation come from whichever two of 12-19 reviewers were assigned (125 to 186 different reviewer pairings per language). Cohen's kappa assumes the same two named reviewers throughout, so it does not fit. Alpha treats reviewers as interchangeable, handles this design, and has an ordinal form for the ordered groups no-error < minor-only < major (Krippendorff 2011; Hayes & Krippendorff 2007). With two reviews per item, nominal alpha is numerically close to Fleiss' kappa. Reading: Krippendorff's convention is 0.80 or more for reliable data and 0.667 as the lowest level for tentative conclusions.

**95% ranges:** percentile bootstrap, 2,000 resamples of source passages, because the 10-15 translations of one passage are not independent (resampling the clustering unit; same practice as paired bootstrap over test segments in MT evaluation, Koehn 2004).

Different reviewers on the same translation:

| Language | Translations | Source passages | Same group | Alpha, 3 groups ordinal | Alpha, any error | Alpha, major |
|---|---:|---:|---:|---|---|---|
| Czech | 4,063 | 297 | 54.5% | 0.30 (0.27-0.33) | 0.27 (0.24-0.30) | 0.22 (0.19-0.26) |
| Hindi | 2,714 | 297 | 57.4% | 0.27 (0.23-0.30) | 0.20 (0.17-0.24) | 0.34 (0.29-0.38) |
| Japanese | 7,003 | 634 | 72.2% | 0.17 (0.14-0.20) | 0.15 (0.12-0.18) | 0.18 (0.14-0.22) |
| Chinese | 6,786 | 634 | 69.0% | 0.18 (0.15-0.20) | 0.16 (0.13-0.18) | 0.18 (0.14-0.21) |

All four are far below 0.667. "Same group" is high in Japanese and Chinese only because most translations are no-error; alpha corrects for that.

Removing speech does not help (alpha, 3 groups ordinal, no speech: Czech 0.27, Hindi 0.25, Japanese 0.15, Chinese 0.16).

The same reviewer seeing the same translation again in the second pass (a by-product of assignment, about 8% of second reviews; not a designed re-test):

| Language | Translations | Same group | Alpha, 3 groups ordinal |
|---|---:|---:|---|
| Czech | 248 | 70.2% | 0.47 (0.34-0.60) |
| Hindi | 256 | 75.0% | 0.53 (0.41-0.64) |
| Japanese | 605 | 85.1% | 0.47 (0.37-0.57) |
| Chinese | 822 | 80.3% | 0.59 (0.52-0.65) |

Reviewers agree with themselves at 0.47-0.59 and with each other at 0.17-0.30.

**When one reviewer marked a major error, the other reviewer:**

| Language | Reviews with a major | Also marked major | Marked only minor | Marked nothing |
|---|---:|---:|---:|---:|
| Czech | 1,282 | 34.5% | 31.5% | 34.0% |
| Hindi | 762 | 43.0% | 20.7% | 36.2% |
| Japanese | 936 | 23.5% | 17.4% | 59.1% |
| Chinese | 1,250 | 25.3% | 17.3% | 57.4% |

A second human reviewer "clears" 34-59% of the translations a first reviewer called major. Any judge scored against a single review inherits this.

**Translations where two different reviewers gave the same verdict:**

| Language | Two reviewers | Both no-error | Both major | Both major, no speech | Exactly one said major |
|---|---:|---:|---:|---:|---:|
| Czech | 4,063 | 1,632 | 221 | 135 | 840 |
| Hindi | 2,714 | 1,230 | 164 | 101 | 434 |
| Japanese | 7,003 | 4,815 | 110 | 61 | 716 |
| Chinese | 6,786 | 4,427 | 158 | 96 | 934 |

## 7. Paper against files

| Item | Paper (section 6, Table 6) | Files |
|---|---|---|
| Source passages per language | 649 | 634 |
| Documents | 170 | 170 |
| Systems | 15 / 13 / 10 / 10 / 12 / 13 / 10 / 12 | Same (Spanish 13 includes MSLC; human reference not counted) |
| Reviewers, Czech | 20 | 19 |
| Reviewers, Chinese | 12 | 14 |
| Reviewers, other six | 14 / 15 / 4 / 14 / 7 / 8 | Same |
| Reviews per translation, Czech and Hindi | 1.3 | 1.46 and 1.47 |
| Reviews per translation, Japanese and Chinese | 1.5 | 2.0 |
| Reviews per system | 370-1,217 | 635-1,281; the paper's figures do not reproduce under any filter I tried |
| MSLC | Deliberately simple baseline (appendix B.10) | The task brief called it broken; the paper does not |
| Agreement between reviewers | Said to be computable; no number reported in section 6 | Section 6 above |

I cannot explain the 649 vs 634 gap or the reviews-per-system gap from the files.

## 8. What is and is not comparable across languages

| Comparable | Not comparable |
|---|---|
| Source passages: identical 634 in every language | Group shares: they mix translation quality with reviewer strictness |
| Protocol and tool: same ESA interface, same quality-control rule | Vendors: four organisations with different reviewer profiles (paper, Table 5) |
| Text-type pattern: speech worst everywhere | Systems: a different set of 10-15 per language |
| Agreement statistics within the four twice-reviewed languages (same design) | "Major": the minor/major line differs by reviewer (section 5) |
| | Label quality: measurable in four languages, unknown in the other four |

So a difference between two languages in any rate here, and later in any judge result, cannot be attributed to the language. Each language is reported on its own.

## 9. Which languages can carry a conclusion

| Language | Verdict | Reason |
|---|---|---|
| Japanese | Usable, with two-reviewer labels | Every translation reviewed twice by different reviewers (7,003). Alpha is low (0.17), so single reviews are weak labels; both-major is thin: 110 (61 without speech) |
| Chinese | Usable, with two-reviewer labels | Same design (6,786). Both-major 158 (96 without speech) |
| Czech | Usable on the twice-reviewed half | 4,063 translations on 297 passages. Both-major 221 (135 without speech). Widest reviewer spread (20-82% flagged) |
| Hindi | Usable on the twice-reviewed half | 2,714 translations on 297 passages. Both-major 164 (101 without speech). Best agreement on major (0.34) |
| Spanish | Not as one set | Vendor decides the label: Microsoft 15% flagged, Toloka 66%. The Microsoft half alone has 119 major translations without speech, single review. The Toloka half rests on two reviewers who disagree with each other by 40 points |
| Icelandic | Descriptive only | 4 consistent reviewers (73-83% flagged) but single review, so label quality is unknown; only 21.5% no-error |
| Russian | Descriptive only | Single review, one vendor, 2 reviewers did 51%; one reviewer calls 93% of flags major |
| Ukrainian | Descriptive only | Single review, one vendor, 2 reviewers did 63%; highest major rate on human references (15%) |

"Descriptive only" means: a judge can be run and compared with the reviews, but a miss-rate claim would rest on labels whose reliability cannot be checked from this data.

## 10. Assumptions and gaps

- Reviewer identity comes from `annotator_mapping.json` (108 pseudonyms). I assume it is correct; vendor is read from the pseudonym suffix.
- Identical outputs: 5-13% of translations are word-for-word the same as another system's output for the same passage (e.g. Spanish 7,608 translations, 6,699 distinct). They were reviewed separately, so they stay separate rows; this is one more reason ranges resample source passages. 0-5 translations per language are empty.
- Target locale: the paper's language list says "English→Spanish (Latin America)". I found no locale statement for the other seven (e.g. script for Chinese). The files state none.
- The second review was added because vendors "finished early" (paper, section 6.1), not by a sampling design. For Czech and Hindi the twice-reviewed 297 passages are 85 whole documents (20 literary, 81 news, 139 social, 57 speech passages; the other half has 60 / 57 / 166 / 54). First-review rates on the two halves: Czech major 16.8% vs 17.9%, Hindi 14.4% vs 13.7%. Close, but the text-type mix differs, so the twice-reviewed half is not a random half.
- Same-reviewer repeats are not a designed re-test; the time between the two looks is not analysed.
- No significance tests were run in this phase; everything is an estimate with a range.
