# Harbor 0.25.0 validation results

Run on Ubuntu 24.04 with Docker, using `harbor run -a nop` and `harbor run -a oracle` (k=1).

| Task | nop reward (expect 0.0) | oracle reward (expect 1.0) |
|---|---|---|
| click-string-length | 0.0 | 1.0 |
| click-choice-prefix | 0.0 | 1.0 |
| click-path-suffix | 0.0 | 1.0 |
| click-group-alias | 0.0 | 1.0 |
| click-help-metavar | 0.0 | 1.0 |

Each oracle run passes all feature tests and all 2,434–2,436 regression tests.
