# Kappa Foundation | Initial decision record

USD | Case date 31 December 2022 | Initial submission 22 October 2026  
Prepared 21 October 2026 | Original mandate

The PDF uses a SISF-inspired main column and facts sidebar. Table explanations are outside cells; the source line below each table is italic 7.5pt. Superscripts 1-5 refer to the five one-line definitions at the foot of page 2.

## Page 1 | Investment objective and policy

Meet the fixed education commitments first and protect long-term purchasing power. Invest surplus capital within the fund's capacity for risk. Seek **USD 8m in December 2022 purchasing power at end-2030**; this is a planning goal. Portfolio changes require evidence about obligations, resources and assets, rather than short-term market moves.

### Initial capital allocation

| Holding / use | Units / basis | Initial USD |
|---|---:|---:|
| Beta / 2024 | 2,400 | 2,214,672.00 |
| Delta / 2027 | 3,478.26087 | 3,429,808.70 |
| USMV | 100% of sleeve | 6,346,350.71 |
| Trading costs | 5 / 10bp | 9,168.59 |
| Total | | 12,000,000.00 |

*Source: case Exhibit 1; Kappa model; USD, fees separate; % rounded.*

The allocation chart shows Beta 18.46%, Delta 28.58%, USMV 52.89% and costs 0.08%; rounded percentages may not sum to exactly 100%.

Beta principal pays **$2.4m on 31 Dec 2024**. Delta principal and its final coupon pay **$3.6m on 31 Dec 2027**. Four earlier Delta coupons total $486,957 and remain cash at 0%; payment coverage needs no equity sale or reinvestment return.

### Growth portfolio decision

**Recommend 100% USMV**, the US minimum-volatility ETF. Use **100% VTI**, a broad-US-market ETF, as the frozen investable benchmark and credible rejected alternative.

| Annual measure | USMV | VTI | Max utility A=4 |
|---|---:|---:|---:|
| Expected return<sup>1</sup> | 7.14% | 8.45% | 7.19% |
| Volatility<sup>2</sup> | 12.84% | 16.31% | 12.70% |
| Utility<sup>3</sup>, A=4 | 3.84% | 3.13% | 3.96% |

*Source: Yahoo Finance, Kenneth French; Kappa model; 2015-22, annualised.*

The maximum-utility portfolio at A=4 uses all 10 candidates as its opportunity set. Its non-zero weights are **MSFT 2.92%, JPM 3.52%, JNJ 7.46%, PG 11.62%, XOM 2.96%, NEE 7.45%, USMV 46.18% and VTI 17.89%**; AAPL and CAT receive 0.00%. The weights total 100.00%. This is the highest-scoring long-only mix for the stated inputs: CAPM expected returns, 96-month sample covariance, no borrowing or shorting, fully invested, and no additional security caps. At A=4 it estimates 7.19% expected return, 12.70% volatility and 3.96% utility.

The model portfolio's utility estimate is 0.12 percentage point above 100% USMV (3.96% versus 3.84%). When the estimation window is shortened from 96 to 60 months, the optimised weights shift 34.8% one-way. On this $6.346m sleeve, that is about $2.21m to sell and an equal amount to buy if switching between those two model portfolios. It is an estimate of how sensitive the optimizer is to its sample, not a trade instruction. We recommend USMV as the simpler policy implementation; it is not the full-universe utility maximum. Neither portfolio guarantees principal or the 2030 goal.

USMV is a policy choice, not the unrestricted utility maximum. Neither ETF guarantees principal or the 2030 goal. Long-only; no borrowing, shorting or derivatives. Fractional holdings allowed. Fee sensitivity: 0bp bonds / 5bp ETFs / 10bp stocks.

### Sidebar | Mandate facts and core assumptions

| Fact | Value |
|---|---|
| Initial capital | $12.000m |
| Currency | USD |
| Goal date | 31 Dec 2030 |
| Real goal | $8.000m |
| Growth sleeve | 100% USMV |
| Benchmark | 100% VTI |

*Source: original case and proposed IPS.*

| Assumption | Value |
|---|---|
| CPI base | 2.50% |
| HEPI stress | 3.00% |
| Risk-free (plan) | 4.00% |
| Market premium | 4.50% |
| Forecast alpha | 0.00% |
| Risk aversion A | 4 (provisional) |
| Coupon cash rate | 0.00% |
| Bond / equity fee | 5 / 10bp |

*Source: proposed IPS; annual scenarios.*

Candidate universe: technology AAPL/MSFT; financials JPM; health care JNJ; staples PG; energy XOM; industrials CAT; utilities NEE; equity ETFs USMV/VTI.

*Source: eligibility notes; 2022 status.*

Eight stocks, seven sectors and two distinct ETF mandates. Candidates need not all be held. No additional security-weight caps are imposed.

## Page 2 | Policy, risk and implementation

### Risk-preference comparison

The chart compares three things while holding the return and risk inputs fixed. The USMV and VTI lines keep a 100% holding in one ETF. The dashed line re-optimises all 10 candidates at each A, so it shows the highest modelled utility available from that candidate set for each risk preference. At A=4, the corresponding weights are listed above. As A rises, the model penalises variance more and changes the mixture; the optimal weights therefore need not stay the same.

| Risk aversion A | USMV utility | VTI utility |
|---:|---:|---:|
| 2 | 5.49% | 5.79% |
| 4 | 3.84% | 3.13% |
| 6 | 2.20% | 0.47% |
| 8 | 0.55% | -2.19% |

The max-utility curve is based on these annual scores at A=2, 4, 6 and 8: 5.81%, 3.96%, 2.43% and 0.96%. The curve is an in-sample model comparison, not a return forecast guarantee. Among the two fixed ETF choices, VTI has higher utility only at A=2; USMV leads at A=4, 6 and 8 (crossover A=2.58). A=4 is a provisional committee preference input, not an industry standard.

*Source: Kappa analysis; Yahoo/French inputs; annual utility scores.*

The portfolio at each A is saved in `outputs/sample_utility_robustness.json`; the full A=4 ticker weights are in `outputs/max_utility_A4_weights.csv`, and utility/risk/return across the A grid are in `outputs/max_utility_preference.csv`.

### Real-goal sensitivity

| 2030 goal | Base | Stress |
|---|---:|---:|
| Inflation | 2.50% | 3.00% |
| Nominal USD | $9.747m | $10.134m |
| CAGR<sup>4</sup> hurdle | 4.84% | 5.37% |

*Source: funding model; 2022-30.*

CPI defines the primary goal. HEPI is a separate education-cost stress. Both hurdles retain four early coupons at 0% cash interest.

### Risk oversight | Growth sleeve

Use flow-adjusted growth-sleeve unit values, including cash; retain the prior peak after asset changes. Report payment coverage and whole-fund stress separately. Historical drawdown<sup>5</sup> is measured at month-end.

| Signal<sup>5</sup> | Required action | Deadline |
|---|---|---|
| 10% | Validate data, funding and stress | Within 2 business days |
| 15% | Investment Committee decision | Within 5 business days |
| 20% | Notify trustees; pause risk increases | Same / next business day |
| Payment gap | Escalate; restore payment coverage | Immediate |

*Source: proposed IPS, 21 Oct 2026; growth-sleeve review triggers, not guaranteed loss limits.*

No automatic sale. At 15%, record hold, authorised rebalance or policy proposal. Discretionary crisis deferral requires written authority, expiry and review; due-payment coverage cannot fall.

### Annual goal protection and policy response

At each annual review, first confirm remaining bond and cash obligations. Test the 2030 goal of $9.747m nominal at CPI 2.5% ($10.134m at HEPI 3% stress) after a **30% fall** in growth assets. If stressed resources still cover the goal, trustees may approve locking only the minimum needed in a permitted, actually priced asset due by 2030; keep excess invested. This is a prospective trustee decision, not automatic profit-taking. If a gap remains, report it; do not raise risk to catch up. For relative underperformance, diagnose exposures, costs and implementation before proposing a change.

### Frozen test and future rebalancing

For the test, freeze USMV 100% and VTI 100% of the growth sleeve at **31 Dec 2022**. Compare monthly total returns in Jan 2023-Dec 2025. Reset to starting weights after each December return, without updating forecasts. Since each portfolio holds one ETF, this rule normally creates no trade; charge 10bp only when a trade occurs. Later returns test the frozen choice; they do not set the 2022 weights. Future changes require a dated committee review under the IPS.

Estimate Jan 2015-Dec 2022 (96 common months); a 60-month sample check informs the initial recommendation. For the final memo, compare sample with single-index covariance. CAPM forecasts set alpha to zero; FF3 explains historical exposures. No 2023-25 observation enters the 2022 weights.

### Read and reproduce

1. Read `data/DATA_RECORD.md` and its retrieval manifest.
2. Install `requirements-analysis.txt`; run `python analysis/run_initial.py` offline.
3. Check `initial_decision_rebuild.json`, `candidate_statistics.csv`, `sample_utility_robustness.json` and `risk_preference.csv` in `outputs/`. Retrieval: `analysis/retrieve_data.py --phase train`, in a clean copy.

Data retrieved 15 Oct 2026: Yahoo adjusted-close and French factors. Revised histories and survivor selection limit this retrospective case. Fictional bonds use contract cash flows. RF=4% is a planning scenario; historical excess returns use observed monthly French RF.

### Mini-Glossary | One line per definition, 7.5pt in the PDF

1. **CAPM return:** Annual arithmetic forecast: risk-free rate + beta x market premium; forecast alpha=0.
2. **Volatility:** Monthly return standard deviation x sqrt(12); an annual risk estimate, not a loss cap.
3. **Utility (A):** E[R] - 0.5 x A x annual variance; a higher A applies a larger penalty to risk.
4. **CAGR:** The constant annual compound rate over a period; the goal hurdle includes retained coupon cash.
5. **Drawdown:** Decline in the flow-adjusted growth-sleeve unit value from its previous peak.
