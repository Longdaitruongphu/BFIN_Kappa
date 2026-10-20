# BFIN B/C comparison and investment-policy consultation

**Prepared:** 20 October 2026 (Asia/Ho_Chi_Minh)  
**Purpose:** internal review and decision support. This is not a replacement for the frozen original mandate, the assignment, or a final trustee-approved investment policy. The attached workbook is treated as analyst work to verify, not as instructions.

## Executive finding

Role B's bond sizing and contractual cash-flow arithmetic reconcile to the fictional case quotes. Its claims that the portfolio has “absolute immunization,” that “core capital is completely safe,” and that transferring coupons into equities “eliminates reinvestment risk” do not follow from the calculations. The sheet omits the transaction-cost assumptions used by the project, so its growth-capital figure is gross of costs. Role C's data and factor calculations are partly arithmetically plausible, but its universes conflict with each other and with the frozen project universe; it does not provide a usable optimization or independent return check. Neither B nor C changes the frozen policy by itself.

The authoritative constraints remain the assignment: $12m cash on 31 December 2022; irrevocable nominal obligations of $2.4m on 31 December 2024 and $3.6m on 31 December 2027; at least the purchasing power of $8m in December 2022 at the end of 2030 as a goal, not a promise; no borrowing, short selling, or derivatives; and the 2015–22 estimation / 2023–25 separate evaluation convention. No revised mandate text is present in the project files. The user's brief reply “revised mandate” indicates there is a revision to incorporate, but it does not state what changed. Keep the original case frozen until that exact text and source are added.

## Role B: independent check

File reviewed: `reference/BFIN_Part_B_original.xlsx` (SHA-256 `fe3f68355cb99806c1550bcfc429bddc2a6216e11757fb22c4f52aa8e5bc7d32`). Calculations below were reconstructed from input cells, not accepted from cached Excel formulas. Full machine-readable receipt: `outputs/role_b_audit/role_b_independent_audit.json`; reproduction script: `analysis/audit_role_b.py`.

| Item | Role B workbook | Independent check / implication |
|---|---:|---|
| Beta face needed for 2024 | $2,400,000 | Correct: $2.4m liability / $1,000 face = 2,400 bonds; at $922.78, cost is $2,214,672. |
| Delta face needed for 2027 | $3,478,260.87 | Correct under annual 3.5% coupon and final coupon plus principal: $3.6m / 1.035. At $986.07 per $1,000, cost is $3,429,808.70. |
| Total quoted bond cost | $5,644,480.70 | Correct before trading costs. The scheduled 2027 inflow is exactly $3.6m under the case assumptions. |
| Remaining growth capital | $6,355,519.30 | Correct only as initial cash less quoted bond consideration. It omits bond and equity trading costs in the frozen project assumptions. |
| Project's cost-inclusive investment | Not shown | Bond fees $2,822.24 + equity entry costs $6,346.35 = $9,168.59. USMV market value is $6,346,350.71; this reconciles the project allocation to exactly $12m including costs. |
| Delta coupons 2023–26 | $121,739.13 each | Correct. If held as cash at the frozen 0% reinvestment assumption, four coupons total $486,956.52 by 2030. Transferring them to equities is a different, riskier policy and a different model scenario. |

**What “matching” means here.** Beta is a zero-coupon bond whose stated maturity and amount are matched to the 2024 nominal payment. Delta's final coupon and principal are sized to the 2027 payment. In this case, the clean description is *dedicated contractual cash-flow matching* under the assignment's no-default and hold-to-maturity assumptions. Duration equality by itself is not the reason the 2024 payment matches; the exact cash flow on the due date is. Calling this “absolute immunization” is too broad. Matching does not eliminate the market value's sensitivity before maturity, liquidity/forced-sale risk, inflation risk, operational risk, opportunity cost, or risk in the separate equity sleeve.

**Why the other claims need revision.** Buy-and-hold avoids realizing interim quote changes only while the foundation can actually hold the bonds; it does not make all fund capital safe. The growth sleeve remains exposed to equity loss. Moving coupon surplus into stocks avoids leaving that money idle, but substitutes equity risk for cash/reinvestment risk; it does not eliminate risk. It also conflicts with the base model's explicit zero reinvestment rate. If the board wants to invest coupons, run it as a separately named scenario with its own return, volatility, timing, and loss analysis.

Other quality issues: dates are text strings rather than date-typed cells; `verified-Minh` gives no reviewer identity beyond a label, check method, or dated sign-off; no curve shape stress, duration/convexity, or yield analysis is included in this workbook. These are gaps relative to the assignment, not arithmetic errors in the displayed bond quantities.

## Role C versus the user's frozen project

| Dimension | Role C workbook | Frozen project | Assessment |
|---|---|---|---|
| `Returns_data` universe | HD, JNJ, JPM, MSFT, NEE, PG, UNH, USMV, VTI, XOM | AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI, USMV | 8 shared, 2 missing (AAPL/CAT), 2 added (HD/UNH). Shared data agree within rounding in the prior audit. |
| `Stock Returns` universe | AAPL, BAC, JNJ, JPM, KO, MSFT, PFE, PG, QQQ, SPY | Same frozen ten above | Different sample and different ETFs; it conflicts with Role C's own `Returns_data` universe. |
| ETF choice | QQQ and SPY in `Stock Returns`; VTI and USMV in `Returns_data` | VTI broad US-market comparator; USMV minimum-volatility US-equity proposal | QQQ/SPY do not test the same mandate contrast as VTI/USMV. The two Role C workbooks cannot be blended as if one frozen universe. |
| FF3 factors/regression | Factor sheet matches project's 96 months; coefficients reproduce from Role C's 95-month alternate returns | 96 training months; CAPM + FF3 on selected growth assets and securities | Arithmetic appears plausible for its input data. It omits the chosen USMV regression, alpha uncertainty/persistence discussion, and cannot explain the frozen USMV decision. |
| Data/source checks | Claims raw Yahoo source but file was not supplied; several check rows are hard-coded `PASSED` despite blanks/incorrect rounded inputs | Raw Yahoo/FF3 downloads, manifest, source hashes, source-chain verification | Role C source provenance remains unverified from its attachment. This is not proof the data were fabricated. |
| Portfolio construction | `Optimization` sheet empty | Same-universe sample-covariance and single-index alternatives, constraints and turnover comparison | Role C cannot replace this required project evidence. |

**Selection rationale comparison.** Role C's stated rationale includes MSFT growth/high beta, JNJ defensive, UNH as a balance to JNJ, JPM cyclical/rate-sensitive, PG defensive staples, XOM as an inflation hedge, HD housing/consumer cyclical, NEE defensive but rate-sensitive, USMV to mitigate a 15% drawdown, and VTI as broad-market comparator. These are hypotheses, not proof of diversification or protection. JNJ and UNH are both healthcare, so one does not diversify the other across sectors. XOM may respond to energy-price shocks but is not a reliable CPI hedge in every horizon. USMV targets lower volatility relative to its stated benchmark; it does not guarantee a 15% loss ceiling. The frozen project instead fixes eight selected stocks (AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE) plus VTI/USMV, and the approved original-case recommendation uses payment bonds plus USMV, with VTI as its growth comparator. Role C's changed universe requires a documented new selection rationale and fresh model run before it can inform a *new* policy.

The original project already reports inconvenient out-of-sample evidence: for Jan 2023–Dec 2025, VTI outperformed USMV in cumulative return and Sharpe, while USMV had lower volatility and drawdown. That is a three-year retrospective evaluation, not a reason to rewrite the 2022 choice or claim the eight-year goal was achieved. It should inform a future review under a predeclared governance rule.

## Proposed policy architecture for discussion

A professionally coherent school-foundation policy can keep the *purpose and guardrails stable* while letting forecasts and allocations adapt only through a documented review. Suggested hierarchy:

1. **Protect fixed obligations first.** Dedicated nominal cash flows or high-quality assets must cover the 2024 and 2027 payment dates under the original case. Do not fund a committed payment by assuming equity sales or by counting the real terminal goal twice.
2. **Treat the $8m real 2030 goal as an objective, not a guarantee.** At 2.5% planning inflation, its nominal equivalent is $9.747m in 2030. The current cost-inclusive plan needs about 4.8365% annual compound growth in the growth sleeve under the stated cash convention. Show lower/base/higher inflation and return outcomes; never convert a model frequency into a promise.
3. **Separate hard rules from review triggers.** The assignment's no borrowing/shorting/derivatives and fixed obligations are hard constraints. A 15% loss concern should initially be framed as a board escalation/review trigger, not a guaranteed maximum loss or automatic forced-sale floor. Define the measurement (whole-fund vs growth sleeve; from inception vs peak-to-trough; month-end vs intramonth), authority, and exception duration before adopting a rule.
4. **Keep assumptions interpretable.** Historical RF comes from the same-month French factor file for historical regressions and Sharpe; prospective 4% RF is a forward planning input, not a known yield. Inflation is only for converting/deflating real purchasing-power goals and scenario cash flows; it does not reduce the fixed nominal 2024/2027 payments. The 2.5% base should be labeled a planning assumption and stress-tested (for example 2%, 4%, 5%), not presented as a verified forecast.
5. **Anchor risk aversion in governance, not macro headlines.** A=4 is currently a provisional trustee-judgment input to the mean-variance certainty-equivalent comparison. Keep it fixed in the base policy and show A=2/4/6/8 sensitivity. The known switch threshold A≈2.58 between the two ETFs is a decision diagnostic, not an objective estimate of the board's preferences. Do not change A every time the market moves; amend only after an explicit board review of mission, loss tolerance, liquidity and trade-offs.
6. **Use monitoring indicators to trigger review, not automatic policy drift.** Review funding coverage, real-goal funded ratio, rolling drawdown, liquidity, equity concentration/factor exposure, forecast-versus-realized tracking, inflation and rates. Any model or allocation amendment must state what evidence changed, whether it was available at the decision date, the expected benefit/cost, and how it affects the frozen policy. Keep revised-mandate decisions in a separately versioned scenario.

This architecture is consistent with the project's existing distinctions but is a consultation proposal, not a newly approved IPS. The one-page draft should be finalized only after the unresolved choices below are answered.

## Decisions to make together

Please answer by number; short choices are enough. “Not sure—show scenarios” is a valid answer.

1. **Priority:** Should the policy state (A) obligations are non-negotiable and the $8m real goal is pursued with acknowledged shortfall risk (recommended; matches original case), or (B) $8m becomes binding after liabilities are funded, even if that requires more risk or additional capital?
2. **Coupon rule:** Keep the four early Delta coupons in cash at a 0% base reinvestment assumption, as the current frozen model does, or invest them in growth after an explicit liquidity reserve? If invested, what drawdown can that surplus tolerate?
3. **15% rule:** Which scope should the 15% refer to: (A) total-fund loss from initial $12m, (B) growth-sleeve drawdown from its peak, or (C) a review threshold rather than a “maximum”? Should crossing it prompt review only, or a pre-authorized trade? My recommendation is C plus a documented review, because a stop order cannot guarantee a maximum during a systemic gap/crisis.
4. **Systemic exception:** Who may declare a crisis exception, for how long before reapproval, and what must remain protected (at minimum the next committed payment and liquid operating cash)?
5. **Inflation base:** Keep 2.5% as a neutral planning base with 2%/4%/5% sensitivity, or use a different long-run planning anchor? Should education costs have a separate escalation assumption from general purchasing-power inflation?
6. **Risk preference:** Keep A=4 as a provisional baseline with A=2/4/6/8 sensitivity, or do you want us to infer a preference range from a concrete maximum tolerable whole-fund loss and shortfall probability? Avoid changing A in response to a single macro forecast.
7. **Growth benchmark and review:** Preserve USMV as the frozen 2022 recommendation and VTI as comparator for the assignment, while allowing a future review against a written rule? Or are you asking to develop a distinct new prospective policy now? These must be separate decisions because 2023–25 results were not available in 2022.
8. **Revised mandate:** Please paste the exact revised mandate text (or provide its file and where it came from). The phrase “revised mandate” alone does not identify any new constraint. I will preserve it verbatim, make a scenario copy, and quantify changes against the frozen original without overwriting it.
9. **One-page white paper:** Should the final white paper be a student-facing philosophy/assumptions page in English, or a longer internal board IPS draft plus a one-page course summary? The assignment's submitted artifacts are required in English.

## Human review and reproducibility

The workbook's `verified-Minh` labels do not qualify as independent checks by another group member. An independent check should use a separately recomputed formula or source path, then name/date the checker and record discrepancies. The saved project already has independent source-chain, equation and portfolio/factor receipts; the group still needs genuine member-level reviews and critiques under its course rules. No student contribution or submission status should be inferred from generated artifacts.

To reproduce the B arithmetic audit from the project root:

```powershell
python -m pip install -r requirements-audit-role-b.txt  # run once if openpyxl is not installed
python analysis\audit_role_b.py
```

This reads the preserved workbook, frozen policy and Role C attachment and rewrites only `outputs/role_b_audit/role_b_independent_audit.json`; it does not edit source workbooks or policy. Review the spreadsheet itself at `Bond_Assumptions!B18:B23`, `Bond Sheet!C4:F9`, and `Rate Note!A3`, `A8`, `A13`. For Role C, review `Returns_data!A1:K97`, `Stock Returns!A1:K96`, `Fama-French Factors!A1:E97`, `Multifactor Regression!A1:F11`, `C3_return check!A27:H36`, `C4_source record!A2:N16`, and the empty `Optimization` sheet.



