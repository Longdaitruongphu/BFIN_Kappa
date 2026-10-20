# Recovery checkpoint

Updated 16 October 2026, Ho Chi Minh City time.

## Confirmed user decisions
- All deliverables in English.
- Main recommendation: payment bonds plus USMV, pursuing USD 8m real terminal assets while accepting investment risk and possible shortfall.
- Save checkpoints throughout the work.
- FF3 is allowed in Lecture 7, confirmed by the user.

## Completed and saved
- Actual Yahoo/yfinance daily downloads and original Kenneth French factor ZIPs, with manifests, settings, package versions and file hashes.
- 96 training months and 36 separate evaluation months.
- Bond funding, curve calibration, exact stress repricing, portfolio optimization, factor regressions, frozen evaluation and goal sensitivity.
- Nine-page committee memo (8 content plus 1 references), two-page initial record, and seven-page detailed requirements and data guide. Editable text versions included.
- Network-disabled rebuild passed with 28 numerical checks. Receipt: logs/offline_rebuild_receipt.json.
- Frozen policy SHA-256: 21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c. Never overwrite it.
- Thirteen-slide editable PowerPoint and PDF saved in deliverables/. Every final slide was rendered from the finalized PPTX and visually reviewed. Native tables and both editable chart workbooks passed structural validation. No claim of opening in native PowerPoint is made.
- Initial prepared snapshot preserved under initial_submission/, with its own source record, working training code, raw training files and snapshot_manifest.json.
- EVIDENCE_MAP.md connects memo pages, source records and calculations.
- The ZIP was extracted into a separate location and rebuilt successfully. All 48 numerical output files matched exactly. Initial-snapshot training also ran successfully. Receipt: logs/archive_rebuild_receipt.json.
- Recovery archive: ../Kappa_Original_Mandate_Package_2026-10-15.zip. Its adjacent receipt records the archive hash. PACKAGE_MANIFEST.csv records included-file hashes.

## Current status
The original-mandate analytical package is complete. No required original-case analysis remains unfinished. The final course submission still needs the external information and genuine group work listed below. Do not describe the package as a completed response to the unreleased revised mandate.

## Codex handoff
- `CODEX_HANDOFF.md` is the single start-here document for a new Codex session.
- `../Kappa_Codex_Handoff_2026-10-16.zip` is the self-contained handoff archive requested by the user.
- The ZIP includes the assignment, deliverables, raw and processed data, analysis and retrieval code, environment pins, policy freeze, initial snapshot, final slide renders, validation receipt, logs, evidence map and file-hash manifest.
- The draft ZIP was extracted to a separate directory. All 206 manifest hashes passed, the offline rebuild passed all 28 explicit checks, the memo remained 9 pages, the initial record remained 2 pages, the guide remained 7 pages, and the frozen policy hash did not change. The result is recorded in `logs/codex_handoff_verification.json`.

## External information pending
- Actual course AI policy and any additional presentation rules.
- Real group members, contributions, independent checks and critiques.
- Revised mandate scheduled for 23 October 2026 at 16:00 HCMC, not yet available. Do not invent it.

## Recovery procedure
Read README.md, DECISION_LOG.md and TEAM_COMPLETION.md. Rebuild saved-data analysis with `python analysis/rebuild.py` after installing requirements-analysis.txt. No new retrieval is needed. Preserve sources/, initial_submission/ and the original frozen policy. When the user supplies missing course details or the revised mandate, make separate recorded changes and update the memo, slides and archive. Preserve this checkpoint in checkpoint_history/.
