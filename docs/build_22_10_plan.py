from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

NAVY = RGBColor(0x1F, 0x38, 0x64)
BLUE = RGBColor(0x2E, 0x54, 0x96)
GREY = RGBColor(0x59, 0x59, 0x59)
DARK = RGBColor(0x22, 0x22, 0x22)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HEADER_FILL = "1F3864"
ALT_FILL = "F3F6FB"
LIGHT_BLUE = "EAF1FB"
BORDER = "B4C6E7"

FONT = "Arial"


def set_font(run, size=9.7, bold=False, italic=False, color=DARK, name=FONT):
    run.font.name = name
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = OxmlElement("w:rFonts")
        rPr.append(rFonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rFonts.set(qn(attr), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = color


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def margins(cell, top=35, bottom=35, left=55, right=55):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for tag, value in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = OxmlElement(f"w:{tag}")
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")
        tcMar.append(node)
    tcPr.append(tcMar)


def borders(table):
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), BORDER)
        tblBorders.append(el)
    tblPr.append(tblBorders)


def header_row(row):
    trPr = row._tr.get_or_add_trPr()
    cs = OxmlElement("w:cantSplit")
    trPr.append(cs)
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trPr.append(th)


def keep_together(table):
    for row in table.rows[:-1]:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.keep_with_next = True


def add_text(p, text, size=9.7, color=DARK, bold=False):
    # Simple **bold** support.
    parts = text.split("**")
    for i, part in enumerate(parts):
        if not part:
            continue
        r = p.add_run(part)
        set_font(r, size=size, color=color, bold=bold or (i % 2 == 1))


def heading(doc, text, size=11.5, color=BLUE, before=6, after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    set_font(r, size=size, bold=True, color=color)
    return p


def bullet(doc, text, size=9.7):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.42)
    p.paragraph_format.first_line_indent = Cm(-0.22)
    p.paragraph_format.space_after = Pt(1.5)
    r = p.add_run("• ")
    set_font(r, size=size, color=BLUE, bold=True)
    add_text(p, text, size=size)


def callout(doc, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    borders(table)
    cell = table.cell(0, 0)
    cell.width = Cm(18.2)
    shade(cell, LIGHT_BLUE)
    margins(cell, 70, 70, 100, 100)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    add_text(p, text, size=9.0, color=NAVY)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)


def table(doc, rows, widths, font_size=8.7):
    ncols = len(widths)
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = False
    borders(table)

    tbl = table._tbl
    tblPr = tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), str(int(sum(widths) * 567)))
    tblW.set(qn("w:type"), "dxa")
    tblPr.append(tblW)

    for j, w in enumerate(widths):
        table.columns[j].width = Cm(w)
        tbl.tblGrid.gridCol_lst[j].set(qn("w:w"), str(int(w * 567)))

    for i, row in enumerate(rows):
        for j, text in enumerate(row):
            cell = table.cell(i, j)
            cell.width = Cm(widths[j])
            margins(cell, 30, 30, 50, 50)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            if i == 0:
                shade(cell, HEADER_FILL)
                add_text(p, text, size=font_size, color=WHITE, bold=True)
            else:
                if i % 2 == 0:
                    shade(cell, ALT_FILL)
                add_text(p, text, size=font_size, color=DARK)
        if i == 0:
            header_row(table.rows[i])
        else:
            trPr = table.rows[i]._tr.get_or_add_trPr()
            trPr.append(OxmlElement("w:cantSplit"))

    keep_together(table)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)
    return table


def page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Kappa Foundation · Kế hoạch 22/10/2026 · Trang ")
    set_font(r, size=7.8, color=GREY)
    run = p.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    run._r.append(begin)
    run2 = p.add_run()
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    run2._r.append(instr)
    run3 = p.add_run()
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    run3._r.append(sep)
    cached = p.add_run("1")
    set_font(cached, size=7.8, color=GREY)
    run4 = p.add_run()
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run4._r.append(end)


def build(out_path: Path):
    doc = Document()
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(1.25)
    section.bottom_margin = Cm(1.15)
    section.left_margin = Cm(1.5)
    section.right_margin = Cm(1.5)
    section.header_distance = Cm(0.5)
    section.footer_distance = Cm(0.45)

    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(9.7)
    normal.font.color.rgb = DARK
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.line_spacing = 1.0

    page_number_footer(section)

    # Header line
    header = section.header
    hp = header.paragraphs[0]
    hp.text = ""
    hr = hp.add_run("KAPPA FOUNDATION  ·  DEADLINE 22/10  ·  16:00")
    set_font(hr, size=7.8, bold=True, color=BLUE)
    pPr = hp._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "4")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), BORDER)
    pBdr.append(bottom)
    pPr.append(pBdr)

    # Title
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run("KẾ HOẠCH 22/10 — CHIA VIỆC NHÓM 4")
    set_font(r, size=19, bold=True, color=NAVY)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Initial decision record 2 trang + Python + dated data record  ·  16:00, 22/10/2026")
    set_font(r, size=9.6, italic=True, color=BLUE)

    callout(
        doc,
        "**Mục tiêu:** nộp đúng 2 trang, đủ 12 triệu USD, có universe – window – benchmark – allocation – assumptions – evaluation rule; kèm Python chạy được và data record có ngày. Đây là kế hoạch, không phải bằng chứng đã nộp.",
    )

    heading(doc, "1. 22/10 phải nộp gì?")
    bullet(doc, "**Initial decision record ≤ 2 trang:** universe, estimation window, benchmark, dollar allocation, material assumptions, evaluation/rebalancing rule.")
    bullet(doc, "**Working Python file:** chạy được từ raw data đã lưu; có retrieval code; không cần internet khi rebuild.")
    bullet(doc, "**Dated data record:** ticker, nguồn, ngày tải, settings, package versions, hash.")
    bullet(doc, "**Frozen policy:** `policy/frozen_policy.json` + SHA-256, khóa trước khi lấy evaluation 2023–2025.")
    bullet(doc, "**Receipt:** ảnh chụp/email xác nhận đã nộp; không nói “đã nộp” khi chưa có.")

    heading(doc, "2. Bốn người, bốn phần")
    table(
        doc,
        [
            ["Người", "Việc chính phải xong", "Output", "Hạn", "Người kiểm"],
            [
                "**Minh**\n(A)",
                "Chốt allocation 12m; viết phần allocation/assumptions/evaluation rule; đóng gói Python + data record; freeze policy; nộp bài.",
                "A1 allocation\nA2 assumptions\nA3 eval rule\nA4 python + data\nA5 receipt",
                "21/10",
                "B, C, D",
            ],
            [
                "**B**",
                "Kiểm Beta/Delta, coupon, funding cash flow; viết 1 trang bond verification; 3 bullet rủi ro lãi suất.",
                "B1 bond sheet\nB2 funding check\nB3 rate note",
                "20/10",
                "Minh, D",
            ],
            [
                "**C**",
                "Chốt 10 mã + 2 ETF; eligibility matrix; benchmark VTI; kiểm 2 monthly returns; source record.",
                "C1 eligibility\nC2 benchmark\nC3 return check\nC4 source record",
                "20/10",
                "Minh, D",
            ],
            [
                "**D**",
                "Viết narrative 2 trang; định nghĩa 15%; assumptions register; AI disclosure; kiểm page limit; đọc lần cuối.",
                "D1 narrative\nD2 15% note\nD3 assumptions\nD4 AI disclosure",
                "21/10",
                "B, C",
            ],
        ],
        widths=[1.7, 7.6, 4.3, 1.2, 1.9],
        font_size=8.6,
    )

    heading(doc, "3. Ai verify ai?")
    table(
        doc,
        [
            ["Người làm", "Người kiểm", "Kiểm gì"],
            ["Minh", "B", "Beta/Delta, coupon, funding cash flow, exact repricing"],
            ["Minh", "C", "2 monthly returns, 96 tháng, ticker/cutoff, data record"],
            ["Minh", "D", "3 claims trọng yếu, page limit 2 trang, wording"],
            ["B", "Minh + D", "Bond math, đơn vị, ngày; memo/slide khớp số"],
            ["C", "Minh + D", "Universe, ETF mandate, nguồn trước 31/12/2022"],
            ["D", "B + C", "15% không mâu thuẫn cash-flow; evidence đủ"],
        ],
        widths=[2.3, 3.4, 11.0],
        font_size=8.7,
    )

    heading(doc, "4. Lịch 18–22/10")
    table(
        doc,
        [
            ["Ngày", "Minh", "B", "C", "D"],
            ["18/10", "Data pack; allocation; đọc PDF", "Đọc PDF/memo; timeline", "Đọc memo; universe", "Rubric; assumptions"],
            ["19/10", "Returns; portfolio; eval rule", "Beta/Delta; funding", "Eligibility; 2 returns", "Draft 2 trang"],
            ["20/10", "Evaluation; freeze; integration", "Bond sheet; rate note", "Benchmark; source", "15%; AI disclosure"],
            ["21/10", "Cross-check; final 2 trang", "Check bond; sign-off", "Check data; sign-off", "Final read; sign-off"],
            ["22/10", "09:00 QA; 15:00 upload; 16:00 deadline", "Có mặt trả lời", "Có mặt trả lời", "Giữ receipt"],
        ],
        widths=[1.3, 5.3, 3.8, 3.8, 2.8],
        font_size=8.4,
    )

    heading(doc, "5. Nếu thiếu thời gian, làm gì trước")
    bullet(doc, "Ưu tiên 1: **đúng 2 trang** + allocation 12m + universe + assumptions + evaluation rule.")
    bullet(doc, "Ưu tiên 2: **bond funding** và **benchmark VTI**; mỗi phần chỉ cần 3 bullet có số.")
    bullet(doc, "Ưu tiên 3: Python chạy được + data record; đừng làm đẹp slide trước 22/10.")
    bullet(doc, "Bỏ qua: white paper dài, extra scenario, factor detail — để sau 22/10.")

    # Page 2
    doc.add_page_break()

    heading(doc, "6. Cấu trúc 2 trang initial record", before=0)
    table(
        doc,
        [
            ["Trang", "Mục", "Nội dung nên có"],
            ["1", "Decision", "1 câu: payment bonds + USMV; tổng 12 triệu USD."],
            ["1", "Allocation", "Beta, Delta, USMV, costs; cộng đúng 12.000.000."],
            ["1", "Universe", "10 mã = 8 stocks + 2 ETFs; 7 sectors; VTI/USMV khác mandate."],
            ["1", "Benchmark", "VTI cho growth; nêu policy benchmark và cách đo."],
            ["2", "Assumptions", "Inflation 2,5%; RF 4%; ERP 4,5%; A=4; costs 5/10bp; zero reinvestment."],
            ["2", "Evaluation", "Jan 2023–Dec 2025; rebalance tháng 12; 10bp mỗi trade."],
            ["2", "Risk", "15% là escalation threshold, không phải guarantee; stress 17,53%."],
            ["2", "Data/AI", "Data record có ngày; AI disclosure; giới hạn dữ liệu."],
        ],
        widths=[1.2, 3.0, 12.6],
        font_size=8.6,
    )

    heading(doc, "7. Checklist trước khi bấm nộp")
    checks = [
        "Đúng **2 trang**, không tràn, không nhét appendix.",
        "Allocation cộng đủ **12.000.000 USD**, gồm costs.",
        "Universe: **10 mã = 8 stocks + 2 ETFs**, 7 sectors; VTI và USMV khác mandate.",
        "Estimation window: **Jan 2015 – Dec 2022**, đúng **96 tháng** common.",
        "Benchmark: **VTI** cho growth; nêu rõ policy benchmark.",
        "Assumptions: inflation 2,5%; RF 4%; ERP 4,5%; A=4; costs 5/10bp; zero reinvestment; no default.",
        "Evaluation rule: **Jan 2023 – Dec 2025**; rebalance tháng 12 về fixed weights; 10bp mỗi lần trade; no terminal liquidation charge.",
        "Python chạy offline từ raw data; có retrieval code và requirements.",
        "Data record có ngày, ticker, settings, versions, hash.",
        "Policy frozen + SHA-256 trước evaluation.",
        "Đủ 4 chữ ký check: Minh, B, C, D.",
        "Receipt nộp bài đã lưu.",
    ]
    for item in checks:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.45)
        p.paragraph_format.first_line_indent = Cm(-0.25)
        p.paragraph_format.space_after = Pt(1.2)
        r = p.add_run("☐  ")
        set_font(r, size=9.5, color=BLUE, bold=True)
        add_text(p, item, size=9.5)

    heading(doc, "8. Năm điều không được làm")
    bullet(doc, "Không đổi **2,4 triệu / 3,6 triệu** hoặc ngày trả.")
    bullet(doc, "Không dùng dữ liệu **sau 31/12/2022** để thiết kế quyết định.")
    bullet(doc, "Không fill missing bằng số bịa, không thay raw data.")
    bullet(doc, "Không nói “đã nộp” khi chưa có receipt.")
    bullet(doc, "Không để quá 2 trang; cắt chữ, không cắt evidence.")

    heading(doc, "9. Điền tên thật trước 18/10")
    table(
        doc,
        [
            ["Vai", "Tên", "Mạnh gì", "Output nhận"],
            ["A", "Minh", "Python, số, tổng hợp", "A1–A5"],
            ["B", "…………", "Excel, đọc đề, cẩn thận", "B1–B3"],
            ["C", "…………", "Đọc tài liệu, ETF, nguồn", "C1–C4"],
            ["D", "…………", "Viết, policy, thuyết trình", "D1–D4"],
        ],
        widths=[1.2, 3.2, 7.0, 4.2],
        font_size=8.7,
    )

    callout(
        doc,
        "**Xong khi:** 2 trang đúng limit + Python chạy được + data record có ngày + policy hash + 4 chữ ký check + receipt. Không xong khi chỉ “đọc thấy ổn”.",
    )

    doc.core_properties.title = "Kappa Foundation — Kế hoạch chia việc 22/10"
    doc.core_properties.author = "Minh"
    doc.core_properties.subject = "BFIN WS2026 initial decision record"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    build(Path(r"docs\KE_HOACH_22_10_2_TRANG.docx"))

