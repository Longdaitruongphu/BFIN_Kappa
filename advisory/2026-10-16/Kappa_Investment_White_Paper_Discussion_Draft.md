# Kappa Foundation: Investment Philosophy and Governance White Paper

Discussion draft v0.1 | 16 October 2026 | All amounts USD

**Status:** Advisory design for discussion, not a newly approved investment policy, revised trustee mandate, or final course submission. The original frozen recommendation remains the reference case. The user's latest direction is to protect mandatory obligations, pursue long-term real growth, and develop contextual risk governance. Numerical limits and new trading rules below require decisions and scenario testing before adoption.

## 1. Executive proposition

Kappa should operate as a mission-led foundation investment pool with dedicated liability funding and a separately governed growth allocation. Its professional standard is reliable execution, transparent trade-offs, proportionate costs and disciplined capital stewardship. It cannot promise a positive market return every year or an unconditional 15% maximum loss while maintaining the current equity exposure.

Proposed mission: meet the foundation's irrevocable educational commitments in full and on time, while investing the remaining capital to preserve and grow its long-term purchasing power.

Proposed vision: establish an enduring source of educational funding whose investment decisions remain understandable, accountable and financially feasible through adverse markets. A perpetual life beyond 2030 is a proposed extension, not a fact supplied by the assignment.

The governing order should be: satisfy the mandate; preserve dedicated payment resources; maintain operational liquidity; pursue the real terminal objective; then seek additional growth within the approved risk budget. This ordering does not mean every temporary market-value loss requires selling.

The 2030 real objective stays anchored to USD 8 million in December-2022 purchasing power unless trustees explicitly authorize and document an alternative. Updating inflation forecasts changes the estimated nominal amount required; it does not silently reduce the real objective. Professional growth also means retaining the ability to fund future programmes, rather than maximizing headline assets under management.

## 2. What the assignment actually requires

Authority: `reference/BFIN-WS2026-Group_Assignment.pdf`, pages 1-4, read in full. The following separates assignment requirements from analyst choices.

| Category | Assignment requirement | Decision space |
|---|---|---|
| Starting position | USD 12m cash on 31 December 2022; no other assets, liabilities or committed donations | Allocate the full amount, including declared costs and any reserve |
| Mandatory programme payments | USD 2.4m on 31 December 2024 and USD 3.6m on 31 December 2027 | Funding method is discretionary; the original payments cannot be changed |
| Terminal aspiration | Remaining assets in 2030 should have at least USD 8m of December-2022 purchasing power | This is a goal, not a guaranteed return; a changed goal needs a feasible alternative and quantified trade-off |
| Loss concern | Trustees are uncomfortable with losses approaching 15% | Measure, horizon, denominator and acceptable compromises must be proposed |
| Assets | Cash, the five fictional case bonds, US common stocks, US-listed equity ETFs primarily investing in US equities | Portfolio selection and additional limits are discretionary |
| Prohibitions | No borrowing, short selling or derivatives | Do not introduce options, futures or swaps as an original-case hedge |
| Other case assumptions | USD reporting, tax exemption, fractional holdings allowed; no case-bond default losses | These are case simplifications, not universal real-world guarantees |
| Equity research universe | 8-12 common stocks spanning at least four sectors, plus two meaningfully different eligible ETFs | Holdings need not include every candidate; case-date eligibility evidence is required |
| Decision information | Information no later than 31 December 2022; at least 60 common monthly returns ending then, drawn from January 2015 onward | Saved training uses 96 months |
| Separate evaluation | January 2023-December 2025, with policy and rule frozen before evaluation | Evaluation must retain inconvenient evidence and cannot redesign the original decision |
| Required analysis | Quantitative risk preference; bonds, incomplete curve, duration/convexity and exact stresses; sample versus single-index covariance; market and Lecture-7 multifactor models; reversal threshold | FF3 eligibility has already been confirmed by the user |
| Reproducibility | Python retrieval from Yahoo/yfinance and Kenneth French, raw responses, settings, versions, source records and offline reproduction | No invented returns or fictional-bond historical quotes |
| Submission | Initial record and working Python/data record: 22 Oct 2026, 16:00; revised mandate release: 23 Oct, 16:00; final: 29 Oct, 16:00 | All deadlines are Ho Chi Minh City time |
| Final package | Memo up to eight pages plus one references page, editable slides and PDF, executable analysis and data, initial submission and change log, genuine contributions/checks/critiques | This longer white paper is a working companion, not a replacement for the page-limited memo |

The assignment does **not** require USMV, 2.5% inflation, risk aversion A=4, a 70% or 90% goal probability, a 5% cash reserve, or a mechanical stop-loss. Those are potential policy choices. It does not authorize assumed future donations, a fee-generating asset-management company, private equity, direct real estate, gold, international equity funds or an expanded bond universe.

## 3. Institutional practices worth adapting

These are contemporary governance references. They must not be presented as information known in 2022 unless an appropriate dated version is obtained. The lessons below are design inferences, not claims that these institutions endorse Kappa.

| Institution | Verified practice | Proposed adaptation for Kappa |
|---|---|---|
| Norges Bank Investment Management | Owner-defined mandate, explicit benchmark and delegated risk; published strategy describes a 70/30 benchmark, a 1.25% expected tracking-error ceiling and a 2 percentage-point equity-drift rebalancing trigger | Define who owns risk decisions and benchmark changes. Do not copy its allocation or numerical limits: Kappa has different liabilities, scale and eligible assets. [S01] |
| NBIM risk management | Uses multiple risk measures and historical/hypothetical stress tests | Combine cash-flow coverage, drawdown, liquidity and goal shortfall; no single statistic can govern the fund. [S02] |
| Yale endowment | Spending policy combines purchasing-power preservation with current support, using a target payout and smoothing | Consider smoothing only for future discretionary grants if a continuing endowment is approved. The fixed 2024/2027 commitments cannot be smoothed or postponed. [S03] |
| CalPERS | Describes asset-liability management as integrated review of assets and liabilities for sustainability | Begin with cash needs and risk-bearing capacity before selecting assets. Kappa has no pension sponsor contributions or presumed bailout. The indexed official page was accessible in search; direct retrieval failed. [S04] |

Kappa can borrow governance discipline without importing the staffing, illiquidity, leverage or manager-selection structure of a multibillion-dollar institution. At USD 12m, an extra 25bp of annual costs is USD 30,000 at initial size; 100bp is USD 120,000. Complexity must demonstrate a benefit after those costs.

## 4. Investment beliefs proposed for the charter

1. Irrevocable obligations should be funded by cash flows that do not depend on selling risky assets or earning a favorable reinvestment rate.
2. Equity risk is accepted to pursue long-term purchasing power, with the possibility of shortfall made explicit.
3. Diversification reduces some risks; broad US equity exposure retains systematic market and geographic risk.
4. A lower-volatility portfolio can be useful without having superior return, Sharpe or crisis protection in every period.
5. Forecasts are decision inputs with error. Estimated historical alpha is not automatically a future return entitlement.
6. A transparent low-cost implementation is preferred when complexity adds only fragile estimated benefits.
7. Macroeconomic analysis should shape scenarios, funding assessments and bounded policy review; a narrative alone does not authorize a trade.
8. Risk limits apply before and after programme payments. Payouts can materially change the risk composition of remaining assets.
9. Investment process and realized outcomes are both evaluated. Poor outcomes require investigation without automatically proving that the original process was unsound.
10. Policy exceptions are specific, time-limited and independently reviewed. A market crisis does not erase the mandate.

The board should promise adherence to these responsibilities and honest reporting. It should describe real growth as an investment objective subject to market outcomes, not an unconditional commitment to investment gains.

## 5. Capital architecture and payment protection

The frozen allocation is Beta USD 2,214,672; Delta USD 3,429,808.70; USMV USD 6,346,350.71; initial transaction costs USD 9,168.59. Those amounts reconcile to USD 12m. They are the approved analytical baseline, not a new recommendation made by this document.

| Capital account | Function | Proposed protection |
|---|---|---|
| Payment account | Beta face USD 2.4m; Delta face about USD 3.478m plus final coupon funds USD 3.6m | Protect the cash flows for both commitments from inception, including the more distant 2027 payment |
| Operational cash | Approved costs, settlement needs and any approved contingency budget | Size against dated cash needs; not a generic percentage or a hidden market-timing allocation |
| Growth account | Pursue the real terminal objective | Risk-bearing capacity is what remains after protected funding and genuine cash needs |

“Hedge” here primarily means contractual cash-flow matching using permitted assets. The principal protection is against forced equity liquidation to meet the two payments. It does not hedge inflation, all mark-to-market losses or operational failures.

Beta covers the 2024 payment by itself. Delta's 2027 principal plus final coupon covers the 2027 payment. Its four earlier coupons total USD 486,956.52 by end-2026, assuming no cash reinvestment return. This cash already contributes to the terminal-goal calculation. It cannot simultaneously be treated as spending money, a trading reserve and retained terminal wealth.

Proposed coverage rule: under each dated cash-flow scenario, cumulative designated cash and contracted inflows available by each payment date must cover all designated outflows up to that date, without counting the same coupon twice. Neither an equity forecast nor a later-dated receipt qualifies as timely coverage. Record a separate settlement-readiness check for practical execution.

The educational case assumes year-end receipts and payments occur as specified. A real operating design would need banking calendars, settlement timing and payment authority. Do not invent executable future bond prices to claim this operational contingency has been fully modeled.

### Cash-reserve trade-off

The assignment contains no additional operating budget. An actual budget therefore requires a separately labeled scenario. The examples below allocate cash at inception from the growth budget, retain the payment bonds, charge the existing 10bp equity entry fee, assume zero reserve income, and keep 2.5% inflation.

| Initial reserve | Growth investment | Required equity CAGR if reserve remains at 2030 | Required equity CAGR if reserve is fully spent by 2030 |
|---:|---:|---:|---:|
| USD 0 | USD 6,346,351 | 4.84% | 4.84% |
| USD 120,000 | USD 6,226,471 | 4.92% | 5.09% |
| USD 250,000 | USD 6,096,600 | 5.00% | 5.36% |
| USD 500,000 | USD 5,846,850 | 5.18% | 5.92% |
| USD 1,000,000 | USD 5,347,350 | 5.59% | 7.11% |

Source: `reserve_tradeoffs.csv`. These are deterministic funding identities, not recommended reserve amounts or expected returns. Spending occurs from the segregated reserve; the illustration includes no income on it, regardless of spending timing. A recurring operating-cost model needs actual annual outflows.

Proposed sizing process: list 12 months of approved non-programme expenses and execution needs; identify dependable unencumbered receipts by date; choose a contingency amount; stress the resulting liquidity schedule. Opportunities to buy equities are a separate use of capital with a separate return trade-off.

## 6. Hard red lines, flexible parameters and crisis authority

| Rule | Status and rationale | Exception treatment |
|---|---|---|
| No borrowing, shorting or derivatives | Hard assignment prohibition | No internal crisis waiver can override the original assignment |
| Original fixed payment amounts and dates | Hard assignment requirement | Only an actual new trustee mandate can change them, with original retained |
| No release of protected payment resources without equivalent timely replacement | Proposed hard operating rule reflecting the user's direction | A permitted replacement must pass the same funding and timing tests before release |
| No reliance on uncommitted donations | Original case constraint | Recognize additional funding only in a documented new scenario or after actual receipt in a permitted implementation |
| No double-counted assets or fabricated returns | Hard analytical integrity rule | No waiver |
| No retrospective policy or benchmark rewriting | Hard research and evaluation discipline | Versioned prospective amendment; preserve original comparisons |
| Inflation outlook, equity budget, cash buffer and rebalancing bands | Flexible proposed policy parameters | Review using dated evidence, impact analysis and authorized limits |
| 15% loss concern | Measurement and consequence still under discussion | Temporary exception can affect the response, never make the reported loss disappear |

### Resolve what “maximum stop-loss” means

A stop order is an execution instruction, not a guaranteed exit price. Market gaps can produce worse fills; a stop-limit can remain unfilled. The SEC explains this distinction. [S05] Portfolio drawdown is also different from an individual ETF stop, a one-year loss and a scenario loss.

The most coherent interpretation of the user's preference is a **15% loss-action threshold with tightly governed exceptions**. It can have a hard requirement to act and report while allowing a context-dependent trade decision. If trustees instead require a genuinely hard economic floor, the asset allocation and real-goal feasibility must be redesigned; wording cannot make the current allocation satisfy that requirement.

The existing memo uses month-end peak-to-trough drawdown in unitized total-fund NAV, excluding programme withdrawals, with a 12% warning and 15% escalation. Keep that as the analytical baseline. A real daily-monitoring policy would be a new proposal; monthly historical observations cannot validate daily stops or intramonth maximum losses. Report the growth sleeve's drawdown separately, since paying liabilities changes the whole-fund denominator.

Proposed response ladder, for discussion:

| Trigger | Required process | Trading implication |
|---|---|---|
| Any payment-coverage or settlement shortfall | Immediate incident escalation and documented funding remedy; pause discretionary capital deployment | Mandatory obligations take precedence over opportunistic trades |
| 12% investment drawdown | Risk reviewer checks valuation, liquidity, payment coverage and updated goal feasibility | No automatic liquidation solely because of the warning |
| 15% investment drawdown | Notify chair and convene committee promptly; proposed maximum two business days; document retain/reduce/rebalance decision | Require an explicit decision, including a rationale for holding and a re-entry plan if selling |
| Severe operational disruption | Follow custody/payment continuity procedure | No trading against unverified positions or missing cash records |

A systemic-stress exception should specify the observed broad-market shock and liquidity evidence; confirm intact payment funding; separate market movement from operational or mandate breach; quantify the risk of holding versus selling; identify approvers and dissent; and set an expiry/review date. A proposed initial expiry is ten business days, renewable only by a fresh recorded decision. These timings are proposed governance settings, not industry standards or approved Kappa rules.

The person managing the exposure should not be the sole approver of its exception. No blanket “crisis exception” should permit borrowing, using protected payment assets or retrospectively raising the threshold. Repeated exceptions trigger strategic policy review.

### The current allocation does not satisfy a guaranteed 15% ceiling

The saved combined stress of equity -30% and rates +100bp loses 17.53% of initial wealth, even though contractual payment cash flows remain intact. The saved stress-specific adjustment moves about USD 1.014m from equity to cash and raises required equity CAGR to 5.60%. That addresses only that specified instantaneous stress, not every market path or future portfolio state.

There is also a lifecycle issue. On an illustrative constant 4.8365% equity-return path, immediately after the 2027 payment the fund holds about USD 8.037m of growth assets and USD 0.487m of coupon cash: approximately 94.29% equity. A subsequent instantaneous equity loss of 30% then loses about 28.29% of remaining wealth. This is a deterministic illustration, not a forecast or historical backtest. It explains why a terminal-risk plan must address the post-payment years explicitly.

## 7. Inflation, macroeconomics and the two information clocks

### Original decision: information available by 31 December 2022

The November 2022 CPI release, published on 13 December, reported 7.1% annual CPI inflation. December CPI was not published until January 2023 and cannot be used as an observed input in the original decision. [S06] The 14 December FOMC raised the policy-rate range to 4.25%-4.50%. [S07] Its December projections had median PCE inflation of 3.1%, 2.5% and 2.1% for 2023-2025, with 2% longer-run inflation. These were conditional projections, not guarantees or an eight-year forecast for Kappa's programme costs. [S08]

The Fed's 2% objective refers to PCE, whereas the board could choose CPI-U as a broad USD purchasing-power proxy. Education costs may behave differently from both. [S09] The present 2.5% constant assumption is a planning scenario that needs a defense and alternatives; it is not an established fact that actual inflation will average 2.5%.

### Contemporary learning appendix: observed sources in October 2026

These facts are excluded from 2022 policy design. The 14 October 2026 BLS release reports September headline CPI at 3.7% year-on-year, core at 2.6%, and gasoline as a major source of the monthly increase. [S10] The 16 September 2026 FOMC statement reports a 25bp increase to 3.75%-4.00%. [S11] Those observations support investigating renewed inflation pressure; they do not establish one inevitable rate path or an eight-year inflation estimate.

An IMF media release dated 14 October, describing a 13 October briefing, distinguishes a war-related adverse supply shock from an AI investment demand shock. [S12] The WEO landing page returned “Coming Soon” in this research session, so this document does not claim to have inspected the complete October report or its tables.

The user's macro thesis should be divided into testable mechanisms:

| Hypothesis | Mechanism to examine | Evidence that could weaken it | Portfolio-policy relevance |
|---|---|---|---|
| Energy/geopolitical disruption sustains inflation | Higher energy, transport and production costs | Normalizing supply, falling pass-through, weak demand | Stress simultaneous equity losses and rising rates; increase nominal-goal sensitivity |
| AI investment raises near-term demand | Infrastructure, electricity, chips and skilled labor expenditure | Capex cancellation, financing constraints, overcapacity | Monitor concentration and valuation, not only GDP growth |
| AI raises longer-term supply capacity | Task productivity diffuses to firms and aggregate output | Weak adoption quality, complementary costs, slow diffusion | Retain a productivity/disinflation scenario alongside the inflationary one |
| Debt pressure forces lower rates | Fiscal sensitivity to debt service may create pressure | Inflation credibility, term-premium or currency risks may instead keep financing costly | Do not infer a mechanical Fed rate cut from high public debt |
| Technology valuations form a bubble | Expectations may outrun realizable cash flows | Strong cash conversion and earnings breadth | Treat “bubble” as a hypothesis requiring valuation and earnings evidence, not a settled diagnosis |

AI productivity has been studied, but task-level results do not settle aggregate long-run outcomes. The 2023 working-paper version of *Generative AI at Work* reports productivity improvements in a particular customer-support setting. Acemoglu's 2024 *The Simple Macroeconomics of AI* derives more limited aggregate gains under its assumptions. These studies differ in scope and model; neither directly supplies Kappa with a market-return forecast. Only indexed official abstracts were accessible in this session, not a full-text methodological review. Both are post-cutoff learning references. [S13, S14]

### Turn the macro view into a decision framework

Use at least four scenarios: disinflation with modest growth; persistent cost inflation; recession and equity losses; AI productivity diffusion with uncertain equity valuations. A fifth scenario can combine high inflation, high term premiums and falling equities. Do not attach invented probabilities. First test funding feasibility across scenarios and identify which assumptions reverse a decision.

The monthly dashboard should distinguish headline/core inflation, shorter-term momentum, wage/productivity measures, policy rates, the yield curve, inflation expectations and market concentration. Record release dates and vintage. Market breakevens mix inflation expectations with liquidity and risk premiums; they are not a pure forecast. New historical series would require dated provenance and separate retrieval rather than silent substitution into frozen files.

| Constant annual inflation scenario | Nominal 2030 goal | Required equity CAGR, coupon cash at zero interest |
|---:|---:|---:|
| 2.0% | USD 9.373m | 4.30% |
| 2.5% | USD 9.747m | 4.84% |
| 3.0% | USD 10.134m | 5.37% |
| 4.0% | USD 10.949m | 6.45% |
| 5.0% | USD 11.820m | 7.52% |

Source: saved `outputs/tables/goal_sensitivity.csv`. A constant-rate scenario is not a claim about the inflation path. For varying annual inflation, use USD 8m multiplied by the product of annual inflation factors. Once a measurement index is chosen, realized purchasing power uses its actual cumulative change; future planning combines realized changes to date with prospective assumptions. Keep the real USD 8m reference visible when updating the nominal estimate.

The existing 68.48% modeled goal frequency at 2.5% inflation and 48.05% at 4% are conditional simulation outputs, not calibrated real-world probabilities. The board should also examine the depth of shortfall and adverse-tail outcomes. A lower simulated frequency is a prompt to review assumptions, capital and goals; it is not an automatic instruction to sell equities, which could worsen feasibility.

## 8. USMV versus VTI: explain the evidence before selecting policy

USMV seeks lower portfolio volatility relative to broad US equities; it remains an equity investment and is not principal-protected. Minimum-volatility index construction considers covariance and constraints, not only individually stable shares. Current issuer methodology descriptions are educational references, not evidence of exact 2022 holdings. [S15, S16] VTI is the saved broad-market investable comparator.

| Measure | USMV | VTI |
|---|---:|---:|
| Training 2015-2022 CAGR | 9.55% | 9.59% |
| Training annual volatility | 12.84% | 16.31% |
| Training realized-RF Sharpe | 0.71 | 0.59 |
| Training CAPM beta | 0.698 | 0.988 |
| Evaluation 2023-2025 cumulative net return | 37.33% | 82.56% |
| Evaluation CAGR | 11.15% | 22.22% |
| Evaluation annual volatility | 9.64% | 12.54% |
| Evaluation annualized arithmetic excess return | 6.36% | 16.28% |
| Evaluation annualized excess-return volatility | 9.61% | 12.53% |
| Evaluation Sharpe | 0.66 | 1.30 |
| Evaluation maximum month-end drawdown | -5.66% | -9.11% |

Sharpe is computed as the monthly mean excess return divided by the sample standard deviation of monthly excess returns, multiplied by sqrt(12). Both portfolios use the same realized monthly French RF series. Its annualized arithmetic mean is 4.71% in evaluation. CAGR is not the Sharpe numerator. Total-return volatility and excess-return volatility are similar here but not identical.

USMV delivers about 39.08% of VTI's arithmetic excess return while retaining 76.69% of its excess-return volatility. Its reduced numerator dominates the volatility improvement, producing the lower Sharpe. The observed difference is unfavorable and economically meaningful; 36 observations do not by themselves establish a persistent future advantage for either ETF.

In the 25 VTI-positive months, mean monthly return is 2.07% for USMV versus 3.66% for VTI. In the 11 VTI-negative months, means are -1.68% versus -2.58%. The ratios are 56.55% and 64.98%, respectively. These are ratios of conditional arithmetic monthly means, not standardized compounded capture statistics. USMV lagged in each evaluation calendar year: 10.22% versus 25.92% in 2023; 15.74% versus 23.81% in 2024; 7.65% versus 17.10% in 2025.

Lower market exposure explains part of weaker participation, but it does not explain the entire gap. Applying frozen training FF3 coefficients to evaluation factor means gives this descriptive arithmetic bridge for USMV minus VTI, in annual percentage points:

| Component | Percentage points |
|---|---:|
| Market-factor loading difference | -4.21 |
| Size-factor loading difference | +1.68 |
| Value-factor loading difference | +0.21 |
| Fitted training-intercept difference | +1.68 |
| Out-of-sample remainder, including entry-cost effects | -9.29 |
| Total annualized arithmetic return difference | -9.92 |

The remainder is not identified stock-selection skill, nor proof that AI stocks alone caused the gap. Exact sector/security attribution needs dated portfolio holdings, constituent returns and trading/index-change information not established in this package. Historical fitted intercepts are shown only to reconcile the bridge; forecast alpha remains zero. Do not use current ETF holdings to explain historical positions.

### What the original USMV choice actually depended on

The original expected-return model uses a 4% risk-free assumption, 4.5% equity risk premium and zero forecast alpha. It implies 7.14% arithmetic expected return for USMV versus 8.45% for VTI. With training risk estimates and A=4, certainty equivalents are 3.84% and 3.13%. USMV is preferred because of the chosen penalty on variance, not a promise of greater returns.

The preference reverses when A falls below about 2.58, holding other inputs fixed; at A=4 it reverses when the market premium exceeds about 6.98%. A=4 was not statistically inferred from the trustees' 15% concern. The user's growth philosophy therefore warrants a preference discussion, not automatic confirmation of A=4.

Comparison candidates for a later approved scenario are: payment bonds plus USMV; the same bonds plus VTI; and the same bonds plus a documented USMV/VTI mix or explicit cash budget. Two US equity ETFs remain highly overlapping equity exposures. Evaluate the same funding, cost and risk rules, and preserve the original 2023-2025 comparison. Do not tune a new mix to win that evaluation period and call it an unseen test.

## 9. Benchmark architecture

A benchmark should answer a defined question. One number cannot simultaneously evaluate mission delivery, manager implementation and strategic opportunity cost.

| Layer | Question | Proposed measure | Interpretation |
|---|---|---|---|
| Payment delivery | Can and did Kappa pay on time? | Dated contractual cash-flow coverage; actual payment completion | Primary mission constraint; not a return index |
| Purchasing power | Is the remaining fund sufficient for the real objective? | Terminal assets divided by actual inflation factor; prospective shortfall distribution | Goal benchmark; not an investable portfolio |
| Strategic policy | Was the chosen allocation a reasonable use of the risk budget? | Liability-matched bond account plus VTI growth comparator, same starting resources and declared costs | Retains broad-market opportunity-cost accountability |
| Implementation | Did implementation deliver the authorized exposure efficiently? | USMV sleeve versus the appropriate USMV index/fund reference, with cost and tracking reconciliation | Diagnoses execution; cannot replace VTI and hide strategic underperformance |

VTI is already frozen as the growth benchmark. The user is reconsidering the broader architecture, not yet authorizing a replacement. A full-fund policy comparator must carry the same obligations, payment dates, cash treatment and cost conventions, with changing weights as payments occur. It is not simply VTI or a static 60/40 benchmark.

Because the bonds are fictional, no historical whole-fund total-return benchmark can be asserted without an explicitly labeled repricing scenario. Growth performance is historical; bond/funding performance remains contractual or scenario-based. Programme spending reduces assets but should not be counted as an investment loss in the manager's unitized return.

Report time-weighted performance to evaluate investment management alongside cash-flow and real-wealth measures that explain mission delivery. A donor-flow-driven rise in assets under management is not investment outperformance.

## 10. Dynamic rules, rebalancing and the 2030 transition

The frozen rule rebalances growth holdings annually after December returns to fixed weights. With 100% of that sleeve in USMV, this does not create a meaningful multi-asset rebalance, nor does it maintain the initial whole-fund equity percentage. It does not sell liability bonds to buy equities or implement an automatic stop-loss.

Proposed operating rhythm: monthly liquidity/coverage/performance dashboard; quarterly committee discussion of scenarios and risk; annual strategic review; immediate review for a mandate, custody, funding or material model-integrity event. Reviews are not compulsory trades.

If a future mixed growth/cash policy is adopted, specify target weights, allowed drift bands, transaction-cost budget, decision authority and order of funding. A 5 percentage-point band is an illustration to test, not a universal standard. Pay liabilities and replenish genuine cash needs first; rebalance only unencumbered capital. Do not sell protected bonds solely to restore an equity weight after a market fall.

Two policies need explicit separation: constant risk exposure versus securing progress toward the terminal goal. A predeclared glide path may gradually reduce growth exposure as the horizon shortens. A funded-status rule may secure part of a sufficiently funded goal. Neither is quantified as an executable new policy in this draft, because future permitted-asset prices and the intended terminal floor are not supplied.

A future nominal goal can be secured only at actual available prices or by holding enough cash under stated assumptions. Original 2022 executable bond prices cannot be reused as future trading quotes. Cash or fixed nominal cash flows do not lock in an unknown future real purchasing-power target.

An illustrative required-return diagnostic, when there are no additional growth-account flows, is:

`required CAGR = ((forecast nominal terminal goal - independently reserved terminal cash) / current growth assets) ** (1 / remaining years) - 1`.

If this becomes implausibly high, the committee must discuss funding, goals, spending and exposure. Raising risk to recover losses is not the automatic remedy. If new expenses or grants are introduced, use a timed cash-flow model instead of this simplified equation.

The all-bond original alternative remains a useful feasibility boundary: about USD 9.102m nominal terminal cash, USD 7.471m real at 2.5% inflation, missing the USD 8m goal by 6.62%. About USD 480,443 of additional initial capital would fund the original real-goal planning amount with the case bonds. Nominal funding still depends on the assumed inflation translation.

## 11. Governance proportionate to USD 12m

| Function | Proposed responsibility | Required evidence |
|---|---|---|
| Trustees/board | Approve mission, risk tolerance, permitted assets, spending, policy benchmarks and major amendments | Signed or recorded decision with quantified alternatives |
| Investment committee/CIO | Recommend allocation, maintain assumptions, propose trades and exceptions | Dated investment rationale and implementation plan |
| Independent risk reviewer | Challenge coverage, concentration, scenario assumptions, breaches and exceptions | Separate check; proposer cannot be sole checker |
| Operations/custody function | Reconcile positions and cash, execute approved payments, verify settlement | Dual approval and reconciliation record |
| Group members in this assignment | Perform genuine substantive work, independent checks and personal critiques | Names, actual contributions and file/table evidence; no invented staffing or work |

A small simulated group can allocate these roles across 3-4 people while preserving different proposer/checker identities. This is a proposed control design, not a claim that Kappa has employees, a regulated management company or live accounts.

The board dashboard should fit a concise pack: payment funding; unrestricted liquidity; real-goal estimate and shortfall severity; total-fund and growth drawdown; growth return versus VTI; implementation costs; factor/concentration exposures; rule breaches; and pending decisions. Where a metric has no reliable data, label it unavailable instead of manufacturing it.

Before introducing exclusions for educational values, ethical concerns or specific industries, define whether they are binding mission constraints or preferences and quantify opportunity costs. No existing exclusion list is assumed.

Scaling the foundation should depend on actual received capital, approved programmes and operating capacity. Donations are reported separately from investment returns. No growth plan may assume that fundraising rescues a deficit already created by the portfolio.

## 12. Policy change protocol

Separate three changes: a forecast revision within the same philosophy; a policy amendment changing limits or implementation; and a charter/mandate change redefining obligations, mission or permissible risk. A market narrative or an underperformance episode does not automatically require all three.

Every consequential proposal should state: triggering evidence and its release date; old and proposed rules; philosophical reason; funding impact; costs and liquidity; scenario effects and model limitations; alternatives rejected; approvers and dissent; implementation date; benchmark implications; review date; and reversal/re-entry conditions. Preserve the old version and distinguish retrospective analysis from prospective decisions.

The user's reference to a “revised mandate” has not yet supplied an actual release. This white paper is not that mandate and does not purport to answer it. Follow `MANDATE_REVISION.md` when the genuine document arrives.

## 13. Decisions for the next board conversation

The detailed question bank is in `Board_Consultation_Questions.md`. The first meeting should settle six choices before optimizing another portfolio: whether Kappa continues beyond 2030; whether USD 8m real remains the reference objective; whether 15% is an action threshold or an economic floor; how much adverse shortfall is tolerable; what operating costs genuinely exist; and what period/extent of broad-market underperformance trustees can withstand.

The adviser proposes a mission-first, liability-funded growth philosophy. The user has not yet approved new thresholds, a revised benchmark, a replacement ETF allocation, extra expenses or a dynamic trading rule. Those decisions remain open.

## 14. Evidence, reproduction and limitations

Local evidence: original assignment; `policy/frozen_policy.json`; `outputs/tables/initial_allocation.csv`, `funding_cashflows.csv`, `risk_preference.csv`, `training_performance.csv`, `evaluation_performance.csv`, `evaluation_calendar_years.csv`, `factor_regressions.csv`, `goal_sensitivity.csv`, `whole_fund_stress.csv`, `risk_limit_sensitivity.json`, and `all_bond_summary.json`.

New calculations are confined to this advisory folder. Run `python advisory/2026-10-16/diagnose_policy.py` from the project root using Python 3.12. It uses only the standard library and saved inputs. It reproduces evaluation Sharpe/cumulative returns, reconciles the factor bridge, checks the reserve baseline, and verifies the frozen-policy hash before and after. It does not re-optimize, retrieve data or alter frozen inputs.

Outputs: `sharpe_decomposition.csv`, `conditional_returns.csv`, `frozen_factor_gap_bridge.csv`, `reserve_tradeoffs.csv`, `diagnostic_receipt.json`. The original handoff manifest is preserved; new files are additive.

All external sources below were checked on 16 October 2026. Web retrieval and indexed snippets are analyst evidence, not a claim that full raw publications have been archived locally. Historical case data remain subject to revised vendor histories and survivorship/selection limitations. Numerical consistency does not validate forecasts or fulfill student contribution requirements.

## Source register

| ID | Source and link | Permitted use / retrieval status |
|---|---|---|
| S01 | [NBIM investment strategy](https://www.nbim.no/en/investments/investment-strategy/) | Current institutional design analogy; page read; not historical 2022 mandate evidence |
| S02 | [NBIM risk management](https://www.nbim.no/en/investments/risk-management/) | Current multi-metric risk design; page read |
| S03 | [Yale spending policy](https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions) | Current spending-governance analogy; page read |
| S04 | [CalPERS asset-liability management](https://www.calpers.ca.gov/about/organization/facts-at-a-glance/asset-liability-management) | Official indexed summary only; direct open failed; no detailed numerical limits used |
| S05 | [SEC investor bulletin on stop orders](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-15) | Execution mechanics; official indexed text; no protection guarantee |
| S06 | [BLS November 2022 CPI, released 13 December](https://www.bls.gov/news.release/archives/cpi_12132022.htm) | Pre-cutoff economic release; archived page read |
| S07 | [FOMC statement, 14 December 2022](https://www.federalreserve.gov/newsevents/pressreleases/monetary20221214a.htm) | Pre-cutoff policy decision; archived page read |
| S08 | [December 2022 Summary of Economic Projections](https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20221214.htm) | Pre-cutoff conditional forecasts; table inspected |
| S09 | [Federal Reserve explanation of its 2% objective](https://www.federalreserve.gov/faqs/economy_14400.htm) | PCE measurement definition; official indexed text |
| S10 | [BLS September 2026 CPI, released 14 October](https://www.bls.gov/news.release/archives/cpi_10142026.htm) | Contemporary learning only; release inspected |
| S11 | [FOMC statement, 16 September 2026](https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm) | Contemporary learning only; statement inspected |
| S12 | [IMF October 2026 WEO media briefing](https://mediacenter.imf.org/news/imf-world-economic-output-press-briefing/s/85df82f1-2ffe-44b3-91c4-a7a0e01042ae) | Contemporary learning only; 14 October release describes 13 October briefing; media text, not full WEO |
| S13 | [Brynjolfsson, Li and Raymond, Generative AI at Work](https://www.nber.org/papers/w31161) | 2023 working paper; official indexed abstract only; post-cutoff research |
| S14 | [Acemoglu, The Simple Macroeconomics of AI](https://www.nber.org/papers/w32487) | 2024 working paper; official indexed abstract only; post-cutoff research |
| S15 | [iShares USMV product description](https://www.ishares.com/us/products/239695/ishares-msci-usa-minimum-volatility-etf) | Current strategy objective; not historical holdings attribution |
| S16 | [iShares minimum-volatility explanation](https://www.ishares.com/us/investor-education/investment-strategies/what-is-minimum-volatility-investing) | Current educational methodology; no claim of unchanged historical constraints |

## Handoff block

Completed: original-mandate context clarified; contemporary institution/macro sources reviewed; Sharpe and frozen-factor gap diagnosed; cash-reserve and post-2027 exposure illustrations computed; proposed charter, risk, benchmark and amendment framework drafted; comprehensive board questions prepared.

Next: obtain the user's first-round governance decisions, resolve explicit cost and risk assumptions, then authorize a separate scenario comparison. Preserve the original recommendation and benchmark. The actual revised mandate, course AI/presentation rules and genuine member work remain external dependencies.

Prompt audit: the user's ten points are addressed in sections 2 (requirements), 1/4/10 (vision and growth), 6 (15% and red lines), 5/11 (funding and scale), 5 (liquidity), 7 (macro), 8 (USMV/VTI), 9 (benchmarks), 10 (rules), and 12 (policy change). Open decisions are labeled; no guaranteed return, calibrated success probability or fictional historical bond series is claimed.
