# Checkpoint: original-case and Role C audit, 20 October 2026

Original frozen policy preserved: SHA-256 `21b4ec3fb864144e7b56e54c668ebaed9c96d5a1771564b50c892700978c9f5c`. Role C attachment preserved: SHA-256 `38fea4b64c09542f3f033c5ff9be8cfd18c14a0f181e187575092ccb9435881c`. The authoritative original assignment is `reference/BFIN-WS2026-Group_Assignment.pdf`; the attachment is analyst output, not a mandate.

The offline rebuild completed successfully and `outputs/tables/reproduction_checks.csv` contains 28 passed checks. Separate independent scripts and receipts:

- `analysis/verify_source_chain.py` → `outputs/role_c_audit/source_chain_receipt.json`: 22 source hashes, 1,320 monthly returns, 528 FF3 values, all passed.
- `analysis/verify_core_equations.py` → `outputs/role_c_audit/core_equations_receipt.json`: budget, five bond YTM quote valuations, cash-flow obligations, 2030 target, preference threshold and evaluation metrics, all passed.
- `analysis/audit_role_c.py` → `outputs/role_c_audit/role_c_independent_audit.json`: Role C return/factor/OLS reconciliation and source/checking gaps. It ran with the system Python containing openpyxl; the original analysis venv does not include openpyxl.

Main finding: Role C workbook has useful reconciled numerical data but cannot be merged as independent source evidence or optimization for the frozen recommendation. See `advisory/2026-10-20/INDEPENDENT_ASSIGNMENT_AND_ROLE_C_AUDIT.md` and Vietnamese runbook in the same folder.

Still pending actual course AI-use/presentation rules, real group checks/contributions, proof of initial submission, and the revised mandate due 23 October. Keep all submitted artifacts English. Preserve this checkpoint and the original policy; analyze the future mandate in a separate scenario.
