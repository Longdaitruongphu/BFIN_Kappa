
## Page 1


Kappa Foundation investment policy

Committee memorandum for the original mandate

Recommendation. Ring-fence both contractual payments with Beta and Delta, and invest the residual growth capital in USMV. Use VTI as the growth benchmark. Authorize this policy only with a clear acknowledgement that the 2030 real-value objective is aspirational and a 15% investment-loss ceiling cannot be promised.

| Use of funds | Initial USD | Share | Implementation |
| --- | --- | --- | --- |
| Beta | $2,214,672.00 | 18.46% | 2,400 bonds; USD 2.4m face |
| Delta | $3,429,808.70 | 28.58% | 3,478.26087 bonds; USD 3.478m face |
| USMV | $6,346,350.71 | 52.89% | Growth allocation |
| Execution costs | $9,168.59 | 0.08% | 5bp bonds and 10bp equities |
| Total | $12,000,000 | 100.00% | Rounding affects displayed percentages |

Why this allocation

The bonds pay the obligations without relying on equity sales, future bond prices, or positive reinvestment rates. USMV provides diversified US equities with lower estimated market sensitivity than VTI. The policy benchmark combines the dedicated payment cash flows with VTI for growth. Individual stocks remain research candidates; the evidence does not justify initial direct holdings.

At 2.5% annual inflation, the terminal objective is $9,747,223 in December 2030. After preserving surplus coupons as cash, the equity sleeve needs 4.84% compound annual growth. Our expected return assumption is 7.14% arithmetic, which is not directly comparable with that compound hurdle.

The specified scenario model reaches the real goal in 68.5% of paths. A 31.5% modeled shortfall frequency is material. This estimate conditions on a small historical sample and uncertain forecasts; it is not a calibrated success guarantee.

The policy accepts a monitoring threshold rather than a hard loss constraint. A stricter requirement would call for a smaller equity allocation, a lower terminal goal, or new funding. The all-bond alternative on page 8 quantifies a feasible compromise.

Generated evidence: initial_allocation.csv; funding_summary.json; mission_simulation.csv. Original case only. The revised mandate due 23 October 2026 is not yet available.


## Page 2


Payment funding and purchasing power

Beta is a zero-coupon bond. Buying USD 2.4 million face costs USD 2,214,672 and delivers exactly USD 2.4 million in year 2. Delta pays 3.5% annually. Buying USD 3,478,260.87 face makes its final coupon plus principal equal USD 3.6 million in year 5.

| Date | Dedicated receipt | Required payment | Surplus to cash |
| --- | --- | --- | --- |
| 31 Dec 2023 | Delta coupon $121,739 | $0 | $121,739 |
| 31 Dec 2024 | Beta $2.4m + Delta coupon | $2,400,000 | $121,739 |
| 31 Dec 2025 | Delta coupon $121,739 | $0 | $121,739 |
| 31 Dec 2026 | Delta coupon $121,739 | $0 | $121,739 |
| 31 Dec 2027 | Delta final payment $3.6m | $3,600,000 | $0 |
| 31 Dec 2030 | Accumulated surplus coupons | $0 | $486,957 retained |

Assumptions that determine feasibility

Hold dedicated bonds to their payment dates. Treat the contractual receipt as available before the same-day programme payment, as the case requires. Confirm settlement and payment instructions in implementation. Keep years 1-4 coupons in segregated USD cash, earning zero in the base case. The USD 6 million outflow is programme spending, not an investment loss.

Adopt 2.5% as a planning inflation rate for the foundation's purchasing power, not as a statistical forecast of its education costs. The December 2022 Federal Reserve projections anticipated PCE inflation of 3.1%, 2.5% and 2.1% for 2023-2025 and 2.0% in the long run [3]. The choice adds a planning margin to long-run PCE, but education costs and CPI may differ. Test 2%-5% inflation.

| Constant inflation | 2030 nominal target | Required equity CAGR |
| --- | --- | --- |
| 2.0% | $9.373m | 4.30% |
| 2.5% | $9.747m | 4.84% |
| 4.0% | $10.949m | 6.45% |
| 5.0% | $11.820m | 7.52% |

A cheaper earmarking structure uses the first two Delta coupons to help pay the scholarship, freeing about USD 224,565 for equities. We reject it initially because separate payment rings simplify operational control. This conservatism has a measurable opportunity cost, shown in funding_alternatives.csv.

Generated evidence: funding_cashflows.csv; goal_sensitivity.csv; funding_alternatives.csv. Formula: equity*(1+g)^8 + surplus cash = 8m*(1+inflation)^8.


## Page 3


Bond valuation and interest rate risk

Solve each annual-compounding yield from the stated price and contractual cash flows. YTM is an internal rate of return, not a spot rate for every cash flow. Zero accrued interest makes the quoted clean and dirty prices identical.

| Bond | YTM | Modified duration | Yield convexity |
| --- | --- | --- | --- |
| Alpha | 4.30% | 0.959 | 1.838 |
| Beta | 4.10% | 1.921 | 5.537 |
| Gamma | 3.91% | 2.778 | 10.553 |
| Delta | 3.81% | 4.499 | 25.402 |
| Epsilon | 3.90% | 6.659 | 54.785 |

The incomplete curve

Bootstrap discount factors at years 1, 2, 3, 5 and 8. Interpolate log discount factors linearly between the observed maturity knots, which imposes constant forward rates within each segment. Solve each unknown maturity discount factor so the entire coupon bond reprices exactly. This is an explicit interpolation assumption, not a uniquely identified market curve. A separately recalibrated linear-zero-rate curve checks sensitivity.

The curve reproduces all five prices to less than USD 0.0000001. Parallel continuous-spot shifts use cash-flow-weighted duration and convexity. The standard YTM duration figures above are checked separately against exact YTM repricing; they are not substituted into the curve-shape stress.

| Instrument | +100bp parallel | -100bp parallel | Steepener |
| --- | --- | --- | --- |
| Beta | -1.98% | +2.02% | +1.44% |
| Delta | -4.56% | +4.79% | -0.48% |
| Epsilon | -6.66% | +7.19% | -5.79% |

The steepener shifts the one-year continuous spot rate down 100bp and the eight-year rate up 100bp, linearly by maturity. The 100bp shocks are deliberately material sensitivity tests in the high-rate uncertainty of late 2022; +200bp is a more severe stress. They are not assigned probabilities. At +100bp, the largest duration-convexity pricing error is only USD 0.069 per bond, but errors grow with shock size.

The payment reserve loses about USD 200,255 in market value after a +100bp shift, while its promised cash receipts remain unchanged. Thus mark-to-market risk and payment funding risk differ. Epsilon is useful for a fixed nominal terminal goal but introduces greater interim interest-rate exposure and coupon reinvestment dependence.

Generated evidence: bond_metrics.csv; bond_curve.csv; bond_stress.csv; ytm_duration_validation.csv; curve_interpolation_sensitivity.csv.


## Page 4


Eligible universe and data design

| Candidate | Sector or mandate | Economic role |
| --- | --- | --- |
| AAPL, MSFT | Information Technology | Devices, enterprise software and cloud |
| JPM | Financials | Credit cycle and banking |
| JNJ | Health Care | Defensive demand |
| PG | Consumer Staples | Staples demand and pricing |
| XOM | Energy | Oil and inflation exposure |
| CAT | Industrials | Capital expenditure cycle |
| NEE | Utilities | Regulated utility and rate sensitivity |
| VTI | Broad US equities | Investable benchmark |
| USMV | US minimum volatility | Defensive growth candidate |

Eight common stocks span seven sectors. Pre-cutoff SEC filings identify their security class and US exchange listing. VTI has a pre-cutoff prospectus. A July 2022 SEC-filed disclosure documents USMV's mandate and listing. The source register links the exact resources. This discretionary universe contains present-day survivors; dated eligibility evidence does not remove selection or survivorship bias.

Use January 2015-December 2022: 96 common monthly observations. This balances sample size with recent regimes, including the pandemic and 2022 inflation shock, but omits the global financial crisis. A 60-month 2018-2022 sensitivity retains the same universe. December 2014 prices supply only the January 2015 return denominator.

Yahoo data were retrieved in Python with yfinance. Daily frequency is the download granularity; every model uses monthly returns calculated from the last trading day's adjusted close. Settings explicitly disable auto-adjustment, back-adjustment and repair while retaining actions and missing values. Adjusted close incorporates Yahoo's corporate-action treatment. Dividends are not added a second time. No missing returns were filled or removed.

Kenneth French's monthly FF3 ZIP supplies Mkt-RF, SMB, HML and RF. Divide all four series by 100, align by calendar month, and subtract RF once from security returns. VTI is an investable benchmark; French's market factor is an explanatory research series. They need not agree. Current French files use revised historical data and the post-2024 CRSP methodology [2].

Raw retrieval began 2026-10-15. The archive retains the untouched download tables, ZIP bytes, hashes, settings and package versions. Direct SEC requests returned 403; official documents were checked through web access, with that limitation recorded. Source summaries are clearly distinguished from full saved documents.

Generated evidence: train_data_quality.csv; train_corporate_actions.csv; data/raw/retrieval_manifest.jsonl; data/raw/supporting/eligibility_checks.json; download_overlap_comparison.csv.


## Page 5


Portfolio choice and robustness

Forecast each asset's annual arithmetic return as 4.0% + beta x 4.5%. Betas come from 2015-2022 excess returns against the French market factor. The 4% planning base is close to case bond yields but is not an eight-year guaranteed cash reinvestment rate. The 4.5% market premium is a judgement input, tested at 2.5%-6.5%. Set forecast alpha to zero. Do not extrapolate the exceptional historical returns of selected technology stocks.

Compare annual certainty equivalents CE = expected return - A x variance / 2 on the growth sleeve. With A = 4, USMV scores 3.84% and VTI 3.13%. A is an assumed preference parameter, not an estimate from the trustees' vague 15% concern. A below 2.58 reverses this choice in favour of VTI; at A = 4, a market premium above 6.98% also reverses it.

| Risk preference A | USMV CE | VTI CE | Preferred |
| --- | --- | --- | --- |
| 1 | 6.32% | 7.12% | VTI |
| 2 | 5.49% | 5.79% | VTI |
| 4 | 3.84% | 3.13% | USMV |
| 8 | 0.55% | -2.19% | USMV |

The full-universe optimizations impose nonnegative weights, no leverage, 10% per direct stock, 30% across direct stocks and at least 70% across the two diversified ETFs. The stock limits apply to direct holdings, not ETF look-through exposures, which require separate monitoring. Both risk models use the same return forecasts and constraints.

| Candidate | Forecast return | Sample risk | Index risk |
| --- | --- | --- | --- |
| Sample A4 | 7.21% | 12.75% | 12.34% |
| Single index A4 | 6.93% | 12.32% | 11.55% |
| Eta historical Sharpe | 7.35% | 13.59% | 13.32% |

At A = 4, the sample model holds 18.10% VTI, 51.90% USMV and 30% direct stocks. The single-index model holds 11.34% VTI, 58.66% USMV and 10% each in JNJ, PG and NEE. Switching models implies 14.09% one-way turnover. The index model suppresses residual correlations; VTI and USMV residual correlation is 0.63, so its diversification estimates are optimistic.

The sample optimizer improves assumed CE over pure USMV by only about 0.12 percentage points. We prefer the simpler ETF implementation given model error and concentrated direct-stock bets. The Eta proxy maximizes historical mean excess return over the 4% case hurdle. A realized-RF variant is reported separately rather than silently redefining that frozen proxy.

Generated evidence: expected_return_inputs.csv; risk_preference.csv; portfolio_candidates.csv; window_and_erp_sensitivity.csv; historical_sharpe_definition_audit.csv.


## Page 6


Return drivers and the advisers claims

Estimate CAPM and Fama-French three-factor regressions on monthly excess returns, with an intercept and heteroskedasticity/autocorrelation-robust standard errors using three lags. Report 95% intervals. Annual alpha is 12 times the monthly intercept, an arithmetic convention. The user confirmed that FF3 is allowed in Lecture 7.

| Security | Model | Market beta | Annual alpha | 95% alpha interval | R squared |
| --- | --- | --- | --- | --- | --- |
| USMV | CAPM | 0.70 | 2.17% | -1.81% to 6.15% | 0.805 |
| USMV | FF3 | 0.74 | 1.49% | -2.09% to 5.06% | 0.848 |
| AAPL | CAPM | 1.21 | 12.13% | -1.57% to 25.84% | 0.468 |
| AAPL | FF3 | 1.27 | 11.04% | -1.53% to 23.62% | 0.538 |
| MSFT | CAPM | 0.96 | 14.47% | 4.36% to 24.59% | 0.495 |
| MSFT | FF3 | 1.06 | 12.81% | 4.54% to 21.08% | 0.602 |

USMV's FF3 market beta is 0.74; its SMB loading is -0.30, consistent with a large-company tilt. HML is approximately -0.05 and statistically uncertain. Its alpha interval includes zero. The model explains about 85% of excess-return variance. The covariance-aware variance allocation attributes 85.6% to market exposure and 15.2% to residual risk, with a small negative size contribution because factors covary.

AAPL and MSFT load negatively on HML, consistent with growth exposure. MSFT has a positive full-sample alpha that is statistically distinguishable from zero in these regressions. This is evidence inconvenient to a blanket rejection of Theta. However, its early-half FF3 alpha interval includes zero, model omissions remain possible, and examining several securities raises selection concerns. The result does not establish a persistent, tradeable future abnormal return.

Eta is right that liability-supporting bonds can separate contractual spending from equity risk. The second step, buying the historical Sharpe winner, is weaker: the same sample both selects and praises the portfolio. The constrained Eta proxy has a high fitted Sharpe, but that is not an unbiased estimate of its future performance.

Theta is right that exposures explain much of risk and return. We use factor evidence to understand the portfolio, not as proof of manager skill. Zero forecast alpha avoids capitalizing unstable residual performance. The market-only model is parsimonious; FF3 adds useful style diagnostics without eliminating estimation uncertainty or establishing causation.

Generated evidence: factor_regressions.csv; alpha_stability.csv; factor_variance_decomposition.csv; training_performance.csv.


## Page 7


Frozen evaluation and adverse evidence

The saved policy defines the growth holdings, benchmark and annual December rebalance rule before the separate evaluation downloads. No parameters are re-estimated in 2023-2025. Dividends follow adjusted-price reinvestment. Charge 10bp on initial invested dollars and on each buy or sell at rebalancing. There is no terminal liquidation charge. ETF operating expenses are already reflected in observed fund returns.

| 2023 to 2025 | CAGR | Volatility | Sharpe | Max drawdown |
| --- | --- | --- | --- | --- |
| Recommended | 11.15% | 9.64% | 0.66 | -5.66% |
| Benchmark VTI | 22.22% | 12.54% | 1.30 | -9.11% |
| Sample A4 | 12.79% | 9.86% | 0.80 | -6.34% |
| Single index A4 | 10.67% | 10.24% | 0.59 | -6.76% |
| Eta historical Sharpe | 14.01% | 9.91% | 0.90 | -6.42% |

[Figure: evaluation_growth.png]

USMV returned 37.33% cumulatively after the assumed entry cost, versus 82.56% for VTI. It lagged in every calendar year and also delivered a lower evaluation Sharpe ratio. Its smaller month-end drawdown and lower volatility do not erase this opportunity cost. The recommendation buys lower estimated risk at the cost of weaker participation in a strong market.

These results weaken any claim that USMV must dominate on risk-adjusted performance. They do not by themselves invalidate a trustee preference for lower risk. The evaluation is only 36 months and uses a retrospective surviving universe with revised vendor histories. Month-end drawdown understates losses between observation dates. It says nothing definitive about the 2030 funding outcome.

Generated evidence: evaluation_performance.csv; evaluation_calendar_years.csv; evaluation_wealth.csv; evaluation_summary.json. Frozen policy hash is checked before and after evaluation.


## Page 8


Risk acceptance and conditions for change

Risk definition. Treat 15% as a board escalation level for peak-to-trough, month-end, unitized total-fund NAV, excluding external programme withdrawals. Track rolling 12-month investment return separately. An operational warning at 12% requests review; neither threshold guarantees a maximum loss or automatically changes the frozen backtest. In real implementation the board must record any discretionary policy amendment.

An instantaneous 30% equity fall combined with a 100bp rate rise loses 17.53% of initial assets before initial costs. Reducing initial equities by approximately USD 1.014m to cash would satisfy that specific stress, but raises the remaining equity CAGR hurdle to 5.60%. This is a stress-specific sensitivity, not a guaranteed drawdown solution. Once payment bonds mature, equities become a larger fraction of remaining wealth, so initial fund volatility is not a permanent risk measure.

| Feasible policy | 2030 real value at 2.5% inflation | Trade-off |
| --- | --- | --- |
| USMV plus payment bonds | Median $8,886,119; 5th percentile $6,244,402 | Goal remains uncertain |
| Dedicated all-bond plan | $7,470,664 | 6.62% below the USD 8m goal |
| All bonds plus new capital | $8,000,000 | Needs $480,443 more initially |

The all-bond linear programme maximizes terminal cash while keeping cash nonnegative and meeting both original payments. At USD 12m it fixes USD 9.102m nominal terminal cash under zero reinvestment. Its real value still depends on inflation, and interim bond prices can fall. This is a feasible alternative if trustees prefer nominal funding certainty to the equity policy's uncertain upside.

Review quarterly: dedicated cash-flow coverage, ETF mandate and concentration, fees, estimated beta, the unitized loss metric, and updated education-cost inflation. Reconsider USMV if the trustees' growth-sleeve A falls below 2.58, the assumed market premium rises above 6.98%, or a changed objective makes the all-bond compromise preferable. Do not switch because of one favourable backtest.

Mandate revision. Preserve the 22 October package. When the 23 October revision arrives, isolate each changed constraint, retain the 31 December 2022 information cutoff, rerun a separate scenario, and quantify allocation, funding, risk and goal changes against the frozen original. The actual revision, course AI rules and member contributions remain group completion items.

Generated evidence: whole_fund_stress.csv; risk_limit_sensitivity.json; all_bond_alternative.csv; all_bond_cashflows.csv; all_bond_summary.json; mission_simulation.csv.


## Page 9


References and evidence map

[1] Assignment case. BFIN-WS2026-Group_Assignment.pdf supplied by the user. Contractual amounts, quotes, investment restrictions and submission rules.

[2] Kenneth French Data Library. [Open official source](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html).

[2a] FF3 monthly original ZIP. [Open official source](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip).

[3] Federal Reserve projections of 14 December 2022. [Open official source](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20221214.htm).

[4] Yahoo Finance and yfinance settings. [Open official source](https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html).

[5] VTI pre-cutoff summary prospectus. [Open official source](https://www.sec.gov/Archives/edgar/data/36405/000168386320005993/f4654d1.htm).

[6] USMV contemporary SEC-filed description. [Open official source](https://www.sec.gov/Archives/edgar/data/886982/000156459022026948/gs-424b2.htm).

Stock eligibility sources

XOM - pre-cutoff filing 2022-02-23. [SEC filing](https://www.sec.gov/Archives/edgar/data/34088/000003408822000011/xom-20211231.htm).

AAPL - pre-cutoff filing 2022-10-28. [SEC filing](https://www.sec.gov/Archives/edgar/data/320193/000032019322000108/aapl-20220924.htm).

MSFT - pre-cutoff filing 2022-07-28. [SEC filing](https://www.sec.gov/Archives/edgar/data/789019/000156459022026876/msft-10k_20220630.htm).

JPM - pre-cutoff filing 2022-02-22. [SEC filing](https://www.sec.gov/Archives/edgar/data/19617/000001961722000272/jpm-20211231.htm).

JNJ - pre-cutoff filing 2022-02-17. [SEC filing](https://www.sec.gov/Archives/edgar/data/200406/000020040622000022/jnj-20220102.htm).

PG - pre-cutoff filing 2022-08-05. [SEC filing](https://www.sec.gov/Archives/edgar/data/80424/000008042422000064/pg-20220630.htm).

CAT - pre-cutoff filing 2022-02-16. [SEC filing](https://www.sec.gov/Archives/edgar/data/18230/000001823022000050/cat-20211231.htm).

NEE - pre-cutoff filing 2022-02-18. [SEC filing](https://www.sec.gov/Archives/edgar/data/37634/000075330822000014/nee-20211231.htm).

How to audit the figures

Each page names its generated CSV or JSON outputs in outputs/tables. Each figure comes from outputs/figures. The source register, dated retrieval manifest, raw files, executable code and package versions are included in the archive. Run python analysis/rebuild.py after installing the environment. It disables network connections during the rebuild.

The model probabilities and forecasts are conditional analytical assumptions. Supporting methodology pages may reflect current data-production conventions; only pre-2023 economic publications inform the case decision. Historical equity and factor values downloaded now are revised vintages.

AI assistance disclosure

AI assisted with interpretation, coding, source identification, numerical analysis and drafting. Automated checks cover budget totals, bond repricing, cash-flow coverage, sample completeness, file integrity and policy preservation. These checks do not replace student verification. Each group member must explain the analysis and record their actual substantive work, independent checks and critique. Confirm the course-specific AI rules before submission.