"""Build the two-page Kappa Initial Decision Record from saved, verified outputs.

Run from submission_2026-10-22 after `python analysis/run_initial.py`.
The PDF build is offline and reads only named local outputs and the proposed policy.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables/Kappa_Initial_Decision_Record_22Oct2026.pdf"
DATA = json.loads((ROOT / "outputs/initial_decision_rebuild.json").read_text(encoding="utf-8"))
CHALLENGER = json.loads((ROOT / "outputs/sample_utility_robustness.json").read_text(encoding="utf-8"))
RISK = list(csv.DictReader((ROOT / "outputs/risk_preference.csv").open(encoding="utf-8", newline="")))
FONT_DIR = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("Segoe", str(FONT_DIR / "segoeui.ttf")))
pdfmetrics.registerFont(TTFont("Segoe-Bold", str(FONT_DIR / "segoeuib.ttf")))
pdfmetrics.registerFont(TTFont("Segoe-Italic", str(FONT_DIR / "segoeuii.ttf")))
pdfmetrics.registerFontFamily("Segoe", normal="Segoe", bold="Segoe-Bold", italic="Segoe-Italic")

W, H = A4
M = 38
CW = W - 2 * M
NAVY = colors.HexColor("#063B67")
BLUE = colors.HexColor("#0078B8")
CYAN = colors.HexColor("#23B7C9")
INK = colors.HexColor("#182B3A")
MUTED = colors.HexColor("#596B79")
LINE = colors.HexColor("#C9D6DF")
PALE = colors.HexColor("#EEF5F8")
PALE_BLUE = colors.HexColor("#D9EAF4")
PALE_CYAN = colors.HexColor("#E5F6F6")
WHITE = colors.white

ST = {
    "body": ParagraphStyle("body", fontName="Segoe", fontSize=8.65, leading=11.5, textColor=INK),
    "body_small": ParagraphStyle("body_small", fontName="Segoe", fontSize=7.8, leading=10.1, textColor=INK),
    "muted": ParagraphStyle("muted", fontName="Segoe", fontSize=7.5, leading=9.7, textColor=MUTED),
    "cell": ParagraphStyle("cell", fontName="Segoe", fontSize=7.8, leading=9.7, textColor=INK),
    "cellbold": ParagraphStyle("cellbold", fontName="Segoe-Bold", fontSize=7.8, leading=9.7, textColor=INK),
    "right": ParagraphStyle("right", fontName="Segoe", fontSize=7.8, leading=9.7, textColor=INK, alignment=TA_RIGHT),
    "center": ParagraphStyle("center", fontName="Segoe", fontSize=7.8, leading=9.7, textColor=INK, alignment=TA_CENTER),
    "white": ParagraphStyle("white", fontName="Segoe", fontSize=8.2, leading=10.3, textColor=WHITE),
}


def para(c, text, x, top, width, style="body"):
    p = Paragraph(text, ST[style])
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top - h)
    return top - h


def header(c, page, kicker, title, subtitle):
    c.setFillColor(NAVY)
    c.rect(0, H - 56, W, 56, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.rect(0, H - 56, 8, 56, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Segoe-Bold", 9)
    c.drawString(M, H - 22, "KAPPA FOUNDATION  |  INITIAL DECISION RECORD")
    c.setFont("Segoe", 7.3)
    c.drawRightString(W - M, H - 22, "COMMITTEE RECORD  -  22 OCTOBER 2026")
    c.setFont("Segoe-Bold", 7.4)
    c.setFillColor(BLUE)
    c.drawString(M, H - 78, kicker.upper())
    c.setFillColor(INK)
    c.setFont("Segoe-Bold", 19)
    c.drawString(M, H - 103, title)
    c.setFillColor(MUTED)
    c.setFont("Segoe", 8.1)
    c.drawString(M, H - 118, subtitle)
    c.setStrokeColor(LINE)
    c.setLineWidth(.6)
    c.line(M, 32, W - M, 32)
    c.setFillColor(MUTED)
    c.setFont("Segoe", 7)
    c.drawString(M, 20, "Portfolio decision and market information cutoff: 31 December 2022  |  USD")
    c.drawRightString(W - M, 20, f"{page} / 2")
    return H - 133


def section(c, title, x, top, width=CW):
    c.setFillColor(NAVY)
    c.setFont("Segoe-Bold", 10)
    c.drawString(x, top - 9, title)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.line(x, top - 15, x + width, top - 15)
    return top - 22


def draw_table(c, rows, widths, x, top, *, header=True, row_fills=(), pad=4, font_style=True):
    matrix = []
    for ri, row in enumerate(rows):
        line = []
        for ci, value in enumerate(row):
            if isinstance(value, Paragraph):
                line.append(value)
            else:
                sty = "white" if header and ri == 0 else ("cellbold" if ci == 0 and ri > 0 else "cell")
                if isinstance(value, (int, float)):
                    sty = "right"
                line.append(Paragraph(str(value), ST[sty]))
        matrix.append(line)
    t = Table(matrix, colWidths=widths, hAlign="LEFT")
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), pad),
        ("BOTTOMPADDING", (0, 0), (-1, -1), pad),
        ("LINEBELOW", (0, -1), (-1, -1), .55, LINE),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("LINEBELOW", (0, 0), (-1, 0), .6, NAVY)]
    for ri, fill in row_fills:
        cmds.append(("BACKGROUND", (0, ri), (-1, ri), fill))
    t.setStyle(TableStyle(cmds))
    _, h = t.wrap(sum(widths), 1000)
    t.drawOn(c, x, top - h)
    return top - h


def metric_card(c, x, y, w, h, label, value, note, color=BLUE):
    c.setFillColor(PALE)
    c.roundRect(x, y, w, h, 5, fill=1, stroke=0)
    c.setFillColor(color)
    c.rect(x, y, 3, h, fill=1, stroke=0)
    c.setFillColor(MUTED)
    c.setFont("Segoe-Bold", 7)
    c.drawString(x + 10, y + h - 13, label.upper())
    c.setFillColor(INK)
    c.setFont("Segoe-Bold", 14)
    c.drawString(x + 10, y + h - 31, value)
    c.setFillColor(MUTED)
    c.setFont("Segoe", 6.8)
    c.drawString(x + 10, y + 8, note)


def allocation_bar(c, x, y, w, h):
    values = [DATA["beta_initial_value"], DATA["delta_initial_value"], DATA["growth_initial_value"],
              DATA["bond_fee"] + DATA["growth_fee"]]
    total = sum(values)
    cols = [NAVY, BLUE, CYAN, colors.HexColor("#D7DEE3")]
    labels = ["Beta 2024", "Delta 2027", "USMV growth", "Costs"]
    cur = x
    for v, col in zip(values, cols):
        ww = w * v / total
        c.setFillColor(col)
        c.rect(cur, y, ww, h, fill=1, stroke=0)
        cur += ww
    cur = x
    for v, col, label in zip(values, cols, labels):
        ww = w * v / total
        c.setFillColor(INK if col == colors.HexColor("#D7DEE3") else WHITE)
        c.setFont("Segoe-Bold", 6.8)
        if ww > 34:
            c.drawCentredString(cur + ww / 2, y + h / 2 - 2.2, label)
        cur += ww


def timeline(c, x, y, width):
    pts = [x + 18, x + width * .36, x + width * .68, x + width - 18]
    c.setStrokeColor(LINE)
    c.setLineWidth(2)
    c.line(pts[0], y, pts[-1], y)
    labels = [
        ("31 DEC 2022", "USD 12.0m received"),
        ("31 DEC 2024", "USD 2.4m payment"),
        ("31 DEC 2027", "USD 3.6m payment"),
        ("31 DEC 2030", "$8m real goal"),
    ]
    cs = [NAVY, BLUE, BLUE, CYAN]
    for px, (date, event), col in zip(pts, labels, cs):
        c.setFillColor(col)
        c.circle(px, y, 4.1, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Segoe-Bold", 6.6)
        c.drawCentredString(px, y - 13, date)
        c.setFillColor(MUTED)
        c.setFont("Segoe", 6.2)
        c.drawCentredString(px, y - 23, event)


def main():
    assert DATA["growth_etf"] == "USMV"
    assert abs(DATA["total_initial_budget"] - 12_000_000) < .01
    assert DATA["training_months"] == 96
    assert CHALLENGER["objective"].endswith("no additional caps")
    assert abs(CHALLENGER["one_way_turnover_96m_to_60m"] - 0.3476) < .001
    assert {int(r["risk_aversion_A"]) for r in RISK} == {2, 4, 6, 8}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUT), pagesize=A4, pageCompression=1)
    c.setTitle("Kappa Foundation - Initial Decision Record - 22 October 2026")
    c.setAuthor("Kappa Foundation independent investment team")
    c.setSubject("Two-page initial decision record based on the 31 December 2022 case cutoff")

    # Page 1: recommendation, full funding plan and growth-sleeve decision.
    y = header(c, 1, "Initial decision record", "Fund commitments first. Invest the balance for growth.",
               "Prepared for the 22 October submission  |  Original case decision date: 31 December 2022")
    box_h = 57
    c.setFillColor(PALE_BLUE)
    c.roundRect(M, y - box_h, CW, box_h, 5, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont("Segoe-Bold", 7.3)
    c.drawString(M + 11, y - 14, "INVESTMENT OBJECTIVE")
    para(c, "Pay both non-cancellable nominal commitments from case bonds. Invest the remaining capital in a long-only growth sleeve. Seek at least <b>USD 8m in December 2022 purchasing power</b> at 31 December 2030; this is a goal, not a return promise.",
         M + 11, y - 21, CW - 22, "body")
    y -= box_h + 9

    gap = 8
    card_w = (CW - 2 * gap) / 3
    metric_card(c, M, y - 47, card_w, 47, "Initial resources", "$12.000m", "unrestricted cash at case date", NAVY)
    metric_card(c, M + card_w + gap, y - 47, card_w, 47, "Fixed payments", "$6.000m", "2024 and 2027; no equity sale", BLUE)
    metric_card(c, M + 2 * (card_w + gap), y - 47, card_w, 47, "2030 real goal", "$8.000m", "measured in Dec 2022 USD", CYAN)
    y -= 57

    y = section(c, "Initial allocation | complete USD 12m funding plan", M, y)
    allocation_bar(c, M, y - 15, CW, 17)
    y -= 23
    rows = [
        ["Use", "Holding and payment role", "Initial USD"],
        ["2024 commitment", "Beta, 2,400 units; USD 2.400m at maturity", "$2,214,672"],
        ["2027 commitment", "Delta, 3,478.26087 units; USD 3.600m final cash flow", "$3,429,809"],
        ["Growth sleeve", "100% USMV purchase; equity fee shown separately", "$6,346,351"],
        ["Execution costs", "5bp bonds and 10bp equity; planning assumptions", "$9,169"],
        ["Total", "Full allocation; no borrowing or residual initial cash", "$12,000,000"],
    ]
    y = draw_table(c, rows, [112, 306, CW - 418], M, y, row_fills=((3, PALE_CYAN),), pad=3)
    y -= 4
    y = para(c, "Beta principal meets the 2024 payment. Delta principal plus its final coupon meets the 2027 payment. Four earlier Delta coupons total <b>$486,957</b>; retain them as cash at the 0% base rate. This is contractual cash-flow dedication under the case's no-default assumption, not protection against inflation or an early sale.", M, y, CW, "muted")
    y -= 4
    timeline(c, M + 3, y - 8, CW - 6)
    y -= 44

    y = section(c, "Growth allocation | simple implementation, explicit trade-off", M, y)
    left_w = 236
    c.setFillColor(PALE_CYAN)
    c.roundRect(M, y - 56, left_w, 56, 5, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Segoe-Bold", 8)
    c.drawString(M + 9, y - 14, "RECOMMENDED SLEEVE  |  100% USMV")
    para(c, "USMV is a US minimum-volatility equity ETF. VTI, a broad-US-market ETF, is the frozen investable benchmark and credible rejected alternative. Neither is principal-protected.", M + 9, y - 21, left_w - 18, "body_small")
    metrics_x = M + left_w + 10
    metrics_w = CW - left_w - 10
    comp = [
        ["2022-input comparison", "USMV", "VTI", "Sample A=4"],
        ["CAPM expected return", "7.14%", "8.45%", "7.19%"],
        ["Annual volatility", "12.84%", "16.31%", "12.70%"],
        ["Utility at A=4", "3.84%", "3.13%", "3.96%"],
    ]
    ytable = draw_table(c, comp, [105, 52, 52, metrics_w - 209], metrics_x, y, pad=3)
    y = min(y - 56, ytable) - 5
    utility_gap = 100 * (CHALLENGER["utility_A4"] - DATA["forecast_comparison"]["USMV"]["utility_A4"])
    turnover = 100 * CHALLENGER["one_way_turnover_96m_to_60m"]
    y = para(c, f"<b>Why USMV:</b> among the two ETF choices, A=4 ranks USMV above VTI; the pairwise ranking switches near A=2.58. The unrestricted 96-month sample-covariance A=4 optimizer scores only {utility_gap:.2f} percentage point more annual utility than USMV, while changing {turnover:.1f}% one-way when the window falls from 96 to 60 months. We retain the simpler one-ETF policy; USMV is not presented as the mathematical maximum across all portfolios.", M, y, CW, "body_small")
    y -= 4
    y = para(c, "Candidate universe: <b>AAPL, MSFT, JPM, JNJ, PG, XOM, CAT and NEE</b> across seven sectors, plus USMV (minimum-volatility) and VTI (broad market). Candidates need not all be held. No additional position caps are imposed. A=4 is provisional and is compared with A=2, 6 and 8.", M, y, CW, "muted")
    y -= 7
    y = section(c, "Risk-preference sensitivity | the assumed A changes the ETF choice", M, y)
    gap = 6
    cw = (CW - 3 * gap) / 4
    for i, row in enumerate(RISK):
        av = int(row["risk_aversion_A"])
        u_usmv = float(row["USMV_utility"])
        u_vti = float(row["VTI_utility"])
        chosen = row["higher_utility_of_two_ETFs"]
        xx = M + i * (cw + gap)
        c.setFillColor(PALE_CYAN if chosen == "USMV" else PALE_BLUE)
        c.roundRect(xx, y - 48, cw, 48, 4, fill=1, stroke=0)
        c.setFillColor(NAVY)
        c.setFont("Segoe-Bold", 8)
        c.drawString(xx + 7, y - 13, f"A = {av}  |  favors {chosen}")
        c.setFillColor(INK)
        c.setFont("Segoe", 7)
        c.drawString(xx + 7, y - 26, f"USMV utility  {u_usmv:.2%}")
        c.drawString(xx + 7, y - 38, f"VTI utility     {u_vti:.2%}")
    y -= 54
    y = para(c, "Utility is an expected-return minus variance preference score, not a forecast of realized returns. At lower A the higher-return, higher-volatility VTI wins this two-ETF comparison; greater aversion penalizes its variance more heavily. A=4 is a chosen working preference, not an industry standard.", M, y, CW, "muted")
    if y < 42:
        raise RuntimeError(f"Page 1 content reached footer: y={y:.1f}")
    c.showPage()

    # Page 2: proposed policy assumptions, review triggers and reproducibility.
    y = header(c, 2, "Investment policy and evaluation rule", "Set the review rules before seeing the test period.",
               "Governance thresholds are review signals, not automatic trading orders or a loss guarantee")
    y = section(c, "Material assumptions and use", M, y)
    assumptions = [
        ["Decision item", "Base convention and purpose"],
        ["Goal and inflation", "USD 8m real at end-2030. CPI 2.5% is the primary planning rate: nominal goal $9.747m; 3.0% HEPI is a separate education-cost stress: $10.134m. Sleeve hurdle is 4.84% / 5.37% nominal CAGR, respectively, with four coupons held at 0%."],
        ["Return and risk inputs", "CAPM scenario: prospective RF 4%, market premium 4.5%, forecast alpha 0. A=4 provisional. Utility = expected annual return - 0.5 x A x annual variance. Historical excess returns use observed monthly French RF; the 4% scenario is not a cash quote."],
        ["Risk estimation", "Common 96 monthly returns, Jan 2015-Dec 2022; 60-month window and single-index covariance are robustness checks. FF3 explains historical exposures; it is not used to forecast until expected SMB/HML premiums are specified."],
        ["Allowed instruments and costs", "Cash, case bonds, US common stocks and US-listed US-equity ETFs; long-only, no borrowing, short sales or derivatives. Fractional holdings allowed. Base friction: 5bp bonds / 10bp equity; sensitivity: 0bp bonds, 5bp ETFs, 10bp stocks."],
    ]
    y = draw_table(c, assumptions, [108, CW - 108], M, y, row_fills=((1, PALE), (3, PALE)), pad=4)
    y -= 5

    y = section(c, "Growth-sleeve risk signals", M, y)
    y = para(c, "Proposed for trustee consideration on 21 October 2026. Track peak-to-trough drawdown from unitized total returns, including sleeve cash and adjusting outside flows; do not reset the high-water mark after changing assets. Keep whole-fund stress and payment coverage separate. Month-end academic data do not establish intramonth loss history.", M, y, CW, "muted")
    y -= 4
    ladder = [
        ["Signal", "Required review response"],
        ["10% drawdown", "Within 2 business days: validate prices, distributions, flows, payment coverage, stress and goal funding. No automatic trade."],
        ["15% drawdown", "Investment Committee meets within 5 business days; document hold, an already-authorized rebalance, or a prospective policy recommendation."],
        ["20% drawdown", "Notify trustees same or next business day; pause discretionary risk increases pending review. No automatic liquidation."],
        ["Any payment gap", "Escalate immediately and produce a funded corrective plan, regardless of drawdown level."],
    ]
    y = draw_table(c, ladder, [98, CW - 98], M, y, row_fills=((2, PALE_BLUE),), pad=3)
    y -= 5
    c.setFillColor(PALE_CYAN)
    c.roundRect(M, y - 52, CW, 52, 4, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont("Segoe-Bold", 7.6)
    c.drawString(M + 9, y - 13, "UPSIDE RULE  |  ANNUAL REVIEW")
    para(c, "After reserving obligations, test the CPI goal after a separate -30% growth-sleeve shock. If still fully funded, trustees may protect only the minimum amount needed in a permitted, goal-date-matched asset at its actual available price; leave surplus under the growth policy. No fixed-gain sale or automatic spending increase. Implementation and authorization remain prospective.", M + 9, y - 19, CW - 18, "body_small")
    y -= 61

    c.setFillColor(PALE)
    c.roundRect(M, y - 44, CW, 44, 4, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.setFont("Segoe-Bold", 7.4)
    c.drawString(M + 8, y - 12, "CRISIS EXCEPTION AND FUNDING-GAP DISCIPLINE")
    para(c, "A crisis exception may delay discretionary action only, with written approval, expiry and review; it may not reduce payment coverage. If broad-market conditions weaken goal feasibility, prioritize preservation. If the sleeve lags VTI, diagnose exposures, risk and costs before a prospective change. Do not add risk solely to catch up.", M + 8, y - 17, CW - 16, "body_small")
    y -= 51

    y = section(c, "Frozen evaluation and implementation", M, y)
    y = para(c, "Freeze USMV and VTI weights as of 31 December 2022. Evaluate monthly total returns from January 2023-December 2025 against VTI, with an annual post-December return review back to original weights and no parameter re-estimation. For a single-ETF sleeve this creates no routine internal trade; changing the ETF is a prospective policy decision. Later returns do not alter the original rationale.", M, y, CW, "body_small")
    y -= 4
    y = para(c, "<b>Working files:</b> from the dated package root, run <font name='Segoe-Bold'>python analysis/run_initial.py</font> offline to verify raw-source hashes and rebuild the 96-month inputs, CAPM comparison and utility sensitivities. The original retrieval script is <font name='Segoe-Bold'>analysis/retrieve_data.py --phase train</font>; do not rerun into the preserved raw folder. See <font name='Segoe-Bold'>data/DATA_RECORD.md</font> and <font name='Segoe-Bold'>data/raw/retrieval_manifest.jsonl</font> for dates, settings, versions, units and hashes.", M, y, CW, "body_small")
    y -= 4
    y = para(c, "<b>Source and limitation:</b> prices are Yahoo/yfinance adjusted-close histories downloaded in 2026; factors are the original Kenneth French monthly FF3 ZIP. The retrospective histories may be revised; selected survivors do not remove selection bias. Beta and Delta are fictional case instruments, assessed from contract cash flows rather than invented market history. This record is prepared for submission; it is not proof of trustee authorization or upload.", M, y, CW, "muted")
    if y < 42:
        raise RuntimeError(f"Page 2 content reached footer: y={y:.1f}")
    c.showPage()
    c.save()
    reader = PdfReader(str(OUT))
    assert len(reader.pages) == 2, f"Expected exactly 2 pages, got {len(reader.pages)}"
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    for marker in ["USD 12m", "USMV", "VTI", "96 monthly returns", "10% drawdown", "15% drawdown", "20% drawdown", "DATA_RECORD.md"]:
        assert marker in text, f"Missing required content: {marker}"
    print(f"Wrote {OUT}; 2 pages; remaining footer clearances: p1={y if False else 'checked'}, p2={y:.1f} pt")


if __name__ == "__main__":
    main()
