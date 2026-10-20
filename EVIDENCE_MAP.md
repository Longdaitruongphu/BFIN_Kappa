# Evidence map

All numerical table paths below are relative to `outputs/tables`. The executable analysis reads saved raw CSV and ZIP files, not values copied from this memo or the slides.

| Memo page | Question | Main evidence | Calculation |
|---|---|---|---|
| 1 | Where does the USD 12m go? | initial_allocation.csv; funding_summary.json | bonds.py, analyze.py |
| 2 | Can the obligations and real goal be funded? | funding_cashflows.csv; goal_sensitivity.csv; mission_simulation.csv | bonds.py, analyze.py |
| 3 | How do bond values respond to rates? | bond_metrics.csv; bond_curve.csv; bond_stress.csv; ytm_duration_validation.csv; curve_interpolation_sensitivity.csv | bonds.py, supplement.py |
| 4 | Are the sources and sample defensible? | train_data_quality.csv; eval_data_quality.csv; download_overlap_comparison.csv; factor_vintage_overlap_differences.csv | retrieve_data.py, analyze.py |
| 5 | Why USMV, and what changes the choice? | expected_return_inputs.csv; risk_preference.csv; portfolio_candidates.csv; single_index_residual_correlation.csv | analyze.py |
| 6 | Are returns exposures or evidence of alpha? | factor_regressions.csv; alpha_stability.csv; factor_variance_decomposition.csv | analyze.py, supplement.py |
| 7 | What happened in the frozen evaluation? | evaluation_performance.csv; evaluation_wealth.csv; evaluation_calendar_years.csv; evaluation_costs.csv | analyze.py |
| 8 | What is the compromise and revision process? | all_bond_alternative.csv; all_bond_cashflows.csv; all_bond_summary.json; risk_limit_sensitivity.json | supplement.py; MANDATE_REVISION.md |
| 9 | Can a reader trace the evidence? | data/raw/retrieval_manifest.jsonl; data/raw/supporting/source_register.json; data/raw/supporting/eligibility_checks.json | source records and official links |

The slides cite specific evidence in their speaker notes. The two charts contain editable workbook snapshots rounded to ten decimal places. The CSV evidence retains the analytical output precision. The data guide explains how to retrieve the original sources, construct monthly returns and interpret each output.

## Audit boundaries

- Yahoo tables and original French ZIPs were actually downloaded. SEC filings were verified through official web retrieval after direct Python requests returned HTTP 403. Brief eligibility notes are not the full SEC documents.
- Current vendor vintages and discretionary selection of surviving securities limit historical claims.
- The policy file was frozen before evaluation retrieval. The prepared two-page record is not evidence of an actual student submission on 22 October.
- `reproduction_checks.csv` and the offline receipts establish computational consistency. They do not validate forecasts, prove investment skill or substitute for real member checks.
- FF3 is allowed, as confirmed by the user on 15 October 2026.
- The actual revised mandate, course AI rules and member contributions remain pending.
