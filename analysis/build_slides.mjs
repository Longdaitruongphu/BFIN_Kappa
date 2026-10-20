import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath,pathToFileURL } from 'node:url';
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const RUNTIME_MODULES=process.env.KAPPA_NODE_MODULES || 'C:/Users/Minh Minh minh/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
process.env.RUNTIME_NODE_MODULES=RUNTIME_MODULES;
const RUNTIME_PYTHON=process.env.KAPPA_PYTHON || 'C:/Users/Minh Minh minh/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe';
const SKILL=process.env.KAPPA_PRESENTATION_SKILL || 'C:/Users/Minh Minh minh/.codex/plugins/cache/openai-primary-runtime/presentations/26.1007.11041/skills/presentations';
const {registerStandardFontAliases}=await import('./font_runtime_compat.mjs');
registerStandardFontAliases(RUNTIME_MODULES,path.join(ROOT,'.slide_build'));
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(RUNTIME_MODULES,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const d=JSON.parse(await fs.readFile(path.join(ROOT,'analysis/slide_data.json'),'utf8'));
const f=d.funding_summary,dc=d.decision_summary,ab=d.all_bond_summary;
const pct=x=>(x*100).toFixed(2)+'%';const usd=x=>'$'+x.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const pres=Presentation.create({slideSize:{width:1280,height:720}});
const build=path.join(ROOT,'.slide_build');await fs.mkdir(build,{recursive:true});
const FONT='Arial',INK='#16384b',TEAL='#157c80',MUTED='#54636f',ORANGE='#b65d37';
function text(s,str,x,y,w,h,size=25,color=INK,bold=false){
  const sh=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  sh.text=str;sh.text.style={typeface:FONT,fontSize:size,color,bold};return sh;
}
function slide(title,notes){const s=pres.slides.add();s.background.fill='#ffffff';text(s,title,65,40,1150,95,44,INK,true);s.speakerNotes.text=notes;text(s,String(pres.slides.items.length),1190,674,40,22,16,MUTED);return s;}
function note(s,str){text(s,str,65,648,1100,45,15,MUTED);}
function para(s,str,y=160,h=120){text(s,str,65,y,1145,h,27,INK);}
function table(s,values,top=180,widths=null,height=320,size=24){
  const tb=s.tables.add({rows:values.length,columns:values[0].length,left:65,top,width:1145,height,values,columnWidths:widths||undefined});
  tb.borders.assign({fill:'#dce3e7',width:.5,style:'solid'});
  for(let r=0;r<values.length;r++)for(let c=0;c<values[0].length;c++){
    const cell=tb.getCell(r,c);cell.fill=r===0?INK:(r%2===0?'#f0f4f5':'#ffffff');
    cell.text.style={typeface:FONT,fontSize:r===0?size-1:size,color:r===0?'#ffffff':INK,bold:r===0};
  }
  return tb;
}
function chart(s,type,categories,series,pos,options={}){
  // The chart workbook displays ten decimal places; full precision stays in the CSV evidence.
  series=series.map(row=>({...row,values:row.values.map(value=>Number(value.toFixed(10)))}));
  const ch=s.charts.add(type,{position:pos,categories,series,lineOptions:{smooth:false},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:19}},
    chartFill:'#ffffff',plotAreaFill:'#ffffff',xAxis:{textStyle:{fontSize:17,fill:MUTED}},
    yAxis:{textStyle:{fontSize:17,fill:MUTED},numberFormatCode:'0%',majorGridlines:{fill:'#dce3e7',width:.7}},...options});
  applyPresentationChartFont(ch,{fontFamily:FONT});return ch;
}
let s=slide('Kappa Foundation investment policy','Original mandate. Case date 31 December 2022. Sources: assignment, initial_allocation.csv, funding_summary.json, mission_simulation.csv. AI-assisted analysis and drafting. Group verification and course-policy confirmation remain required.');
text(s,'Payment bonds plus USMV',65,170,1145,80,56,TEAL,true);
text(s,'Protect the scheduled payments and pursue the 2030 real-value goal',65,280,1080,110,35,INK);
text(s,'USD 5.64m payment bonds\nUSD 6.35m growth allocation\nUSD 9,169 assumed initial costs',65,435,900,140,30,INK);
note(s,'Original case only. The real-value goal and a 15% maximum-loss ceiling are not guaranteed.');

s=slide('The full USD 12 million allocation','Source: initial_allocation.csv. Exact unrounded dollars sum to USD 12m. 5bp bond cost and 10bp equity cost. Fractional holdings. December 2022 close is a paper sizing proxy, not a live executable quote on 31 December.');
table(s,[['Holding','Initial amount','Purpose'],['Beta',usd(f.beta_cost),'USD 2.4m scholarship in 2024'],['Delta',usd(f.delta_cost),'USD 3.6m learning centre in 2027'],['USMV',usd(f.equity_investment),'Long-term purchasing power'],['Costs',usd(f.total_fees),'Assumed initial trading costs'],['Total','$12,000,000.00','100% of initial resources']],155,[225,285,635],390,26);
note(s,'VTI benchmarks the growth sleeve. The full policy reference combines VTI growth with the dedicated payment cash flows.');

s=slide('Contractual cash flows cover both payments','Sources: funding_cashflows.csv and funding_summary.json. Beta face USD 2.4m. Delta face USD 3,478,260.87. Hold bonds to maturity. Cash earns zero. Same-day bond receipts are assumed available before programme disbursement.');
table(s,[['Date','Payment funding','Surplus retained'],['2023','No mandatory payment','$121,739'],['2024','Beta principal pays $2.4m','$121,739'],['2025 and 2026','No mandatory payment','$243,478 combined'],['2027','Delta final payment pays $3.6m','$0'],['2030','Earlier coupons remain in cash','$486,957 total']],155,[215,585,345],370,25);
para(s,'No equity sale or positive reinvestment rate is needed to meet the original obligations.',555,62);
note(s,'Amounts rounded. Cash custody and payment settlement still require operational controls.');

s=slide('Interest rate shocks change value, not the promised receipts','Sources: bond_metrics.csv, bond_stress.csv, ytm_duration_validation.csv, curve_interpolation_sensitivity.csv. Log-linear discount-factor interpolation bootstraps years 1,2,3,5,8. YTM and continuous-spot risk conventions are checked separately. Steepener: -100bp at year 1 to +100bp at year 8.');
table(s,[['Bond','YTM','Modified duration','+100bp price change'],...d.bond_metrics.map(x=>[x.bond,pct(x.ytm),x.modified_duration.toFixed(2),({Alpha:'-1.00%',Beta:'-1.98%',Gamma:'-2.84%',Delta:'-4.56%',Epsilon:'-6.66%'})[x.bond]])],155,[245,220,320,360],340,25);
para(s,'The payment reserve loses about $200,255 after a +100bp curve shift. Its contractual payment coverage stays intact.',525,95);
note(s,'Parallel and curve-shape stresses are scenarios, not probability forecasts. Exact repricing checks duration and convexity.');

s=slide('A 15% loss ceiling cannot be promised','Sources: whole_fund_stress.csv and risk_limit_sensitivity.json. Initial wealth denominator USD 12m, before initial costs. Stress is instantaneous, not a historical price series for the fictional bonds.');
table(s,[['Equity shock','Rate shock','Loss on initial wealth'],['-20%','+100bp parallel','12.25%'],['-30%','+100bp parallel','17.53%'],['-40%','+100bp parallel','22.82%']],165,[330,365,450],255,28);
para(s,'A $1.014m switch from equities to cash meets the specific -30% / +100bp stress. It raises the equity growth hurdle to 5.60%.',465,100);
note(s,'That change does not guarantee a drawdown limit. Equity becomes a larger share of remaining assets after payment bonds mature.');

s=slide('The data separate the decision from its later evaluation','Sources: retrieval_manifest.jsonl, train_data_quality.csv, eval_data_quality.csv, eligibility_checks.json. Official source links: finance.yahoo.com; ranaroussi.github.io/yfinance; mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html.');
table(s,[['Design choice','Implementation'],['Candidate universe','8 US stocks, 7 sectors, VTI and USMV'],['Estimation','96 common monthly returns, Jan 2015 to Dec 2022'],['Evaluation','36 months, Jan 2023 to Dec 2025'],['Market source','Python yfinance, saved untransformed daily responses'],['Factor source','Kenneth French FF3 monthly ZIP, original bytes retained']],155,[360,785],375,25);
para(s,'No invented missing returns. No fictional bond price histories. Current vendor vintages and survivor selection remain limitations.',555,74);
note(s,'Dated SEC eligibility evidence is documented. Direct SEC downloads returned 403, so source notes distinguish web verification from saved files.');

s=slide('USMV is preferred at the assumed risk aversion','Sources: risk_preference.csv and decision_summary.json. CE = annual expected arithmetic return - A*annual variance/2. Forecast: 4% + beta*4.5%, alpha zero. A applies to the growth sleeve, not directly to a whole-fund loss limit.');
const as=[0,1,2,3,4,5,6,7,8];
chart(s,'line',as.map(String),['USMV','VTI'].map((k,i)=>({name:k,values:as.map(a=>{const ce0=d.risk_preference.find(x=>x.strategy===k&&x.risk_aversion===0).certainty_equivalent;const ce1=d.risk_preference.find(x=>x.strategy===k&&x.risk_aversion===1).certainty_equivalent;return ce0+a*(ce1-ce0);}),fill:i?ORANGE:TEAL})),{left:65,top:160,width:730,height:425});
text(s,'A = 4\nUSMV CE 3.84%\nVTI CE 3.13%',850,205,340,170,32,INK,true);
text(s,'The ranking reverses below A = 2.58',850,420,340,130,30,ORANGE,true);
note(s,'Horizontal axis: risk-aversion A. Vertical axis: annual certainty equivalent. The preference parameter requires trustee agreement.');

s=slide('Covariance assumptions change the optimized holdings','Sources: portfolio_candidates.csv; single_index_residual_correlation.csv. Same forecasts and constraints. Direct stocks <=10% each, <=30% combined. Minimum 70% combined ETF weight.');
table(s,[['A = 4 portfolio','VTI','USMV','Direct stocks','Sample volatility'],...['Sample_A4','Single_index_A4'].map(k=>{const x=d.portfolio_candidates.find(r=>r.strategy===k);return [k==='Sample_A4'?'Sample covariance':'Single-index covariance',pct(x.VTI),pct(x.USMV),'30.00%',pct(x.sample_vol)]})],175,[355,165,165,190,270],200,24);
para(s,'Changing the risk model implies 14.09% one-way turnover. VTI and USMV residual correlation is 0.63, which the single-index model suppresses.',425,100);
text(s,'The sample optimizer adds only about 0.12 percentage points of assumed utility over pure USMV.',65,550,1145,70,27,TEAL,true);
note(s,'The preferred policy avoids direct-stock complexity and concentration. Model fit alone does not justify implementation.');

s=slide('Factor exposure and uncertainty in alpha','Sources: factor_regressions.csv and alpha_stability.csv. Training Jan 2015-Dec 2022, 96 observations. HAC confidence intervals, three lags. Annual alpha is monthly intercept times 12. The user confirmed FF3 is allowed in Lecture 7.');
const fr=[];for(const k of ['USMV','AAPL','MSFT'])for(const m of ['CAPM','FF3']){const x=d.factor_regressions.find(r=>r.security===k&&r.model===m);fr.push([k,m,x['Mkt-RF'].toFixed(2),pct(x.alpha_annual),pct(x.alpha_low)+' to '+pct(x.alpha_high)])}
table(s,[['Security','Model','Market beta','Annual alpha','95% alpha interval'],...fr],150,[155,135,210,210,435],350,24);
para(s,'MSFT has positive full-sample alpha. Its early-half interval includes zero, and model and selection uncertainty remain. Forecast alpha stays at zero.',535,94);
note(s,'USMV FF3 beta 0.74 and SMB -0.30 indicate lower market sensitivity and a large-company tilt. Its alpha interval includes zero.');

s=slide('USMV substantially lagged VTI in the frozen evaluation','Sources: evaluation_wealth.csv, evaluation_performance.csv, evaluation_calendar_years.csv. Weights and December rebalance rule frozen before evaluation retrieval. 10bp entry cost and buy/sell costs. No terminal liquidation cost.');
const ew=d.evaluation_wealth;
chart(s,'line',['Dec 2022',...ew.map(x=>x.month)], [{name:'USMV recommendation',values:[1,...ew.map(x=>x.Recommended)],fill:TEAL},{name:'VTI benchmark',values:[1,...ew.map(x=>x['Benchmark VTI'])],fill:ORANGE}],{left:65,top:155,width:790,height:430},{xAxis:{textStyle:{fontSize:12,fill:MUTED},tickLabelInterval:6},yAxis:{numberFormatCode:'0.0',textStyle:{fontSize:18},majorGridlines:{fill:'#dce3e7',width:.7}}});
text(s,'2023 to 2025\n\nUSMV +37.33%\nVTI +82.56%',895,175,315,205,32,INK,true);
text(s,'USMV also had the lower evaluation Sharpe ratio',895,440,315,120,26,ORANGE,true);
note(s,'Growth of USD 1, net of assumed trading costs. Lower volatility and month-end drawdown came with substantial opportunity cost.');

s=slide('The 2030 real-value goal remains uncertain','Sources: goal_sensitivity.csv, mission_simulation.csv and mission_scenarios.csv. 20,000 paths, fixed seed, circular 12-month blocks of historical log shocks centered to a prospective log-growth approximation. Cash reinvestment zero. Conditional scenario model, not a calibrated probability forecast.');
table(s,[['USMV scenario','Base','Higher inflation'],['Annual inflation','2.5%','4.0%'],['Required equity CAGR','4.84%','6.45%'],['Modeled chance of real goal','68.5%','48.1%'],['Median real 2030 assets','$8.89m','$7.91m']],170,[535,305,305],310,27);
para(s,'Even in the base scenario, about 31.5% of paths miss the goal. Parameter uncertainty is larger than Monte Carlo sampling noise.',535,100);
note(s,'Forecast equity arithmetic return 7.14%, annual volatility 12.84%. Historical mean returns are not used as forecasts.');

s=slide('The all-bond alternative makes the compromise explicit','Sources: all_bond_alternative.csv, all_bond_cashflows.csv and all_bond_summary.json. Linear programming over case bond cash flows with nonnegative cash each year and zero cash reinvestment. Original payment obligations unchanged.');
table(s,[['Choice','Outcome under 2.5% inflation'],['USD 12m in dedicated case bonds','$9.102m fixed nominal terminal cash'],['Implied 2030 purchasing power','$7.471m in December 2022 dollars'],['Gap from the USD 8m real goal','6.62% lower real target'],['Extra initial capital to fund the full target','$480,443']],165,[610,535],320,27);
para(s,'We recommend payment bonds plus USMV to retain the chance of reaching the full real goal, accepting investment risk and possible shortfall.',535,94);
note(s,'Nominal cash flows are fixed under case assumptions. Real value depends on inflation and interim bond prices can still fall.');

s=slide('Monitoring and the revised mandate','Sources: policy/frozen_policy.json, DECISION_LOG.md, MANDATE_REVISION.md, TEAM_COMPLETION.md. Assignment deadlines in Ho Chi Minh City time. No actual revised mandate is available yet.');
text(s,'Quarterly review',65,160,520,55,32,TEAL,true);
text(s,'Payment coverage and cash custody\nUnitized losses excluding programme payments\nETF mandate, concentration and costs\nEducation-cost inflation and goal feasibility',65,235,1100,220,29,INK);
text(s,'22 October: preserve the original decision\n23 October: quantify the actual mandate change\n29 October: submit the final package',65,490,1100,125,27,INK,true);
note(s,'AI assistance is disclosed. The group must confirm course policy, add real contributions, and independently check the analysis.');

await fs.writeFile(path.join(build,'deck.proto.json'),JSON.stringify(pres.toProto()));
const draft=path.join(build,'candidate.pptx');await (await PresentationFile.exportPptx(pres)).save(draft);
for(let i=0;i<pres.slides.items.length;i++){
  const blob=await pres.export({slide:pres.slides.items[i],format:'png',scale:1});
  await fs.writeFile(path.join(build,`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const pdf=await pres.export({format:'pdf'});await fs.writeFile(path.join(ROOT,'deliverables/Kappa_Committee_Presentation.pdf'),new Uint8Array(await pdf.arrayBuffer()));
const output=process.env.KAPPA_PPTX_OUTPUT || path.join(ROOT,'deliverables/Kappa_Committee_Presentation.pptx');
const result=await finalizePresentation({workspaceDir:ROOT,candidatePath:draft,finalPath:output,pythonExecutable:RUNTIME_PYTHON,
  integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[2,3,4,5,6,8,9,11,12].flatMap(n=>['--require-native-table-slide',String(n)])],
  requiredNativeTableOwnerSlides:[2,3,4,5,6,8,9,11,12],requiredNativeChartOwnerSlides:[7,10],
  materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,
  receiptPath:path.join(build,'validation.json')});
console.log(JSON.stringify({slides:pres.slides.items.length,final:output,result}));
