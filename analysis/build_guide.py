from pathlib import Path
import sys,re,html,textwrap
ROOT=Path(__file__).resolve().parents[1]
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Preformatted
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def main():
    src=ROOT/'deliverables/Kappa_Requirements_and_Data_Guide.md'
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='GBody',fontName='Helvetica',fontSize=10.5,leading=15,spaceAfter=9))
    styles.add(ParagraphStyle(name='GTitle',fontName='Helvetica-Bold',fontSize=23,leading=27,spaceAfter=20))
    styles.add(ParagraphStyle(name='GHead',fontName='Helvetica-Bold',fontSize=15,leading=19,spaceBefore=14,spaceAfter=10,keepWithNext=True))
    styles.add(ParagraphStyle(name='GCode',fontName='Courier',fontSize=8,leading=11,spaceAfter=12))
    text=src.read_text(encoding='utf-8');items=[];code=False;buf=[]
    def markup(s):
        s=html.escape(s)
        s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
        s=re.sub(r'`(.+?)`',r'<font name="Courier">\1</font>',s)
        return s
    for block in text.split('\n\n'):
        if block.startswith('```'):
            lines=block.splitlines()[1:-1]
            items.append(Preformatted('\n'.join(lines),styles['GCode']));continue
        if block.startswith('# '):items.append(Paragraph(markup(block[2:]),styles['GTitle']))
        elif block.startswith('## '):items.append(Paragraph(markup(block[3:]),styles['GHead']))
        elif block.startswith('- '):
            for line in block.splitlines():items.append(Paragraph(markup(line[2:]),styles['GBody'],bulletText='-'))
        else:items.append(Paragraph(markup(block.replace('\n',' ')),styles['GBody']))
    def footer(c,d):
        c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#65737e'));c.drawString(48,27,'Kappa Foundation requirements and data guide');c.drawRightString(A4[0]-48,27,str(d.page))
    doc=SimpleDocTemplate(str(src.with_suffix('.pdf')),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=42,bottomMargin=45,
        title='Kappa Foundation requirements and data guide')
    doc.build(items,onFirstPage=footer,onLaterPages=footer)
    print('Data guide generated')
if __name__=='__main__':main()
