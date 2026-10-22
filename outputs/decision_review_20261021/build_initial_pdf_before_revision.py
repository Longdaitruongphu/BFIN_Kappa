"""Typeset the approved-scope initial decision record (exactly two A4 pages)."""
from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "outputs/initial_decision_rebuild.json").read_text(encoding="utf-8"))
DEST = ROOT / "deliverables/Kappa_Initial_Decision_Record_22Oct2026.pdf"
DEST.parent.mkdir(exist_ok=True)
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Segoe", str(FONT_DIR / "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("Segoe-Bold", str(FONT_DIR / "segoeuib.ttf")))
pdfmetrics.registerFontFamily("Segoe", normal="Segoe", bold="Segoe-Bold")

NAVY = colors.HexColor("#163044")
TEAL = colors.HexColor("#087E83")
INK = colors.HexColor("#18313D")
GREY = colors.HexColor("#576B76")
LIGHT = colors.HexColor("#F1F6F6")
LINE = colors.HexColor("#D6E2E4")
ORANGE = colors.HexColor("#B86631")
W, H = A4
L, R = 42, W - 42
WIDTH = R - L

styles = {
    "body": ParagraphStyle("body", fontName="Segoe", fontSize=9.0, leading=12.2, textColor=INK),
    "small": ParagraphStyle("small", fontName="Segoe", fontSize=8.0, leading=10.5, textColor=GREY),
    "table": ParagraphStyle("table", fontName="Segoe", fontSize=8.4, leading=11.0, textColor=INK),
    "tablebold": ParagraphStyle("tablebold", fontName="Segoe-Bold", fontSize=8.4, leading=11.0, textColor=NAVY),
    "right": ParagraphStyle("right", fontName="Segoe", fontSize=8.4, leading=11.0, textColor=INK, alignment=TA_RIGHT),
    "rightbold": ParagraphStyle("rightbold", fontName="Segoe-Bold", fontSize=8.4, leading=11.0, textColor=NAVY, alignment=TA_RIGHT),
    "whitehead": ParagraphStyle("whitehead", fontName="Segoe-Bold", fontSize=8.4, leading=11.0, textColor=colors.white),
    "whiteheadright": ParagraphStyle("whiteheadright", fontName="Segoe-Bold", fontSize=8.4, leading=11.0, textColor=colors.white, alignment=TA_RIGHT),
}


def clean_dashes(txt: str) -> str:
    """Keep PDF punctuation compatible with the artifact rendering contract."""
    for mark in ("\u2011", "\u2012", "\u2013", "\u2014", "\u2212"):
        txt = txt.replace(mark, "-")
    return txt


def para(c: canvas.Canvas, txt: str, y: float, width: float = WIDTH, kind: str = "body", x: float = L) -> float:
    p = Paragraph(clean_dashes(txt), styles[kind]); _, h = p.wrap(width, 1000)
    p.drawOn(c, x, y - h)
    return y - h


def section(c: canvas.Canvas, label: str, y: float) -> float:
    y -= 12
    c.setFillColor(TEAL); c.setFont("Segoe-Bold", 9.0); c.drawString(L, y, label.upper())
    c.setStrokeColor(LINE); c.setLineWidth(.65); c.line(L, y - 4, R, y - 4)
    return y - 11


def table(c: canvas.Canvas, rows: list[list[str]], widths: list[float], y: float,
          header: bool = True, right_cols: tuple[int, ...] = ()) -> float:
    styled = []
    for row_i, row in enumerate(rows):
        cells = []
        for col_i, text in enumerate(row):
            if row_i == 0 and header:
                k = "whiteheadright" if col_i in right_cols else "whitehead"
            elif col_i in right_cols:
                k = "rightbold" if (row_i == 0 and header) or (row_i == len(rows)-1 and text.startswith("$")) else "right"
            else:
                k = "tablebold" if row_i == 0 and header else "table"
            cells.append(Paragraph(clean_dashes(text), styles[k]))
        styled.append(cells)
    t = Table(styled, colWidths=widths, hAlign="LEFT")
    commands = [
        ("VALIGN", (0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),4), ("BOTTOMPADDING",(0,0),(-1,-1),4),
        ("LINEBELOW",(0,-1),(-1,-1),.65,LINE),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ]
    if header:
        commands += [("BACKGROUND",(0,0),(-1,0),NAVY),
                     ("TEXTCOLOR",(0,0),(-1,0),colors.white)]
    t.setStyle(TableStyle(commands))
    _, h = t.wrap(WIDTH, 1000); t.drawOn(c, L, y-h)
    return y-h


def page_head(c: canvas.Canvas, page: int, title: str, subtitle: str) -> float:
    c.setFillColor(NAVY); c.rect(0, H-9, W, 9, fill=1, stroke=0)
    c.setFillColor(TEAL); c.setFont("Segoe-Bold", 8.1)
    c.drawString(L, H-33, "KAPPA FOUNDATION  /  BOARD DECISION MATERIAL")
    c.setFillColor(GREY); c.setFont("Segoe", 7.4)
    c.drawRightString(R, H-33, "22 OCT 2026  ·  INITIAL RECORD")
    c.setFillColor(NAVY); c.setFont("Segoe-Bold", 18)
    c.drawString(L, H-61, title)
    c.setFillColor(GREY); c.setFont("Segoe", 8.5)
    c.drawString(L, H-76, subtitle)
    c.setStrokeColor(LINE); c.line(L, H-85, R, H-85)
    c.setStrokeColor(LINE); c.line(L, 36, R, 36)
    c.setFillColor(GREY); c.setFont("Segoe", 7.1)
    c.drawString(L, 24, "Prepared recommendation  |  Case information through 31 Dec 2022  |  USD")
    c.drawRightString(R, 24, f"{page} / 2")
    return H-99


def main() -> None:
    c = canvas.Canvas(str(DEST), pagesize=A4, pageCompression=1)
    c.setTitle("Kappa Foundation - Initial Decision Record - 22 October 2026")
    c.setAuthor("Kappa Foundation independent investment team - prepared draft")
    y = page_head(c, 1, "Initial decision record", "Recommendation to trustees  ·  Decision date 31 Dec 2022  ·  Prepared for 22 Oct deadline")
    c.setFillColor(LIGHT); c.roundRect(L, y-62, WIDTH, 59, 6, stroke=0, fill=1)
    c.setFillColor(TEAL); c.rect(L, y-62, 3, 59, fill=1, stroke=0)
    y_box = y-11
    y_box = para(c, "<b>DECISION  /  Fund the two fixed commitments with case bonds, then invest the residual in USMV.</b>", y_box, WIDTH-27, "body", L+13)
    para(c, "Payment security comes first; the USD 8m December-2022 purchasing-power target for 2030 is an objective, not a promise. Review risk on the growth sleeve and payment coverage separately.", y_box-4, WIDTH-27, "small", L+13)
    y -= 69

    y = section(c, "01  Capital and obligations", y)
    y = table(c, [
        ["Initial use", "Case instrument / purpose", "USD", "% of fund"],
        ["2024 commitment", "2,400 Beta zeros; USD 2.4m face", "$2,214,672.00", "18.456%"],
        ["2027 commitment", "3,478.26087 Delta; final USD 3.6m", "$3,429,808.70", "28.582%"],
        ["Growth sleeve", "USMV, after entry friction", "$6,346,350.71", "52.886%"],
        ["Execution costs", "5bp bonds + 10bp equity", "$9,168.59", "0.076%"],
        ["Total initial cash", "Fully allocated", "$12,000,000.00", "100.000%"],
    ], [113, 215, 103, WIDTH-431], y, right_cols=(2,3))
    y -= 7
    y = para(c, "<b>Coverage:</b> Beta pays USD 2.4m on 31 Dec 2024; Delta's last coupon plus principal pays USD 3.6m on 31 Dec 2027. Its four earlier coupons total USD 486,956.52 and stay in cash at 0% base reinvestment. No equity sale or assumed bond resale price funds either obligation.", y)

    y = section(c, "02  Candidate set, horizon and comparator", y)
    y = para(c, "<b>Eight US stocks / seven sectors:</b> AAPL, MSFT (technology); JPM (financials); JNJ (health care); PG (staples); XOM (energy); CAT (industrials); NEE (utilities). <b>Two distinct US equity ETFs:</b> USMV (US minimum-volatility factor) and VTI (broad US market). They are candidates, not required holdings; pre-2023 SEC eligibility references are in the data record.", y)
    y -= 4
    y = para(c, "<b>Estimation:</b> 96 common monthly adjusted-price returns, Jan 2015–Dec 2022; Dec 2014 closes supply the first return baseline. Test 60 months as robustness later. <b>Investable growth comparator:</b> 100% VTI, frozen on the same 2022 decision date and evaluated separately from the case bonds.", y)

    y = section(c, "03  Growth portfolio: selection and rejected alternative", y)
    y = para(c, "<b>Selected weights inside the growth sleeve:</b> USMV 100% (USD 6,346,350.71); VTI 0%; eight direct-stock candidates 0%. VTI is the frozen, investable comparator, not a second holding. The stock list is a research universe: the initial allocation does not depend on repeating any individual stock's historical Sharpe ratio or estimated alpha.", y)
    y -= 5
    y = table(c, [
        ["2022-input comparison", "USMV · recommended", "VTI · credible alternative"],
        ["CAPM annual return scenario", "7.14%", "8.45%"],
        ["2015–22 annualized volatility", "12.84%", "16.31%"],
        ["Utility at A = 4", "3.84%", "3.13%"],
    ], [208, 149, WIDTH-357], y)
    y -= 6
    y = para(c, "<b>Decision logic:</b> USMV spreads the sleeve across US stocks with a minimum-volatility mandate and has lower 2015-22 modeled volatility than broad-market VTI. Utility = expected annual return − ½A × annual variance. A = 4 is <b>provisional</b>; VTI ranks higher at A = 2, USMV at A = 4/6/8, with a two-ETF crossover near A = 2.58. VTI is a credible rejected growth allocation because of its higher forecast return. USMV can still lose more than 15%; its arithmetic forecast is not a guarantee of the required eight-year CAGR or a global portfolio optimum.", y)
    if y < 44: raise RuntimeError(f"Page 1 overflows: y={y:.1f}")
    c.showPage()

    y = page_head(c, 2, "Policy, evidence and controls", "Only the 2022 information set supports the initial decision  ·  All thresholds below are proposals")
    y = section(c, "04  Material assumptions and limits", y)
    y = table(c, [
        ["Topic", "Proposed convention / decision use"],
        ["Real goal", "CPI planning 2.5%: 2030 nominal USD 9.747m; USMV sleeve needs 4.84% nominal CAGR with coupon cash at 0%. Education-cost 3.0% stress: USD 10.134m / 5.37% hurdle. Do not blend CPI and HEPI."],
        ["Return & risk", "CAPM scenario: annual RF 4%, market premium 4.5%, forecast alpha 0; monthly French RF is used for historical excess returns. FF3 explains historical exposures, not a factor-premium forecast. Compare A = 2, 4, 6, 8."],
        ["Instruments / costs", "Case permits cash, its five bonds, US common stocks and US equity ETFs; no leverage, shorts or derivatives. Fractional bonds allowed. Base friction: 5bp bonds, 10bp equity; 0bp bonds / 5bp ETFs is a sensitivity, not the base."],
    ], [109, WIDTH-109], y)
    y -= 5
    y = para(c, "<b>No additional stock-position cap has been approved.</b> The two mandatory nominal payments are covered by contractual cash flows under the case's default-free assumption; the 2030 real goal, modeled returns and a maximum loss cannot be guaranteed.", y, kind="small")

    y = section(c, "05  Monitoring, downside and upside", y)
    y = para(c, "Primary signal: <b>unitized growth-sleeve total-return drawdown</b> from its running high; adjust external transfers, include sleeve cash and do not reset the high-water mark after switching assets. Track whole-fund value, dated bond-payment coverage and 2030 real-goal feasibility as separate measures. Monthly historical data support month-end signals only.", y)
    y -= 4
    y = table(c, [
        ["Signal", "Required governance response · proposed, not a price stop"],
        ["10% drawdown", "Within 2 business days, validate data, payment coverage and stress. No automatic transaction."],
        ["15% drawdown", "Committee meets within 5 business days; record a hold, authorized rebalance or prospective policy recommendation."],
        ["20% drawdown", "Notify trustees same/next business day; pause discretionary risk increases. Do not force an equity sale."],
        ["Payment gap · any level", "Escalate immediately with a funded corrective plan. Crisis exceptions cannot weaken due-payment coverage."],
    ], [119, WIDTH-119], y)
    y -= 5
    y = para(c, "<b>Upside review:</b> annually recheck liabilities, the CPI goal and a −30% growth-sleeve shock. If the goal remains fundable after that stress, trustees may prospectively protect only the minimum required amount in an eligible, actually priced asset matched to 2030; keep surplus invested. No fixed-gain sale or automatic spending increase. This requires a documented forward decision, not a rewrite of the frozen backtest.", y)

    y = section(c, "06  Frozen evaluation rule and decision control", y)
    y = para(c, "Freeze USMV and VTI at 31 Dec 2022. For Jan 2023–Dec 2025, compare the growth sleeve and benchmark using a declared annual post-December-return reset to inception weights, <b>without re-estimating</b> parameters; a one-ETF sleeve normally has no internal trade. Report costs and unfavorable evidence. Review payment coverage each year; changed mandates, assumptions or allocation need a dated before/after analysis and prospective effective date. Do not reset payment bonds to an initial percentage after they pay.", y)

    y = section(c, "07  Reproduce and inspect the dated data record", y)
    y = para(c, "<b>1.</b> Read <font color='#087E83'>data/DATA_RECORD.md</font> and <font color='#087E83'>data/raw/retrieval_manifest.jsonl</font> for source URLs, UTC timestamps, request settings, package versions and SHA-256. <b>2.</b> Install <font color='#087E83'>requirements-analysis.txt</font>, then run <font color='#087E83'>python analysis/run_initial.py</font> from the archive root, offline. <b>3.</b> Inspect <font color='#087E83'>initial_decision_rebuild.json</font> (budget/goal), <font color='#087E83'>growth_portfolio_weights.csv</font> (holdings), <font color='#087E83'>candidate_statistics.csv</font> (CAPM) and <font color='#087E83'>risk_preference.csv</font> (A sensitivity), all in <font color='#087E83'>outputs/</font>. Online retrieval: <font color='#087E83'>analysis/retrieve_data.py --phase train</font>.", y, kind="small")
    y -= 4
    y = para(c, "<b>Source caveat:</b> saved Yahoo/French downloads were retrieved in Oct 2026 and may contain revised history; this is a retrospective case, not a genuinely unseen 2022 trade. Ten Yahoo raw CSVs + one French ZIP passed saved-byte hash and 96-month checks. SEC filing checks are dated links, not locally saved SEC bytes (direct downloads returned HTTP 403). The 2023–25 evaluation is outside this initial record.", y, kind="small")
    y -= 4
    y = para(c, "<b>Scope of this two-page record:</b> detailed bond duration/curve shocks, sample-versus-single-index optimization, multifactor alpha tests and 2023-25 outcomes belong in the final committee memo; none is claimed as completed by this initial record.", y, kind="small")
    y -= 5
    y = para(c, "<b>Practice reference:</b> University of California, <i>General Endowment Pool Investment Policy Statement</i> (2012), pp. 3–4, 7–8: mission, fiduciary oversight, benchmarks and reporting. Kappa's numerical rules are case-specific proposals. https://www.ucop.edu/investment-office/_files/invpol/GEP_IPS.pdf", y, kind="small")
    if y < 44: raise RuntimeError(f"Page 2 overflows: y={y:.1f}")
    c.showPage(); c.save()
    assert len(PdfReader(str(DEST)).pages) == 2
    print(f"PDF complete: {DEST} | 2 pages | bottom clearance p2={y:.1f}pt")


if __name__ == "__main__":
    main()
