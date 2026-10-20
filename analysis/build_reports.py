"""Create the committee memo and initial decision record from named outputs."""
from pathlib import Path
import sys,json,html
ROOT=Path(__file__).resolve().parents[1]
if (ROOT.parent/'.analysis_packages').exists():sys.path.insert(0,str(ROOT.parent/'.analysis_packages'))
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True)
T=ROOT/'outputs/tables';F=ROOT/'outputs/figures'
fund=json.loads((T/'funding_summary.json').read_text());dec=json.loads((T/'decision_summary.json').read_text())
ab=json.loads((T/'all_bond_summary.json').read_text());sim=pd.read_csv(T/'mission_simulation.csv').set_index('strategy')
port=pd.read_csv(T/'portfolio_candidates.csv').set_index('strategy');reg=pd.read_csv(T/'factor_regressions.csv').set_index(['security','model'])
ev=pd.read_csv(T/'evaluation_performance.csv').set_index('strategy');bond=pd.read_csv(T/'bond_metrics.csv')
retrieval=json.loads((ROOT/'data/raw/retrieval_manifest.jsonl').read_text().splitlines()[0])['recorded_utc']
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyK',fontName='Helvetica',fontSize=10.6,leading=14.6,spaceAfter=8,textColor=colors.HexColor('#202b34')))
styles.add(ParagraphStyle(name='SmallK',parent=styles['BodyK'],fontSize=8.2,leading=11,spaceAfter=5,textColor=colors.HexColor('#52606b')))
styles.add(ParagraphStyle(name='TitleK',fontName='Helvetica-Bold',fontSize=24,leading=28,spaceAfter=16,textColor=colors.black))
styles.add(ParagraphStyle(name='HeadK',fontName='Helvetica-Bold',fontSize=16,leading=20,spaceAfter=12,textColor=colors.black))
styles.add(ParagraphStyle(name='SubK',fontName='Helvetica-Bold',fontSize=11,leading=14,spaceBefore=4,spaceAfter=7,textColor=colors.black))
styles.add(ParagraphStyle(name='CellK',fontName='Helvetica',fontSize=9,leading=12))
styles.add(ParagraphStyle(name='CellHeadK',fontName='Helvetica-Bold',fontSize=9,leading=12,textColor=colors.white))

def p(text,kind='BodyK'):return Paragraph(text,styles[kind])
def table(headers,rows,widths=None):
    vals=[[p(str(v),'CellHeadK') for v in headers]]+[[p(html.escape(str(v)),'CellK') for v in row] for row in rows]
    tb=Table(vals,colWidths=widths,repeatRows=1,hAlign='LEFT')
    tb.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#18394d')),
       ('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
       ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
       ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f4f5')]),
       ('LINEBELOW',(0,-1),(-1,-1),.5,colors.HexColor('#c4cdd2'))]))
    return tb
def pct(x,d=2):return f'{x*100:.{d}f}%'
def money(x):return f'${x:,.0f}'
def image(name,w=490,h=None):
    from PIL import Image as PI
    with PI.open(F/name) as im:iw,ih=im.size
    return Image(str(F/name),width=w,height=h or w*ih/iw)
def src(text):return p('Generated evidence: '+text,'SmallK')
def footer(canvas,doc):
    canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#65737e'))
    canvas.drawString(48,27,'Kappa Foundation  |  Case decision 31 December 2022')
    canvas.drawRightString(A4[0]-48,27,str(doc.page))
def build(name,pages):
    flow=[]
    for i,page in enumerate(pages):
        if i:flow.append(PageBreak())
        flow+=page
    doc=SimpleDocTemplate(str(OUT/name),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=42,bottomMargin=45,
       title=name.replace('_',' ').replace('.pdf',''),author='Kappa independent investment team - AI-assisted preparation')
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
    return len(PdfReader(OUT/name).pages)

def main():
    allocation=[['Beta',f"${fund['beta_cost']:,.2f}",'18.46%','2,400 bonds; USD 2.4m face'],
        ['Delta',f"${fund['delta_cost']:,.2f}",'28.58%','3,478.26087 bonds; USD 3.478m face'],
        ['USMV',f"${fund['equity_investment']:,.2f}",'52.89%','Growth allocation'],
        ['Execution costs',f"${fund['total_fees']:,.2f}",'0.08%','5bp bonds and 10bp equities'],
        ['Total','$12,000,000','100.00%','Rounding affects displayed percentages']]
    pages=[]
    pages.append([
      p('Kappa Foundation investment policy','TitleK'),
      p('Committee memorandum for the original mandate','SubK'),
      p('<b>Recommendation.</b> Ring-fence both contractual payments with Beta and Delta, and invest the residual growth capital in USMV. Use VTI as the growth benchmark. Authorize this policy only with a clear acknowledgement that the 2030 real-value objective is aspirational and a 15% investment-loss ceiling cannot be promised.'),
      table(['Use of funds','Initial USD','Share','Implementation'],allocation,[73,94,58,274]),
      Spacer(1,10),p('Why this allocation','SubK'),
      p('The bonds pay the obligations without relying on equity sales, future bond prices, or positive reinvestment rates. USMV provides diversified US equities with lower estimated market sensitivity than VTI. The policy benchmark combines the dedicated payment cash flows with VTI for growth. Individual stocks remain research candidates; the evidence does not justify initial direct holdings.'),
      p(f'At 2.5% annual inflation, the terminal objective is {money(fund["nominal_goal"])} in December 2030. After preserving surplus coupons as cash, the equity sleeve needs {pct(fund["required_equity_cagr"])} compound annual growth. Our expected return assumption is {pct(dec["forecast_return"])} arithmetic, which is not directly comparable with that compound hurdle.'),
      p(f'The specified scenario model reaches the real goal in {pct(sim.loc["USMV","probability_goal"],1)} of paths. A 31.5% modeled shortfall frequency is material. This estimate conditions on a small historical sample and uncertain forecasts; it is not a calibrated success guarantee.'),
      p('The policy accepts a monitoring threshold rather than a hard loss constraint. A stricter requirement would call for a smaller equity allocation, a lower terminal goal, or new funding. The all-bond alternative on page 8 quantifies a feasible compromise.'),
      src('initial_allocation.csv; funding_summary.json; mission_simulation.csv. Original case only. The revised mandate due 23 October 2026 is not yet available.')])
    pages.append([
      p('Payment funding and purchasing power','HeadK'),
      p('Beta is a zero-coupon bond. Buying USD 2.4 million face costs USD 2,214,672 and delivers exactly USD 2.4 million in year 2. Delta pays 3.5% annually. Buying USD 3,478,260.87 face makes its final coupon plus principal equal USD 3.6 million in year 5.'),
      table(['Date','Dedicated receipt','Required payment','Surplus to cash'],[
        ['31 Dec 2023','Delta coupon $121,739','$0','$121,739'],
        ['31 Dec 2024','Beta $2.4m + Delta coupon','$2,400,000','$121,739'],
        ['31 Dec 2025','Delta coupon $121,739','$0','$121,739'],
        ['31 Dec 2026','Delta coupon $121,739','$0','$121,739'],
        ['31 Dec 2027','Delta final payment $3.6m','$3,600,000','$0'],
        ['31 Dec 2030','Accumulated surplus coupons','$0','$486,957 retained']],[90,166,111,132]),
      Spacer(1,9),p('Assumptions that determine feasibility','SubK'),
      p('Hold dedicated bonds to their payment dates. Treat the contractual receipt as available before the same-day programme payment, as the case requires. Confirm settlement and payment instructions in implementation. Keep years 1-4 coupons in segregated USD cash, earning zero in the base case. The USD 6 million outflow is programme spending, not an investment loss.'),
      p('Adopt 2.5% as a planning inflation rate for the foundation\'s purchasing power, not as a statistical forecast of its education costs. The December 2022 Federal Reserve projections anticipated PCE inflation of 3.1%, 2.5% and 2.1% for 2023-2025 and 2.0% in the long run [3]. The choice adds a planning margin to long-run PCE, but education costs and CPI may differ. Test 2%-5% inflation.'),
      table(['Constant inflation','2030 nominal target','Required equity CAGR'],[
        ['2.0%','$9.373m','4.30%'],['2.5%','$9.747m','4.84%'],['4.0%','$10.949m','6.45%'],['5.0%','$11.820m','7.52%']],[135,185,179]),
      Spacer(1,8),p('A cheaper earmarking structure uses the first two Delta coupons to help pay the scholarship, freeing about USD 224,565 for equities. We reject it initially because separate payment rings simplify operational control. This conservatism has a measurable opportunity cost, shown in funding_alternatives.csv.'),
      src('funding_cashflows.csv; goal_sensitivity.csv; funding_alternatives.csv. Formula: equity*(1+g)^8 + surplus cash = 8m*(1+inflation)^8.')])
    bondrows=[[r.bond,pct(r.ytm),f'{r.modified_duration:.3f}',f'{r.yield_convexity:.3f}'] for _,r in bond.iterrows()]
    pages.append([
      p('Bond valuation and interest rate risk','HeadK'),
      p('Solve each annual-compounding yield from the stated price and contractual cash flows. YTM is an internal rate of return, not a spot rate for every cash flow. Zero accrued interest makes the quoted clean and dirty prices identical.'),
      table(['Bond','YTM','Modified duration','Yield convexity'],bondrows,[100,100,150,149]),
      Spacer(1,9),p('The incomplete curve','SubK'),
      p('Bootstrap discount factors at years 1, 2, 3, 5 and 8. Interpolate log discount factors linearly between the observed maturity knots, which imposes constant forward rates within each segment. Solve each unknown maturity discount factor so the entire coupon bond reprices exactly. This is an explicit interpolation assumption, not a uniquely identified market curve. A separately recalibrated linear-zero-rate curve checks sensitivity.'),
      p('The curve reproduces all five prices to less than USD 0.0000001. Parallel continuous-spot shifts use cash-flow-weighted duration and convexity. The standard YTM duration figures above are checked separately against exact YTM repricing; they are not substituted into the curve-shape stress.'),
      table(['Instrument','+100bp parallel','-100bp parallel','Steepener'],[
        ['Beta','-1.98%','+2.02%','+1.44%'],['Delta','-4.56%','+4.79%','-0.48%'],['Epsilon','-6.66%','+7.19%','-5.79%']],[110,130,130,129]),
      Spacer(1,8),p('The steepener shifts the one-year continuous spot rate down 100bp and the eight-year rate up 100bp, linearly by maturity. The 100bp shocks are deliberately material sensitivity tests in the high-rate uncertainty of late 2022; +200bp is a more severe stress. They are not assigned probabilities. At +100bp, the largest duration-convexity pricing error is only USD 0.069 per bond, but errors grow with shock size.'),
      p('The payment reserve loses about USD 200,255 in market value after a +100bp shift, while its promised cash receipts remain unchanged. Thus mark-to-market risk and payment funding risk differ. Epsilon is useful for a fixed nominal terminal goal but introduces greater interim interest-rate exposure and coupon reinvestment dependence.'),
      src('bond_metrics.csv; bond_curve.csv; bond_stress.csv; ytm_duration_validation.csv; curve_interpolation_sensitivity.csv.')])
    pages.append([
      p('Eligible universe and data design','HeadK'),
      table(['Candidate','Sector or mandate','Economic role'],[
        ['AAPL, MSFT','Information Technology','Devices, enterprise software and cloud'],
        ['JPM','Financials','Credit cycle and banking'],['JNJ','Health Care','Defensive demand'],['PG','Consumer Staples','Staples demand and pricing'],
        ['XOM','Energy','Oil and inflation exposure'],['CAT','Industrials','Capital expenditure cycle'],['NEE','Utilities','Regulated utility and rate sensitivity'],
        ['VTI','Broad US equities','Investable benchmark'],['USMV','US minimum volatility','Defensive growth candidate']],[90,155,254]),
      Spacer(1,9),p('Eight common stocks span seven sectors. Pre-cutoff SEC filings identify their security class and US exchange listing. VTI has a pre-cutoff prospectus. A July 2022 SEC-filed disclosure documents USMV\'s mandate and listing. The source register links the exact resources. This discretionary universe contains present-day survivors; dated eligibility evidence does not remove selection or survivorship bias.'),
      p('Use January 2015-December 2022: 96 common monthly observations. This balances sample size with recent regimes, including the pandemic and 2022 inflation shock, but omits the global financial crisis. A 60-month 2018-2022 sensitivity retains the same universe. December 2014 prices supply only the January 2015 return denominator.'),
      p('Yahoo data were retrieved in Python with yfinance. Daily frequency is the download granularity; every model uses monthly returns calculated from the last trading day\'s adjusted close. Settings explicitly disable auto-adjustment, back-adjustment and repair while retaining actions and missing values. Adjusted close incorporates Yahoo\'s corporate-action treatment. Dividends are not added a second time. No missing returns were filled or removed.'),
      p('Kenneth French\'s monthly FF3 ZIP supplies Mkt-RF, SMB, HML and RF. Divide all four series by 100, align by calendar month, and subtract RF once from security returns. VTI is an investable benchmark; French\'s market factor is an explanatory research series. They need not agree. Current French files use revised historical data and the post-2024 CRSP methodology [2].'),
      p(f'Raw retrieval began {retrieval[:10]}. The archive retains the untouched download tables, ZIP bytes, hashes, settings and package versions. Direct SEC requests returned 403; official documents were checked through web access, with that limitation recorded. Source summaries are clearly distinguished from full saved documents.'),
      src('train_data_quality.csv; train_corporate_actions.csv; data/raw/retrieval_manifest.jsonl; data/raw/supporting/eligibility_checks.json; download_overlap_comparison.csv.')])
    rows=[]
    for name in ['Sample_A4','Single_index_A4','Eta_historical_Sharpe']:
        q=port.loc[name];rows.append([name.replace('_',' '),pct(q.forecast_return),pct(q.sample_vol),pct(q.index_vol)])
    pages.append([
      p('Portfolio choice and robustness','HeadK'),
      p('Forecast each asset\'s annual arithmetic return as 4.0% + beta x 4.5%. Betas come from 2015-2022 excess returns against the French market factor. The 4% planning base is close to case bond yields but is not an eight-year guaranteed cash reinvestment rate. The 4.5% market premium is a judgement input, tested at 2.5%-6.5%. Set forecast alpha to zero. Do not extrapolate the exceptional historical returns of selected technology stocks.'),
      p('Compare annual certainty equivalents CE = expected return - A x variance / 2 on the growth sleeve. With A = 4, USMV scores 3.84% and VTI 3.13%. A is an assumed preference parameter, not an estimate from the trustees\' vague 15% concern. A below 2.58 reverses this choice in favour of VTI; at A = 4, a market premium above 6.98% also reverses it.'),
      table(['Risk preference A','USMV CE','VTI CE','Preferred'],[
        ['1','6.32%','7.12%','VTI'],['2','5.49%','5.79%','VTI'],['4','3.84%','3.13%','USMV'],['8','0.55%','-2.19%','USMV']],[130,110,110,149]),
      Spacer(1,9),p('The full-universe optimizations impose nonnegative weights, no leverage, 10% per direct stock, 30% across direct stocks and at least 70% across the two diversified ETFs. The stock limits apply to direct holdings, not ETF look-through exposures, which require separate monitoring. Both risk models use the same return forecasts and constraints.'),
      table(['Candidate','Forecast return','Sample risk','Index risk'],rows,[190,103,103,103]),
      Spacer(1,8),p('At A = 4, the sample model holds 18.10% VTI, 51.90% USMV and 30% direct stocks. The single-index model holds 11.34% VTI, 58.66% USMV and 10% each in JNJ, PG and NEE. Switching models implies 14.09% one-way turnover. The index model suppresses residual correlations; VTI and USMV residual correlation is 0.63, so its diversification estimates are optimistic.'),
      p('The sample optimizer improves assumed CE over pure USMV by only about 0.12 percentage points. We prefer the simpler ETF implementation given model error and concentrated direct-stock bets. The Eta proxy maximizes historical mean excess return over the 4% case hurdle. A realized-RF variant is reported separately rather than silently redefining that frozen proxy.'),
      src('expected_return_inputs.csv; risk_preference.csv; portfolio_candidates.csv; window_and_erp_sensitivity.csv; historical_sharpe_definition_audit.csv.')])
    fr=[]
    for sec in ['USMV','AAPL','MSFT']:
        for model in ['CAPM','FF3']:
            q=reg.loc[(sec,model)];fr.append([sec,model,f'{q["Mkt-RF"]:.2f}',pct(q.alpha_annual),f'{pct(q.alpha_low)} to {pct(q.alpha_high)}',f'{q.r_squared:.3f}'])
    pages.append([
      p('Return drivers and the advisers claims','HeadK'),
      p('Estimate CAPM and Fama-French three-factor regressions on monthly excess returns, with an intercept and heteroskedasticity/autocorrelation-robust standard errors using three lags. Report 95% intervals. Annual alpha is 12 times the monthly intercept, an arithmetic convention. The user confirmed that FF3 is allowed in Lecture 7.'),
      table(['Security','Model','Market beta','Annual alpha','95% alpha interval','R squared'],fr,[56,48,65,72,181,77]),
      Spacer(1,9),p('USMV\'s FF3 market beta is 0.74; its SMB loading is -0.30, consistent with a large-company tilt. HML is approximately -0.05 and statistically uncertain. Its alpha interval includes zero. The model explains about 85% of excess-return variance. The covariance-aware variance allocation attributes 85.6% to market exposure and 15.2% to residual risk, with a small negative size contribution because factors covary.'),
      p('AAPL and MSFT load negatively on HML, consistent with growth exposure. MSFT has a positive full-sample alpha that is statistically distinguishable from zero in these regressions. This is evidence inconvenient to a blanket rejection of Theta. However, its early-half FF3 alpha interval includes zero, model omissions remain possible, and examining several securities raises selection concerns. The result does not establish a persistent, tradeable future abnormal return.'),
      p('Eta is right that liability-supporting bonds can separate contractual spending from equity risk. The second step, buying the historical Sharpe winner, is weaker: the same sample both selects and praises the portfolio. The constrained Eta proxy has a high fitted Sharpe, but that is not an unbiased estimate of its future performance.'),
      p('Theta is right that exposures explain much of risk and return. We use factor evidence to understand the portfolio, not as proof of manager skill. Zero forecast alpha avoids capitalizing unstable residual performance. The market-only model is parsimonious; FF3 adds useful style diagnostics without eliminating estimation uncertainty or establishing causation.'),
      src('factor_regressions.csv; alpha_stability.csv; factor_variance_decomposition.csv; training_performance.csv.')])
    erows=[]
    for name in ['Recommended','Benchmark VTI','Sample_A4','Single_index_A4','Eta_historical_Sharpe']:
        q=ev.loc[name];erows.append([name.replace('_',' '),pct(q.cagr),pct(q.annual_volatility),f'{q.annual_sharpe:.2f}',pct(q.max_month_end_drawdown)])
    pages.append([
      p('Frozen evaluation and adverse evidence','HeadK'),
      p('The saved policy defines the growth holdings, benchmark and annual December rebalance rule before the separate evaluation downloads. No parameters are re-estimated in 2023-2025. Dividends follow adjusted-price reinvestment. Charge 10bp on initial invested dollars and on each buy or sell at rebalancing. There is no terminal liquidation charge. ETF operating expenses are already reflected in observed fund returns.'),
      table(['2023 to 2025','CAGR','Volatility','Sharpe','Max drawdown'],erows,[175,80,80,65,99]),
      Spacer(1,8),image('evaluation_growth.png',w=490,h=210),
      p('USMV returned 37.33% cumulatively after the assumed entry cost, versus 82.56% for VTI. It lagged in every calendar year and also delivered a lower evaluation Sharpe ratio. Its smaller month-end drawdown and lower volatility do not erase this opportunity cost. The recommendation buys lower estimated risk at the cost of weaker participation in a strong market.'),
      p('These results weaken any claim that USMV must dominate on risk-adjusted performance. They do not by themselves invalidate a trustee preference for lower risk. The evaluation is only 36 months and uses a retrospective surviving universe with revised vendor histories. Month-end drawdown understates losses between observation dates. It says nothing definitive about the 2030 funding outcome.'),
      src('evaluation_performance.csv; evaluation_calendar_years.csv; evaluation_wealth.csv; evaluation_summary.json. Frozen policy hash is checked before and after evaluation.')])
    pages.append([
      p('Risk acceptance and conditions for change','HeadK'),
      p('<b>Risk definition.</b> Treat 15% as a board escalation level for peak-to-trough, month-end, unitized total-fund NAV, excluding external programme withdrawals. Track rolling 12-month investment return separately. An operational warning at 12% requests review; neither threshold guarantees a maximum loss or automatically changes the frozen backtest. In real implementation the board must record any discretionary policy amendment.'),
      p('An instantaneous 30% equity fall combined with a 100bp rate rise loses 17.53% of initial assets before initial costs. Reducing initial equities by approximately USD 1.014m to cash would satisfy that specific stress, but raises the remaining equity CAGR hurdle to 5.60%. This is a stress-specific sensitivity, not a guaranteed drawdown solution. Once payment bonds mature, equities become a larger fraction of remaining wealth, so initial fund volatility is not a permanent risk measure.'),
      table(['Feasible policy','2030 real value at 2.5% inflation','Trade-off'],[
        ['USMV plus payment bonds',f'Median {money(sim.loc["USMV","real_median"])}; 5th percentile {money(sim.loc["USMV","real_p05"])}','Goal remains uncertain'],
        ['Dedicated all-bond plan',money(ab['real_terminal_at_assumed_2_5pct_inflation']),'6.62% below the USD 8m goal'],
        ['All bonds plus new capital','$8,000,000',f'Needs {money(ab["additional_initial_capital"])} more initially']],[132,205,162]),
      Spacer(1,9),p('The all-bond linear programme maximizes terminal cash while keeping cash nonnegative and meeting both original payments. At USD 12m it fixes USD 9.102m nominal terminal cash under zero reinvestment. Its real value still depends on inflation, and interim bond prices can fall. This is a feasible alternative if trustees prefer nominal funding certainty to the equity policy\'s uncertain upside.'),
      p('Review quarterly: dedicated cash-flow coverage, ETF mandate and concentration, fees, estimated beta, the unitized loss metric, and updated education-cost inflation. Reconsider USMV if the trustees\' growth-sleeve A falls below 2.58, the assumed market premium rises above 6.98%, or a changed objective makes the all-bond compromise preferable. Do not switch because of one favourable backtest.'),
      p('<b>Mandate revision.</b> Preserve the 22 October package. When the 23 October revision arrives, isolate each changed constraint, retain the 31 December 2022 information cutoff, rerun a separate scenario, and quantify allocation, funding, risk and goal changes against the frozen original. The actual revision, course AI rules and member contributions remain group completion items.'),
      src('whole_fund_stress.csv; risk_limit_sensitivity.json; all_bond_alternative.csv; all_bond_cashflows.csv; all_bond_summary.json; mission_simulation.csv.')])
    references=[
      ('1','Assignment case','BFIN-WS2026-Group_Assignment.pdf supplied by the user. Contractual amounts, quotes, investment restrictions and submission rules.'),
      ('2','Kenneth French Data Library','https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html'),
      ('2a','FF3 monthly original ZIP','https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip'),
      ('3','Federal Reserve projections of 14 December 2022','https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20221214.htm'),
      ('4','Yahoo Finance and yfinance settings','https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html'),
      ('5','VTI pre-cutoff summary prospectus','https://www.sec.gov/Archives/edgar/data/36405/000168386320005993/f4654d1.htm'),
      ('6','USMV contemporary SEC-filed description','https://www.sec.gov/Archives/edgar/data/886982/000156459022026948/gs-424b2.htm')]
    refs=[p('References and evidence map','HeadK')]
    for number,title,url in references:
        refs.append(p(f'[{number}] <b>{title}.</b> '+(f'<link href="{url}" color="#185a78">Open official source</link>.' if url.startswith('https') else url)))
    refs.append(p('Stock eligibility sources','SubK'))
    source=json.loads((ROOT/'data/raw/supporting/eligibility_checks.json').read_text())
    for item in source['notes']:
        if item['ticker'] in ['VTI','USMV']:continue
        refs.append(p(f'<b>{item["ticker"]}</b> - pre-cutoff filing {item["filed"]}. <link href="{item["url"]}" color="#185a78">SEC filing</link>.','SmallK'))
    refs.extend([p('How to audit the figures','SubK'),p('Each page names its generated CSV or JSON outputs in outputs/tables. Each figure comes from outputs/figures. The source register, dated retrieval manifest, raw files, executable code and package versions are included in the archive. Run python analysis/rebuild.py after installing the environment. It disables network connections during the rebuild.'),
      p('The model probabilities and forecasts are conditional analytical assumptions. Supporting methodology pages may reflect current data-production conventions; only pre-2023 economic publications inform the case decision. Historical equity and factor values downloaded now are revised vintages.'),
      p('AI assistance disclosure','SubK'),p('AI assisted with interpretation, coding, source identification, numerical analysis and drafting. Automated checks cover budget totals, bond repricing, cash-flow coverage, sample completeness, file integrity and policy preservation. These checks do not replace student verification. Each group member must explain the analysis and record their actual substantive work, independent checks and critique. Confirm the course-specific AI rules before submission.')])
    pages.append(refs)
    n=build('Kappa_Committee_Memo.pdf',pages)
    if n!=9:raise ValueError(f'Memo requires 8 content pages plus 1 reference page, rendered {n}')
    # Two-page initial decision record has no evaluation-period results.
    initial=[[
      p('Kappa Foundation initial decision record','TitleK'),p('Prepared for the 22 October 2026 submission','SubK'),
      p('Case decision: 31 December 2022. Information cutoff: 31 December 2022. The original policy is frozen in policy/frozen_policy.json with a SHA-256 record. This is a prepared submission, not evidence that a student submitted it.'),
      p('<b>Decision.</b> Protect the two nominal obligations with dedicated Beta and Delta holdings. Invest the residual growth sleeve in USMV, with VTI as the simple investable comparator. Accept the real-value target as an aspiration and the 15% loss concern as an escalation threshold, not a guaranteed maximum loss.'),
      table(['Use','USD','Share','Implementation'],allocation,[73,94,58,274]),Spacer(1,10),
      p('<b>Universe.</b> Eight US common stocks: AAPL, MSFT, JPM, JNJ, PG, XOM, CAT and NEE, spanning seven sectors. ETFs: VTI for broad US market exposure and USMV for minimum volatility. Dated SEC evidence is in the supporting source record; retrospective selection bias remains.'),
      p('<b>Estimation.</b> January 2015-December 2022, 96 common months. Daily Yahoo downloads supply month-end adjusted prices; December 2014 is the initial denominator only. FF3 monthly factors come directly from Kenneth French\'s ZIP. No future returns enter estimation.'),
      p('<b>Payment plan.</b> Beta face USD 2.4m matures in 2024. Delta face USD 3,478,260.87 produces exactly USD 3.6m at maturity in 2027. Retain four earlier Delta coupons of USD 121,739.13 in cash. Base reinvestment is zero. All payment amounts remain unchanged.')],
      [p('Assumptions and frozen evaluation rule','HeadK'),
       p('<b>Planning assumptions.</b> Inflation 2.5% annually, tested at 2%-5%. Forecast return = 4.0% + estimated market beta x 4.5%, with zero forecast alpha. Compare growth-sleeve utility CE = mean - A x variance / 2 at A = 4 and sensitivities from 1 to 8. These are judgement inputs rather than estimated trustee preferences.'),
       p('<b>Constraints and execution.</b> Long only, no borrowing or derivatives. Candidate optimization caps direct stocks at 10% each and 30% collectively. Pure ETF policies are allowed. Cost assumptions are 5bp on initial bond consideration and 10bp per equity dollar traded. Fractional holdings are permitted. December 2022 last close is a sizing and paper-evaluation proxy, not a claim of a live executable equity quote on Saturday 31 December.'),
       p('<b>Risk.</b> Monitor month-end unitized total-fund peak-to-trough loss net of external programme payments. At 12%, request review; at 15%, escalate to trustees. No automatic tactical trading enters the evaluation. Dedicated bonds stay earmarked. The growth share rises after payment bonds mature, so later risk must be reviewed explicitly.'),
       p('<b>Evaluation.</b> January 2023-December 2025 remains separate. Freeze initial weights and the VTI comparator. Reinvest equity dividends through adjusted-price total-return proxies. For multi-asset diagnostic alternatives, rebalance after December returns to inception weights without re-estimation, using only prices then available. Charge costs on both purchase and sale notionals. The one-ETF recommendation and benchmark require no cross-asset rebalance.'),
       p('<b>Comparisons.</b> Report CAGR, volatility, Sharpe, month-end drawdown, calendar-year returns and turnover, including unfavourable results. Test the 60-month estimation alternative, market premiums, risk aversion, covariance model and inflation. Evaluate fictional bonds only through contractual cash flows and explicit rate scenarios.'),
       p('<b>Preservation.</b> The archive contains working Python code, raw training data, a dated source record and the frozen policy. Keep an unchanged copy of this submission before responding to the 23 October revised mandate. The revision must retain the original case date and be compared quantitatively with this record.'),
       src('analysis/config.json; policy/frozen_policy.json; policy/frozen_policy.sha256; data/raw/retrieval_manifest.jsonl. AI assistance and member verification must be disclosed under course rules.')]]
    ni=build('Kappa_Initial_Decision_Record.pdf',initial)
    if ni!=2:raise ValueError(f'Initial record exceeded two pages: {ni}')
    # Retain exact narrative as an editable source linked to table/figure filenames.
    def render_source(pages):
        result=[]
        def cell_text(c):
            if isinstance(c,(list,tuple)):return ' '.join(cell_text(x) for x in c)
            text=getattr(c,'text',str(c))
            text=re.sub(r'<link href="([^"]+)"[^>]*>(.*?)</link>',r'[\2](\1)',text)
            return re.sub('<[^>]+>','',text)
        for i,page in enumerate(pages,1):
            result.append(f'\n## Page {i}\n')
            for item in page:
                if isinstance(item,Paragraph):result.append(cell_text(item))
                elif isinstance(item,Table):
                    for ri,row in enumerate(item._cellvalues):
                        result.append('| '+' | '.join(cell_text(c) for c in row)+' |')
                        if ri==0:result.append('| '+' | '.join('---' for c in row)+' |')
                elif isinstance(item,Image):result.append('[Figure: '+Path(item.filename).name+']')
        return '\n\n'.join(result).replace(' |\n\n|',' |\n|')
    import re
    (OUT/'Kappa_Committee_Memo_Editable.md').write_text(render_source(pages),encoding='utf-8')
    (OUT/'Kappa_Initial_Decision_Record_Editable.md').write_text(render_source(initial),encoding='utf-8')
    print(json.dumps({'memo_pages':n,'initial_record_pages':ni}))

if __name__=='__main__':main()
