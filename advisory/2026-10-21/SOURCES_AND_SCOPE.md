**Source and scope record — 21 October 2026**

Local authority: `reference/BFIN-WS2026-Group_Assignment.pdf`, four pages; extracted text in `docs/_source/BFIN_assignment_extracted.txt`. Original payments and instrument restrictions are mandatory. Objectives, additional limits and risk-aversion assumptions require justification. The revised mandate retains the original case date and information cutoff.

Local numerical inputs: saved case bond quotes, `policy/frozen_policy.json`, processed training returns/factors (2015–2022) and separate evaluation returns/factors (2023–2025). File hashes and dependency hashes are recorded by `analysis/mandate_preparedness.py` in `outputs/mandate_preparedness/calculation_receipt.json`.

External primary sources accessed through web tools on 21 October 2026:

| Source | Date/vintage | Use and limitation |
|---|---|---|
| [Yale reports investment return for fiscal 2022](https://news.yale.edu/2022/10/04/yale-reports-investment-return-fiscal-2022) | Published 4 October 2022 | Supports the dual mission of current support and future purchasing power; no Yale allocation or historical return imported into the Kappa forecast |
| [CFA Institute: Elements of an Investment Policy Statement for Institutional Investors](https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/investment-policy-statement-institutional-investors.pdf) | 2010 | Governance, liabilities/liquidity and explicit review/rebalancing process; does not establish A=4 or Kappa's numeric triggers |
| [Yale policy 2202: Endowment Spending and Distributions](https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions) | Effective 1 March 2023; revised 1 July 2026 | Current advisory example of smoothing discretionary distributions only; excluded from evidence available at 31 December 2022 |
| [Harvard endowment payout FAQ](https://finance.harvard.edu/faq/how-does-harvard-determine-its-endowment-payout) | Current official FAQ; page date not specified | Illustrates payout smoothing, spending stability and governance discretion; not used as a Kappa withdrawal rate |
| [Stanford endowment payout process](https://fingate.stanford.edu/managing-funds/endowment-payout-process) | Current official process page; includes revised smoothing rule | Illustrates multi-year payout smoothing and boundaries; current policy is not evidence available at the 2022 cutoff |
| [University of California General Endowment Pool IPS](https://www.ucop.edu/investment-office/gep-investment-policy-statement.pdf) | Official pool policy; current document | Illustrates real-return objectives, benchmark oversight, rebalancing and monitoring; not imported as Kappa's return forecast |
| [UC FY2021–22 endowment report](https://ucop.edu/investment-office/investment-reports/annual-reports/uc-investments-annual-endowment-report-fy-2021-2022-public-final.pdf) | FY2021–22 | Institutional example of long-term real-return objective and benchmark; publication timing relative to 31 December 2022 is not treated as known at case cutoff |

No external macro series was newly imported in this calculation. The 5% CAGR illustration, new liabilities, capital changes and revised risk limits are constructed scenarios, not retrieved facts or the actual lecturer mandate. No probabilities are assigned to which mandate will be released.

The institutional endowment policies are used as governance comparisons only. They show examples of stable payout rules, purchasing-power objectives, benchmarks and review controls; they do not establish universal A, VaR, stop-loss or drawdown thresholds. Kappa's fixed 2024/2027 payments are handled as dated liabilities and should not be confused with an endowment's smoothed discretionary payout.

The user selected CPI 2.5% for the primary real-goal test and HEPI 3.0% as a separate education-cost stress. This is the group's proposed policy input pending trustee authorization; the limitation that HEPI may not match Kappa's exact scholarship cost basket remains. The user also selected the base transaction-cost assumptions (5bp bonds, 10bp equity) and a separate lower-friction sensitivity (0bp bonds, 5bp ETFs, 10bp direct stocks). `analysis/goal_inflation_sensitivity.py` reproduces the deterministic hurdle and terminal-value arithmetic under both fee conventions in `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`; it does not generate probabilities or forecasts. The user's upside principle is also selected: at annual review, if the goal remains funded after a -30% growth-sleeve stress, protect only the minimum goal amount and leave surplus under growth policy; eligible asset and valuation convention remain open.

The observed evaluation-gap bridge uses frozen 2015–2022 FF3 loadings and realized 2023–2025 factors to explain differences in raw ETF arithmetic mean returns. Its residual includes model error and is not a causal attribution or a statistical alpha finding.

The all-bond capital requirement is an independent linear-programming solution for dated payments and a fixed nominal terminal target. It does not also impose the extra immediate reserve/stress constraints in scenarios Q1/R1–R4. Do not interpret that column as proving all those additional constraints can be satisfied at the same capital.

This work verifies calculation consistency and preserved inputs; it does not newly repeat the complete Yahoo/French raw-download provenance audit, validate forecasts, or establish any group member's independent contribution.
