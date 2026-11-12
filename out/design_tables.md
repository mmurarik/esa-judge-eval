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

### D6. Judge calls and API cost (Claude Opus 5.5 at $4 input / $20 output per million tokens, standard API)

| Language | Dev | Calibration (majors) | Test majors | Test clean | Test other | Speech arm (test only) | Calls | Input tokens per call (est.) | Cost, expected $ | Cost, high $ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | 60 | 87 | 48 | 200 | 150 | 146 | 691 | 3,220 | 15.12 | 24.41 |
| Hindi | 60 | 64 | 37 | 200 | 150 | 123 | 634 | 4,020 | 15.9 | 25.44 |
| Japanese | 60 | 36 | 25 | 200 | 150 | 109 | 580 | 3,430 | 13.18 | 21.22 |
| Chinese | 60 | 59 | 37 | 200 | 150 | 122 | 628 | 3,250 | 13.82 | 22.29 |
| Spanish | 60 | 65 | 38 | 200 | 96 | 0 | 459 | 3,210 | 10.02 | 16.18 |
| Icelandic | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 3,390 | 16.02 | 25.8 |
| Russian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 3,540 | 16.44 | 26.44 |
| Ukrainian | 60 | 150 | 150 | 200 | 150 | 0 | 710 | 3,590 | 16.59 | 26.65 |
| Total | 480 | 761 | 635 | 1,600 | 1,146 | 500 | 5,122 |  | 117.09 | 188.43 |

Expected: estimated input tokens and 450 output tokens per call. High: input x 1.5 and 800 output tokens. The Message Batches API halves both figures.

Twice-reviewed languages only: 2,533 calls, expected $58.02, high $93.36.

Same without the speech arm: 2,033 calls.
