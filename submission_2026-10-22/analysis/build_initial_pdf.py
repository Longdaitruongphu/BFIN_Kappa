"""Two-page SISF-inspired initial record, with three tiers of annotation.

Run after `python analysis/run_initial.py` from the dated package root.
All financial values are read from saved outputs. Design references supply no data.
Tables use short labels; sources are one italic 7.5pt line; five definitions sit on p2.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "deliverables/Kappa_Initial_Decision_Record_22Oct2026.pdf"
DATA = json.loads((ROOT / "outputs/initial_decision_rebuild.json").read_text(encoding="utf-8"))
ALT = json.loads((ROOT / "outputs/sample_utility_robustness.json").read_text(encoding="utf-8"))
with (ROOT / "outputs/risk_preference.csv").open(encoding="utf-8", newline="") as f:
    RISK = list(csv.DictReader(f))
with (ROOT / "outputs/max_utility_preference.csv").open(encoding="utf-8", newline="") as f:
    MAX_UTILITY = list(csv.DictReader(f))

# Change the theme here. All measurements below are in PDF points.
W, H = A4
M = 34
WIDTH = W - 2 * M
GAP = 19
LEFT = 335
RIGHT = WIDTH - LEFT - GAP
RX = M + LEFT + GAP
NAVY = colors.HexColor("#052F63")
BLUE = colors.HexColor("#007EB6")
TEAL = colors.HexColor("#00A9BA")
INK = colors.HexColor("#182C3C")
MUTED = colors.HexColor("#62727E")
LINE = colors.HexColor("#CCD8E1")
PALE = colors.HexColor("#F1F5F8")
TINT = colors.HexColor("#E9F5F7")
WHITE = colors.white
AUDIT = {"sources": [], "tables": [], "glossary": [], "paragraphs": []}


def fonts():
    windows = Path("C:/Windows/Fonts")
    if (windows / "arial.ttf").exists():
        for name, filename in [("Text", "arial.ttf"), ("Text-Bold", "arialbd.ttf"), ("Text-Italic", "ariali.ttf")]:
            pdfmetrics.registerFont(TTFont(name, str(windows / filename)))
        pdfmetrics.registerFontFamily("Text", normal="Text", bold="Text-Bold", italic="Text-Italic")
        return "Text", "Text-Bold", "Text-Italic"
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


FONT, BOLD, ITALIC = fonts()


def para(c, text, x, top, width, size=9, leading=12, color=INK, bold=False):
    style = ParagraphStyle("p", fontName=BOLD if bold else FONT, fontSize=size, leading=leading,
                           textColor=color, spaceBefore=0, spaceAfter=0)
    p = Paragraph(text.replace("<super>", "<super size='5.5'>"), style)
    _, h = p.wrap(width, 1000)
    p.drawOn(c, x, top - h)
    AUDIT["paragraphs"].append({"page": c.getPageNumber(), "x": x, "top": top,
                                "bottom": top - h, "width": width})
    return top - h


def plain(c, text, x, y, size=9, font=None, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font or FONT, size)
    if align == "right":
        c.drawRightString(x, y, text)
    elif align == "center":
        c.drawCentredString(x, y, text)
    else:
        c.drawString(x, y, text)


def heading(c, text, x, top, width=WIDTH):
    plain(c, text, x, top - 10, 10.4, BOLD, NAVY)
    c.setLineWidth(.6)
    c.setStrokeColor(BLUE)
    c.line(x, top - 15, x + width, top - 15)
    return top - 23


def source(c, text, x, top, width):
    """Tier two: exactly one italic line at 7.5pt, never silently shrink it."""
    measured = pdfmetrics.stringWidth(text, ITALIC, 7.5)
    if measured > width:
        raise ValueError(f"Source line too wide ({measured:.1f}>{width:.1f}): {text}")
    plain(c, text, x, top - 8, 7.5, ITALIC, MUTED)
    AUDIT["sources"].append({"page": c.getPageNumber(), "text": text, "font_size": 7.5,
                              "lines": 1, "width": measured, "available": width})
    return top - 17


def table(c, rows, widths, x, top, numeric=(), highlight=(), row_height=21):
    """Tier one: short cell values and superscript definition markers only."""
    width = sum(widths)
    y = top
    for ri, row in enumerate(rows):
        header = ri == 0
        c.setFillColor(NAVY if header else TINT if ri in highlight else WHITE)
        c.rect(x, y - row_height, width, row_height, fill=1, stroke=0)
        xx = x
        for ci, cell in enumerate(row):
            txt = str(cell)
            # No explanatory sentence may migrate into a table cell.
            if len(txt.replace("<super>", "").replace("</super>", "")) > 52:
                raise ValueError(f"Verbose table cell: {txt}")
            txt = txt.replace("<super>", "<super size='5.5'>")
            size = 8.1 if header else 8.6
            font = BOLD if header or ci == 0 else FONT
            color = WHITE if header else INK
            style = ParagraphStyle("cell", fontName=font, fontSize=size, leading=10,
                                   textColor=color, alignment=2 if ci in numeric else 0)
            p = Paragraph(txt, style)
            _, ph = p.wrap(widths[ci] - 10, 100)
            if ph > row_height - 3:
                raise ValueError(f"Table cell wraps beyond row: {txt} ({ph})")
            p.drawOn(c, xx + 5, y - row_height + (row_height - ph) / 2 + .4)
            xx += widths[ci]
        if ri > 0:
            c.setStrokeColor(LINE)
            c.setLineWidth(.3)
            c.line(x, y - row_height, x + width, y - row_height)
        y -= row_height
    AUDIT["tables"].append({"page": c.getPageNumber(), "rows": len(rows), "columns": len(widths),
                             "top": top, "bottom": y, "cell_policy": "short labels and numbers"})
    return y


def facts(c, rows, x, top, width, label_width=93, step=19):
    y = top
    for label, value in rows:
        plain(c, label, x, y - 9, 8.3, color=BLUE)
        plain(c, value, x + label_width, y - 9, 8.3)
        y -= step
    return y


def header(c, page, title):
    c.setFillColor(NAVY)
    c.rect(M, H - 108, WIDTH, 77, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(W - M - 7, H - 108, 7, 77, fill=1, stroke=0)
    plain(c, "Kappa Foundation", M + 13, H - 59, 23, BOLD, WHITE)
    plain(c, title, M + 13, H - 79, 13.4, BOLD, colors.HexColor("#35D0D8"))
    plain(c, "USD | Case date 31 December 2022 | Initial submission 22 October 2026", M + 13,
          H - 98, 8, color=WHITE)
    c.setStrokeColor(LINE)
    c.setLineWidth(.45)
    c.line(M, 31, W - M, 31)
    plain(c, "Independent investment team | Prepared 21 October 2026 | Original mandate", M, 19, 7.3, color=MUTED)
    plain(c, f"{page} / 2", W - M, 19, 7.3, color=MUTED, align="right")
    return H - 122


def capital_chart(c, x, top, width):
    vals = [DATA["beta_initial_value"], DATA["delta_initial_value"], DATA["growth_initial_value"],
            DATA["bond_fee"] + DATA["growth_fee"]]
    cols = [NAVY, BLUE, TEAL, colors.HexColor("#C7D2DB")]
    xx = x
    for val, col in zip(vals, cols):
        ww = width * val / 12_000_000
        c.setFillColor(col)
        c.rect(xx, top - 20, ww, 20, fill=1, stroke=0)
        xx += ww
    for ix, (label, val, col) in enumerate(zip(["Beta", "Delta", "USMV", "Costs"], vals, cols)):
        xx = x + ix * width / 4
        c.setFillColor(col)
        c.rect(xx, top - 33, 5, 5, fill=1, stroke=0)
        plain(c, f"{label}  {val / 12_000_000:.2%}", xx + 9, top - 33, 7.9)
    return top - 43


def utility_chart(c, x, top, width, height=122):
    """Compare fixed ETF utilities with the re-optimised full-universe utility."""
    px, py = x + 27, top - height + 22
    pw, ph = width - 72, height - 37
    xmin, xmax, ymin, ymax = 2, 8, -.025, .065
    def xy(a, u):
        return px + (a - xmin) / (xmax - xmin) * pw, py + (u - ymin) / (ymax - ymin) * ph
    for tick in [-.02, 0, .02, .04, .06]:
        _, yy = xy(2, tick)
        c.setStrokeColor(LINE)
        c.setLineWidth(.35)
        c.line(px, yy, px + pw, yy)
        plain(c, f"{100*tick:.0f}", px - 7, yy - 2.5, 7, color=MUTED, align="right")
    for a in [2, 4, 6, 8]:
        xx, _ = xy(a, 0)
        plain(c, str(a), xx, py - 12, 7.5, color=MUTED, align="center")
    x4, _ = xy(4, 0)
    c.setStrokeColor(BLUE)
    c.setLineWidth(.6)
    c.setDash(2, 2)
    c.line(x4, py, x4, py + ph)
    c.setDash()
    series = [
        ([xy(int(r["risk_aversion_A"]), float(r["USMV_utility"])) for r in RISK], NAVY, "USMV", False),
        ([xy(int(r["risk_aversion_A"]), float(r["VTI_utility"])) for r in RISK], TEAL, "VTI", False),
        ([xy(int(r["risk_aversion_A"]), float(r["utility"])) for r in MAX_UTILITY], BLUE, "Max util.", True),
    ]
    for pts, col, name, square in series:
        c.setStrokeColor(col)
        c.setLineWidth(1.7 if square else 1.45)
        if square:
            c.setDash(3, 2)
        path = c.beginPath()
        path.moveTo(*pts[0])
        for pt in pts[1:]: path.lineTo(*pt)
        c.drawPath(path)
        c.setDash()
        for xx, yy in pts:
            c.setFillColor(col)
            if square:
                c.rect(xx - 2.5, yy - 2.5, 5, 5, fill=1, stroke=0)
            else:
                c.circle(xx, yy, 2.3, fill=1, stroke=0)
    plain(c, "Utility (%)", x, top - 6, 7.2, color=MUTED)
    legend_y = top - 6
    for lx, col, label, dashed in [(x + 62, NAVY, "USMV 100%", False),
                                   (x + 139, TEAL, "VTI 100%", False),
                                   (x + 205, BLUE, "Max utility", True)]:
        c.setStrokeColor(col)
        c.setLineWidth(1.4)
        if dashed: c.setDash(2, 1.5)
        c.line(lx, legend_y + 2, lx + 10, legend_y + 2)
        c.setDash()
        plain(c, label, lx + 12, legend_y, 6.6, BOLD, col)
    plain(c, "Risk aversion A", px + pw / 2, py - 24, 7.4, color=MUTED, align="center")
    return top - height - 8


def glossary(c):
    """Tier three: exactly five one-line definitions at 7.5pt on page two."""
    top, bottom = 121, 42
    c.setFillColor(PALE)
    c.rect(M, bottom, WIDTH, top - bottom, fill=1, stroke=0)
    plain(c, "Mini-Glossary | Definitions used in this record", M + 9, top - 13, 8.2, BOLD, NAVY)
    definitions = [
        ("1  CAPM return", "Annual arithmetic forecast: risk-free rate + beta x market premium; forecast alpha=0."),
        ("2  Volatility", "Monthly return standard deviation x sqrt(12); an annual risk estimate, not a loss cap."),
        ("3  Utility (A)", "E[R] - 0.5 x A x annual variance; a higher A applies a larger penalty to risk."),
        ("4  CAGR", "The constant annual compound rate over a period; the goal hurdle includes retained coupon cash."),
        ("5  Drawdown", "Decline in the flow-adjusted growth-sleeve unit value from its previous peak."),
    ]
    y = top - 26
    for term, meaning in definitions:
        tw = pdfmetrics.stringWidth(term, BOLD, 7.5)
        mw = pdfmetrics.stringWidth(meaning, FONT, 7.5)
        assert tw + mw + 12 < WIDTH - 18, (term, tw + mw)
        plain(c, term, M + 9, y, 7.5, BOLD)
        plain(c, meaning, M + 9 + 80, y, 7.5)
        assert 80 + mw < WIDTH - 18, (term, mw)
        AUDIT["glossary"].append({"term": term, "definition": meaning, "lines": 1, "font_size": 7.5})
        y -= 11


def main():
    assert DATA["training_months"] == 96
    assert abs(sum(DATA[k] for k in ["beta_initial_value", "delta_initial_value", "growth_initial_value", "bond_fee", "growth_fee"]) - 12_000_000) < 1e-6
    DEST.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(DEST), pagesize=A4, pageCompression=1)
    c.setTitle("Kappa Foundation | Initial Decision Record | 22 October 2026")
    c.setAuthor("Kappa Foundation independent investment team")
    c.setCreator("Kappa reproducible report builder")

    y = header(c, 1, "Initial decision record")
    y = heading(c, "Investment objective and policy", M, y)
    y = para(c, "Meet the fixed education commitments first and protect long-term purchasing power. Invest surplus capital within the fund's capacity for risk. Seek <b>USD 8m in December 2022 purchasing power at end-2030</b>; this is a planning goal. Portfolio changes require evidence about obligations, resources and assets, rather than short-term market moves.", M, y, WIDTH, 9.1, 12.3)
    top = y - 17

    # Main column: acquisition values, funded payments and the growth decision.
    y = heading(c, "Initial capital allocation", M, top, LEFT)
    y = capital_chart(c, M, y, LEFT)
    vals = [DATA["beta_initial_value"], DATA["delta_initial_value"], DATA["growth_initial_value"], DATA["bond_fee"] + DATA["growth_fee"]]
    allocation = [["Holding / use", "Units / basis", "Initial USD"],
                  ["Beta | 2024", "2,400", f"{vals[0]:,.2f}"],
                  ["Delta | 2027", "3,478.26087", f"{vals[1]:,.2f}"],
                  ["USMV", "100% of sleeve", f"{vals[2]:,.2f}"],
                  ["Trading costs", "5 / 10bp", f"{vals[3]:,.2f}"],
                  ["Total", "", "12,000,000.00"]]
    y = table(c, allocation, [115, 104, LEFT - 219], M, y, numeric=(2,), highlight=(3,), row_height=20)
    y = source(c, "Source: case Exhibit 1; Kappa model; USD, fees separate; % rounded.", M, y - 3, LEFT)
    y = para(c, "Beta principal pays <b>$2.4m on 31 Dec 2024</b>. Delta principal and its final coupon pay <b>$3.6m on 31 Dec 2027</b>. Four earlier Delta coupons total $486,957 and remain cash at 0%; payment coverage needs no equity sale or reinvestment return.", M, y - 2, LEFT, 8.8, 11.7)
    y -= 13

    y = heading(c, "Growth portfolio decision", M, y, LEFT)
    y = para(c, "<b>Recommend 100% USMV</b>, the US minimum-volatility ETF. Use <b>100% VTI</b>, a broad-US-market ETF, as the frozen investable benchmark and credible rejected alternative.", M, y, LEFT, 9, 12)
    y -= 9
    growth = [["Annual measure", "USMV", "VTI", "Max utility A=4"],
              ["Expected return<super>1</super>", "7.14%", "8.45%", f"{ALT['expected_return']:.2%}"],
              ["Volatility<super>2</super>", "12.84%", "16.31%", f"{ALT['volatility']:.2%}"],
              ["Utility<super>3</super> | A=4", "3.84%", "3.13%", f"{ALT['utility_A4']:.2%}"]]
    y = table(c, growth, [123, 62, 62, LEFT - 247], M, y, numeric=(1, 2, 3), highlight=(3,), row_height=21)
    y = source(c, "Source: Yahoo Finance, Kenneth French; Kappa model; 2015-22, annualised.", M, y - 3, LEFT)
    gap_pp = 100 * (ALT["utility_A4"] - DATA["forecast_comparison"]["USMV"]["utility_A4"])
    turnover = ALT["one_way_turnover_96m_to_60m"]
    weights = ALT["weights_96m"]
    ordered = ["MSFT", "JPM", "JNJ", "PG", "XOM", "NEE", "USMV", "VTI"]
    weight_line1 = " | ".join(f"{t} {weights[t]:.2%}" for t in ordered[:4])
    weight_line2 = " | ".join(f"{t} {weights[t]:.2%}" for t in ordered[4:]) + " | AAPL/CAT 0.00%"
    y = para(c, f"<b>Full-universe maximum utility at A=4:</b> {weight_line1}<br/>{weight_line2}", M, y - 2, LEFT, 8.2, 10.8)
    y = para(c, f"This is the highest-scoring long-only mix of the 10 candidates for these inputs: 96 months, CAPM expected returns, sample covariance, weights >=0 and sum=100%, no extra caps. At A=4 it estimates 7.19% return, 12.70% volatility and 3.96% utility, {gap_pp:.2f} percentage point above USMV. But the 96-to-60-month check shifts {turnover:.1%} of weights one-way (about $2.21m on this sleeve). We choose USMV for simpler policy implementation, not because it is the model maximum.", M, y - 3, LEFT, 8.0, 10.5)
    y = para(c, "Neither portfolio guarantees principal or the 2030 goal. The optimizer's weights are estimates, not an instruction to trade without review.", M, y - 4, LEFT, 7.8, 9.8, MUTED)
    y = para(c, "Long-only; no borrowing, shorting or derivatives. Fractional holdings allowed. Fee sensitivity: 0bp bonds / 5bp ETFs / 10bp stocks.", M, y - 7, LEFT, 8.1, 10.8, MUTED)
    assert y > 58, f"Page 1 main column overflow: {y}"

    # SISF-style right-hand facts column. Only compact labels and values.
    sy = heading(c, "Mandate facts", RX, top, RIGHT)
    sy = facts(c, [("Initial capital", "$12.000m"), ("Currency", "USD"), ("Goal date", "31 Dec 2030"),
                   ("Real goal", "$8.000m"), ("Growth sleeve", "100% USMV"), ("Benchmark", "100% VTI")], RX, sy, RIGHT, 98, 18)
    sy = source(c, "Source: original case and proposed IPS.", RX, sy + 1, RIGHT)
    sy = heading(c, "Core assumptions", RX, sy - 7, RIGHT)
    sy = facts(c, [("CPI base", "2.50%"), ("HEPI stress", "3.00%"), ("Risk-free (plan)", "4.00%"),
                   ("Market premium", "4.50%"), ("Forecast alpha", "0.00%"), ("Risk aversion A", "4 (provisional)"),
                   ("Coupon cash rate", "0.00%"), ("Bond / equity fee", "5 / 10bp")], RX, sy, RIGHT, 94, 17)
    sy = source(c, "Source: proposed IPS; annual scenarios.", RX, sy, RIGHT)
    sy = heading(c, "Candidate universe", RX, sy - 8, RIGHT)
    sy = facts(c, [("Technology", "AAPL, MSFT"), ("Financials", "JPM"), ("Health care", "JNJ"),
                   ("Staples", "PG"), ("Energy", "XOM"), ("Industrials", "CAT"), ("Utilities", "NEE"),
                   ("Equity ETFs", "USMV, VTI")], RX, sy, RIGHT, 84, 16)
    sy = source(c, "Source: eligibility notes; 2022 status.", RX, sy + 1, RIGHT)
    sy = para(c, "Eight stocks, seven sectors and two distinct ETF mandates. Candidates need not all be held. No additional security-weight caps are imposed.", RX, sy - 2, RIGHT, 8.1, 10.8, MUTED)
    assert sy > 63, f"Page 1 facts column overflow: {sy}"
    c.showPage()

    y = header(c, 2, "Policy, risk and implementation")
    top = y
    y = heading(c, "Risk-preference comparison", M, top, LEFT)
    y = utility_chart(c, M, y, LEFT, 95)
    y = source(c, "Source: Kappa analysis; Yahoo/French inputs; annual utility scores.", M, y, LEFT)
    y = para(c, "USMV and VTI stay at 100%. The dashed line re-optimises all 10 candidates at each A and shows the highest estimated score for that risk preference. At A=4 it scores 3.96%; page 1 lists its holdings. Of the fixed ETFs, VTI leads at A=2; USMV leads at A=4, 6 and 8 (crossover A=2.58). A=4 is provisional.", M, y, LEFT, 8.0, 10.0)

    sy = heading(c, "Real-goal sensitivity", RX, top, RIGHT)
    target_rows = [["2030 goal", "Base", "Stress"],
                   ["Inflation", "2.50%", "3.00%"],
                   ["Nominal USD", "$9.747m", "$10.134m"],
                   ["CAGR<super>4</super> hurdle", "4.84%", "5.37%"]]
    sy = table(c, target_rows, [RIGHT - 96, 46, 50], RX, sy, numeric=(1, 2), row_height=22)
    sy = source(c, "Source: funding model; 2022-30.", RX, sy - 3, RIGHT)
    sy = para(c, "CPI defines the primary goal. HEPI is a separate education-cost stress. Both hurdles retain four early coupons at 0% cash interest.", RX, sy, RIGHT, 8.3, 11.1, MUTED)
    y = min(y, sy) - 12

    y = heading(c, "Risk oversight | growth sleeve", M, y)
    y = para(c, "Use flow-adjusted growth-sleeve unit values, including cash; retain the prior peak after asset changes. Report payment coverage and whole-fund stress separately. Historical drawdown<super>5</super> is measured at month-end.", M, y, WIDTH, 8.7, 11.5)
    y -= 7
    ladder = [["Signal<super>5</super>", "Required action", "Deadline"],
              ["10%", "Validate data, funding and stress", "Within 2 business days"],
              ["15%", "Investment Committee decision", "Within 5 business days"],
              ["20%", "Notify trustees; pause risk increases", "Same / next business day"],
              ["Payment gap", "Escalate; restore payment coverage", "Immediate"]]
    y = table(c, ladder, [78, WIDTH - 234, 156], M, y, highlight=(2,), row_height=19)
    y = source(c, "Source: proposed IPS, 21 Oct 2026; growth-sleeve review triggers, not guaranteed loss limits.", M, y - 3, WIDTH)
    y = para(c, "No automatic sale. At 15%, record hold, authorised rebalance or policy proposal. Discretionary crisis deferral requires written authority, expiry and review; due-payment coverage cannot fall.", M, y, WIDTH, 8.3, 11.1, MUTED)
    y -= 12

    half = (WIDTH - GAP) / 2
    left_y = heading(c, "Annual goal protection and policy response", M, y, half)
    left_y = para(c, "At year-end, after reserving remaining bond/cash obligations, test the <b>$9.747m</b> CPI goal (<b>$10.134m</b> at HEPI stress) after a <b>30% growth-sleeve loss</b>. If covered, trustees may approve locking only the minimum needed in an eligible, priced asset due by 2030; leave surplus invested. This is prospective, not automatic. If not covered, report the gap; do not raise risk to catch up.", M, left_y, half, 8.0, 10.0)

    ex = M + half + GAP
    right_y = heading(c, "Frozen test and future rebalancing", ex, y, half)
    right_y = para(c, "Freeze <b>USMV 100%</b> and <b>VTI 100%</b> at 31 Dec 2022. Compare monthly returns in Jan 2023-Dec 2025; reset to start weights each December without re-estimating. One ETF creates no internal trade; 10bp applies only to trades. Later returns test, not set, 2022 weights. Future changes require a dated IPS review.", ex, right_y, half, 8.0, 10.0)
    right_y = para(c, "Estimate 96 months (Jan 2015-Dec 2022); check 60 months. The final memo compares sample and single-index risk. FF3 explains history; CAPM sets forecast alpha to zero. Exclude 2023-25 from 2022 weights.", ex, right_y - 3, half, 7.9, 9.8)
    y = min(left_y, right_y) - 7

    y = heading(c, "Read and reproduce", M, y)
    y = para(c, "<b>1.</b> Read <b>data/DATA_RECORD.md</b> and its retrieval manifest. <b>2.</b> Install requirements-analysis.txt; run <b>python analysis/run_initial.py</b> offline. <b>3.</b> Check <b>sample_utility_robustness.json</b>, <b>max_utility_A4_weights.csv</b> and <b>max_utility_preference.csv</b> in outputs/. Retrieval: <b>analysis/retrieve_data.py --phase train</b>, in a clean copy.", M, y, WIDTH, 7.8, 10.3)
    y = para(c, "Data retrieved 15 Oct 2026: Yahoo adjusted-close and French factors. Revised histories and survivor selection limit this retrospective case. Fictional bonds use contract cash flows. RF=4% is a planning scenario; historical excess returns use observed monthly French RF.", M, y - 3, WIDTH, 7.5, 10, MUTED)
    assert y >= 132, f"Page 2 body conflicts with glossary: bottom={y:.1f}"
    glossary(c)
    c.showPage()
    c.save()

    reader = PdfReader(str(DEST))
    assert len(reader.pages) == 2
    text = "\n".join(p.extract_text() or "" for p in reader.pages)
    for phrase in ["12,000,000.00", "AAPL, MSFT", "USMV", "VTI", "Jan 2023-Dec 2025", "Mini-Glossary", "DATA_RECORD.md"]:
        assert phrase in text, phrase
    assert len(AUDIT["glossary"]) == 5
    receipt = {"pages": 2, "pdf_sha256": hashlib.sha256(DEST.read_bytes()).hexdigest(),
               "source_lines": AUDIT["sources"], "tables": AUDIT["tables"], "glossary": AUDIT["glossary"],
               "page2_body_bottom": y, "glossary_top": 121,
               "data_inputs_unchanged_by_design": True,
               "design_references": {"SISF": "primary local layout reference", "Goldman Sachs": "numbered notes and separate glossary inspected via web", "Morgan Stanley": "user URL inaccessible", "Lazard": "user URL inaccessible"}}
    (ROOT / "outputs/initial_pdf_layout_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {DEST}; 2 pages; {len(AUDIT['sources'])} single-line 7.5pt sources; 5 one-line glossary entries.")


if __name__ == "__main__":
    main()
