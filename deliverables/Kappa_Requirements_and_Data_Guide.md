# Kappa Foundation requirements and data guide

This guide explains what the assignment requires, what the accompanying analysis does, how each dataset was obtained, and how to reproduce and inspect the results. The main recommendation is dedicated payment bonds plus USMV, as selected by the user after reviewing the all-bond alternative.

## 1. What the assignment asks you to decide

Act as an independent investment team for Kappa Foundation on 31 December 2022. Allocate all USD 12 million. Pay USD 2.4 million on 31 December 2024 and USD 3.6 million on 31 December 2027. Those nominal payments cannot be reduced in the original case. After paying them, aim to retain the purchasing power of USD 8 million in December 2022 at the end of 2030.

The trustees' discomfort near a 15% loss is ambiguous. You must define the metric, horizon and response, and explain any compromise. You must propose an inflation assumption, return forecasts, risk preference and benchmark. There is no prescribed optimal portfolio, and high realized returns earn no marks by themselves.

The available assets are cash, the five fictional default-free case bonds, US common stocks, and US-listed equity ETFs investing primarily in US equities. No borrowing, short selling or derivatives. Fractional holdings are permitted. The analysis must not substitute real bond histories for the fictional instruments.

The candidate universe must have 8-12 common stocks across at least four sectors and two ETFs with meaningfully different mandates. Not every candidate has to be held. This package uses eight stocks across seven sectors, VTI and USMV.

## 2. Deadlines and exact deliverables

All times below are Ho Chi Minh City time, UTC+7.

- **22 October 2026, 16:00:** initial decision record, maximum two pages, with universe, estimation period, benchmark, dollar allocation, major assumptions and evaluation/rebalancing rule. Include working Python and a dated data record. Freeze the policy.
- **23 October 2026, 16:00:** receive the revised trustee mandate. Preserve the original submission and quantify how the revision changes the recommendation using the same 2022 information cutoff.
- **29 October 2026, 16:00:** final committee memo, presentation, reproducible analysis and supporting data in one archive.

The final archive needs: a memo of at most eight pages including tables/figures, plus at most one additional reference page; slide deck as PDF and editable source; executed Python scripts or notebook; environment/package file; concise offline rebuilding instructions; raw and processed data; generated outputs and source record; the initial submission and decision log; and a truthful contribution statement with another member's check and each member's critique. The group has 3-4 students. Material AI assistance must be disclosed under the actual course policy.

## 3. What earns marks and where the evidence is

- **Mandate, assumptions and judgement, 10 marks:** full USD 12m allocation, protected payments, real goal, risk interpretation and sensitivity to risk aversion. See memo pages 1-2 and 8, initial_allocation.csv and risk_preference.csv.
- **Bond valuation and funding risk, 20 marks:** valuation, YTM, incomplete curve, duration, convexity, exact repricing, parallel and shape shocks, and the effect on liabilities. See memo page 3 and bond_* outputs.
- **Data integrity and reproducibility, 15 marks:** own Python downloads, retained raw responses, dates/settings/versions, transparent return construction and an offline rebuild. See raw manifest, this guide and reproduction_checks.csv.
- **Portfolio construction and robustness, 15 marks:** recommended/rejected choices, same universe under sample and single-index covariance, forecast inputs, constraints, execution and sensitivity. See memo page 5 and portfolio_candidates.csv.
- **Market and factor interpretation, 15 marks:** CAPM versus a Lecture 7 multifactor model for the portfolio and at least two securities, with uncertainty and a careful alpha interpretation. See memo page 6. The user confirmed FF3 is allowed in Lecture 7.
- **Evaluation and mandate response, 15 marks:** frozen strategy versus frozen benchmark in 2023-2025, adverse results, a decision-reversal threshold and the actual mandate change. Evaluation is complete; the actual mandate response awaits the release.
- **Memo and presentation, 10 marks:** decision-led narrative, readable exhibits and a defendable recommendation. The memo and editable slide deck are included.

## 4. The two dates that must never be confused

**Information date:** the investment case uses information through 31 December 2022. Training observations are January 2015-December 2022. Supporting economic publications must have been available by the cutoff.

**Retrieval date:** files were downloaded in October 2026. A historical observation labelled 2020 is not necessarily the same vintage that an investor saw in 2020 or 2022. Yahoo can revise adjustment histories and French can revise factor data. The source manifest records the actual retrieval timestamp in UTC. Convert to local time by adding seven hours if needed.

The frozen policy was saved before the separate evaluation retrieval. That protects the code's decision/evaluation separation. It does not make this a genuinely unseen experiment: the universe was selected retrospectively and the analyst can know historical events.

## 5. Exact market data retrieval procedure

The required source is Yahoo Finance, accessed in Python through yfinance. No course workbook, lecture cache, search-result return, or third-party processed return series is substituted.

**Step 1. Create an analysis environment.** Install Python 3.12 if needed. Open PowerShell in the extracted BFIN_Kappa folder. Run the environment creation and package installation commands from README.md. Installation requires internet once. The provided requirements-analysis.txt pins the versions actually used.

**Step 2. Read analysis/config.json before running.** It specifies AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI and USMV. The stock list covers Information Technology, Financials, Health Care, Consumer Staples, Energy, Industrials and Utilities. The selected names are established liquid companies chosen for contrasting exposures; the list is not an unbiased sample of all 2022 securities.

**Step 3. Understand the requests.** Training requests start 2014-12-01 and end 2023-01-01, exclusive. Evaluation requests start 2022-12-01 and end 2026-01-01, exclusive. The preceding December is needed to calculate the first January return. Daily data are downloaded only to identify an exact last-trading-day observation each month. All model returns are monthly.

The explicit settings are interval='1d', auto_adjust=False, back_adjust=False, actions=True, repair=False, keepna=True and rounding=False. The script calls yfinance.Ticker(ticker).history with these settings. Disabling auto_adjust preserves both Close and Adj Close. Disabling repair avoids undisclosed library repairs. Preserving missing values allows the analysis to reject missing data rather than invent observations.

**Step 4. Retrieve in a new working copy, not over the submitted raw folder.** Run the following only if you intentionally want a fresh vendor vintage:

```powershell
.\.venv\Scripts\python.exe analysis\retrieve_data.py --phase train
```

The script skips files that already exist and logs that reuse. It retries a failed ticker up to three times, records every failure and stops the workflow if failures remain. It saves the untransformed returned DataFrame as CSV and pickle before calculating any returns. The CSV is the offline analysis input; only load trusted pickle files because pickle can execute code.

**Step 5. Inspect data/raw/retrieval_manifest.jsonl.** Each line is a JSON record. A successful record identifies the ticker or dataset, source URL, requested dates, settings, row count, first/last date, columns, package versions, UTC retrieval time and SHA-256 of the saved CSV or ZIP. This is the source trail, not a narrative assertion that data are reliable.

**Step 6. Estimate and freeze before evaluation.** In a fresh research copy without an existing frozen policy:

```powershell
.\.venv\Scripts\python.exe analysis\analyze.py --stage train --freeze
.\.venv\Scripts\python.exe analysis\retrieve_data.py --phase eval
```

The first command refuses to overwrite an existing freeze. The second refuses to run unless a frozen policy exists. For this delivered package, the freeze and both download phases already exist. Use rebuild.py for normal verification instead.

## 6. Exact factor data retrieval procedure

**Step 1. Open the official Kenneth French Data Library.** The resource is https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html . Locate Fama/French 3 Factors and select the monthly CSV ZIP, not its daily or weekly variant.

**Step 2. Use the exact ZIP resource.** The retrieval code requests https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip through Python requests. It checks HTTP status and the ZIP signature, then writes the response bytes without modification. It retains the source URL, response headers and file hash.

**Step 3. Parse monthly rows only.** The ZIP contains explanatory text, monthly rows and annual rows. The parser finds the Mkt-RF/SMB/HML header, selects date keys of exactly six digits YYYYMM and ignores annual YYYY rows. It rejects duplicate months and missing matches.

**Step 4. Convert units once.** A vendor value 1.25 means 1.25%, which becomes 0.0125 in calculations. Divide Mkt-RF, SMB, HML and RF by 100. RF is already a monthly return, not an annual yield; do not divide it by 12.

**Step 5. Align on months.** Join January 2015 with January 2015, regardless of day labels. The common training panel must have exactly 96 observations; evaluation must have 36. No rolling data from 2023-2025 enter a 2022 estimate.

**Step 6. Acknowledge methodology.** French changed the US research-return production to CRSP CIZ beginning with the January 2025 release, including dividend reinvestment conventions. This current-vintage methodology is a data limitation, not a pre-2023 investment insight. French's market series and VTI have different universes/construction and need not match exactly. The analysis never edits one to force agreement with the other.

## 7. How returns are constructed and checked

For each security, select the actual final trading-day row in each calendar month. Monthly total-return proxy = adjusted close this month / adjusted close last month - 1. For example, if adjusted closes were 100 and 103, the return would be 3%; this numerical example is illustrative and is not an observation in the dataset.

Adjusted Close already incorporates the vendor's dividend/split adjustments. Do not add dividend cash again. Retain the separate Dividends and Stock Splits columns for audit. Close is used only for the December 2022 share-sizing proxy; buying shares at a dividend-adjusted historical price would give the wrong quantity. Historical Close may itself be split-adjusted by the vendor, so the estimate remains a paper implementation convention rather than a reconstructed exchange order.

Every ticker had 2,036 daily training-download rows and 773 evaluation-download rows, including the preceding December. The processed analysis contains 96 and 36 common monthly returns. See train_data_quality.csv and eval_data_quality.csv for month-by-month row counts, dates and missing values. All tickers must share the same last trading date for a month. A missing last-day price causes failure rather than fallback to a prior day.

Inspect train_corporate_actions.csv and eval_corporate_actions.csv. Especially review splits and unusual distributions. Vendor adjustments are accepted as supplied; this does not independently audit every corporate action or prove that spinoff treatment matches another data vendor. No missing observation was filled with zero, a market proxy or an invented value.

The overlap audit compares December 2022 adjusted prices from the two downloads. A difference should be reported as a vendor-vintage issue, not overwritten. Factor overlap differences are also saved. Zero differences in this run do not mean future downloads will be identical.

## 8. Eligibility evidence and source checking

Open data/raw/supporting/eligibility_checks.json. Each candidate has a dated pre-cutoff filing or ETF description, an exact official URL and a concise statement of what was checked. For stocks, verify the company identity, common-stock class, exchange ticker and US registration. Do not confuse common stock with a preferred security that has a similar ticker.

For AAPL and MSFT, the 2022 fiscal reports were published in 2022. For calendar-year companies, the 2021 annual report filed in early 2022 is used. A fiscal-2022 annual report filed in February 2023 would fail the information cutoff despite the '2022' title. This distinction is central to the source audit.

VTI's April 2020 summary prospectus identifies its US broad-market mandate and US listing. USMV's mandate is documented in a July 2022 SEC-filed description of an underlying ETF in a structured-note disclosure. The ETF is the candidate investment; the structured note is not eligible and is not purchased. A dated original USMV fund prospectus would strengthen the evidence, so the group can retain one if available, without replacing the documented source silently.

Direct Python requests to SEC returned HTTP 403 for the selected filings. That failure is retained in source_register.json. Official SEC documents were checked via web retrieval instead. eligibility_checks.json is an analyst evidence note, not a complete original download. FOMC and French methodology pages were downloaded and saved successfully. Raw Yahoo tables and French ZIPs meet the required self-retrieval rule.

Eligibility at 2022 is necessary but does not prove unbiased selection. The list excludes delisted firms and contains surviving, well-known names. No historical index-membership claim is made. Do not describe results as a representative US-stock strategy or as a live out-of-sample experiment.

## 9. How to read the financial outputs

**initial_allocation.csv:** amounts sum to USD 12m, including initial costs. Bond units each represent USD 1,000 face value. USMV shares use the final 2022 Close only as a paper sizing proxy. The dates are contractual case dates; a real account would need settlement and cash-transfer arrangements.

**funding_cashflows.csv:** read each row in time order. In year 2, Beta pays the scholarship. In year 5, Delta's principal plus final coupon pays the centre. Surplus coupons stay in cash. A nonnegative cumulative cash balance demonstrates cash-flow feasibility under the stated zero-reinvestment assumption.

**bond_curve.csv:** the five quotes do not identify every annual spot rate. The main curve interpolates log discount factors between maturity knots. A different plausible interpolation also reprices the quotes. This shows why exact calibration does not establish a uniquely correct curve.

**bond_metrics.csv, bond_stress.csv and ytm_duration_validation.csv:** YTM duration applies to parallel changes in the bond's own annually compounded yield. Continuous-spot duration applies to the specified curve shift. Keep their conventions separate. Convexity improves the local approximation, and the exact repricing columns reveal the remaining approximation error.

**expected_return_inputs.csv:** forecast returns use the explicit 4% base plus beta times 4.5% market premium. Historical means are shown separately. Annual covariance is monthly sample covariance times 12; annual volatility is its square root. This annualization assumes stable second moments and does not capture every form of serial dependence.

**portfolio_candidates.csv:** compare the same tickers and constraints under sample and single-index risk. The single-index model keeps beta-driven market covariance and individual residual variances while zeroing residual cross-correlations. ETF overlap makes that simplifying assumption especially questionable. A high optimized score is not sufficient reason to implement a complex portfolio.

**risk_preference.csv:** the certainty equivalent is annual expected arithmetic return minus half of A times annual variance. A belongs to the growth-sleeve preference comparison; it is not inferred from the 15% whole-fund loss concern. The VTI/USMV ranking changes at A=2.58. The 15% concern is checked separately through stress and monitoring definitions.

**factor_regressions.csv:** each row is one security/model. Read beta, alpha interval, p-value and R-squared together. A positive alpha estimate with a confidence interval spanning zero is weak evidence. Even a statistically positive alpha, such as MSFT in the full sample, is conditional on the model and sample and does not guarantee future abnormal performance. Confidence intervals use HAC standard errors with three lags. They are pointwise, not adjusted for searching multiple securities.

**mission_simulation.csv:** 20,000 joint paths use circular 12-month blocks of historical log-return shocks, recentered to the stated prospective log-growth approximation. The seed is fixed. This preserves some within-block dependence while assuming it can recur. Monte Carlo error measures simulation sampling noise only. It excludes uncertainty in model structure, inflation, expected returns and the selected historical window. No fictional bond price history enters the simulation.

**evaluation_performance.csv:** strategy and benchmark are frozen. Returns are after assumed entry/rebalance costs. CAGR measures compound growth; Sharpe uses monthly realized RF. Maximum drawdown uses month-end observations and includes the initial value of 1, so an early loss is not missed. The evaluation cannot establish that the 2030 goal is funded.

**all_bond_alternative.csv:** a linear programme uses contractual cash flows and zero-interest cash carry to maximize terminal nominal cash subject to all intermediate payments and the USD 12m initial budget. Its USD 7.47m real value is conditional on 2.5% inflation, not an inflation-protected guarantee. The all-bond plan may still have interim market losses.

## 10. Offline reproducibility and failure handling

Run analysis/rebuild.py after the environment is installed. It blocks network connections in the process, rebuilds all numeric outputs and PDFs from raw CSV/ZIP files, verifies the frozen-policy hash, and writes logs/offline_rebuild_receipt.json. The primary numerical checks are in reproduction_checks.csv. An error is a request to investigate, not a reason to delete the offending observation.

The first package-install attempt failed because the restricted environment could not resolve pypi.org; the authorized network-enabled installation succeeded. All Yahoo and French market-data requests then succeeded. Current yfinance emitted a deprecation warning for raise_errors; this warning did not change the downloaded tables. SEC supporting-source requests failed with 403 and are explicitly distinguished from successful market-data downloads. See logs/KNOWN_ISSUES.md.

For a fresh rerun, preserve the original data directory, download into a separate copy, compare hashes and monthly returns, and record changes. Never quietly overwrite the submitted raw files. The retrieval script's existing-file behavior intentionally prevents accidental replacement.

The archive contains raw data, not Python package binaries. Installing packages on a new machine requires internet or a separately prepared wheelhouse. Once that environment exists, the saved-data analysis runs without internet. Slide regeneration uses the Codex bundled JavaScript artifact runtime; the delivered PowerPoint remains directly editable without that runtime.

## 11. What a human must verify before submission

FF3 eligibility was confirmed by the user on 15 October 2026. Read the actual course AI policy. Review the eight stock listings and both ETF mandates. Independently recompute at least one zero-coupon price, one coupon-bond duration, each mandatory payment and two monthly returns. Explain why an arithmetic expected return differs from a compound required return. Explain why a low-volatility ETF can still underperform and suffer large losses.

Each member should inspect the main recommendation and write an independent critique. Good questions include whether a 31.5% modeled goal-shortfall frequency is acceptable, whether 2.5% understates education-cost inflation, whether the survivor universe flatters risk-adjusted results, and whether the foundation can tolerate rising equity concentration after 2027. These are prompts for original student reasoning, not completed member critiques.

Keep the actual 22 October submission unchanged. Add the genuine 23 October mandate, quantify its effect and update the final memo and slides. Complete actual names, contributions and checks. The prepared package should not be represented as the final submission until these remaining requirements are addressed.
