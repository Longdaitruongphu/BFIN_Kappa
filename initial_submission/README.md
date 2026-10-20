# Prepared initial decision snapshot

Prepared on 15 October 2026 for the 22 October initial submission. No claim of actual submission is made. The original policy was frozen before evaluation retrieval. Preserve the eventual actual submission separately if the group changes this prepared version.

The two-page record is in deliverables/. Working training-analysis code and saved raw training data are included. The raw French ZIP is a current complete vendor file; the parser explicitly restricts estimation to January 2015-December 2022. No evaluation equity downloads are included here.

From this folder, install requirements-analysis.txt into a Python 3.12 environment, then run `python analysis/analyze.py --stage train`. This reproduces training calculations from saved files without downloading data. Do not use --freeze: the policy is already preserved. The complete original-mandate package outside this snapshot also contains evaluation results and supporting sources.
