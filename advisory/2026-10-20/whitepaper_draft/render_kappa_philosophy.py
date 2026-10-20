from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import re

root = Path(__file__).resolve().parent
lines = (root / 'Kappa_One_Page_Investment_Philosophy.md').read_text(encoding='utf-8').splitlines()
dest = root / 'Kappa_One_Page_Investment_Philosophy.pdf'
doc = SimpleDocTemplate(str(dest), pagesize=A4, leftMargin=42, rightMargin=42, topMargin=34, bottomMargin=32, title='Kappa Investment Philosophy - Discussion Draft')
title = ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=15, leading=18, textColor=colors.HexColor('#15324b'), spaceAfter=4)
subtitle = ParagraphStyle('subtitle', fontName='Helvetica', fontSize=8.2, leading=10, textColor=colors.HexColor('#607386'), spaceAfter=9)
body = ParagraphStyle('body', fontName='Helvetica', fontSize=8.65, leading=11.3, textColor=colors.HexColor('#172332'), spaceAfter=6.5)
foot = ParagraphStyle('foot', parent=body, fontSize=7.6, leading=9.3, spaceBefore=1, spaceAfter=0)

def markup(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = re.sub(r'\[([^]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#205b8a">\1</link>', s)
    return re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)

story = []
for line in lines:
    if not line.strip():
        continue
    if line.startswith('# '):
        story.append(Paragraph(markup(line[2:]), title))
    elif line.startswith('**Discussion'):
        story.append(Paragraph(markup(line), subtitle))
    else:
        story.append(Paragraph(markup(line), foot if line.startswith('**Evidence:') else body))
doc.build(story)
print(dest)
