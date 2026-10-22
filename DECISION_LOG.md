# Decision log

| Date | Decision or issue | Evidence and disposition |
|---|---|---|
| 15 Oct 2026 | All deliverables in English | Explicit user preference |
| 15 Oct 2026 | Use the original case date and information cutoff | Assignment pages 1-2 require 31 Dec 2022 |
| 15 Oct 2026 | Select eight stocks across seven sectors plus VTI and USMV | Dated eligibility record; discretionary selection bias disclosed |
| 15 Oct 2026 | Use 96 training months, with a 60-month sensitivity | More observations while retaining the prescribed 2015-2022 range |
| 15 Oct 2026 | Ring-fence both payments separately | USD 5.644m quoted bond consideration; no equity sale needed |
| 15 Oct 2026 | Base growth choice USMV, benchmark VTI | A=4 certainty equivalent from training data; zero forecast alpha |
| 15 Oct 2026 | Freeze policy before separate evaluation retrieval | policy/frozen_policy.json and SHA-256 record |
| 15 Oct 2026 | Retain underperformance in 2023-2025 | USMV 37.33% cumulative versus VTI 82.56% after assumed entry cost |
| 15 Oct 2026 | Reject direct-stock optimizer as initial implementation | Small forecast utility gain, covariance sensitivity and concentration |
| 15 Oct 2026 | Document historical Sharpe definition | Frozen Eta proxy uses historical means minus a 4% case hurdle. A separate realized-RF audit is supplied; the frozen proxy is not silently changed |
| 15 Oct 2026 | Quantify all-bond alternative | USD 9.102m fixed nominal terminal cash; USD 7.471m real at assumed 2.5% inflation; USD 480,443 additional initial capital for the original goal |
| 15 Oct 2026 | User selects payment bonds plus USMV | Explicit user choice after seeing the all-bond trade-off; accepted investment risk and possible shortfall |
| Pending 23 Oct 2026 | Respond to revised mandate | Preserve original, create a separate scenario and compare quantified effects |

The initial decision record is prepared for the 22 October submission. No claim is made that it has been submitted. Later policy changes must be appended here, not substituted for the original decision.

## Course-model confirmation, 15 October 2026
The user confirmed FF3 is allowed. Retain CAPM and FF3. The numerical models and frozen allocation are unchanged.

## 20 October 2026 advisory confirmations (not a policy amendment)

The user confirmed the intended hierarchy as mandatory obligations first, then the $8m real 2030 goal; 2.5% inflation as base with sensitivity scenarios; provisional A=4 with sensitivity; and preserving the original 2022 USMV decision/VTI comparator while treating 2023–25 as separate evaluation. The user later proposed a staged 10% validation / 15% Investment Committee review / 20% trustee escalation ladder, plus immediate escalation for threatened obligations and a crisis exception limited to deferring discretionary action. These thresholds remain proposed; the denominator for “fund loss,” exception authority/expiry and exact implementation rules still require confirmation. These consultation notes do not amend the original frozen policy or represent approval of a revised mandate. See `advisory/2026-10-20/MANDATE_RELEASE_AND_POLICY_DECISIONS_VI.md` and `advisory/2026-10-20/LOSS_LIMITS_RESEARCH_AND_DESIGN_VI.md`.

## 21 October 2026 — user clarification and hypothetical mandate preparation

The user selected **growth sleeve as the primary 15% drawdown measure**, with graded signals for review. The user also clarified that broad-market difficulty reaching the goal should favor preservation and risk management, while portfolio underperformance may justify review/reconstruction after its cause is understood. These clarify the advisory design; they do not authorize rewriting the frozen 2022 allocation or changing the original evaluation.

Prepared 18 original/hypothetical cases and 36 uncapped model combinations in `outputs/mandate_preparedness/`; the Python script is `analysis/mandate_preparedness.py`. The actual revised mandate remains unreleased. All numerical response deadlines, allocation bands, funding-gap triggers and crisis expiry terms in the new playbook remain proposals. No 10% per-stock / 30% aggregate stock caps are applied to the new optimizer cases.

The new English review draft corrects stale working-record wording without changing the initial archive. It keeps the original annual, fixed-weight evaluation rule and removes later evaluation outcomes from the initial decision rationale. Older PDFs/report-generator wording have not yet been regenerated.

Calculation receipt verifies the original funding/hurdle, cash coverage, budget reconciliation, specified fee-inclusive stress limits, fully invested long-only weights and unchanged frozen policy hash. No new raw data downloads or probability forecasts are claimed.

The user explicitly approved inclusion of the growth-sleeve 10%/15%/20% review ladder in the group's proposed IPS. The primary metric is peak-to-trough unitized total-return growth-sleeve drawdown, with sleeve cash included and flows unitized; the rule requires review/escalation and never guarantees a 15% maximum loss. The addendum is `policy/IPS_addendum_selected_drawdown_rules_2026-10-21.json`. This is the user's policy choice for the project; trustee authorization and submission have not occurred.

New audit `advisory/2026-10-21/PROPOSAL_AUDIT_AND_POLICY_QUESTIONS_VI.md` checks Treasury/TIPS and Commonfund HEPI figures, identifies the one-versus-two-Delta-coupon mismatch in the sample text and saved code, keeps VaR separate from drawdown, and lays out an upside goal-funding/partial-protection process. Coupon funding and fee convention are selected for the proposal; concentration limits and execution details for the upside rule remain open. No new Yahoo or French data are imported.

The user selected an upside principle: at annual review, if the 2030 goal remains funded after a -30% growth-sleeve shock, protect only the minimum amount required for the goal and keep any surplus invested. Detailed implementation remains conditional on the permitted priced instrument, valuation date, costs and trustee authority. The user selected CPI 2.5% as the primary pass/fail goal measure and HEPI 3.0% as a separate education-cost stress; HEPI is not blended into or substituted for the primary measure. Research comparison across Yale, Harvard, Stanford and UC policies is recorded in the 21 October audit; payout smoothing rules are not applied to Kappa's two fixed obligations. The user confirmed full Beta funding ($2.4m face) for 2024, with Delta coupons kept separate as surplus cash at the existing 0% base reinvestment assumption. One- and two-coupon variants remain sensitivities only.

The CPI/HEPI selection has been added to the machine-readable IPS proposal as the primary CPI2.5% goal test and separate HEPI3.0% education-cost stress (trustee authorization pending). `analysis/goal_inflation_sensitivity.py` writes `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`; arithmetic assertions pass for the $9.747m/$10.134m nominal goals and 4.8365%/5.3743% required growth CAGRs. The frozen policy hash remains unchanged.

The user confirmed transaction-cost policy for the proposed IPS: 5bp bonds and 10bp equity are the base assumptions; 0bp bonds, 5bp ETFs and 10bp direct stocks are shown only as a separate sensitivity. The calculation script and CSV now compare both fee schedules. For the 100% USMV case the lower-friction schedule adds $5,992 to net growth capital and reduces required CAGR by about 0.0124 percentage points under either inflation scenario. Rates remain planning assumptions, not broker quotes.

## 21 October 2026 - Initial Decision Record rebuilt for 22 October

Rebuilt the two-page initial record from the verified pre-2023 package outputs. The record uses a SISF-style institutional factsheet hierarchy, with Invesco used only as a secondary layout reference; neither reference fund's performance or holdings entered Kappa's analysis. It now includes the full $12m allocation, the 8+2 candidate universe, 96-month formation window, VTI comparator, sample A=4 challenger, A=2/4/6/8 sensitivity, CPI/HEPI goal convention, user-approved proposed 10/15/20 growth-sleeve review ladder, annual upside test, and frozen 2023-25 evaluation rule. The full 2023-25 outcomes and final memo-only evidence are explicitly reserved for the later submission. `submission_2026-10-22/submission_manifest.json` was updated for the new generator, PDF and editable source. The raw data and `policy/frozen_policy.json` were not changed; the prepared record is not represented as submitted or trustee-authorized.

Later design revision on 21 October: at the user's request, replaced the card-heavy layout with a SISF-style title band, main column and facts sidebar. Removed explanatory sentences from table cells; used 5.5pt superscript definitions, single-line italic 7.5pt sources, and five one-line 7.5pt glossary definitions at the foot of page 2. Added a vector utility-versus-risk-aversion chart using the existing sensitivity CSV. Goldman Sachs's notes and glossary were inspected; the supplied Morgan Stanley and Lazard URLs were inaccessible. This revision changes presentation and wording, while preserving all numerical inputs, selected assumptions, proposed policy and initial holdings. Both pages were rendered and inspected, and actual PDF typography was checked independently.
