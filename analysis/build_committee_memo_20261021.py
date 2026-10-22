from __future__ import annotations

import csv
import html
import json
import math
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverables"
FIG = ROOT / "outputs" / "figures" / "memo_20261021"
TAB = ROOT / "outputs" / "tables"
DEC = ROOT / "outputs" / "decision_review_20261021"
FIG.mkdir(parents=True, exist_ok=True)

NAVY = "#16324F"
TEAL = "#287C7B"
BLUE = "#6C93B8"
GOLD = "#D09A3A"
RED = "#B85C5C"
PALE = "#E8EFF4"
INK = "#243543"
GREY = "#647381"
LIGHT = "#F4F7F9"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
                     "axes.titlesize": 12, "axes.labelsize": 9,
                     "axes.edgecolor": "#B8C4CE", "axes.labelcolor": INK,
                     "xtick.color": GREY, "ytick.color": GREY,
                     "text.color": INK, "grid.color": "#D9E1E7",
                     "figure.facecolor": "white", "axes.facecolor": "white"})

def read_csv(name: str) -> pd.DataFrame:
    return pd.read_csv(TAB / name)

def money_m(x): return f"${x/1e6:,.3f}m"
def pct(x, d=2): return f"{100*x:.{d}f}%"

def chart_allocation():
    fig, ax = plt.subplots(figsize=(8.4, 2.5))
    labels = ["Beta purchase", "Delta purchase", "Growth sleeve", "Execution costs"]
    vals = [2214672, 3429808.6956521743, 6346350.713286715, 9168.591061112802]
    cols = [NAVY, BLUE, TEAL, GOLD]
    left = 0
    for lab, val, col in zip(labels, vals, cols):
        ax.barh([0], [val/1e6], left=left/1e6, height=.52, color=col, label=lab)
        if val > 1e6:
            ax.text((left+val/2)/1e6, 0, f"{lab}\n${val/1e6:.2f}m", ha="center", va="center",
                    color="white", fontsize=8, fontweight="bold")
        left += val
    ax.set_xlim(0, 12); ax.set_ylim(-.55, .55); ax.set_yticks([])
    ax.set_xlabel("Initial resources (USD millions)")
    ax.set_xticks(range(0,13,2)); ax.grid(axis="x", alpha=.65)
    ax.set_axisbelow(True); ax.spines[["top","right","left"]].set_visible(False)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(.5,1.28), frameon=False, fontsize=8)
    fig.tight_layout()
    p=FIG/"capital_allocation.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

def chart_liabilities():
    fig, ax = plt.subplots(figsize=(8.4, 2.8))
    yrs=[2023,2024,2025,2026,2027,2030]
    coupon=121739.13
    inflows=[coupon,coupon,coupon,coupon,3600000,486956.52]
    outflows=[0,2400000,0,0,3600000,0]
    x=np.arange(len(yrs)); w=.34
    ax.bar(x-w/2,np.array(inflows)/1e6,width=w,color=TEAL,label="Dedicated receipts / retained cash")
    ax.bar(x+w/2,np.array(outflows)/1e6,width=w,color=GOLD,label="Mandatory payment")
    ax.set_xticks(x, ["2023","2024","2025","2026","2027","2030"])
    ax.set_ylabel("USD millions"); ax.grid(axis="y",alpha=.65); ax.set_axisbelow(True)
    ax.spines[["top","right"]].set_visible(False)
    ax.legend(frameon=False,ncol=2,loc="upper left",fontsize=8)
    ax.set_title("Contractual payment coverage and surplus coupons",loc="left",fontweight="bold",color=NAVY)
    fig.tight_layout(); p=FIG/"liability_timeline.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

def chart_portfolios():
    df=pd.read_csv(DEC/"growth_candidate_comparison.csv")
    # Reconstruct the long-only efficient frontiers from the saved 2022 inputs.
    import sys
    sys.path.insert(0, str(ROOT / "analysis"))
    import interactive_surplus_portfolio_lab as lab
    _,_,capm,_,sample,sim=lab.load_local_inputs()
    mu=lab.forecast_returns("CAPM",.04,.045,0,0,capm,None)
    from scipy.optimize import minimize
    def frontier(cov):
        low=float(np.min(mu)); high=float(np.max(mu)); pts=[]
        n=len(mu); bounds=[(0,1)]*n
        for target in np.linspace(low,high,50):
            res=minimize(lambda w: float(w@cov@w), np.ones(n)/n, method="SLSQP", bounds=bounds,
                         constraints=[{"type":"eq","fun":lambda w: w.sum()-1},
                                      {"type":"ineq","fun":lambda w,t=target: w@mu-t}],
                         options={"maxiter":600,"ftol":1e-12})
            if res.success: pts.append((math.sqrt(max(0,res.fun))*100,float(res.x@mu)*100))
        return np.array(pts)
    sf=frontier(sample.to_numpy()); inf=frontier(sim.to_numpy())
    names={"100% USMV":"USMV","100% VTI":"VTI","Sample Max Utility A=4":"Sample A=4",
           "Single-index Max Utility A=4":"Index A=4","Sample Max Sharpe":"Sample max Sharpe",
           "Single-index Max Sharpe":"Index max Sharpe","Sample GMV":"Sample GMV",
           "Single-index GMV":"Index GMV","Equal-weight 1/N":"1/N"}
    fig,ax=plt.subplots(figsize=(8.1,4.0))
    if len(sf): ax.plot(sf[:,0],sf[:,1],color=TEAL,lw=2,label="Efficient frontier - sample covariance")
    if len(inf): ax.plot(inf[:,0],inf[:,1],color=BLUE,lw=1.6,ls="--",label="Efficient frontier - single index")
    for _,r in df.iterrows():
        key=names.get(r.portfolio)
        if key is None: continue
        c=TEAL if key in ("USMV","Sample A=4") else (GOLD if key in ("VTI","Index A=4") else BLUE)
        size=100 if key in ("USMV","VTI","Sample A=4","Index A=4") else 58
        ax.scatter(r.annual_volatility*100,r.expected_return*100,s=size,color=c,edgecolor="white",linewidth=.8,zorder=4)
        if key in ("USMV","VTI","Sample A=4","Index A=4","Sample GMV","Index GMV"):
            offsets={"USMV":(7,9),"Sample A=4":(-62,17),"Index A=4":(10,-15),
                     "VTI":(8,7),"Sample GMV":(8,10),"Index GMV":(8,-13)}
            ax.annotate(key,(r.annual_volatility*100,r.expected_return*100),xytext=offsets[key],textcoords="offset points",fontsize=7.5)
    ax.set_xlabel("Forecast annual volatility (sample covariance, %)")
    ax.set_ylabel("CAPM forecast annual arithmetic return (%)")
    ax.set_title("Candidate portfolios at the 31 December 2022 decision date",loc="left",fontweight="bold",color=NAVY)
    ax.grid(alpha=.65); ax.spines[["top","right"]].set_visible(False); ax.set_axisbelow(True)
    ax.legend(frameon=False,fontsize=7.2,loc="upper left")
    ax.text(.99,.02,"Frontiers use each model's covariance estimate. Candidate\npoints use common sample-covariance risk axes for comparability.",
            transform=ax.transAxes,ha="right",va="bottom",fontsize=7,color=GREY)
    fig.tight_layout(); p=FIG/"portfolio_comparison.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

def chart_oos():
    df=pd.read_csv(DEC/"growth_candidate_evaluation_wealth.csv")
    df["month"]=pd.to_datetime(df["month"])
    cols=[("100% USMV","USMV recommendation",TEAL),("100% VTI","VTI benchmark",GOLD),
          ("Sample Max Utility A=4","Sample A=4 candidate",BLUE),
          ("Single-index Max Utility A=4","Single-index A=4",RED),
          ("Historical max Sharpe (Eta)","Historical max-Sharpe rule","#7C6BA8")]
    fig,ax=plt.subplots(figsize=(8.4,3.1))
    for col,label,c in cols:
        if col in df: ax.plot(df.month,df[col],label=label,color=c,lw=2 if col=="Recommended" else 1.55)
    ax.axhline(1,color=GREY,lw=.7)
    ax.set_ylabel("Growth of $1 (before terminal sale)"); ax.set_title("Frozen 2023-2025 out-of-sample comparison",loc="left",fontweight="bold",color=NAVY)
    ax.legend(frameon=False,ncol=2,loc="upper left",fontsize=8); ax.grid(alpha=.6); ax.set_axisbelow(True)
    ax.spines[["top","right"]].set_visible(False); fig.autofmt_xdate(); fig.tight_layout()
    p=FIG/"frozen_evaluation.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

def chart_factor():
    df=read_csv("factor_regressions.csv")
    keys=[("USMV","CAPM"),("USMV","FF3"),("AAPL","CAPM"),("AAPL","FF3"),("MSFT","CAPM"),("MSFT","FF3")]
    rows=[df[(df.security==s)&(df.model==m)].iloc[0] for s,m in keys]
    labels=[f"{s} {m}" for s,m in keys]; y=np.arange(len(rows))
    a=np.array([r.alpha_annual*100 for r in rows]); lo=np.array([r.alpha_low*100 for r in rows]); hi=np.array([r.alpha_high*100 for r in rows])
    fig,ax=plt.subplots(figsize=(8.4,2.9))
    for i,(v,l,h) in enumerate(zip(a,lo,hi)):
        c=TEAL if labels[i].startswith("USMV") else BLUE
        ax.errorbar(v,i,xerr=[[v-l],[h-v]],fmt="o",color=c,ecolor=c,capsize=3,lw=1.3,markersize=4)
    ax.axvline(0,color=RED,lw=1,ls="--"); ax.set_yticks(y,labels); ax.invert_yaxis()
    ax.set_xlabel("Annualized intercept / alpha (%) with 95% HAC interval")
    ax.set_title("Historical alpha is uncertain; FF3 changes exposure estimates",loc="left",fontweight="bold",color=NAVY)
    ax.grid(axis="x",alpha=.6); ax.set_axisbelow(True); ax.spines[["top","right","left"]].set_visible(False)
    fig.tight_layout(); p=FIG/"factor_alpha_intervals.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

def chart_triggers():
    fig,ax=plt.subplots(figsize=(8.4,1.5))
    bands=[(0,10,"Routine monitoring",TEAL),(10,15,"10%: validate + review",BLUE),(15,20,"15%: IC decision",GOLD),(20,30,"20%: notify trustees",RED)]
    for a,b,t,c in bands:
        ax.barh(0,b-a,left=a,height=.48,color=c)
        ax.text((a+b)/2,0,t,ha="center",va="center",color="white",fontsize=7.5,fontweight="bold")
    ax.set_xlim(0,30); ax.set_yticks([]); ax.set_xticks([0,10,15,20,30],["0%","10%","15%","20%","30%"])
    ax.set_xlabel("Peak-to-trough drawdown in unitized growth sleeve")
    ax.spines[:].set_visible(False); ax.grid(axis="x",alpha=.3); ax.set_axisbelow(True)
    fig.tight_layout(); p=FIG/"governance_triggers.png"; fig.savefig(p,dpi=220,bbox_inches="tight"); plt.close(fig); return p

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="KTitle",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=23,leading=27,textColor=colors.HexColor(NAVY),spaceAfter=7))
styles.add(ParagraphStyle(name="KSub",parent=styles["Normal"],fontName="Helvetica",fontSize=10,leading=14,textColor=colors.HexColor(GREY),spaceAfter=7))
styles.add(ParagraphStyle(name="KH1",parent=styles["Heading1"],fontName="Helvetica-Bold",fontSize=15,leading=18,textColor=colors.HexColor(NAVY),spaceBefore=2,spaceAfter=8))
styles.add(ParagraphStyle(name="KH2",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=10,leading=12,textColor=colors.HexColor(TEAL),spaceBefore=7,spaceAfter=4))
styles.add(ParagraphStyle(name="KBody",parent=styles["BodyText"],fontName="Helvetica",fontSize=8.4,leading=11.2,textColor=colors.HexColor(INK),spaceAfter=5))
styles.add(ParagraphStyle(name="KSmall",parent=styles["BodyText"],fontName="Helvetica",fontSize=7.2,leading=9,textColor=colors.HexColor(GREY),spaceAfter=3))
styles.add(ParagraphStyle(name="KCall",parent=styles["BodyText"],fontName="Helvetica-Bold",fontSize=9.4,leading=13,textColor=colors.HexColor(NAVY),backColor=colors.HexColor(PALE),borderPadding=8,spaceBefore=3,spaceAfter=8))
styles.add(ParagraphStyle(name="KCell",parent=styles["BodyText"],fontName="Helvetica",fontSize=7.1,leading=8.7,textColor=colors.HexColor(INK)))
styles.add(ParagraphStyle(name="KCellHead",parent=styles["BodyText"],fontName="Helvetica-Bold",fontSize=7.1,leading=8.7,textColor=colors.white))
styles.add(ParagraphStyle(name="KRef",parent=styles["BodyText"],fontName="Helvetica",fontSize=7.25,leading=9.2,textColor=colors.HexColor(INK),spaceAfter=5))

def P(txt,style="KBody"): return Paragraph(txt,styles[style])
def table(rows,widths,fontsize=7.2,repeatRows=1):
    data=[]
    for i,row in enumerate(rows):
        data.append([P(str(x),"KCellHead" if i==0 else "KCell") for x in row])
    t=Table(data,colWidths=widths,repeatRows=repeatRows,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor(NAVY)),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor(LIGHT)]),
        ("GRID",(0,0),(-1,-1),.35,colors.HexColor("#D3DDE5")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ])); return t

def img(path,width=7.05*inch):
    probe=Image(str(path))
    return Image(str(path),width=width,height=width*probe.imageHeight/probe.imageWidth)

def header(canvas,doc):
    canvas.saveState(); w,h=letter
    canvas.setFillColor(colors.HexColor(NAVY)); canvas.rect(0,h-0.19*inch,w,0.19*inch,fill=1,stroke=0)
    canvas.setFont("Helvetica-Bold",7.3); canvas.setFillColor(colors.HexColor(NAVY)); canvas.drawString(.62*inch,h-.42*inch,"KAPPA FOUNDATION  |  INVESTMENT COMMITTEE MEMORANDUM")
    canvas.setFont("Helvetica",7); canvas.setFillColor(colors.HexColor(GREY)); canvas.drawRightString(w-.62*inch,h-.42*inch,"Original case date: 31 December 2022")
    canvas.setStrokeColor(colors.HexColor("#D3DDE5")); canvas.line(.62*inch,.48*inch,w-.62*inch,.48*inch)
    canvas.setFont("Helvetica",7); canvas.setFillColor(colors.HexColor(GREY)); canvas.drawString(.62*inch,.31*inch,"Decision analysis | Forecasts and policy are assumptions, not guarantees")
    canvas.drawRightString(w-.62*inch,.31*inch,f"{doc.page}")
    canvas.restoreState()

class MemoDoc(BaseDocTemplate):
    def __init__(self,path):
        super().__init__(path,pagesize=letter,leftMargin=.62*inch,rightMargin=.62*inch,topMargin=.63*inch,bottomMargin=.62*inch,
                         title="Kappa Foundation - Investment Committee Memorandum",author="Kappa Foundation Investment Committee")
        f=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id="normal",leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id="all",frames=f,onPage=header)])

def build_story():
    figs=[chart_allocation(),chart_liabilities(),chart_portfolios(),chart_oos(),chart_factor(),chart_triggers()]
    out=[]
    # PAGE 1
    out += [Spacer(1,5),P("Kappa Foundation investment policy","KTitle"),
            P("Committee memorandum | Original mandate | Decision date: 31 December 2022 | Prepared for the 29 October committee submission","KSub"),
            P("Recommendation","KH2"),
            P("Fund the two fixed education payments first with Beta and Delta bonds. Invest the remaining growth capital in USMV as the selected, simple long-only implementation; use VTI as the investable growth benchmark. The allocation seeks to protect obligations and preserve long-run purchasing power; it does not guarantee the 2030 goal or a maximum loss.","KCall"),
            P("Mandate and investment objective","KH1"),
            P("Kappa begins with USD 12.0m, must pay USD 2.4m on 31 December 2024 and USD 3.6m on 31 December 2027, and aims to retain at least USD 8.0m of December-2022 purchasing power by 31 December 2030. The priority is to meet non-cancellable education commitments, then invest surplus capital for real growth within the fund's risk capacity. The fund will not raise risk solely to make a shortfall forecast look attainable."),
            P("Working policy and assumptions","KH2"),
            table([["Decision input","Base convention","Purpose / limit"],
                   ["Goal inflation","CPI 2.5%; HEPI 3.0% separate stress","CPI defines the primary real-goal test; HEPI tests education-cost pressure."],
                   ["Risk preference","A = 4; compare A = 1, 2, 6, 8","Provisional utility preference, not inferred from the 15% trigger."],
                   ["Forecast inputs","CAPM: RF 4.0%, market premium 4.5%, alpha 0","Planning inputs as of the case date; FF3 explains returns, but factor premia are not forecast."],
                   ["Estimation","96 monthly observations, Jan 2015-Dec 2022; 60-month sensitivity","All portfolio weights are formed using information through 31 Dec 2022."],
                   ["Implementation","Long-only; no borrowing, short sales or derivatives; no extra concentration caps","10%/30% caps from an earlier draft were not approved and are excluded."],
                   ["Costs","5bp bonds; 10bp equity; 0% cash reinvestment","Planning friction; lower-fee schedule is reported as a sensitivity."]],
                  [1.18*inch,2.3*inch,3.52*inch]),
            Spacer(1,5),img(figs[0]),
            P("Exhibit 1. Full USD 12m: Beta $2,214,672; Delta $3,429,809; growth sleeve $6,346,351; total assumed execution costs $9,169 ($2,822 bonds and $6,346 equities).", "KSmall"),
            P("The 2.5% CPI planning rate is anchored approximately to the 30 December 2022 nominal Treasury-TIPS spread; it is not a forecast guarantee. HEPI is a separate 3.0% mission-cost stress and may not match Kappa's scholarship cost basket. The nominal 2030 goal is USD 9.747m under CPI and USD 10.134m under HEPI.","KSmall"),PageBreak()]

    # PAGE 2
    out += [P("1 | Fund contractual payments before taking growth risk","KH1"),
            P("The payment portfolio is designed around cash due dates. Beta is a two-year zero-coupon bond. Delta's year-five principal plus final coupon equals the 2027 payment. The Delta coupons are retained as cash and earn 0% in the base case; no coupon is counted twice."),
            table([["Use","Face amount","Purchase cost","Due-date cash flow"],
                   ["Beta","$2,400,000","$2,214,672","$2,400,000 on 31 Dec 2024"],
                   ["Delta","$3,478,261","$3,429,809","$3,600,000 on 31 Dec 2027"],
                   ["Bond fees","-","$2,822","5bp assumed"],
                   ["Total dedicated bonds","$5,878,261","$5,647,303","Both fixed payments covered"]],
                  [1.35*inch,1.28*inch,1.25*inch,3.12*inch]),
            Spacer(1,6),img(figs[1]),P("Exhibit 2. Delta's four coupons before maturity total USD 486,957. They remain separate cash; the 2024 payment is covered by the full USD 2.4m Beta face amount.","KSmall"),
            P("Bond valuation and incomplete curve","KH2"),
            table([["Bond","YTM","Mod. duration","Convexity","+100bp parallel","-100 to +100bp steepener"],
                   ["Beta","4.10%","1.921","5.537","-1.98%","+1.44%"],
                   ["Delta","3.81%","4.499","25.402","-4.56%","-0.48%"],
                   ["Epsilon","3.90%","6.659","54.785","-6.66%","-5.79%"]],
                  [.72*inch,.72*inch,1.0*inch,.9*inch,1.2*inch,2.12*inch]),
            P("Spot discount factors are observed or bootstrapped at years 1, 2, 3, 5 and 8. Log discount factors are interpolated linearly between knots; a separately calibrated linear-zero curve is the interpolation sensitivity. Both curves reproduce the five case quotes. The parallel test shifts every continuous spot rate by +100bp. The curve-shape test moves the one-year rate down 100bp and the eight-year rate up 100bp, linearly by maturity. Exact repricing from contractual cash flows is compared with duration-convexity estimates."),
            P("The +100bp parallel shock is a material late-2022 sensitivity; +200bp is also calculated as a severe stress. A forced early sale or a changed payment date would reintroduce market-price risk. Epsilon is not used to fund near-term liabilities in the base allocation because its longer duration creates interim loss exposure. Curve-shape risk is asymmetric: the steepener raises Beta's price slightly but lowers Delta and Epsilon prices.","KBody"),
            P("Generated evidence: outputs/tables/bond_metrics.csv, bond_curve.csv, bond_stress.csv, ytm_duration_validation.csv and funding_cashflows.csv; calculation in analysis/bonds.py and analysis/supplement.py.","KSmall"),PageBreak()]

    # PAGE 3
    out += [P("2 | Growth allocation: a decision rule, then a portfolio","KH1"),
            P("After bond costs and equity execution costs, the investable growth sleeve is USD 6,346,351 (52.9% of initial resources). Under the primary CPI assumption, the goal requires a 4.84% annual compound return from this sleeve for eight years, plus the retained USD 486,957 coupons. Under the HEPI stress, the growth hurdle rises to 5.37%. These are deterministic hurdles, not forecasts."),
            P("Optimization objective","KH2"),
            P("For the risk-bearing sleeve, compare U = E(Rp) - 0.5 x A x variance(Rp), with A=4 as the working preference and a sensitivity grid around it. This is a transparent risk-return comparison, not a complete model of a university foundation's liabilities. The bond sleeve separately addresses the fixed payment dates. Long-only weights sum to 100%; there are no unapproved single-name or ETF caps."),
            P("Expected return is CAPM: 4.0% prospective risk-free rate + estimated market beta x 4.5% market risk premium. Forecast alpha is zero. Risk is estimated twice: (i) sample covariance of the 96 monthly asset returns, annualized by multiplying covariance by 12, and (ii) a single-index covariance using market betas and idiosyncratic residual variances. The same ten candidates and CAPM means are used for both optimizations."),
            Spacer(1,3),img(figs[2]),P("Exhibit 3. The A=4 portfolios were optimized under separate covariance models. All displayed points use the common sample covariance axes for direct comparison; single-index risk changes the optimization inputs, not the candidate list.","KSmall"),
            P("Selected growth allocation | USMV-only, the approved working policy","KH2"),
            table([["Holding","Weight","USD allocation","Portfolio role"],
                   ["USMV","100.00%","$6,346,351","Diversified US minimum-volatility equity exposure"],
                   ["Total","100.00%","$6,346,351","Long-only; no borrowing or shorting"]],
                  [1.0*inch,.85*inch,1.3*inch,3.65*inch]),
            P("The full-universe A=4 optimizer is a diagnostic, not the selected implementation. Its sample point estimates marginally dominate USMV, with slightly higher expected return and slightly lower volatility, but the certainty-equivalent gain is only about 0.12 percentage points. It adds six direct positions and materially model-sensitive weights. The committee therefore retains the previously selected one-fund policy as a governance choice, while recording the optimizer's result as adverse evidence that should be reconsidered if the weights prove robust.","KSmall"),PageBreak()]

    # PAGE 4
    candidate_stats=pd.read_csv(DEC/"growth_candidate_comparison.csv").set_index("portfolio")
    def stat_row(name,label,rule,weights):
        r=candidate_stats.loc[name]
        return [label,rule,f"{100*r.expected_return:.2f}%",
                f"{100*r.annual_volatility:.2f} / {100*r.single_index_volatility:.2f}",
                f"{r.forecast_sharpe:.2f} / {r.single_index_sharpe:.2f}",
                f"{100*r.utility_at_A:.2f} / {100*r.single_index_utility_A4:.2f}",weights]
    out += [P("3 | Alternatives, covariance sensitivity and implementation","KH1"),
            P("At A=4, expected returns are the same CAPM means in both covariance runs. The table shows volatility, Sharpe and certainty equivalent under sample covariance and single-index covariance, respectively. The sample optimizer's own utility is 3.96%; the single-index optimizer's own utility is 4.29%. Re-scoring the single-index portfolio with sample covariance gives 3.83%. Switching between the two optimized sets changes 18.3% of the sleeve one-way. Expected returns and covariances are uncertain, so the optimizer result is evidence for review rather than an automatic mandate change."),
            table([["Candidate","Model / rule","E(R) CAPM","Vol S/Idx (%)","SR S/Idx","CE S/Idx (%)","Weights"],
                   stat_row("100% USMV","Selected policy","USMV 100%","100% USMV"),
                   stat_row("Sample Max Utility A=4","Optimizer candidate","Sample max utility","USMV 46.2%; VTI 17.9%; 6 stocks"),
                   stat_row("Single-index Max Utility A=4","Model sensitivity","Single-index max utility","USMV 49.6%; VTI 8.3%; 4 stocks"),
                   stat_row("100% VTI","Credible rejected alternative","100% VTI","Broad US market only"),
                   stat_row("Sample GMV","Risk floor reference","Sample GMV","USMV 39.5%; PG 24.2%; JNJ 16.0%"),
                   stat_row("ETF mix VTI 50% / USMV 50%","Simple benchmark mix","50/50 ETF mix","Two ETFs only"),
                   stat_row("Historical max Sharpe (Eta)","Historical rule","Historical max Sharpe","Largest positions NEE 41.3%; MSFT 33.2%")],
                  [.92*inch,1.14*inch,.72*inch,1.03*inch,.75*inch,.9*inch,1.53*inch]),
            P("Columns show annual CAPM forecast return, then sample / single-index volatility (%), Sharpe and A=4 certainty equivalent (%). Both risk models use the same forecast mean vector. The Eta row reports CAPM scores for the historical-Sharpe weights; the weights were formed from 2015-2022 historical average returns relative to French RF. Its 20.38% training CAGR is an in-sample outcome, not a forecast.","KSmall"),
            P("The sample optimizer allocates USMV 46.18%, VTI 17.89%, PG 11.62%, JNJ 7.46%, NEE 7.45%, JPM 3.52%, XOM 2.96% and MSFT 2.92%; AAPL and CAT receive zero. The single-index result holds USMV 49.63%, PG 15.79%, JNJ 15.08%, NEE 10.51%, VTI 8.35% and MSFT 0.64%; the remaining names receive zero. The 60-month sensitivity changes sample A=4 weights by 34.8% one-way, a warning that the optimizer is sensitive to its estimation window."),
            P("VTI is the credible rejected alternative: it offers the higher forecast return and is investable as a simple broad-market fund, but its A=4 certainty equivalent is lower because its modeled variance is higher. The 50/50 ETF mix and GMV portfolio remain useful reference points, not additional recommendations."),
            P("Why the covariance estimate matters","KH2"),
            P("The sample model estimates all pairwise relationships directly. The single-index model assumes common co-movement is mostly explained by the market and treats residual covariance as zero. The different weights and 18.3% model-switch turnover are material enough to monitor, but they do not outweigh the policy preference for a simple defensive implementation. No extra stock/ETF caps were imposed; long-only, fully invested weights are the assignment constraints."),
            P("Implementation: rebalance only after an authorized annual review or a documented drift/funding event. The original decision is frozen at 31 December 2022; use the same weights for the 2023-2025 evaluation. No extra caps, turnover bands or automatic sales are assumed unless separately approved.","KSmall"),
            P("Generated evidence: outputs/decision_review_20261021/growth_candidate_comparison.csv and growth_candidate_weights.csv; original candidate universe and source returns are retained under data/raw and outputs/tables.","KSmall"),PageBreak()]

    # PAGE 5
    out += [P("4 | Market and factor evidence: exposure is not alpha","KH1"),
            P("The selected growth sleeve is 100% USMV, so its USMV regressions below are also the growth-portfolio regressions. CAPM gives a market-only account; FF3 adds size (SMB) and value (HML) exposures. AAPL and MSFT are two selected candidate securities reviewed alongside the ETF, not direct holdings in the chosen allocation. All models use 96 monthly excess returns ending in December 2022 and three-lag HAC standard errors."),
            Spacer(1,3),img(figs[4]),P("Exhibit 4. Alpha estimates with 95% HAC confidence intervals. AAPL and MSFT intervals are wide; a positive point estimate is not proof of persistent skill.","KSmall"),
            table([["Security / model","Market beta","SMB beta","HML beta","Annual alpha (95% interval)","Alpha p"],
                   ["USMV CAPM","0.70","-","-","2.17% (-1.81, 6.15)","0.285"],
                   ["USMV FF3","0.74","-0.30","-0.05","1.49% (-2.09, 5.06)","0.415"],
                   ["AAPL CAPM","1.21","-","-","12.13% (-1.57, 25.84)","0.083"],
                   ["AAPL FF3","1.27","-0.29","-0.54","11.04% (-1.53, 23.62)","0.085"],
                   ["MSFT CAPM","0.96","-","-","14.47% (4.36, 24.59)","0.005"],
                   ["MSFT FF3","1.06","-0.62","-0.36","12.81% (4.54, 21.08)","0.002"]],
                  [1.12*inch,.72*inch,.63*inch,.63*inch,2.55*inch,.7*inch]),
            P("For USMV, FF3 raises R-squared from 0.805 to 0.848 and identifies negative SMB exposure; its alpha remains statistically indistinguishable from zero. For AAPL and MSFT, FF3 adds negative SMB and HML loadings. MSFT's positive in-sample alpha is statistically significant under both fitted models, but it was selected after screening a small survivor universe and can reflect omitted exposures, model selection or chance. Forecast alpha remains zero rather than extrapolating any of these intercepts."),
            P("The model therefore uses CAPM betas for expected-return inputs and FF3 for explanation and challenge. SMB/HML premia are not inserted into the forecast because the policy has not fixed defensible prospective factor premia. Factor regressions do not establish that a security will earn abnormal returns in the next period; they describe covariance with historical factor portfolios."),
            P("Universe limitation: eight US stocks and VTI/USMV were selected for data continuity and mandate coverage. They are not a point-in-time investable universe; later-known survivors can bias historical comparison. No 2023-2025 performance was used to select the 2022 weights. Factor data are the saved Kenneth French vintage, scaled from percent to decimal; Yahoo adjusted close is used once for total-return construction, with no second dividend addition.","KSmall"),
            P("Generated evidence: outputs/tables/factor_regressions.csv, alpha_stability.csv, expected_return_inputs.csv and train_data_quality.csv; analysis/analyze.py and analysis/verify_factor_portfolio.py.","KSmall"),PageBreak()]

    # PAGE 6
    out += [P("5 | Frozen out-of-sample evidence, 2023-2025","KH1"),
            P("The original allocation was fixed using data through 2022. This section tests those frozen weights using 36 monthly observations from January 2023 through December 2025. The portfolio starts with a 10bp entry-cost assumption; VTI is charged the same assumed entry friction. No 2023-2025 information feeds back into the original selection."),
            Spacer(1,3),img(figs[3]),P("Exhibit 5. Wealth paths start at USD 0.999 after the assumed 10bp entry cost; annual rebalance friction is included. Adjusted prices include distributions. The figure is retrospective, not evidence available at the decision date.","KSmall"),
            table([["Frozen strategy","Cumulative return","CAGR","Annual vol.","Sharpe","Month-end max DD"],
                   ["Recommended USMV","37.33%","11.15%","9.64%","0.66","-5.66%"],
                   ["VTI benchmark","82.56%","22.22%","12.54%","1.30","-9.11%"],
                   ["Sample A=4 optimizer","43.37%","12.76%","9.94%","0.79","-6.53%"],
                   ["Single-index A=4","32.47%","9.83%","10.59%","0.50","-6.89%"],
                   ["Eta historical Sharpe","55.59%","15.88%","15.15%","0.74","-13.90%"]],
                  [1.5*inch,1.12*inch,.68*inch,.78*inch,.55*inch,1.3*inch]),
            P("The convenient result is that USMV had a smaller month-end drawdown and lower volatility than VTI. The inconvenient result is that it lagged VTI's cumulative return by 45.23 percentage points and its Sharpe ratio by 0.64. The sample A=4 optimizer and Eta also beat USMV over this particular window, while the single-index optimizer lagged it. None of these results proves that a rule will persist or justifies choosing it with hindsight."),
            P("Decision implication: the evaluation supports the risk trade-off but rejects any claim of benchmark outperformance. It is too short to establish a full market-cycle result; month-end data miss intramonth losses; the present-day survivor universe and revised vendor histories remain limitations. Continue the selected policy only while the liability funding, risk preference and mandate remain valid. Underperformance triggers diagnosis and review, not automatic risk-taking to catch up."),
            P("Generated evidence: outputs/decision_review_20261021/growth_candidate_comparison.csv, growth_candidate_weights.csv and growth_candidate_evaluation_wealth.csv; analysis/compare_growth_options_20261021.py. The separate original evaluation tables remain available for audit, but this comparison uses one common no-cap universe, rebalance rule and entry-cost convention.","KSmall"),PageBreak()]

    # PAGE 7
    out += [P("6 | Risk limits, stress and governance","KH1"),
            P("The 15% concern applies primarily to the growth sleeve's cash-flow-adjusted, unitized total-return drawdown from its prior high-water mark. A drawdown trigger starts a review; it is not a promise that losses stop at that number. Because equity prices can gap, a stop order cannot guarantee a 15% economic-loss floor."),
            img(figs[5]),
            table([["Signal","Required response","Trading rule"],
                   ["10% growth-sleeve drawdown","Within 2 business days, validate prices, distributions, unitization, cash flows, payment coverage, stress and goal funding; report to IC.","No automatic trade."],
                   ["15% drawdown","IC meets within 5 business days; records hold, a separately pre-authorized rebalance, or a prospective policy change for trustees.","No automatic full sale."],
                   ["20% drawdown","Notify trustees same or next business day; pause discretionary risk increases pending review; record funding, owner and next review.","No automatic liquidation."],
                   ["Payment shortfall risk","Escalate immediately, regardless of drawdown; prepare a dated funding plan and restore due-date coverage through authorized action.","Do not wait for 10/15/20%."]],
                  [1.25*inch,4.35*inch,1.35*inch]),
            P("Use month-end unit values for academic replication; operational monitoring may be weekly if reliable prices and cash-flow records are available. External contributions and withdrawals are unitized so payments do not masquerade as investment losses. Whole-fund stress and liability coverage are reported separately."),
            P("Upside rule","KH2"),
            P("At each annual review, first reconfirm payment coverage and the CPI-based 2030 goal. Apply a -30% shock to the remaining growth sleeve using current executable prices and permitted assets. If the goal remains funded after that shock, transfer only the minimum amount required into an eligible asset matched to the goal date; keep surplus under the growth policy. If the test fails, disclose the dollar gap and required return; do not raise risk solely to catch up. No fixed gain triggers a sale."),
            P("Any crisis deferral of discretionary action requires written approval from the authorized body, a reason, an expiry date and review schedule. It cannot reduce coverage for a payment already due. Instrument eligibility and valuation convention for goal protection require formal approval before implementation.","KBody"),
            P("Source: user-selected working IPS rules recorded in policy/IPS_addendum_selected_drawdown_rules_2026-10-21.json; these are proposed group policy, not trustee authorization.","KSmall"),PageBreak()]

    # PAGE 8
    out += [P("7 | Sensitivity, reversal point and committee monitoring","KH1"),
            P("A decision should change when a key input changes enough to alter the trade-off, not when a noisy monthly return changes sign. One transparent reversal threshold comes from the two ETF utility comparison. Under the saved CAPM means and sample covariance, USMV has higher A=4 certainty equivalent than VTI. The ranking reverses at A approximately 2.58: below that preference parameter, VTI's higher return outweighs its higher variance. At A=4, raising the assumed market risk premium above approximately 6.98% also reverses the two-ETF ranking. These thresholds are model-specific and are not policy commands."),
            table([["Sensitivity","Base","Stress / threshold","Implication"],
                   ["Inflation / goal","CPI 2.5%; nominal goal $9.747m","HEPI 3.0%; goal $10.134m; hurdle 5.37%","Recalculate real-goal funding; do not blend indices."],
                   ["Risk preference","A=4","A<2.58 favors VTI over USMV","Trustees must define risk preference; drawdown triggers do not estimate A."],
                   ["Market risk premium","4.5%","Above 6.98% reverses USMV/VTI at A=4","Revisit expected returns only with an evidence-based premium."],
                   ["Training window","96 months","60-month A=4 weight turnover 34.8% one-way","Optimizer weights are sensitive; preserve simple benchmark and governance."],
                   ["Costs","5bp bonds / 10bp equity","0bp bonds / 5bp ETF / 10bp direct equity","Lower fee schedule raises growth capital by about $5,992; ranking unchanged."],
                   ["Stress path","Base goal path","Immediate -30% growth shock raises remaining CAGR hurdle to about 9.6%","Protect obligations first; diagnose market-wide shock vs portfolio underperformance."]],
                  [1.08*inch,1.4*inch,2.15*inch,2.32*inch]),
            P("Committee monitoring after implementation","KH2"),
            P("Each quarter, report dated payment coverage, cash and coupon reconciliation, growth-sleeve drawdown, current weights, benchmark-relative return, costs, mandate changes and the CPI goal funding ratio. At the annual review, refresh expected returns only from approved inputs, compare sample and single-index risk, test current liabilities and run the -30% goal-protection test. For underperformance, separate broad-market conditions, strategy/benchmark mismatch, asset-specific evidence, data errors and implementation costs before changing the portfolio."),
            P("Evidence against the recommendation must remain visible: the sample optimizer marginally dominates USMV on point estimates, VTI outperformed over 2023-2025, Eta's historical-Sharpe strategy also had a stronger period return, and the 60-month sensitivity changes optimized weights substantially. The favorable evidence is the lower estimated volatility and better A=4 utility than a VTI-only allocation, plus the payment bonds' contractual cash-flow coverage. The choice is therefore a reviewable governance judgment, not the model's numerical maximum and not a claim that future returns are known."),
            P("Data and record status","KH2"),
            P("The assignment is retrospective, not a live investment experiment. Yahoo Finance and Kenneth French files were downloaded after the case date, with raw bytes, retrieval settings, versions and hashes retained. Historical data vintages may have been revised. The original candidate universe is selected with hindsight risk. The actual 23 October revised mandate is not yet available as of this memo's preparation; apply it in a separate version while preserving the 2022 decision and the frozen 2023-2025 evaluation. AI-assisted analysis requires student source checks, genuine contribution statements and compliance with course AI rules before submission.","KBody"),
            P("This memorandum is an academic case analysis; it is not an investment offer or a guarantee of returns, goal achievement or a loss ceiling.","KSmall"),PageBreak()]

    # PAGE 9 references
    out += [P("References and audit trail","KH1"),
            P("Assignment and case data","KH2"),
            P("[1] BFIN-WS2026 Group Assignment, supplied course document. Contractual payment dates and amounts, bond quotes, initial resources, candidate-selection and analysis requirements, 2022 decision cutoff, and 2023-2025 evaluation period." ,"KRef"),
            P("Data sources and construction","KH2"),
            P("[2] Yahoo Finance price and corporate-action history accessed through yfinance. Retrieval settings and raw file hashes are in data/raw/retrieval_manifest.jsonl. Monthly returns use last-trading-day adjusted closes; dividends are not added again. [3] yfinance download API documentation: https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html.","KRef"),
            P("[4] Kenneth R. French Data Library, Fama/French monthly factors and U.S. research returns: https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html. Original saved ZIP bytes are in data/raw/factors/. Percent units are converted to decimals before regression.","KRef"),
            P("[5] Federal Reserve, Summary of Economic Projections, 14 December 2022: https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20221214.htm. [6] Federal Reserve Bank of St. Louis FRED, 10-year Treasury inflation-indexed security and nominal constant-maturity series; the 30 December 2022 spread is an approximate market-implied CPI planning anchor, not an unbiased forecast. https://fred.stlouisfed.org/series/T10YIE.","KRef"),
            P("[7] Commonfund Institute, Higher Education Price Index (HEPI), annual historical series: https://www.commonfund.org/hepi. HEPI is used as a separate mission-cost stress; the 3.0% planning value is an assumption.","KRef"),
            P("Instrument and eligibility references","KH2"),
            P("[8] Vanguard Total Stock Market ETF (VTI), summary prospectus filed with the SEC before the decision date: https://www.sec.gov/Archives/edgar/data/36405/000168386320005993/f4654d1.htm. [9] iShares MSCI USA Min Vol Factor ETF (USMV), contemporaneous SEC-filed description: https://www.sec.gov/Archives/edgar/data/886982/000156459022026948/gs-424b2.htm. Direct Python SEC requests returned HTTP 403; the links and concise eligibility notes are retained in data/raw/supporting/source_register.json. Full SEC documents were not saved locally.","KRef"),
            P("[10] SISF Global Multi-Asset Income Fund A Acc, factsheet dated 21 September 2026, provided by the user. Used only as a visual-reference example for information hierarchy and chart/table clarity; no SISF performance, allocation or product facts are used as Kappa evidence.","KRef"),
            P("Calculation trail","KH2"),
            P("Bond valuation and cash-flow schedules: analysis/bonds.py and analysis/supplement.py. Return and factor analysis: analysis/analyze.py. Source-byte and equation checks: analysis/verify_source_chain.py and analysis/verify_core_equations.py. Candidate portfolio comparisons: analysis/compare_growth_options_20261021.py and outputs/decision_review_20261021/. The report's tables cite named CSV/JSON files at the end of each relevant page. Run analysis/rebuild.py offline to regenerate canonical figures and checks; run analysis/build_committee_memo_20261021.py to rebuild this memo from saved tables.","KRef"),
            P("Disclosure","KH2"),
            P("AI tools assisted with source discovery, scripting, calculations and drafting. Automated checks establish repeatability and arithmetic consistency, not investment judgment, data completeness, course-policy compliance or students' individual contributions. The group must review source records and record actual work and independent checks before submission.","KRef")]
    return out,figs

def markdown_text(s):
    s=re.sub(r"<br\s*/?>"," ",s,flags=re.I)
    s=re.sub(r"</?(b|i|u|font|super|sub)[^>]*>","",s,flags=re.I)
    return html.unescape(s).replace("|","\\|").strip()

def write_editable_markdown(story,path):
    chunks=["# Kappa Foundation investment policy\n\nCommittee memorandum | Original mandate | Decision date: 31 December 2022\n"]
    page=1; chunks.append(f"\n## Page {page}\n")
    for flow in story:
        if isinstance(flow,PageBreak):
            page+=1; chunks.append(f"\n## Page {page}\n")
        elif isinstance(flow,Paragraph):
            txt=markdown_text(flow.text)
            if flow.style.name in ("KH1","KH2"):
                chunks.append(f"\n### {txt}\n")
            elif flow.style.name=="KTitle":
                chunks.append(f"\n# {txt}\n")
            elif flow.style.name=="KCall":
                chunks.append(f"\n> {txt}\n")
            else:
                chunks.append(f"\n{txt}\n")
        elif isinstance(flow,Table):
            rows=[]
            for row in flow._cellvalues:
                vals=[]
                for cell in row:
                    vals.append(markdown_text(cell.text) if isinstance(cell,Paragraph) else markdown_text(str(cell)))
                rows.append(vals)
            if rows:
                chunks.append("\n| "+" | ".join(rows[0])+" |\n")
                chunks.append("| "+" | ".join(["---"]*len(rows[0]))+" |\n")
                for row in rows[1:]: chunks.append("| "+" | ".join(row)+" |\n")
        elif isinstance(flow,Image):
            name=Path(flow.filename).name
            chunks.append(f"\n![{name}](../outputs/figures/memo_20261021/{name})\n")
    path.write_text("\n".join(chunks),encoding="utf-8")

def main():
    story,_=build_story()
    dest=OUT/"Kappa_Committee_Memo.pdf"
    write_editable_markdown(story,OUT/"Kappa_Committee_Memo_Editable.md")
    doc=MemoDoc(str(dest)); doc.build(story)
    print(dest)
    print(json.dumps({"pages":doc.page,"charts":6,"output_bytes":dest.stat().st_size},indent=2))

if __name__=="__main__": main()
