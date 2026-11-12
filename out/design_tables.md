### D1. Major-error translations needed so the one-sided 95% exact-binomial upper bound on the miss rate is under the limit

| Misses allowed | Majors needed, limit 5% | Majors needed, limit 10% |
|---:|---:|---:|
| 0 | 59 | 29 |
| 1 | 93 | 46 |
| 2 | 124 | 61 |
| 3 | 153 | 76 |
| 4 | 181 | 89 |
| 5 | 208 | 103 |

### D2. Two-sided 95% exact-binomial range for a cleared share

| No-error translations | Cleared share | 95% range | Half-width, points |
|---:|---|---|---:|
| 100 | 25% | 16.9% to 34.7% | 8.9 |
| 100 | 35% | 25.7% to 45.2% | 9.7 |
| 100 | 50% | 39.8% to 60.2% | 10.2 |
| 150 | 25% | 18.6% to 33.1% | 7.2 |
| 150 | 35% | 27.1% to 42.9% | 7.9 |
| 150 | 50% | 41.7% to 58.3% | 8.3 |
| 200 | 25% | 19.2% to 31.6% | 6.2 |
| 200 | 35% | 28.4% to 42.0% | 6.8 |
| 200 | 50% | 42.9% to 57.1% | 7.1 |

### D3. Two-reviewer labels (two different reviewers), twice-reviewed languages

| Language | Cut | Translations | Confirmed clean | Confirmed major | on source passages | distinct texts | Major + minor | Major + no-error | Minor involved, no major |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | no speech | 3,279 | 1,471 | 135 | 94 | 134 | 245 | 317 | 1,111 |
| Czech | speech | 784 | 161 | 86 | 37 | 86 | 159 | 119 | 259 |
| Hindi | no speech | 2,185 | 1,072 | 101 | 83 | 101 | 102 | 189 | 721 |
| Hindi | speech | 529 | 158 | 63 | 39 | 63 | 56 | 87 | 165 |
| Japanese | no speech | 5,774 | 4,213 | 61 | 51 | 60 | 99 | 383 | 1,018 |
| Japanese | speech | 1,229 | 602 | 49 | 34 | 49 | 64 | 170 | 344 |
| Chinese | no speech | 5,589 | 3,874 | 96 | 74 | 96 | 136 | 487 | 996 |
| Chinese | speech | 1,197 | 553 | 62 | 39 | 62 | 80 | 231 | 271 |

### D4. One-reviewer labels, once-reviewed languages

| Language | Translations, no speech | Source passages | No-error | Minor-only | Major | Major on source passages |
|---|---:|---:|---:|---:|---:|---:|
| Spanish (Microsoft half, spent passages removed) | 3,264 | 272 | 2,867 | 287 | 110 | 79 |
| Icelandic | 5,230 | 523 | 1,304 | 1,870 | 2,056 | 477 |
| Russian | 6,799 | 523 | 3,991 | 1,632 | 1,176 | 415 |
| Ukrainian | 5,230 | 523 | 3,674 | 700 | 856 | 379 |

### D5. Proposed split by source passage (no speech) and what the calibration set can certify, 95% confidence

| Language | Label | Passages dev / cal / test | Majors available cal / test | Majors used cal | Majors used test | Limit 5%: misses allowed | Limit 5%: chance to certify if true miss rate is 1% | Limit 5%: chance to certify if true miss rate is 3% | Limit 10%: misses allowed | Limit 10%: chance to certify if true miss rate is 1% | Limit 10%: chance to certify if true miss rate is 3% | Test: upper bound if 0 missed |
|---|---|---|---|---:|---:|---|---|---|---:|---|---|---|
| Czech | two reviewers | 20 / 133 / 87 | 87 / 48 | 87 | 48 | 0 | 42% | 7% | 3 | 99% | 74% | 6.1% |
| Hindi | two reviewers | 20 / 131 / 89 | 64 / 37 | 64 | 37 | 0 | 53% | 14% | 2 | 97% | 70% | 7.8% |
| Japanese | two reviewers | 20 / 301 / 202 | 36 / 25 | 36 | 25 | cannot certify | 0% | 0% | 0 | 70% | 33% | 11.3% |
| Chinese | two reviewers | 20 / 303 / 200 | 59 / 37 | 59 | 37 | 0 | 55% | 17% | 1 | 88% | 47% | 7.8% |
| Spanish | one reviewer | 20 / 152 / 100 | 65 / 38 | 65 | 38 | 0 | 52% | 14% | 2 | 97% | 69% | 7.6% |
| Icelandic | one reviewer | 20 / 301 / 202 | 1200 / 784 | 150 | 150 | 2 | 81% | 17% | 8 | 100% | 96% | 2.0% |
| Russian | one reviewer | 20 / 302 / 201 | 681 / 447 | 150 | 150 | 2 | 81% | 17% | 8 | 100% | 96% | 2.0% |
| Ukrainian | one reviewer | 20 / 301 / 202 | 486 / 328 | 150 | 150 | 2 | 81% | 17% | 8 | 100% | 96% | 2.0% |

Split: 20 dev passages; the rest 60% calibration / 40% test, stratified by text type and by whether the passage has a major-error translation. Seeded; ids in ids/split_<lang>.csv.

### D6. Judge calls and API cost without caching (Claude Opus 5.5 at $4 input / $20 output per million tokens)

| Language | Dev | Calibration (majors) | Test majors | Test clean | Test other | Speech arm (test only) | Calls | Fixed tokens per call | Variable tokens per call (est.) | Standard, expected $ | Standard, high $ | Batch, expected $ | Batch, high $ |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---:|---:|
| Czech | 60 | 87 | 48 | 200 | 150 | 146 | 691 | 2,063 | 1,300 | 15.51 | 22.72 | 7.76 | 11.36 |
| Hindi | 60 | 64 | 37 | 200 | 150 | 123 | 634 | 2,063 | 2,110 | 16.29 | 23.93 | 8.14 | 11.96 |
| Japanese | 60 | 36 | 25 | 200 | 150 | 109 | 580 | 2,063 | 1,520 | 13.53 | 19.83 | 6.77 | 9.92 |
| Chinese | 60 | 59 | 37 | 200 | 150 | 122 | 628 | 2,063 | 1,330 | 14.18 | 20.76 | 7.09 | 10.38 |
| Spanish | 60 | 65 | 38 | 200 | 96 | 0 | 459 | 2,063 | 1,290 | 10.29 | 15.06 | 5.14 | 7.53 |
| Icelandic | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 2,063 | 1,470 | 16.42 | 24.07 | 8.21 | 12.03 |
| Russian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 2,063 | 1,620 | 16.85 | 24.71 | 8.42 | 12.35 |
| Ukrainian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 2,063 | 1,670 | 16.99 | 24.92 | 8.5 | 12.46 |
| Total | 480 | 761 | 635 | 1,600 | 1,146 | 500 | 5,122 |  |  | 120.06 | 176 | 60.03 | 87.99 |

Fixed tokens: measured (see D7 note). Variable tokens: estimated from character counts. Expected: 450 output tokens per call. High: fixed x 1.1, variable x 1.5, 800 output tokens. Batch is half the standard price.

### D7. Cost with prompt caching of the fixed part (expected unless marked high)

| Option | Calls | Standard, no cache $ | Standard + cache, all hits $ | Batch, no cache $ | Batch + cache, half hits $ | Batch + cache, all hits $ | Batch, no cache, high $ | Batch + cache, all hits, high $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A. Pilot | 628 | 14.18 | 9.25 | 7.09 | 6.18 | 4.63 | 10.38 | 7.67 |
| B. Twice-reviewed | 2,533 | 59.51 | 39.65 | 29.76 | 26.1 | 19.83 | 43.62 | 32.7 |
| C. All eight | 5,122 | 120.06 | 79.91 | 60.03 | 52.63 | 39.95 | 88 | 65.91 |

Fixed part: 2,063 input tokens per call (95% range 2,042-2,086), from a least-squares fit of project 1's 108 measured calls on message length (R2 0.99). Cache read $0.20 and 5-minute cache write $5.00 per million tokens; batch halves both. A call that misses the cache pays the write price, so caching only pays above a 21% hit rate. Hit rate inside a batch is not guaranteed; half hits and all hits are shown as assumptions, not forecasts.

Twice-reviewed languages without the speech arm: 2,033 calls.
