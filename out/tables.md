### T0. Rows in the files and what was dropped

| Language | Rows in files | Dropped (quality-control, tutorial, #dup, #incomplete) | Kept | Repeat submissions dropped | Reviews used | of which human reference | of which MSLC | Spans with severity 'undecided' |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | 19,086 | 4,065 | 15,021 | 364 | 14,657 | 919 | 0 | 28 |
| Spanish | 11,443 | 2,534 | 8,909 | 33 | 8,876 | 634 | 634 | 6 |
| Hindi | 13,175 | 2,879 | 10,296 | 55 | 10,241 | 931 | 0 | 10 |
| Icelandic | 8,918 | 1,928 | 6,990 | 16 | 6,974 | 634 | 0 | 5 |
| Japanese | 21,341 | 4,768 | 16,573 | 89 | 16,484 | 1,268 | 0 | 10 |
| Russian | 11,426 | 2,526 | 8,900 | 24 | 8,876 | 634 | 0 | 3 |
| Ukrainian | 8,933 | 1,929 | 7,004 | 30 | 6,974 | 634 | 0 | 6 |
| Chinese | 21,402 | 4,751 | 16,651 | 167 | 16,484 | 1,268 | 0 | 5 |

### T1. Per language, machine systems only; group shares from the first review of each translation

| Language | Vendor | Source passages | Documents | Machine systems | Translations | Reviewers | Reviews | Reviewed twice % | Reviews per translation | No-error % | Minor-only % | Major % | Major n | Mean score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | Charles Univ. | 634 | 170 | 15 | 9,283 | 19 | 13,738 | 45.7 | 1.48 | 55.1 | 27.6 | 17.4 | 1,612 | 84.6 |
| Spanish | Microsoft + Toloka | 634 | 170 | 12 | 7,608 | 14 | 7,608 | 0 | 1 | 62 | 19.5 | 18.5 | 1,411 | 88.4 |
| Hindi | Microsoft | 634 | 170 | 10 | 6,340 | 15 | 9,310 | 46.8 | 1.47 | 65.2 | 20.8 | 14 | 890 | 86.8 |
| Icelandic | Arni Magnusson Inst. | 634 | 170 | 10 | 6,340 | 4 | 6,340 | 0 | 1 | 21.5 | 35.2 | 43.3 | 2,748 | 70.1 |
| Japanese | Microsoft | 634 | 170 | 12 | 7,608 | 14 | 15,216 | 100 | 2 | 82.1 | 11.9 | 6 | 456 | 88.4 |
| Russian | Toloka | 634 | 170 | 13 | 8,242 | 7 | 8,242 | 0 | 1 | 54.1 | 24.9 | 21 | 1,732 | 83 |
| Ukrainian | Toloka | 634 | 170 | 10 | 6,340 | 8 | 6,340 | 0 | 1 | 66.4 | 14.1 | 19.5 | 1,234 | 84.2 |
| Chinese | Microsoft | 634 | 170 | 12 | 7,608 | 14 | 15,216 | 100 | 2 | 77.6 | 12.2 | 10.2 | 778 | 87.3 |

### T1b. First and second review, languages reviewed twice

| Language | Review | Translations | Reviewers | No-error % | Minor-only % | Major % | Major n | Major % on twice-reviewed only | Flagged % on twice-reviewed only |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | first | 9,283 | 19 | 55.1 | 27.6 | 17.4 | 1,612 | 16.8 | 45.1 |
| Czech | second | 4,455 | 12 | 62.5 | 23.7 | 13.8 | 617 | 14.1 | 38.1 |
| Hindi | first | 6,340 | 15 | 65.2 | 20.8 | 14 | 890 | 14.4 | 37.3 |
| Hindi | second | 2,970 | 12 | 66 | 20.9 | 13 | 387 | 13 | 34 |
| Japanese | first | 7,608 | 14 | 82.1 | 11.9 | 6 | 456 | 6 | 17.9 |
| Japanese | second | 7,608 | 12 | 81.7 | 11.2 | 7.2 | 544 | 7.2 | 18.3 |
| Chinese | first | 7,608 | 10 | 77.6 | 12.2 | 10.2 | 778 | 10.2 | 22.4 |
| Chinese | second | 7,608 | 14 | 80 | 10.9 | 9 | 688 | 9 | 20 |

### T2. Excluded from the main tables: human references and MSLC (first review)

| Language | Excluded | Translations | No-error % | Minor-only % | Major % | Major n | Mean score | Machine systems: major % | Machine systems: mean score |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | human reference (refA) | 622 | 71.1 | 20.9 | 8 | 50 | 91.9 | 17.4 | 84.6 |
| Spanish | human reference (refA) | 634 | 77.4 | 15.9 | 6.6 | 42 | 95.4 | 18.5 | 88.4 |
| Spanish | MSLC | 634 | 31.2 | 14.4 | 54.4 | 345 | 62.3 | 18.5 | 88.4 |
| Hindi | human reference (refA) | 634 | 72.6 | 18.9 | 8.5 | 54 | 88.9 | 14 | 86.8 |
| Icelandic | human reference (refA) | 634 | 70.3 | 25.4 | 4.3 | 27 | 93.7 | 43.3 | 70.1 |
| Japanese | human reference (refA) | 634 | 88.8 | 7.6 | 3.6 | 23 | 89.6 | 6 | 88.4 |
| Russian | human reference (refA) | 634 | 66.9 | 21.8 | 11.4 | 72 | 88.4 | 21 | 83 |
| Ukrainian | human reference (refA) | 634 | 70.8 | 13.9 | 15.3 | 97 | 86.3 | 19.5 | 84.2 |
| Chinese | human reference (refA) | 634 | 82 | 11.8 | 6.2 | 39 | 90.7 | 10.2 | 87.3 |

### T3a. Major % by text type (first review)

| Language | literary | news | social | speech |
|---|---:|---:|---:|---:|
| Czech | 19.6 | 10.9 | 15.8 | 28.3 |
| Spanish | 14.7 | 14.6 | 15.2 | 35.6 |
| Hindi | 11 | 14.8 | 10.6 | 24.7 |
| Icelandic | 45.4 | 48.8 | 33.4 | 62.3 |
| Japanese | 5.6 | 2.7 | 5.5 | 11.6 |
| Russian | 18.5 | 16.5 | 17.4 | 38.5 |
| Ukrainian | 21.2 | 14 | 16.2 | 34.1 |
| Chinese | 11.7 | 4.8 | 9.2 | 18.8 |

### T3b. Flagged % (any error) by text type (first review)

| Language | literary | news | social | speech |
|---|---:|---:|---:|---:|
| Czech | 49.6 | 39.2 | 39.6 | 63.4 |
| Spanish | 26.7 | 35.5 | 34.4 | 59.4 |
| Hindi | 31.8 | 35.9 | 30.4 | 47.7 |
| Icelandic | 80.6 | 86.8 | 68.3 | 94.8 |
| Japanese | 17.9 | 13.2 | 15.6 | 30.1 |
| Russian | 46.3 | 44.1 | 38.7 | 67.6 |
| Ukrainian | 39.5 | 28.6 | 27.7 | 51.6 |
| Chinese | 24.2 | 16.5 | 19.8 | 35.9 |

### T3c. Major-error translations by text type (first review)

| Language | literary | news | social | speech |
|---|---:|---:|---:|---:|
| Czech | 229 | 223 | 700 | 460 |
| Spanish | 141 | 241 | 555 | 474 |
| Hindi | 88 | 204 | 324 | 274 |
| Icelandic | 363 | 673 | 1,020 | 692 |
| Japanese | 54 | 45 | 202 | 155 |
| Russian | 192 | 296 | 688 | 556 |
| Ukrainian | 170 | 193 | 493 | 378 |
| Chinese | 112 | 80 | 335 | 251 |

### T3d. Source passages by text type (same in every language)

| Text type | Source passages |
|---|---:|
| literary | 80 |
| news | 138 |
| social | 305 |
| speech | 111 |

### T4. Flag rate (any error) by vendor, and the spread across that vendor's reviewers (all reviews, machine systems)

| Language | Vendor | Reviewers | Reviews | Flagged % | 95% range | Major % | Reviewer flagged %: lowest | median | highest | Reviewers with 100+ reviews | Share of reviews by the 2 busiest % |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| Czech | Charles Univ. | 19 | 13,738 | 42.5 | 39.7-45.8 | 16.2 | 20.3 | 44.3 | 81.6 | 17 | 22 |
| Spanish | Microsoft | 12 | 4,188 | 15.3 | 13.4-17.6 | 4.5 | 7.8 | 14.25 | 27.2 | 10 | 29.3 |
| Spanish | Toloka | 2 | 3,420 | 65.9 | 61.8-70.1 | 35.7 | 43.7 | 63.55 | 83.4 | 2 | 100 |
| Hindi | Microsoft | 15 | 9,310 | 34.5 | 32.4-36.9 | 13.7 | 9.6 | 38.4 | 56.5 | 15 | 18.3 |
| Icelandic | Arni Magnusson Inst. | 4 | 6,340 | 78.5 | 75.8-81.6 | 43.3 | 73.4 | 79 | 82.8 | 4 | 50.3 |
| Japanese | Microsoft | 14 | 15,216 | 18.1 | 16.6-19.9 | 6.6 | 2.6 | 18.7 | 56.5 | 13 | 20.1 |
| Russian | Toloka | 7 | 8,242 | 45.9 | 43.1-49.2 | 21 | 22.9 | 46.3 | 59.7 | 6 | 51.1 |
| Ukrainian | Toloka | 8 | 6,340 | 33.6 | 30.8-36.7 | 19.5 | 18.1 | 33.2 | 50.6 | 6 | 62.9 |
| Chinese | Microsoft | 14 | 15,216 | 21.2 | 19.4-23.3 | 9.6 | 2.8 | 18 | 57.7 | 12 | 24.3 |

95% range: percentile bootstrap, 1,000 resamples of documents. Reviewer spread uses reviewers with 100 or more reviews.

### T4-es. Spanish: each reviewer

| Vendor | Reviewer | Reviews | Documents | Flagged % (95% range) | Major % | Flagged %, no speech | Mean score |
|---|---|---:|---:|---|---:|---:|---:|
| Microsoft | Annotator03microsoft | 463 | 67 | 7.8 (4.2-12.5) | 3.5 | 3.1 | 95.9 |
| Microsoft | Annotator11microsoft | 61 | 20 | 11.5 (1.6-22.2) | 4.9 | 10.6 | 87.3 |
| Microsoft | Annotator08microsoft | 371 | 59 | 11.9 (7.6-17.4) | 5.1 | 8.5 | 96.2 |
| Microsoft | Annotator06microsoft | 686 | 73 | 12.1 (7.9-16.9) | 5.2 | 9.7 | 96.6 |
| Microsoft | Annotator05microsoft | 542 | 71 | 12.2 (8.7-16.4) | 4.2 | 10.6 | 87 |
| Microsoft | Annotator12microsoft | 327 | 58 | 12.2 (7.5-17.5) | 2.1 | 12.3 | 97 |
| Microsoft | Annotator07microsoft | 313 | 60 | 16.3 (10.9-22.4) | 1.6 | 14.9 | 99.3 |
| Microsoft | Annotator02microsoft | 277 | 47 | 16.6 (11.7-22.7) | 4.7 | 13.4 | 91.6 |
| Microsoft | Annotator04microsoft | 491 | 66 | 18.5 (15.2-22.4) | 3.9 | 15.9 | 83.4 |
| Microsoft | Annotator01microsoft | 242 | 46 | 25.6 (20.4-34.6) | 10.7 | 18.5 | 93.2 |
| Microsoft | Annotator09microsoft | 346 | 59 | 27.2 (21.0-35.4) | 4.6 | 20.3 | 93.1 |
| Microsoft | Annotator10microsoft | 69 | 19 | 29.0 (14.7-43.2) | 10.1 | 30.4 | 94.3 |
| Toloka | Annotator17toloka | 1,509 | 84 | 43.7 (38.9-49.8) | 27.1 | 39.5 | 87.9 |
| Toloka | Annotator16toloka | 1,911 | 85 | 83.4 (80.0-87.0) | 42.5 | 79.2 | 79 |

### T4-ru. Russian: each reviewer

| Vendor | Reviewer | Reviews | Documents | Flagged % (95% range) | Major % | Flagged %, no speech | Mean score |
|---|---|---:|---:|---|---:|---:|---:|
| Toloka | Annotator07toloka | 1,085 | 85 | 22.9 (18.1-28.7) | 21.2 | 16.5 | 87 |
| Toloka | Annotator02toloka | 2,600 | 162 | 43.5 (39.6-47.7) | 23.5 | 38.1 | 87.2 |
| Toloka | Annotator04toloka | 794 | 140 | 43.8 (38.0-49.7) | 18.3 | 40 | 80.6 |
| Toloka | Annotator05toloka | 1,034 | 85 | 48.8 (43.4-55.8) | 25.7 | 44.8 | 81.1 |
| Toloka | Annotator03toloka | 1,610 | 140 | 54.1 (49.1-59.5) | 14.2 | 49.9 | 77 |
| Toloka | Annotator01toloka | 1,039 | 127 | 59.7 (54.8-64.7) | 22.3 | 55.7 | 82.2 |
| Toloka | Annotator06toloka | 80 | 25 | 72.5 (59.8-88.1) | 22.5 | 68.9 | 76.9 |

### T4-uk. Ukrainian: each reviewer

| Vendor | Reviewer | Reviews | Documents | Flagged % (95% range) | Major % | Flagged %, no speech | Mean score |
|---|---|---:|---:|---|---:|---:|---:|
| Toloka | Annotator09toloka | 513 | 80 | 18.1 (14.1-23.4) | 10.5 | 14.1 | 95.4 |
| Toloka | Annotator08toloka | 2,278 | 168 | 22.9 (19.6-26.7) | 20.4 | 18.8 | 86.6 |
| Toloka | Annotator13toloka | 71 | 12 | 31.0 (19.3-47.2) | 15.5 | 25.8 | 81.8 |
| Toloka | Annotator15toloka | 74 | 18 | 31.1 (13.7-48.8) | 16.2 | 33.3 | 87.3 |
| Toloka | Annotator14toloka | 471 | 67 | 32.3 (27.5-37.4) | 16.6 | 30.7 | 86.5 |
| Toloka | Annotator12toloka | 367 | 61 | 34.1 (28.0-40.9) | 19.3 | 32.6 | 91.4 |
| Toloka | Annotator10toloka | 1,709 | 166 | 44.4 (40.6-48.7) | 18.1 | 39.1 | 81.4 |
| Toloka | Annotator11toloka | 857 | 123 | 50.6 (45.0-56.4) | 27.4 | 47.9 | 72.8 |

### T4-is. Icelandic: each reviewer

| Vendor | Reviewer | Reviews | Documents | Flagged % (95% range) | Major % | Flagged %, no speech | Mean score |
|---|---|---:|---:|---|---:|---:|---:|
| Arni Magnusson Inst. | Annotator03isl | 1,585 | 162 | 73.4 (68.8-77.8) | 39.9 | 69.4 | 62.6 |
| Arni Magnusson Inst. | Annotator04isl | 1,603 | 163 | 76.0 (71.8-80.8) | 42.4 | 72.3 | 64.4 |
| Arni Magnusson Inst. | Annotator01isl | 1,570 | 159 | 82.0 (78.6-85.3) | 49.1 | 78.3 | 71.9 |
| Arni Magnusson Inst. | Annotator02isl | 1,582 | 158 | 82.8 (78.9-86.7) | 42 | 80.3 | 81.6 |

### T4-cs. Czech: each reviewer, with the other reviewer's rate on the same translations

| Reviewer | Reviews | Flagged % | Major % | Mean score | Same translations, other reviewer: n | Own flagged % on those | Same translations, other reviewer: flagged % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Annotator11ufal | 1,260 | 20.3 | 6.3 | 88.3 | 600 | 20 | 44.8 |
| Annotator07ufal | 1,555 | 20.9 | 4.6 | 91.1 | 1,075 | 20.4 | 45.5 |
| Annotator25ufal | 441 | 27.4 | 6.6 | 97.1 | 291 | 26.1 | 46.4 |
| Annotator16ufal | 709 | 31.3 | 8 | 92.6 | 411 | 29.9 | 36.3 |
| Annotator14ufal | 798 | 35.7 | 14.5 | 93.7 | 505 | 33.5 | 40.8 |
| Annotator13ufal | 1,211 | 36.2 | 20.5 | 77.7 | 651 | 35.9 | 46.4 |
| Annotator21ufal | 578 | 41.2 | 26.5 | 83.2 | 393 | 36.1 | 39.9 |
| Annotator26ufal | 303 | 41.3 | 13.9 | 92.9 | 171 | 38 | 42.7 |
| Annotator08ufal | 1,468 | 44.3 | 18.5 | 90.8 | 991 | 45 | 45.7 |
| Annotator33ufal | 71 | 46.5 | 29.6 | 87 | 48 | 39.6 | 12.5 |
| Annotator12ufal | 1,261 | 48 | 6 | 84.3 | 866 | 49.5 | 40.6 |
| Annotator18ufal | 602 | 48.2 | 20.3 | 90.3 | 358 | 50 | 41.3 |
| Annotator32ufal | 76 | 51.3 | 15.8 | 91.5 | 55 | 54.5 | 41.8 |
| Annotator27ufal | 206 | 55.3 | 26.2 | 87.2 | 113 | 50.4 | 18.6 |
| Annotator15ufal | 747 | 60 | 28.2 | 83.2 | 334 | 61.7 | 41.3 |
| Annotator09ufal | 1,371 | 63 | 19 | 70.8 | 620 | 67.1 | 41.1 |
| Annotator22ufal | 496 | 67.1 | 42.1 | 85.6 | 267 | 69.3 | 36.7 |
| Annotator24ufal | 444 | 77 | 27.9 | 73.4 | 306 | 80.1 | 37.6 |
| Annotator29ufal | 141 | 81.6 | 50.4 | 83.7 | 71 | 81.7 | 40.8 |

### T4-hi. Hindi: each reviewer, with the other reviewer's rate on the same translations

| Reviewer | Reviews | Flagged % | Major % | Mean score | Same translations, other reviewer: n | Own flagged % on those | Same translations, other reviewer: flagged % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Annotator14microsoft | 605 | 9.6 | 1.7 | 88.6 | 348 | 8.3 | 37.6 |
| Annotator16microsoft | 612 | 10.6 | 9.3 | 85.4 | 381 | 9.4 | 41.2 |
| Annotator17microsoft | 857 | 13.1 | 2 | 93.7 | 410 | 13.4 | 36.1 |
| Annotator21microsoft | 139 | 15.8 | 4.3 | 91.5 | 60 | 13.3 | 25 |
| Annotator22microsoft | 806 | 33.5 | 23.1 | 92.8 | 525 | 30.1 | 35.2 |
| Annotator15microsoft | 745 | 34.8 | 12.1 | 93.6 | 441 | 34.2 | 37 |
| Annotator24microsoft | 848 | 36.7 | 20 | 84.9 | 496 | 38.5 | 37.1 |
| Annotator27microsoft | 705 | 38.4 | 10.8 | 82.1 | 412 | 38.6 | 37.1 |
| Annotator26microsoft | 355 | 40.8 | 16.6 | 85.9 | 201 | 47.3 | 32.3 |
| Annotator25microsoft | 433 | 41.3 | 15.9 | 72.7 | 253 | 44.3 | 39.5 |
| Annotator23microsoft | 808 | 41.6 | 15.3 | 91 | 442 | 46.4 | 39.6 |
| Annotator13microsoft | 227 | 42.7 | 7 | 87.8 | 133 | 50.4 | 37.6 |
| Annotator20microsoft | 822 | 44.3 | 17.4 | 87.5 | 447 | 50.1 | 33.6 |
| Annotator19microsoft | 707 | 51.5 | 13 | 85.4 | 504 | 54.6 | 34.7 |
| Annotator18microsoft | 641 | 56.5 | 25.3 | 79.2 | 375 | 54.7 | 31.7 |

### T4-ja. Japanese: each reviewer, with the other reviewer's rate on the same translations

| Reviewer | Reviews | Flagged % | Major % | Mean score | Same translations, other reviewer: n | Own flagged % on those | Same translations, other reviewer: flagged % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Annotator38microsoft | 683 | 2.6 | 0.7 | 84.3 | 683 | 2.6 | 19.8 |
| Annotator36microsoft | 1,291 | 3.4 | 1.4 | 83 | 1,173 | 3.2 | 20.7 |
| Annotator29microsoft | 68 | 5.9 | 0 | 77.7 | 68 | 5.9 | 19.1 |
| Annotator34microsoft | 1,454 | 9.1 | 4.1 | 91.5 | 1,324 | 9.9 | 18 |
| Annotator28microsoft | 1,611 | 12.2 | 8.5 | 95.2 | 1,489 | 12.6 | 16.5 |
| Annotator30microsoft | 1,192 | 12.8 | 6.2 | 90.2 | 1,078 | 12.6 | 19.2 |
| Annotator40microsoft | 1,114 | 16.4 | 6.7 | 93.2 | 1,066 | 16.7 | 19.5 |
| Annotator37microsoft | 1,384 | 18.7 | 9 | 86.2 | 1,246 | 18.2 | 17.3 |
| Annotator39microsoft | 1,301 | 19.2 | 1.6 | 84.3 | 1,219 | 19.9 | 18.6 |
| Annotator32microsoft | 956 | 19.8 | 4.2 | 91.7 | 822 | 21.2 | 18.9 |
| Annotator33microsoft | 1,347 | 20.6 | 4.6 | 97.1 | 1,285 | 20.8 | 18.7 |
| Annotator41microsoft | 539 | 24.1 | 17.4 | 84.7 | 479 | 25.7 | 16.3 |
| Annotator35microsoft | 1,178 | 25.5 | 1.9 | 80.5 | 1,042 | 25.4 | 21.6 |
| Annotator31microsoft | 1,098 | 56.5 | 24.3 | 90.9 | 1,032 | 57.9 | 15.3 |

### T4-zh. Chinese: each reviewer, with the other reviewer's rate on the same translations

| Reviewer | Reviews | Flagged % | Major % | Mean score | Same translations, other reviewer: n | Own flagged % on those | Same translations, other reviewer: flagged % |
|---|---:|---:|---:|---:|---:|---:|---:|
| Annotator49microsoft | 1,645 | 2.8 | 0.7 | 93.1 | 1,511 | 2.6 | 22.2 |
| Annotator44microsoft | 1,810 | 10.2 | 4 | 77.1 | 1,610 | 9.4 | 22.5 |
| Annotator48microsoft | 1,751 | 11.2 | 3.1 | 95.8 | 1,503 | 11.4 | 20.6 |
| Annotator39microsoft | 1,132 | 14.3 | 0.9 | 86.8 | 1,046 | 14.3 | 20.5 |
| Annotator47microsoft | 1,668 | 14.8 | 2.9 | 90.7 | 1,564 | 14.7 | 22.5 |
| Annotator50microsoft | 160 | 16.9 | 11.2 | 83.8 | 160 | 16.9 | 31.2 |
| Annotator41microsoft | 1,627 | 19.1 | 14.5 | 87.8 | 1,391 | 19.3 | 20.8 |
| Annotator42microsoft | 791 | 21.9 | 12.5 | 89.5 | 729 | 22.2 | 21.4 |
| Annotator51microsoft | 373 | 26.3 | 4.6 | 89.4 | 373 | 26.3 | 25.5 |
| Annotator43microsoft | 585 | 30.1 | 5.5 | 90.2 | 581 | 29.8 | 20.8 |
| Annotator45microsoft | 1,886 | 30.6 | 26.5 | 77.3 | 1,558 | 29.9 | 19.9 |
| Annotator52microsoft | 71 | 36.6 | 16.9 | 88 | 71 | 36.6 | 25.4 |
| Annotator46microsoft | 1,656 | 57.7 | 20.9 | 91 | 1,414 | 58.1 | 14.5 |
| Annotator53microsoft | 61 | 73.8 | 18 | 74.1 | 61 | 73.8 | 16.4 |

### T4-es-b. Spanish: flagged % by vendor and text type

| vendor | literary | news | social | speech |
|---|---:|---:|---:|---:|
| Microsoft | 10.4 | 11.1 | 13.5 | 32.5 |
| Toloka | 75.4 | 67.2 | 57.1 | 83.1 |

### T4-es-c. Spanish: translations by vendor and text type

| vendor | literary | news | social | speech |
|---|---:|---:|---:|---:|
| Microsoft | 720 | 936 | 1,908 | 624 |
| Toloka | 240 | 720 | 1,752 | 708 |

### T5. Agreement between the first and second review, different reviewers (Krippendorff's alpha, 95% range from resampling source passages)

| Language | Reviewer pairs | Translations | Source passages | Same group % | alpha, 3 groups (ordinal) | alpha, 3 groups (nominal) | alpha, any error yes/no | alpha, major yes/no |
|---|---:|---:|---:|---:|---|---|---|---|
| Czech | 186 | 4,063 | 297 | 54.5 | 0.30 (0.27-0.33) | 0.20 (0.17-0.23) | 0.27 (0.24-0.30) | 0.22 (0.19-0.26) |
| Hindi | 163 | 2,714 | 297 | 57.4 | 0.27 (0.23-0.30) | 0.19 (0.16-0.22) | 0.20 (0.17-0.24) | 0.34 (0.29-0.38) |
| Japanese | 153 | 7,003 | 634 | 72.2 | 0.17 (0.14-0.20) | 0.12 (0.10-0.15) | 0.15 (0.12-0.18) | 0.18 (0.14-0.22) |
| Chinese | 125 | 6,786 | 634 | 69 | 0.18 (0.15-0.20) | 0.12 (0.09-0.14) | 0.16 (0.13-0.18) | 0.18 (0.14-0.21) |

### T5b. Same cut, speech separated

| Language | Cut | Translations | Source passages | Same group % | alpha, 3 groups (ordinal) | alpha, 3 groups (nominal) | alpha, any error yes/no | alpha, major yes/no |
|---|---|---:|---:|---:|---|---|---|---|
| Czech | no speech | 3,279 | 240 | 56.7 | 0.27 (0.22-0.31) | 0.18 (0.15-0.21) | 0.23 (0.19-0.27) | 0.23 (0.18-0.27) |
| Czech | speech only | 784 | 57 | 45.4 | 0.24 (0.16-0.31) | 0.18 (0.11-0.24) | 0.27 (0.20-0.33) | 0.13 (0.05-0.21) |
| Hindi | no speech | 2,185 | 240 | 59.8 | 0.25 (0.21-0.29) | 0.18 (0.15-0.22) | 0.20 (0.16-0.24) | 0.33 (0.28-0.39) |
| Hindi | speech only | 529 | 57 | 47.4 | 0.25 (0.18-0.31) | 0.15 (0.09-0.21) | 0.16 (0.09-0.22) | 0.29 (0.19-0.37) |
| Japanese | no speech | 5,774 | 523 | 75.5 | 0.15 (0.11-0.18) | 0.11 (0.08-0.13) | 0.14 (0.10-0.17) | 0.16 (0.11-0.20) |
| Japanese | speech only | 1,229 | 111 | 56.5 | 0.15 (0.08-0.22) | 0.10 (0.05-0.15) | 0.12 (0.05-0.18) | 0.19 (0.10-0.27) |
| Chinese | no speech | 5,589 | 523 | 72.2 | 0.16 (0.13-0.19) | 0.11 (0.08-0.13) | 0.14 (0.11-0.17) | 0.18 (0.13-0.22) |
| Chinese | speech only | 1,197 | 111 | 53.8 | 0.14 (0.08-0.20) | 0.09 (0.05-0.13) | 0.12 (0.07-0.18) | 0.13 (0.07-0.18) |

### T5c. Same reviewer reviewing the same translation twice (first and second pass)

| Language | Translations | Source passages | Same group % | alpha, 3 groups (ordinal) | alpha, 3 groups (nominal) | alpha, any error yes/no | alpha, major yes/no |
|---|---:|---:|---:|---|---|---|---|
| Czech | 248 | 170 | 70.2 | 0.47 (0.34-0.60) | 0.40 (0.28-0.51) | 0.45 (0.32-0.57) | 0.41 (0.21-0.58) |
| Hindi | 256 | 188 | 75 | 0.53 (0.41-0.64) | 0.44 (0.34-0.54) | 0.49 (0.37-0.60) | 0.57 (0.40-0.72) |
| Japanese | 605 | 404 | 85.1 | 0.47 (0.37-0.57) | 0.40 (0.30-0.49) | 0.45 (0.35-0.55) | 0.51 (0.34-0.64) |
| Chinese | 822 | 489 | 80.3 | 0.59 (0.52-0.65) | 0.50 (0.44-0.56) | 0.55 (0.48-0.62) | 0.61 (0.52-0.68) |

### T5d. When one reviewer put a translation in a group, what the other reviewer said

| Language | One reviewer said | Reviews | Other said no-error % | minor-only % | major % |
|---|---|---:|---:|---:|---:|
| Czech | no-error | 4,708 | 69.3 | 21.4 | 9.3 |
| Czech | minor-only | 2,136 | 47.2 | 33.9 | 18.9 |
| Czech | major | 1,282 | 34 | 31.5 | 34.5 |
| Hindi | no-error | 3,458 | 71.1 | 20.9 | 8 |
| Hindi | minor-only | 1,208 | 59.8 | 27.2 | 13.1 |
| Hindi | major | 762 | 36.2 | 20.7 | 43 |
| Japanese | no-error | 11,417 | 84.3 | 10.8 | 4.8 |
| Japanese | minor-only | 1,653 | 74.7 | 15.5 | 9.9 |
| Japanese | major | 936 | 59.1 | 17.4 | 23.5 |
| Chinese | no-error | 10,743 | 82.4 | 10.9 | 6.7 |
| Chinese | minor-only | 1,579 | 74.2 | 12.2 | 13.7 |
| Chinese | major | 1,250 | 57.4 | 17.3 | 25.3 |

### T5e. Translations where two different reviewers gave the same verdict

| Language | Cut | Translations with two reviewers | Both no-error | Both major | Exactly one major | One major, other no-error | Source passages with a both-major translation |
|---|---|---:|---:|---:|---:|---:|---:|
| Czech | all | 4,063 | 1,632 | 221 | 840 | 436 | 131 |
| Czech | no speech | 3,279 | 1,471 | 135 | 562 | 317 | 94 |
| Hindi | all | 2,714 | 1,230 | 164 | 434 | 276 | 122 |
| Hindi | no speech | 2,185 | 1,072 | 101 | 291 | 189 | 83 |
| Japanese | all | 7,003 | 4,815 | 110 | 716 | 553 | 85 |
| Japanese | no speech | 5,774 | 4,213 | 61 | 482 | 383 | 51 |
| Chinese | all | 6,786 | 4,427 | 158 | 934 | 718 | 113 |
| Chinese | no speech | 5,589 | 3,874 | 96 | 623 | 487 | 74 |

### T6. WMT24 findings paper (Table 6) against the files

| Language | Systems: paper | files | Reviewers: paper | files | Reviews per translation: paper | files | Reviews per system: paper | files, incl. refA, before de-duplication | Source passages: paper | files | Documents: paper | files |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Czech | 15 | 15 | 20 | 19 | 1.3 | 1.46 | 751 | 939 | 649 | 634 | 170 | 170 |
| Spanish | 13 | 13 | 14 | 14 | 1 | 1 | 370 | 636 | 649 | 634 | 170 | 170 |
| Hindi | 10 | 10 | 15 | 15 | 1.3 | 1.47 | 775 | 936 | 649 | 634 | 170 | 170 |
| Icelandic | 10 | 10 | 4 | 4 | 1 | 1 | 376 | 635 | 649 | 634 | 170 | 170 |
| Japanese | 12 | 12 | 14 | 14 | 1.5 | 2 | 1,212 | 1,275 | 649 | 634 | 170 | 170 |
| Russian | 13 | 13 | 7 | 7 | 1 | 1 | 370 | 636 | 649 | 634 | 170 | 170 |
| Ukrainian | 10 | 10 | 8 | 8 | 1 | 1 | 376 | 637 | 649 | 634 | 170 | 170 |
| Chinese | 12 | 12 | 12 | 14 | 1.5 | 2 | 1,217 | 1,281 | 649 | 634 | 170 | 170 |
