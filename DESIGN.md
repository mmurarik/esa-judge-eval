# Phase 2 design: the judge study

Status: proposal. Nothing here has been run. No LLM call is made until the cost in section 9 is approved.

Numbers come from `python3 src/design.py` ([out/design_tables.md](out/design_tables.md)); the human-review facts come from [REPORT.md](REPORT.md).

## 1. Question

For one language at a time: if the judge clears a translation (says it needs no human look), how often is a translation with a major error cleared, and what share of error-free translations is cleared?

| Term | Meaning |
|---|---|
| Judge | Claude Opus 5.5 (`claude-opus-5-5`), effort medium, prompt v4 from `mqm-judge-eval/src/judge.py`. Instructions change only in language and locale wording (section 8) |
| Penalty | Sum over the judge's errors: minor 1, minor punctuation 0.1, major or critical 5, non-translation 25. Same weights as project 1 (Google MQM weights; critical counted as major, WMT24 metrics practice) |
| Cleared | Penalty at or below the cut-off |
| Miss | A major-error translation that is cleared |
| Miss rate | Misses / major-error translations |
| Cleared share | Cleared / no-error translations |

## 2. Method: clearing with a guarantee

Source: Jung, Brahman, Choi, "Trust or Escalate: LLM Judges with Provable Guarantees for Human Agreement", arXiv 2407.18370 (ICLR 2025 per the brief; the arXiv page I read shows v1 and no venue).

### What the paper does

| Step | Paper (section 2.1, eqs. 1-5, theorem 1) |
|---|---|
| Rule | Trust the judge when its confidence is at or above a threshold; otherwise send to a human |
| Guarantee | P(judge agrees with the human label, given it was trusted) ≥ 1 − α, holding with probability ≥ 1 − δ over the draw of the calibration set |
| Calibration | For each threshold, count errors among trusted calibration items and take the exact-binomial upper confidence bound at level δ |
| Choosing the threshold | Fixed-sequence testing (Bauer 1991): start at the strictest threshold, loosen step by step, stop at the first threshold whose upper bound exceeds α. No multiple-testing correction is needed because the order is fixed in advance |
| Their settings | 392-500 calibration items; 1 − α of 0.80-0.90; δ = 0.1; human label = majority of 3-5 annotators |
| Their data | English summarisation and chat comparisons. No translation, nothing multilingual |

### Assumptions the guarantee needs

| Assumption | Paper | Here |
|---|---|---|
| Calibration items are independent draws from one population | Stated (section 3.4) | Partly broken: 10-15 translations share a source passage, and 5-13% are identical outputs. Handled by splitting by passage and adding a passage-resampling check (section 7). Stated as a limitation |
| Test items come from the same population | Implied | Holds by design within one language, one vendor, non-speech text. Does not transfer to another language, vendor, text type or set of systems |
| The judge is fixed | Implied | Model id, effort and prompt version are pinned; every answer is cached |
| The human label is the truth | Majority vote; label noise not analysed | Weakest point here. Reviewer-to-reviewer alpha is 0.17-0.30 (REPORT section 6). Section 3 defines labels to reduce this |
| Shift between calibration and use | No theorem; tested empirically | Not claimed |

Gaps in the paper that I noticed and do not rely on: the proof shows the bound for a fixed threshold and asserts it for the chosen one; ties and skipped items in the human label are not specified.

### How this study differs from the paper

| | Paper | This study | Why |
|---|---|---|---|
| Quantity bounded | Disagreement among trusted items | Miss rate among major-error translations | The brief asks for a miss-rate limit; it does not depend on how common major errors are, so it is not moved by reviewer strictness the way a "share of cleared that are bad" figure is. The second figure is reported too |
| Confidence score | Simulated annotators (several few-shot prompts) | The judge's penalty | Decided by the user. One call per translation |
| Procedure | Exact-binomial bound + fixed sequence | Same | Miss count can only rise as the cut-off loosens, so the fixed order is natural |

The general form of this procedure (any bounded risk, fixed-sequence testing) is "Learn then Test", Angelopoulos et al. 2021, arXiv 2110.01052.

### Cut-off grid, fixed in advance

Cut-offs tested in this order: 0, 0.5, 1, 2, 3, 4, 4.9. A cut-off of 5 or more would clear translations in which the judge itself reported a major error, so the grid stops at 4.9. The chosen cut-off is the last one before the first failure. If cut-off 0 fails, the result is "no cut-off certified" and that is reported.

## 3. Labels

| Languages | Label | Major | No-error | Basis |
|---|---|---|---|---|
| Czech, Hindi, Japanese, Chinese | Two different reviewers | Confirmed major: both marked a major error | Confirmed clean: both marked nothing | A second human clears 34-59% of single-review majors (REPORT section 6). A limit on misses only means something against majors that two people saw |
| Spanish (Microsoft half), Icelandic, Russian, Ukrainian | One reviewer | That reviewer marked a major error | That reviewer marked nothing | Only label there is. Reliability cannot be checked |

- Translations where the two reviews disagree form a third stratum ("other"). They are judged in the test set and reported descriptively: what the judge does when humans split.
- Second reviews by the same reviewer (about 8%) are not used as two-reviewer labels.
- Known bias: a translation is more likely to be "confirmed major" if it happened to get two strict reviewers. Confirmed majors are therefore the clearer majors, and the miss rate against them is probably lower than against all true majors. Stated, not corrected.
- Secondary analysis in the twice-reviewed languages: the same procedure against "at least one reviewer marked major", to show how much the label definition moves the result.

Counts (no speech):

| Language | Confirmed major | on source passages | Confirmed clean | Other |
|---|---:|---:|---:|---:|
| Czech | 135 | 94 | 1,471 | 1,673 |
| Hindi | 101 | 83 | 1,072 | 1,012 |
| Japanese | 61 | 51 | 4,213 | 1,500 |
| Chinese | 96 | 74 | 3,874 | 1,619 |

| Language (one reviewer) | Major | on source passages | No-error | Minor-only |
|---|---:|---:|---:|---:|
| Spanish, Microsoft half, spent passages removed | 110 | 79 | 2,867 | 287 |
| Icelandic | 2,056 | 477 | 1,304 | 1,870 |
| Russian | 1,176 | 415 | 3,991 | 1,632 |
| Ukrainian | 856 | 379 | 3,674 | 700 |

## 4. Sample sizes (exact binomial)

Statistic: Clopper-Pearson exact-binomial bound. Why: counts are small and the miss rate is near zero, where normal-approximation ranges are wrong; it is also what the paper uses. One-sided 95% for the miss-rate limit (a limit is a one-sided claim); two-sided 95% for the cleared share.

Major-error translations needed in the calibration set:

| Misses allowed at the chosen cut-off | For a 5% limit | For a 10% limit |
|---:|---:|---:|
| 0 | 59 | 29 |
| 1 | 93 | 46 |
| 2 | 124 | 61 |
| 3 | 153 | 76 |
| 4 | 181 | 89 |

The brief's starting point (about 100 majors for "under 5%") matches the second row: 93 majors allow one miss.

Cleared share, two-sided 95% range:

| No-error translations | Range if 35% are cleared | Half-width |
|---:|---|---:|
| 100 | 25.7% to 45.2% | 9.7 points |
| 150 | 27.1% to 42.9% | 7.9 points |
| 200 | 28.4% to 42.0% | 6.8 points |

200 no-error translations per language give about ±7 points (the brief's 150 gives about ±8).

## 5. Sets and what each language can support

Split by source passage, seeded, so a passage is in exactly one set (`ids/split_<lang>.csv`).

| Set | Passages | Use |
|---|---|---|
| Development | 20 per language. In the twice-reviewed languages they are drawn from passages with no confirmed major, so no scarce major is spent | 60 calls: check the locale wording renders, answers parse, token counts match the cost estimate. Not used to change instructions or pick the cut-off |
| Calibration | 60% of the rest | Majors only. Picks the cut-off |
| Test | 40% of the rest | All majors, 200 no-error, 150 other. Reports miss rate, cleared share, agreement |

The 60/40 split is stratified by text type and by whether the passage has a major-error translation.

Twice-reviewed languages have too few confirmed majors to draw a sample: all of them are used. This is the binding constraint of the whole design.

| Language | Label | Majors: calibration / test | 5% limit: misses allowed | Chance to certify 5% if the true miss rate is 1% | 10% limit: misses allowed | Chance to certify 10% if true rate is 1% / 3% | Test upper bound if 0 missed |
|---|---|---|---|---:|---:|---|---:|
| Czech | two reviewers | 87 / 48 | 0 | 42% | 3 | 99% / 74% | 6.1% |
| Hindi | two reviewers | 64 / 37 | 0 | 53% | 2 | 97% / 70% | 7.8% |
| Chinese | two reviewers | 59 / 37 | 0 | 55% | 1 | 88% / 47% | 7.8% |
| Japanese | two reviewers | 36 / 25 | cannot certify | 0% | 0 | 70% / 33% | 11.3% |
| Spanish (Microsoft) | one reviewer | 65 / 38 | 0 | 52% | 2 | 97% / 69% | 7.6% |
| Icelandic | one reviewer | 150 / 150 | 2 | 81% | 8 | 100% / 96% | 2.0% |
| Russian | one reviewer | 150 / 150 | 2 | 81% | 8 | 100% / 96% | 2.0% |
| Ukrainian | one reviewer | 150 / 150 | 2 | 81% | 8 | 100% / 96% | 2.0% |

Reading:

- A 5% limit is not realistic with two-reviewer labels and no speech. Czech, Hindi and Chinese would need zero misses and would fail about half the time even with a judge whose true miss rate is 1%. Japanese cannot certify 5% at all (36 < 59).
- A 10% limit at 95% confidence is supportable in Czech and Hindi, borderline in Chinese, weak in Japanese. This is still stricter than the paper's own settings (10-20% at 90%).
- The once-reviewed languages have plenty of majors but the label rests on one reviewer.

**Recommendation:** limit 10%, confidence 95%, for all languages; also report whether the 5% line was met. Japanese is run and reported with its low power stated up front.

Alternative if 5% matters more than clean scope: include speech in the population (confirmed majors rise to 221 / 164 / 110 / 158). Not recommended, see section 6.

## 6. Speech

| Fact | Source |
|---|---|
| Reviewers watched the video; the judge would see only a machine transcript | WMT24 findings, section 6 |
| Speech has about twice the major rate of other text in every language | REPORT section 3 |
| Agreement on speech is no better than elsewhere | REPORT section 6 |

**Recommendation:** exclude speech from calibration and from every guaranteed number. Run it as a separate test-only arm in the twice-reviewed languages (all speech confirmed majors plus 60 confirmed clean; 109-146 calls per language) and report the miss rate at the cut-off chosen on non-speech text, labelled as outside the guarantee. Reason: the judge and the reviewers did not see the same input, so a miss on speech cannot be read as a judge failure.

## 7. Analyses, announced in advance

| # | Analysis | Statistic | Why this one |
|---|---|---|---|
| 1 | Pick the cut-off (calibration) | One-sided 95% exact-binomial upper bound on the miss rate, fixed-sequence over the grid | Paper's procedure; exact because counts are small |
| 2 | Miss rate at the chosen cut-off (test) | Misses / majors with a one-sided 95% exact-binomial upper bound | Independent check of 1 on unseen passages |
| 3 | Cleared share (test) | Cleared / no-error with a two-sided 95% exact-binomial range | Same reason |
| 4 | Independence check for 2 and 3 | Percentile bootstrap, 2,000 resamples of source passages | Translations of one passage are not independent; if this range is clearly wider than the exact one, the exact one is too optimistic and I say so |
| 5 | Overall share cleared and share of cleared with a major | Stratum results weighted by each stratum's size in the test passages | Test strata are sampled at different rates |
| 6 | Judge against the reviewers, three groups | Krippendorff's alpha (ordinal), judge vs each review, next to reviewer vs reviewer on the same translations; difference with a passage-bootstrap range | Same statistic as REPORT so the judge is placed on the human scale. A judge cannot be expected to agree with reviewers more than they agree with each other |
| 7 | Label-definition sensitivity | Repeat 1-3 with "at least one reviewer marked major" | Shows how far the result depends on section 3 |
| 8 | Own-family check | Repeat 2-3 without Claude-3.5's translations | The judge is a Claude model and Claude-3.5 is one of the translation systems |

- Significance thresholds, where a test is used (the difference in 6): p ≤ .10 significant, .10-.20 trending, ≥ .20 non-significant. The p-value is the share of bootstrap differences on the other side of zero, doubled.
- No test compares languages. Each language gets its own row; no pooled figure is computed.
- Nothing is tuned after the test set is opened. The 108 spent Spanish translations and every passage they sit on are excluded (`ids/spent_enes.csv`, 96 passages).

## 8. Language and locale wording (needs your approval)

Only these parts of the v4 instructions change; everything else is identical in all languages. The paper states a locale only for Spanish ("Latin America"). The rest are my proposals.

| Language | "The target is ..." | Replacement for the Spain/Mexico example in the language-variety category | Basis |
|---|---|---|---|
| Spanish | Latin American Spanish, as used in Mexico (unchanged from v4) | Unchanged | Paper: Latin America; WMT24 metrics paper: Mexico |
| Chinese | Simplified Chinese, as used in mainland China | Traditional characters, or vocabulary typical of Taiwan or Hong Kong | The reference translation is in Simplified characters (checked) |
| Japanese | Japanese, as used in Japan | Character forms or wording not used in standard Japanese | Assumption |
| Hindi | Hindi, as used in India, written in Devanagari | Romanised Hindi where Devanagari is expected, or a mix of varieties | Assumption; least sure about this one |
| Czech | Czech, as used in the Czech Republic | Words or forms from another language variety, such as Slovak | Assumption |
| Icelandic | Icelandic, as used in Iceland | Words or forms that do not belong to standard Icelandic | Assumption |
| Russian | Russian, as used in Russia | Vocabulary or forms from another regional variety | Assumption |
| Ukrainian | Ukrainian, as used in Ukraine | Russian words or forms where standard Ukrainian is expected | Assumption |

Also swapped mechanically: the language name wherever "Spanish" appears (task description, the labels on the source and translation).

Known mismatch, not fixed because instructions are frozen: v4 follows MQM guidelines with error categories; the ESA reviewers marked spans with no categories and lighter instructions.

## 9. Calls and cost

Prices: Claude Opus 5.5, per million tokens: $4 input, $20 output, $0.20 cache read, $5 cache write with the 5-minute lifetime (claude-api skill, price table cached 2026-11-03). The Message Batches API halves all four and suits this job (no need for instant answers).

Token basis, revised 2026-11-12:

| Part of a call | Tokens | Basis |
|---|---:|---|
| Fixed: instructions, answer schema, request overhead | 2,063 (95% range 2,042-2,086) | Measured. Least-squares fit of project 1's 108 Spanish calls: input tokens against the length of the per-translation message, rebuilt from local data. R² 0.99. Range from resampling calls. Least squares because the relation is linear by construction (tokens = fixed + rate × characters) |
| Variable: the passage, its translation, five neighbours each side | 1,290-2,110 by language | Estimated from character counts with assumed tokens-per-character by script. Only Spanish is measured (0.362 tokens per character) |
| Output | 450 expected | Project 1 measured a mean of 371 |

The fixed part is 64% of project 1's mean input (2,063 of 3,215), not the 45% the first version of this section assumed. "High" = fixed × 1.1, variable × 1.5, 800 output tokens.

Without caching:

| Language | Dev | Calibration | Test majors | Test clean | Test other | Speech arm | Calls | Variable tokens (est.) | Standard: expected / high | Batch: expected / high |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| Czech | 60 | 87 | 48 | 200 | 150 | 146 | 691 | 1,300 | $15.51 / $22.72 | $7.76 / $11.36 |
| Hindi | 60 | 64 | 37 | 200 | 150 | 123 | 634 | 2,110 | $16.29 / $23.93 | $8.14 / $11.96 |
| Japanese | 60 | 36 | 25 | 200 | 150 | 109 | 580 | 1,520 | $13.53 / $19.83 | $6.77 / $9.92 |
| Chinese | 60 | 59 | 37 | 200 | 150 | 122 | 628 | 1,330 | $14.18 / $20.76 | $7.09 / $10.38 |
| Spanish (Microsoft) | 60 | 65 | 38 | 200 | 96 | 0 | 459 | 1,290 | $10.29 / $15.06 | $5.14 / $7.53 |
| Icelandic | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 1,470 | $16.42 / $24.07 | $8.21 / $12.03 |
| Russian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 1,620 | $16.85 / $24.71 | $8.42 / $12.35 |
| Ukrainian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 1,670 | $16.99 / $24.92 | $8.50 / $12.46 |

With prompt caching of the fixed part (expected cost unless marked high):

| Option | Languages | Calls | Standard, no cache | Standard + cache, all hits | Batch, no cache | Batch + cache, half hits | Batch + cache, all hits | Batch high: no cache / all hits |
|---|---|---:|---:|---:|---:|---:|---:|---|
| A. Pilot | Chinese | 628 | $14.18 | $9.25 | $7.09 | $6.18 | $4.63 | $10.38 / $7.67 |
| B. Recommended | Czech, Hindi, Japanese, Chinese | 2,533 | $59.51 | $39.65 | $29.76 | $26.10 | $19.83 | $43.62 / $32.70 |
| C. Everything | All eight | 5,122 | $120.06 | $79.91 | $60.03 | $52.63 | $39.95 | $88.00 / $65.91 |

What caching can and cannot do here:

| Point | Detail |
|---|---|
| Saving | Up to 33% on top of batch (option B: $29.76 to $19.83). After caching, output tokens are over half the bill, so there is little left to cut without changing the judge |
| Hit rate in a batch is not guaranteed | Batch requests run in parallel, so several can start before the first one has written the cache. "Half hits" and "all hits" are assumptions, not forecasts |
| A miss costs more than no caching | A call that misses pays the write price (1.25 × input) for the fixed part. Caching pays only above a 21% hit rate |
| One cache per language | The instructions differ by language and locale wording, so each language writes its own entry |
| Not yet verified | That the answer schema's tokens sit inside the cached part. The 2,063 includes them. The development run reads this off the usage fields |
| Does not change the judge | Same model, effort, instructions and answers; only billing changes |

Batch beats the standard API even when the standard API gets every cache hit ($29.76 against $39.65 for option B), so batch stays the base choice and caching is an add-on.

**Recommendation:** option B on the Batch API with caching switched on, and the hard cap kept at $50 in the run script (it refuses to submit if the worst case would pass the cap, as in project 1). The cap is set from the no-cache high figure ($43.62), so the run stays inside it if caching fails entirely. Run the development sets first (240 calls, about $3 on batch): they measure the variable tokens per language and the cache hit rate. Stop if measured tokens are more than 1.5 times the estimate.

Why B and not C: the four once-reviewed languages can only be described, not certified, and REPORT section 9 explains why. Icelandic is the most interesting of them for a low-resource story and could be added alone for about $8 on batch without caching.

## 10. What a result will and will not mean

| It will mean | It will not mean |
|---|---|
| In language X, on WMT24 non-speech passages and these systems, with this vendor's reviewers, the judge's miss rate against majors that two reviewers agreed on is under the limit, with 95% confidence | That the judge is this good in language X in general |
| The cleared share at that cut-off, with a range | That language X is easier or harder for the judge than language Y: labels come from different reviewers with different strictness |
| Where the judge sits relative to human-to-human agreement | That the judge is right when it disagrees with the reviewers. With alpha at 0.17-0.30 some "misses" will be reviewer noise and some judge flags on "clean" translations will be real |

## 11. Decisions needed before any run

| # | Decision | Recommendation |
|---|---|---|
| 1 | Miss-rate limit | 10% at 95% confidence; report 5% as a stretch line |
| 2 | Speech | Separate test-only arm, outside the guarantee |
| 3 | Languages | Option B: the four twice-reviewed languages |
| 4 | Locale wording | Table in section 8 |
| 5 | Spend | Batch API with prompt caching, hard cap $50 |
