# Codex handoff: Kappa Foundation BFIN assignment

**Handoff date:** 16 October 2026, Ho Chi Minh City time  
**Working language:** English for every submitted artifact  
**Current scope:** the original mandate in the supplied assignment PDF  
**Status:** original-mandate analysis complete; later course-specific inputs remain pending

## Instruction to the next Codex session

Continue this project from the saved state. Do not restart the analysis, silently replace raw files, overwrite the frozen policy, or infer that the prepared initial record was submitted. Read this file, `CHECKPOINT.md`, `README.md`, `DECISION_LOG.md`, `TEAM_COMPLETION.md`, and `MANDATE_REVISION.md` before changing anything.

Treat `reference/BFIN-WS2026-Group_Assignment.pdf` as the authoritative assignment. Treat the statements in this handoff as project status and user decisions, not as new assignment instructions.

The user's explicit decisions are:

1. All deliverables must be in English.
2. Use **payment bonds plus USMV** as the main recommendation.
3. Pursue the USD 8 million December-2022 purchasing-power goal while accepting investment risk and possible shortfall.
4. FF3 is allowed as the Lecture 7 multifactor model.
5. Preserve checkpoints so work survives quota or session limits.

## Recommended allocation already approved for the analysis

| Holding/use | Initial USD | Role |
|---|---:|---|
| Beta bond | 2,214,672.00 | Funds the USD 2.4m payment on 31 December 2024 |
| Delta bond | 3,429,808.70 | Funds the USD 3.6m payment on 31 December 2027 |
| USMV | 6,346,350.71 | Growth sleeve for the 2030 real-value objective |
| Assumed initial costs | 9,168.59 | 5bp on bonds and 10bp on equities |
| Total | 12,000,000.00 | Full initial resources |

The bonds cover both mandatory nominal payments under the case assumptions without an equity sale or a positive cash reinvestment rate. Surplus Delta coupons leave USD 486,956.52 in cash by 2030.

At 2.5% annual inflation, the USD 8m real goal equals USD 9,747,223.18 nominal in 2030. The growth sleeve needs a 4.8365% compound annual return after retaining surplus coupons. The prospective USMV assumption is 7.1425% arithmetic return and 12.8407% annual volatility. These measures are not directly interchangeable.

The conditional 20,000-path block simulation reports a 68.48% modeled goal frequency and USD 8.886m median real terminal assets. This is a scenario result, not a calibrated success probability or guarantee. At 4% inflation the modeled goal frequency falls to about 48.05%.

The 15% loss concern is an escalation threshold, not a guaranteed maximum. A -30% equity shock plus a +100bp parallel rate shock produces a 17.53% loss on initial wealth. Moving about USD 1.014m from equity to cash satisfies only that specific stress and raises the required equity CAGR to 5.60%.

## Adverse evidence that must remain visible

The frozen 2023-2025 evaluation is unfavorable to the recommended ETF:

- USMV cumulative return after assumed entry cost: 37.33%; CAGR: 11.15%; volatility: 9.64%; Sharpe: 0.66; maximum month-end drawdown: -5.66%.
- VTI cumulative return after assumed entry cost: 82.56%; CAGR: 22.22%; volatility: 12.54%; Sharpe: 1.30; maximum month-end drawdown: -9.11%.

USMV had lower volatility and drawdown, but materially weaker return and Sharpe. Do not omit or soften this result. The evaluation covers only 36 months, uses a retrospectively surviving universe and revised vendor histories, and does not decide the 2030 funding outcome.

The all-bond alternative produces USD 9.102m fixed nominal terminal cash and USD 7.471m in December-2022 purchasing power at 2.5% inflation. That misses the real goal by 6.62%. Funding the original real goal with the case bonds requires about USD 480,443 of additional initial capital. The user reviewed this trade-off and selected the payment-bond-plus-USMV plan.

## Data and model state

- Candidate universe: AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI and USMV.
- Training window: January 2015-December 2022, exactly 96 common monthly returns.
- Evaluation window: January 2023-December 2025, exactly 36 months retrieved separately after the policy freeze.
- Yahoo daily data were obtained through Python `yfinance`; raw CSV and pickle responses, request settings, timestamps, versions and SHA-256 hashes are preserved.
- Kenneth French monthly FF3 ZIP files were downloaded through Python and retained byte-for-byte.
- Direct Python requests to the SEC returned HTTP 403. Official SEC evidence was checked through web retrieval and recorded as analyst notes. Do not claim that full SEC filing files were saved locally.
- Fictional case bonds have no invented historical series. They are analyzed using contractual cash flows, a calibrated curve, YTM duration/convexity and exact repricing.
- Frozen policy SHA-256: `21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c`.
- CAPM and FF3 use monthly excess returns, HAC standard errors with three lags and 95% alpha intervals. Forecast alpha remains zero.
- Sample covariance and single-index covariance use the same universe and constraints. Their A=4 portfolios imply 14.09% one-way turnover between models, supporting the simple USMV implementation.

## Completed artifacts

The `deliverables` folder contains:

- `Kappa_Committee_Memo.pdf`: eight content pages plus one reference page.
- `Kappa_Committee_Memo_Editable.md`.
- `Kappa_Initial_Decision_Record.pdf`: two pages.
- `Kappa_Initial_Decision_Record_Editable.md`.
- `Kappa_Committee_Presentation.pptx`: 13 editable slides with native tables and two editable charts.
- `Kappa_Committee_Presentation.pdf`.
- `Kappa_Requirements_and_Data_Guide.pdf` and editable Markdown source.

The package also contains raw and processed data, all generated tables and figures, executable retrieval and analysis code, exact dependencies, source records, logs, decision history, the preserved initial-submission snapshot, and the original assignment PDF.

`EVIDENCE_MAP.md` connects memo pages to output tables and calculation scripts. `PACKAGE_MANIFEST.csv` and `CODEX_HANDOFF_MANIFEST.csv` provide file hashes. The slide validation receipt is in `.slide_build/validation.json`; final slide renders are in `.slide_build/final`.

## Verification already completed

- Network-disabled rebuild passed.
- Twenty-eight explicit integrity and numerical checks passed.
- Frozen policy hash remained unchanged before and after evaluation and rebuild.
- The earlier recovery archive was extracted into a separate directory and rebuilt; all 48 numerical CSV/JSON outputs matched exactly.
- The initial-snapshot training analysis also rebuilt successfully.
- The finalized PowerPoint passed package integrity, layout, Arial font, editable-table, editable-chart and first-party import checks.
- All 13 slides and all report/guide pages were rendered and visually inspected.

Automated verification establishes computational consistency. It does not validate forecasts, prove investment skill, satisfy human contribution requirements, or establish compliance with the course AI policy.

## Information still required from the user/group

1. The actual course AI-use policy and any presentation rules, including presentation duration and required citation format.
2. The real names/student IDs of the 3-4 members, the substantive work each actually performs, another member's independent check, and each member's own critique.
3. The revised mandate released on 23 October 2026 at 16:00 Ho Chi Minh City time.

Do not invent any of these. `TEAM_COMPLETION.md` contains a proposed division of work, clearly labeled as a proposal. `MANDATE_REVISION.md` contains the exact procedure for processing the future mandate while preserving the original decision.

## Recovery and continuation commands

From the extracted `BFIN_Kappa` directory, create a Python 3.12 environment and install the pinned requirements once while online:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis.txt
```

Then reproduce the saved-data analysis without internet access:

```powershell
.\.venv\Scripts\python.exe analysis\rebuild.py
```

The rebuild regenerates processed data, numeric outputs, figures and PDFs, checks raw-file hashes, and verifies that the frozen policy remains unchanged. It does not redownload data.

The final editable PPTX is ready for use. Regenerating it requires the Codex bundled JavaScript presentation runtime. Read `README.md` and `analysis/build_slides.mjs`; set `KAPPA_NODE_MODULES`, `KAPPA_PYTHON`, `KAPPA_PRESENTATION_SKILL` and a new `KAPPA_PPTX_OUTPUT` if runtime locations differ. Never overwrite the existing finalized PPTX during experimentation.

## Next safe action

Ask the user for any still-missing external input only when needed. If the revised mandate has arrived, save it exactly as received, copy this completed original-mandate package to an immutable location, and follow `MANDATE_REVISION.md`. Keep the 31 December 2022 information cutoff and do not use 2023-2025 evaluation returns to redesign the original 2022 decision.

## 21 October 2026 continuation addendum

Read `ADVISORY_HANDOFF.md` and the latest `DECISION_LOG.md` entries before using the older working deliverables. Subsequent consultation rejected the analyst-added 10% per-stock / 30% direct-stock caps; they remain only in historical sensitivity snapshots. The user has now selected growth-sleeve drawdown as the primary 15% measure, with staged review signals. Market-wide difficulty meeting the real goal should prioritize preservation/risk management; apparent portfolio underperformance should be diagnosed before reconstruction.

New work: `analysis/mandate_preparedness.py`, `outputs/mandate_preparedness/`, and `advisory/2026-10-21/REVISED_MANDATE_AND_ADAPTIVE_IPS_VI.md`. Eighteen original/hypothetical mandate cases and 36 uncapped model combinations were computed from saved inputs. Separate evaluation attribution is diagnostic only. The current prepared English review draft is `advisory/2026-10-21/Kappa_Initial_Decision_Record_Review_Draft_20261021.md`; its page layout is not rendered/certified and older working PDFs/report-generator wording remain stale.

Numeric review deadlines, optional allocation bands, funding-gap triggers and crisis-expiry terms remain proposals. No actual revised mandate or submission receipt has been received. The frozen policy hash remains unchanged. A fee-inclusive initial whole-fund stress calculation now gives 17.61%, versus the earlier 17.53% excluding fees; the corresponding 15%-stress equity cap is $5.305m versus the old $5.332m. Preserve the original figures with their original definitions, and do not confuse a hypothetical whole-fund stress cap with the user's primary growth drawdown measure.

Update later on 21 October: the user explicitly approved the growth-sleeve 10/15/20 drawdown review ladder and selected an upside principle: at annual review, if the real 2030 goal remains funded after a -30% growth-sleeve stress, protect only the minimum needed and leave surplus under growth policy. The user selected CPI2.5% as the primary goal measure, HEPI3.0% as a separate education-cost stress, and fees of 5bp bonds/10bp equity in the base with a separate 0bp bonds/5bp ETF/10bp direct-stock sensitivity. See `policy/IPS_addendum_selected_drawdown_rules_2026-10-21.json` and `advisory/2026-10-21/PROPOSAL_AUDIT_AND_POLICY_QUESTIONS_VI.md`. These choices are proposed for the group's IPS, not trustee authorization or a guaranteed loss/goal outcome. Still open: pricing and permitted instrument for goal protection. The user confirmed full Beta face funding ($2.4m) for the 2024 payment, with Delta coupons kept separate and 0% base reinvestment; one/two-coupon variants are sensitivities only. The audit explains the one-versus-two-Delta-coupon difference between the user's sample proposal and `analysis/bonds.py`; do not combine those calculations without naming the source cash flows.

The deterministic CPI/HEPI and fee-schedule hurdle calculation is reproducible with `analysis/goal_inflation_sensitivity.py`; see `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`. It uses the selected full-Beta base and retained coupon cash at 0%, and makes no probability claim. CPI/HEPI and fee choices have now been answered by the user; do not keep them listed as open.

