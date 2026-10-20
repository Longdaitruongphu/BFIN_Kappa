# Advisory continuation: investment philosophy and board consultation

Updated 18 October 2026, Ho Chi Minh City time.

Read CODEX_HANDOFF.md for the preserved original case, then this file for the latest advisory work. The actual revised mandate has still not been supplied.

## Latest user direction

The user wants a professional board-style consultation, beginning with the mandatory assignment context, then developing vision, investment philosophy, hard and dynamic rules, liquidity, macro scenarios, USMV/VTI analysis, benchmarks, rebalancing and amendment procedures into a comprehensive white paper. The user favors protecting mandatory obligations and pursuing long-term growth. The user described 15% as a maximum stop-loss with possible systemic-crisis exceptions. This ambiguity needs resolution; no hard economic loss floor or new trading rule has been adopted.

The user is reconsidering the underlying reasoning and has not approved a new allocation, benchmark, inflation assumption, operating budget or terminal goal. Preserve the original analytical recommendation and adverse evaluation evidence.

On 18 October, the user asked to assign project work to four real team members although only one or two may have Python/technical skills, explain what AI has completed and the outputs, and provide beginner-friendly step-by-step process guidance. A Vietnamese internal runbook now covers role splits for four, two, or one Python users; duties and independent checks; AI-output status; a deadline plan for 22/23/29 October; and an explanation of the saved data/rebuild/CSV workflow.

## New artifacts

- advisory/2026-10-16/Kappa_Investment_White_Paper_Discussion_Draft.md: English discussion draft, mandate map, institutional analogies, macro source register, quantitative diagnostics, proposed governance and policy architecture, handoff and prompt audit.
- advisory/2026-10-16/Board_Consultation_Questions.md: 48 English questions in six rounds, with a decision-record template.
- advisory/2026-10-16/diagnose_policy.py: Python standard-library reproduction of additional diagnostics using frozen saved inputs only.
- Same folder: sharpe_decomposition.csv, conditional_returns.csv, frozen_factor_gap_bridge.csv, reserve_tradeoffs.csv, diagnostic_receipt.json.
- advisory/2026-10-18/PHAN_CONG_VA_RUNBOOK_NHOM_KAPPA_VI.md: internal, non-submission Vietnamese guide. Its relative links to the current official outputs were checked. Do not replace the English submitted artifacts with this guide.

## Verified findings

1. Evaluation Sharpe uses realized monthly excess returns. Annualized arithmetic excess return is 6.36% for USMV and 16.28% for VTI; excess-return volatility is 9.61% and 12.53%. Thus the return reduction outweighs volatility reduction. Reproduced saved Sharpe and cumulative returns within 1e-9.
2. A frozen-training FF3 bridge does not attribute the entire evaluation return gap to market beta. It has a large out-of-sample remainder. Exact historical sector/security attribution has not been established.
3. An illustrative constant required-return path leaves about 94.29% of remaining assets in equities just after the 2027 payment. A 30% equity shock would then cost about 28.29% of remaining assets. This is an illustration, not a forecast or backtest.
4. A USD 250,000 inception cash reserve raises required equity CAGR to about 5.00% if retained at zero interest through 2030, or 5.36% if fully consumed. Bonds remain unchanged and the existing equity entry fee is included.
5. All 208 original handoff-manifest file hashes still match after this work. Frozen policy SHA-256 remains 21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c. Original files were not changed and the full original analysis was not rerun.

## Current team/deadline status

The actual student names, Python-capable members, independent checks, course AI policy and proof of submission have not been supplied. `TEAM_COMPLETION.md` remains a proposed role split until members actually do and record the work. As of 18 October the initial-record deadline (22 October, 16:00 HCMC) and final deadline (29 October, 16:00 HCMC) are upcoming; the revised-mandate release is scheduled for 23 October, 16:00 HCMC. Do not state these were submitted or released without evidence.

## Evidence boundaries

The draft distinguishes the original 31 December 2022 information cutoff from contemporary October 2026 macro/institutional education. Post-cutoff sources must not justify the original allocation retrospectively. Sources are linked with access limits; several CalPERS/NBER pages were available only as official indexed text, and the full October 2026 WEO was not inspected. These are analyst research notes, not archived full raw publications.

Correct the earlier conversational wording: 68.48% is a conditional simulation goal frequency, not a calibrated success probability. A stop instruction does not guarantee a maximum loss. A 15% action threshold with time-limited exceptions is a proposal, not an approved rule.

## Next conversation

Conduct the first round of the board consultation in Vietnamese. Resolve institutional horizon, real-goal priority, loss threshold versus hard floor, tolerable shortfall, actual operating expenses and tolerance for benchmark underperformance. The complete English workbook supplies later questions. Keep artifacts in English.

After material choices are supplied, compare separately versioned scenarios against the original policy using identical evaluation conventions. Do not rewrite the frozen policy or tune to evaluation returns. Preserve missing course AI rules, actual member contributions and the revised mandate as external dependencies without inventing them.

## 20 October 2026 audit continuation

The user attached `D:\Downloads\BFIN_Part C.xlsx` and requested a complete assignment/data/model audit with a step-by-step check guide. The workbook was copied unchanged to `reference/role_c/BFIN_Part_C_original.xlsx`; the source and copy SHA-256 is `38fea4b64c09542f3f033c5ff9be8cfd18c14a0f181e187575092ccb9435881c`.

Read `advisory/2026-10-20/INDEPENDENT_ASSIGNMENT_AND_ROLE_C_AUDIT.md` for the English audit and `advisory/2026-10-20/HUONG_DAN_KIEM_TRA_TUNG_TASK_VI.md` for the Vietnamese internal step-by-step verification. Role C comparison details are in `outputs/role_c_audit/role_c_independent_audit.json`. The workbook's two return universes conflict, its advertised raw source file is absent from the supplied materials, rows 27–36 of its return-check sheet show false hard-coded PASSED statuses, its Optimization sheet is empty, and its regression is for the non-frozen universe. Its shared returns/factors and rounded regression coefficients mostly reconcile; do not call them fabricated.

New read-only scripts `analysis/verify_source_chain.py` and `analysis/verify_core_equations.py` passed. The first hashed 22 saved Yahoo/FF3 files and recomputed 1,320 returns plus 528 factor values from source bytes. The second independently checked all five bond YTM quote valuations, the full budget, mandatory payments, real goal, preference threshold and 36-month after-cost evaluation/Sharpe. Receipts are under `outputs/role_c_audit/`. A 20 October offline rebuild passed all 28 checks, the memo remained eight content pages plus references, and the original policy SHA-256 remained `21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c`. These audit additions are not in the older 16 October handoff ZIP or manifests. The original submitted-work status, revised mandate and actual student/AI policy inputs remain unverified.
