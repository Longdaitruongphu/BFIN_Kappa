# Kappa Foundation | 22 October 2026 submission check

The case decision and information cutoff are 31 December 2022. This is a **prepared package**, not proof of upload or trustee approval. Deadline in the assignment: **16:00 Ho Chi Minh City time, 22 October 2026**.

| Assignment item | File and verification |
|---|---|
| Initial Decision Record, at most two pages | `deliverables/Kappa_Initial_Decision_Record_22Oct2026.pdf` (2 pages). Matching editable copy: `.docx` with the same stem (Word print check: 2 pages). |
| Candidate universe, estimation window, benchmark, dollars, assumptions, evaluation/rebalance rule | Pages 1-2 of the record; details in `policy/initial_policy_proposed.json`. |
| Working Python and no-internet rebuild | `analysis/run_initial.py`, `analysis/compare_initial_candidates.py`, `analysis/config.json`; run `python analysis/run_initial.py`. |
| Functioning original retrieval code | `analysis/retrieve_data.py --phase train`. Keep this separate from offline rebuild; never overwrite the saved raw files in the submitted copy. |
| Dated source record and raw data | `data/DATA_RECORD.md`, `data/raw/retrieval_manifest.jsonl`, ten Yahoo daily CSVs, original Kenneth French ZIP. |
| Environment and generated evidence | `requirements-analysis.txt`; `outputs/initial_decision_rebuild.json`, `growth_portfolio_weights.csv`, `candidate_statistics.csv`, `risk_preference.csv`, `sample_utility_robustness.json`, `max_utility_A4_weights.csv` and `max_utility_preference.csv`. |

## Checks completed 21 October 2026

- Saved-file hash check: 11 training downloads and four supporting files passed. Ten failed direct SEC support downloads are explicitly logged; eligibility references remain dated notes rather than locally archived SEC filing bytes.
- The offline rebuild used 96 common monthly returns from January 2015 through December 2022. December 2014 only supplies the opening adjusted-price baseline. No 2023-25 price file is in this initial package or read by the decision script.
- An independent source-chain check recomputed the saved Yahoo adjusted-price returns and French factors. The maximum absolute differences were below `7e-16` for returns and `3e-17` for factors.
- The USD 12m budget reconciles: Beta $2,214,672.00; Delta $3,429,808.70; USMV $6,346,350.71; entry costs $9,168.59, with rounding to cents. Contractual payments cover $2.4m in 2024 and $3.6m in 2027 under the case assumptions.
- The full-universe A=4 maximum-utility portfolio has eight non-zero positions; its saved weights sum to 100%. The chart re-optimises that same 10-candidate universe at A=2/4/6/8 and compares the resulting utility with fixed 100% USMV and 100% VTI.
- The Word document was opened in Microsoft Word, exported and visually inspected on both pages. The PDF print master is also two pages. `outputs/submission_readiness_20261021.json` records the hashes and checks.

## What the sources establish

Yahoo Finance via `yfinance` supplies the ten saved adjusted-price histories. The Kenneth French Data Library ZIP supplies monthly Mkt-RF, SMB, HML and RF. The case exhibit supplies fictional bond quotes and the mandatory obligations. **Bloomberg and Morningstar are not Kappa calculation sources in this package.** The report style draws on fund factsheets; a design reference does not validate a market observation.

Monthly equity returns are simple `Adj Close_t / Adj Close_(t-1) - 1`, not log returns. French percentages are divided by 100 before analysis. Historical excess returns use observed monthly French RF; the annual 4% risk-free figure is a prospective planning assumption. CPI 2.5%, the education-cost 3% stress, market premium 4.5%, risk aversion A=4 and trading frictions are declared scenarios, not observed guarantees.

## Before the actual upload

1. Open the PDF and confirm the two pages, the USMV decision, Beta/Delta amounts, VTI benchmark, and 10/15/20 growth-sleeve review triggers.
2. Submit the PDF with the working Python files, raw `data/` folder, dated record and requirements file, or use the companion ZIP if the course portal accepts one archive. The `.docx` is an editable companion.
3. Freeze this original package after upload. Record the portal receipt separately. The revised mandate is scheduled for 23 October; do not revise the 2022 choice with 2023-25 evidence.

The full bond repricing, factor comparisons, frozen 2023-25 evaluation, revised-mandate response, committee memo/slides, member contributions and AI disclosure are requirements of the later final submission. Confirm the course's AI-use rules and actual member contributions before making those claims. This initial package does not certify them.
