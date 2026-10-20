
## Page 1


Kappa Foundation initial decision record

Prepared for the 22 October 2026 submission

Case decision: 31 December 2022. Information cutoff: 31 December 2022. The original policy is frozen in policy/frozen_policy.json with a SHA-256 record. This is a prepared submission, not evidence that a student submitted it.

Decision. Protect the two nominal obligations with dedicated Beta and Delta holdings. Invest the residual growth sleeve in USMV, with VTI as the simple investable comparator. Accept the real-value target as an aspiration and the 15% loss concern as an escalation threshold, not a guaranteed maximum loss.

| Use | USD | Share | Implementation |
| --- | --- | --- | --- |
| Beta | $2,214,672.00 | 18.46% | 2,400 bonds; USD 2.4m face |
| Delta | $3,429,808.70 | 28.58% | 3,478.26087 bonds; USD 3.478m face |
| USMV | $6,346,350.71 | 52.89% | Growth allocation |
| Execution costs | $9,168.59 | 0.08% | 5bp bonds and 10bp equities |
| Total | $12,000,000 | 100.00% | Rounding affects displayed percentages |

Universe. Eight US common stocks: AAPL, MSFT, JPM, JNJ, PG, XOM, CAT and NEE, spanning seven sectors. ETFs: VTI for broad US market exposure and USMV for minimum volatility. Dated SEC evidence is in the supporting source record; retrospective selection bias remains.

Estimation. January 2015-December 2022, 96 common months. Daily Yahoo downloads supply month-end adjusted prices; December 2014 is the initial denominator only. FF3 monthly factors come directly from Kenneth French's ZIP. No future returns enter estimation.

Payment plan. Beta face USD 2.4m matures in 2024. Delta face USD 3,478,260.87 produces exactly USD 3.6m at maturity in 2027. Retain four earlier Delta coupons of USD 121,739.13 in cash. Base reinvestment is zero. All payment amounts remain unchanged.


## Page 2


Assumptions and frozen evaluation rule

Planning assumptions. Inflation 2.5% annually, tested at 2%-5%. Forecast return = 4.0% + estimated market beta x 4.5%, with zero forecast alpha. Compare growth-sleeve utility CE = mean - A x variance / 2 at A = 4 and sensitivities from 1 to 8. These are judgement inputs rather than estimated trustee preferences.

Constraints and execution. Long only, no borrowing or derivatives. Candidate optimization caps direct stocks at 10% each and 30% collectively. Pure ETF policies are allowed. Cost assumptions are 5bp on initial bond consideration and 10bp per equity dollar traded. Fractional holdings are permitted. December 2022 last close is a sizing and paper-evaluation proxy, not a claim of a live executable equity quote on Saturday 31 December.

Risk. Monitor month-end unitized total-fund peak-to-trough loss net of external programme payments. At 12%, request review; at 15%, escalate to trustees. No automatic tactical trading enters the evaluation. Dedicated bonds stay earmarked. The growth share rises after payment bonds mature, so later risk must be reviewed explicitly.

Evaluation. January 2023-December 2025 remains separate. Freeze initial weights and the VTI comparator. Reinvest equity dividends through adjusted-price total-return proxies. For multi-asset diagnostic alternatives, rebalance after December returns to inception weights without re-estimation, using only prices then available. Charge costs on both purchase and sale notionals. The one-ETF recommendation and benchmark require no cross-asset rebalance.

Comparisons. Report CAGR, volatility, Sharpe, month-end drawdown, calendar-year returns and turnover, including unfavourable results. Test the 60-month estimation alternative, market premiums, risk aversion, covariance model and inflation. Evaluate fictional bonds only through contractual cash flows and explicit rate scenarios.

Preservation. The archive contains working Python code, raw training data, a dated source record and the frozen policy. Keep an unchanged copy of this submission before responding to the 23 October revised mandate. The revision must retain the original case date and be compared quantitatively with this record.

Generated evidence: analysis/config.json; policy/frozen_policy.json; policy/frozen_policy.sha256; data/raw/retrieval_manifest.jsonl. AI assistance and member verification must be disclosed under course rules.