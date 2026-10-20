
## Page 1


Kappa Foundation initial decision record

Prepared for the 22 October 2026 submission

Case decision: 31 December 2022. Information cutoff: 31 December 2022. The original policy is frozen in policy/frozen_policy.json with a SHA-256 record. This is a prepared submission, not evidence that a student submitted it.

Decision. Protect the two nominal obligations with dedicated Beta and Delta holdings. Invest the residual growth sleeve in USMV, with VTI as the simple investable comparator. Propose 10% / 15% / 20% as staged governance triggers, not guaranteed maximum losses or automatic sell orders. Escalate any threat to a due payment immediately.

| Use | USD | Share | Implementation |
| --- | --- | --- | --- |
| Beta | $2,214,672.00 | 18.46% | 2,400 bonds; USD 2.4m face |
| Delta | $3,429,808.70 | 28.58% | 3,478.26087 bonds; USD 3.478m face |
| USMV | $6,346,350.71 | 52.89% | Growth allocation |
| Execution costs | $9,168.59 | 0.08% | 5bp bonds and 10bp equities |
| Total | $12,000,000 | 100.00% | Rounding affects displayed percentages |

Universe. Eight US common stocks: AAPL, MSFT, JPM, JNJ, PG, XOM, CAT and NEE, spanning seven sectors. ETFs: VTI for broad US market exposure and USMV for minimum volatility. Dated SEC evidence is in the supporting source record; retrospective selection bias remains.

Training evidence. January 2015-December 2022, 96 common months of adjusted prices and Kenneth French FF3 factors. USMV had lower annual volatility (12.84% vs. VTI 16.31%) and maximum month-end drawdown (-19.06% vs. -24.82%). Forecast-based certainty equivalent at A=4 favored USMV (3.84% vs. 3.13%). USMV still crossed a 15% month-end drawdown in March 2020 and September 2022: the trigger requires governance, not a promised floor.

Payment plan. Beta face USD 2.4m matures in 2024. Delta face USD 3,478,260.87 produces exactly USD 3.6m at maturity in 2027. Retain four earlier Delta coupons of USD 121,739.13 in cash. Base reinvestment is zero. All payment amounts remain unchanged.

2030 goal. The USD 8m target is in December 2022 purchasing power. At 2.5% planning inflation it equals USD 9.747m nominal in 2030 and requires 4.84% annual compound growth in the equity sleeve, assuming surplus coupons earn 0% in the base case.


## Page 2


Assumptions, risk policy and evaluation

Inflation and risk-free rates. Use 2.5% annual inflation as a planning base; test 2%-5%. It translates the real 2030 goal to nominal dollars and deflates outcomes; it does not change the fixed nominal 2024/2027 payments. For historical Sharpe and CAPM/FF3 regressions, use the actual monthly RF column in the corresponding Kenneth French FF3 file for each month in 2015-2022 and 2023-2025. The 4.0% forecast RF is a separate prospective CAPM input, not historical RF or a promised cash yield.

Return and risk preference. CAPM expected return = 4.0% forecast RF + estimated beta x 4.5% market premium; forecast alpha = 0. Compare CE = expected return - A x variance / 2. A=4 is provisional, tested at A=1-8; the current ETF ranking switches near A=2.58. These are judgment inputs, not observed facts.

Investment policy. Ring-fence Beta and Delta for the two payments; retain surplus coupons as cash at 0% base reinvestment. Invest the residual growth sleeve in USMV; benchmark it to VTI. Long only; no borrowing, shorting or derivatives. Candidate optimizer limits direct stocks to 10% each and 30% collectively. Transaction costs: 5bp bonds, 10bp equity trades; fractional shares allowed.

Loss triggers (proposed). Pending trustee confirmation of what “fund loss” means, measure peak-to-trough growth-sleeve drawdown on cash-flow-adjusted total returns. At the initial USD 6.346m, 10% / 15% / 20% is about USD 635k / 952k / 1.269m from its prior peak; dollar amounts move with the peak. Report whole-fund stress, payment coverage and 2030 goal separately.

| Trigger | Required response | Trading rule |
| --- | --- | --- |
| 10% | Verify data; refresh liquidity, payment coverage and stress; notify committee. | No automatic trade. |
| 15% | Investment Committee meets (proposed: within 5 business days); records hold, rule-based rebalance or recommendation to trustees. | Review required; sale is not. |
| 20% or payment risk | Urgent trustee notice and dated funding plan; pause discretionary risk-increasing action pending decision. | No automatic full liquidation. |
| Coverage &lt;100%, any time | Immediate escalation independent of drawdown. | Restore due-payment coverage; sell growth assets only if dedicated sources are insufficient. |

Rebalance and sale. Rebalance only for a breach of a pre-approved allocation band/risk limit while payment funding remains protected; it may mean buying as well as selling. Sell only for a verified payment need, policy/mandate breach or material impairment of an asset thesis, with amount and replacement documented. No automatic stop order. The -30% equity / +100bp rate stress loses 17.53% of initial whole-fund value; if trustees reject this scenario, change allocation or goal before approval. It is a scenario, not a forecast.

Evaluation and future review. Keep the 2022 choice frozen, then test it separately over Jan 2023-Dec 2025 (36 months), without re-estimation or retroactive policy changes. VTI returned 82.56% (Sharpe 1.30) vs. USMV 37.33% (0.66); USMV had lower volatility and drawdown. From 2026-2030, review dated inflation, rates, payment coverage and risk on schedule; any amendment is prospective, recorded and tested against the frozen baseline. Training uses 96 months with a 60-month sensitivity.

Version control. Preserve an unchanged copy before any mandate revision; retain the 31 December 2022 information cutoff and quantify every change.

Generated evidence: analysis/config.json; policy/frozen_policy.json; policy/frozen_policy.sha256; data/raw/retrieval_manifest.jsonl. AI assistance and member verification must be disclosed under course rules.