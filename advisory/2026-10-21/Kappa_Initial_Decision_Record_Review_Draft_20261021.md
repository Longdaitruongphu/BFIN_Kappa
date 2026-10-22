**Kappa Foundation — Initial decision record, review draft**

Prepared 21 October 2026 for review before the 22 October submission. Case date and information cutoff: 31 December 2022. This draft corrects the working record's unapproved concentration limits and inconsistent rebalance wording. It does not replace the archived policy, certify submission, or implement the unreleased revised mandate. Page layout has not been rendered or certified.

**Mandate and decision.** Fund the fixed nominal obligations of $2.4m on 31 December 2024 and $3.6m on 31 December 2027 with dedicated case bonds. Invest the remaining growth sleeve in USMV and retain VTI as the simple investable comparator. Seek $8m in December-2022 purchasing power at the end of 2030, accepting that this goal is not guaranteed.

| Initial use | USD |
|---|---:|
| Beta: 2,400 units | 2,214,672.00 |
| Delta: 3,478.26087 units | 3,429,808.70 |
| USMV growth allocation | 6,346,350.71 |
| Execution costs | 9,168.59 |
| Total | 12,000,000.00 |

Beta principal meets the first payment. Delta's final coupon plus principal meets the second. Four earlier Delta coupons total $486,956.52 and remain in cash at a base reinvestment rate of zero. Coverage is checked at every payment date, without relying on equity sales.

**Universe and evidence.** Candidates are AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI and USMV. Use 96 common monthly returns from January 2015 to December 2022, with a 60-month sensitivity. Yahoo/yfinance downloads, French factor files and retrieval records are preserved. Dated eligibility evidence does not eliminate retrospective selection bias or vendor-history revisions.

**Assumptions.** Planning inflation is 2.5%, with 2–5% sensitivities. It makes the terminal nominal goal $9,747,223.18; the original equity sleeve requires 4.8365% nominal compound annual growth after allowing for retained coupons. Historical excess-return analysis uses the corresponding observed monthly French RF series. Prospective CAPM inputs are RF 4%, equity market premium 4.5% and zero forecast alpha. RF 4% is not an executable eight-year cash yield. FF3 explains exposures and historical returns; forecasting from it would require explicit expected factor premiums.

Compare utility as expected annual arithmetic return minus one-half of A times annual variance. Provisional A=4 represents a conservative preference, not an industry standard. Test alternative A values and both sample and single-index covariance. The training-based USMV/VTI utility ranking reverses near A=2.58 with other inputs fixed. USMV is a simple implementation choice, not a claim to be the global utility optimum across all feasible portfolios.

**Constraints and costs.** Long only; no borrowing, short selling or derivatives. Fractional holdings are allowed. The user selected 5bp on bonds and 10bp on equity as the base planning friction; compare separately against 0bp bonds, 5bp ETFs and 10bp direct stocks. These are assumptions, not broker quotes. No additional 10%-per-stock or 30%-aggregate-stock limits have been approved; earlier results using those limits are capped sensitivity cases.

**Risk governance.** The user approved the 10% / 15% / 20% ladder for inclusion in the group's proposed IPS. The primary measure is growth-sleeve drawdown on unitized total returns. Include cash raised by selling sleeve assets; adjust external transfers and do not reset the high-water mark when changing holdings. Report whole-fund stress, dated payment coverage and real-goal feasibility separately. Historical monthly observations support month-end drawdown only.

| Growth drawdown or funding event | Proposed response |
|---|---|
| 10% | Within two business days verify data, coverage and stress; no automatic trade |
| 15% | Investment Committee meets within five business days; document hold, a separately authorized rule-based rebalance, or recommendation to trustees to change policy |
| 20% | Notify trustees the same or next business day; pause discretionary risk increases pending review; no automatic liquidation |
| Any threatened payment deficit | Immediate escalation and a funded corrective plan, regardless of drawdown |

These thresholds and response deadlines are the group's proposed governance rules, user-approved for inclusion in this record; trustees have not yet authorized them. They are not universal standards or guaranteed loss limits. A price stop cannot ensure an absolute 15% loss ceiling. A crisis exception may defer only discretionary action, with written authority, expiry and review; it cannot reduce payment coverage. A threatened mandatory payment is escalated immediately at any drawdown.

**Evaluation and implementation.** Preserve the original rule: annual rebalancing after December returns to fixed inception growth weights, without re-estimation in January 2023–December 2025. With a single-ETF growth allocation, internal rebalancing normally requires no trade. Changing ETF or strategic cash exposure is a prospective policy amendment. Do not restore initial bond percentages after bonds have fulfilled their payment purpose.

Evaluate the frozen growth portfolio and frozen VTI comparator separately over 2023–2025. Retain unfavorable results in the evaluation report; do not use them to justify or redesign the 2022 decision. Additional allocation bands require explicit definition and authorization before use. At present the 100% USMV sleeve has no internal weight drift to rebalance.

**Future review principles.** Prioritize payment security and risk control when market-wide conditions undermine the real goal. Diagnose relative underperformance using factor/style exposure, realized risk, costs and implementation quality before changing assets. Report the dollar shortfall and remaining return hurdle; do not lower A merely to chase recovery. Review the remaining fund after major payments and as 2030 approaches. Any change in mandate, assumptions, benchmark or policy must have a dated rationale, before/after comparison and prospective effective date.

**Upside review.** The user selected this principle for the proposed IPS: at each annual review, confirm all obligations, update the real goal using CPI 2.5% as the primary measure, and test funding after a -30% growth-sleeve shock. HEPI 3.0% is a separate education-cost stress. If the goal still remains fully funded, protect only the minimum amount needed in a permitted asset matched to the goal date; keep any surplus invested under the growth policy. Do not sell winners at a fixed gain percentage or raise spending automatically after a strong year. The eligible instrument, market-price convention, fee treatment and authorized execution steps remain to be confirmed; the stress rule does not guarantee real purchasing power.

**Institutional practice and inflation sensitivity.** University endowment policies commonly distinguish payout smoothing from the investment portfolio's long-term purchasing-power objective and benchmark monitoring. Kappa's two fixed payments are dated liabilities, not discretionary annual spending, so payout rates such as 5% are not imported. The user selected CPI 2.5% as the primary $8m real-goal test and HEPI 3.0% as a separate education-cost stress. The corresponding nominal 2030 goals are $9.747m and $10.134m. At the original capital and retained-coupon assumptions, required growth-sleeve CAGR is approximately 4.84% under CPI and 5.37% under HEPI stress. Do not combine the indices in one goal formula. Reproduce this sensitivity with `analysis/goal_inflation_sensitivity.py` and `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`.
