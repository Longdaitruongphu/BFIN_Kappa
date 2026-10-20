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
