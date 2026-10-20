# Kappa Foundation assignment package

## Interactive surplus portfolio lab

**Desktop v2:** double-click `OPEN_PORTFOLIO_LAB.cmd`, or use the Python command below. The redesigned interface has a resizable sidebar, Vietnamese hover explanations, background calculation, a pinned-baseline comparison, custom weights/shocks, eight chart types and selected-portfolio PNG/SVG/CSV exports. No additional packages are required in the existing environment.

Read the detailed Vietnamese walkthrough: [Portfolio Lab user guide](advisory/2026-10-20/PORTFOLIO_LAB_USER_GUIDE_VI.md). Fresh default charts/settings are in `outputs/figures/portfolio_lab_v2/`. The old radar exports had an inverted drawdown direction; v2 corrects it. Use the new figures or export again.

Run the v2 numerical and Tk construction checks:

```powershell
.venv\Scripts\python.exe analysis\test_portfolio_lab_v2.py
```

These graphs describe the **equity growth sleeve**, not full-fund loss or a guaranteed 15% loss ceiling. The CAL is illustrative; cash is not an optimized holding in this lab. The historical-cost convention excludes entry/exit costs and includes scheduled rebalances only. See the guide before comparing with older full-fund or entry-cost-adjusted outputs.

The no-extra-weight-cap comparison tool is `analysis/interactive_surplus_portfolio_lab.py`. It reads saved local inputs, keeps 2015–2022 estimation separate from 2023–2025 evaluation, and lets the user change CAPM/FF3 assumptions, covariance basis, risk aversion, inflation and optional concentration limits. The 10% per-stock and 30% aggregate-stock limits in the older `analysis/config.json` are analyst-added working assumptions, not requirements from the assignment or confirmed user policy. Leave their controls blank for the no-extra-cap baseline.

Run the interactive checkbox and graph exporter:

```powershell
.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py
```

Run calculations and chart smoke checks, or export the default no-extra-cap example figures and metrics:

```powershell
.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py --self-test
.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py --export-defaults
```

The prior static surplus comparisons remain capped scenario sensitivities. See `advisory/2026-10-20/MODEL_CHOICES_AND_CONSTRAINT_CORRECTION_VI.md` before interpreting them.

Main recommendation confirmed by the user: dedicated payment bonds plus USMV. All amounts are USD. The case date is 31 December 2022. The package contains an analysis of the **original mandate**, not the still-unreleased 23 October 2026 revision.

## Read these first

0. `PROJECT_MAP.md`: current folder structure, canonical files, and the dated verification inventory.
1. `deliverables/Kappa_Requirements_and_Data_Guide.pdf`: requirements, deadlines, source checks and step-by-step data workflow.
2. `deliverables/Kappa_Committee_Memo.pdf`: eight content pages plus one reference page.
3. `deliverables/Kappa_Initial_Decision_Record.pdf`: two-page prepared record for 22 October.
4. `deliverables/Kappa_Committee_Presentation.pdf` and `.pptx`: presentation and editable slides.
5. `TEAM_COMPLETION.md`: information and genuine student work still required.
6. `CHECKPOINT.md`: saved progress, confirmed decisions and recovery instructions. `EVIDENCE_MAP.md` links each memo page to its calculations.
7. `advisory/2026-10-20/INDEPENDENT_ASSIGNMENT_AND_ROLE_C_AUDIT.md`: independent source, equation and Role C workbook review; its Vietnamese check-by-check manual is beside it.
8. `advisory/2026-10-20/SECOND_PASS_SOURCE_AND_STRUCTURE_AUDIT.md`: source, factor/portfolio and current-folder inventory reconciliation.

## Quick Start (Hướng dẫn tải về và chạy thử)

### 1. Clone repository
```bash
git clone https://github.com/Longdaitruongphu/BFIN_Kappa.git
cd BFIN_Kappa
```

### 2. Cài đặt môi trường (Khuyến nghị Python 3.12)

**Trên Windows (PowerShell):**
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis.txt
```

**Trên macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-analysis.txt
```

### 3. Tái lập và chạy kiểm thử phân tích (Rebuild Analysis)

Tái lập toàn bộ dữ liệu, bảng tính và báo cáo hoàn toàn offline từ nguồn lưu trữ:

**Trên Windows (PowerShell):**
```powershell
.\.venv\Scripts\python.exe analysis\rebuild.py
```

**Trên macOS / Linux:**
```bash
python analysis/rebuild.py
```

The rebuild blocks network connections in its own process. It regenerates processed data, numerical outputs, figures, the memo, initial record and data guide, then checks raw-file hashes and the frozen policy. It does **not** download new data or overwrite the original policy. The current slide export is supplied as editable PPTX; `analysis/build_slides.mjs` regenerates it in the Codex bundled presentation runtime. A standard Python environment is sufficient to reproduce all analysis numbers and the report PDFs.

The delivered archive was extracted into another folder and successfully rebuilt offline using the installed pinned environment. All 48 numerical output files matched exactly. The initial snapshot's training analysis also ran successfully. See `logs/archive_rebuild_receipt.json`. This is not a claim that a fresh package installation on every operating system has been tested.

Presentation regeneration requires the supplied JavaScript artifact runtime and its presentation helper package. Set `KAPPA_NODE_MODULES`, `KAPPA_PYTHON` and `KAPPA_PRESENTATION_SKILL` if their paths differ. Set `KAPPA_PPTX_OUTPUT` to a new output filename when regenerating, because the finalizer preserves existing finalized files. The supplied PPTX is directly editable in PowerPoint without these authoring dependencies.

## Folder map

| Folder | Purpose |
|---|---|
| `analysis` | Retrieval, analysis, stress tests, report generation and offline rebuild |
| `data/raw/train` | Untransformed yfinance tables and original French ZIP for training |
| `data/raw/eval` | Separate evaluation downloads |
| `data/raw/supporting` | Official methodological pages, source register and eligibility evidence notes |
| `data/processed` | Derived monthly prices, returns, dates and factor tables |
| `policy` | Frozen original weights, assumptions, hash and user decision record |
| `outputs/tables` | Named numerical evidence used in the memo and slides |
| `outputs/figures` | Code-generated figures |
| `logs` | Execution and audit records |
| `initial_submission` | Preserved prepared initial decision record and dated source record |
| `deliverables` | Documents and presentation |

## Status and limits

- Both required market-data sources were downloaded successfully in Python. No market returns were invented or silently filled.
- Eight stock candidates span seven sectors, plus two distinct equity ETFs.
- Training has 96 common months; evaluation has 36 common months.
- Direct SEC downloads returned HTTP 403. Eligibility was checked using official SEC documents available through web retrieval. The record distinguishes brief evidence notes from fully downloaded source documents. Do not represent the notes as full raw SEC filings.
- The use of current vendor histories and a discretionary surviving universe makes this a retrospective case, not a genuinely unseen investment experiment.
- The 23 October revised mandate, course AI policy and actual student contributions are outstanding. The archive is not a final course submission until those items are addressed.

Do not edit raw files, replace the frozen policy, claim the prepared initial record has been submitted, or invent student contributions.
