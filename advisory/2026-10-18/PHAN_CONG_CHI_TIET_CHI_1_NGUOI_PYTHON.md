# Kappa Foundation: phân công chi tiết khi chỉ một người làm Python

**Ngày lập:** 18/10/2026, giờ Việt Nam  
**Giả định:** nhóm có bốn người; chỉ Thành viên A (bạn) có thể chạy Python và thực hiện phân tích định lượng phức tạp.  
**Mục tiêu:** mỗi thành viên có một phần chuyên môn thật, sản phẩm cụ thể, người kiểm tra khác và nội dung có thể tự bảo vệ trước giảng viên.

## 1. Cách tổ chức nhóm

Nhóm nên vận hành như một investment committee nhỏ:

| Thành viên | Vai trò | Câu hỏi mà người đó phải trả lời được |
|---|---|---|
| **A — Quant Lead & Integration Lead (bạn)** | Dữ liệu, Python, mô hình, kết nối toàn bài | Các con số được tạo từ đâu, tính thế nào, giả định nào quyết định kết quả? |
| **B — Liability & Fixed-Income Analyst** | Nghĩa vụ, trái phiếu, dòng tiền, rủi ro lãi suất | Quỹ có chắc tiền trả đúng ngày không, và trái phiếu chịu rủi ro gì? |
| **C — Equity, ETF & Evidence Analyst** | USMV, VTI, candidate universe, nguồn và dữ liệu | Quỹ cổ phiếu đang mua cái gì, vì sao so sánh như vậy, bằng chứng có đúng mốc 2022 không? |
| **D — Investment Policy, Risk & Committee Analyst** | Mandate, benchmark, IPS, phản biện, trình bày | Hội đồng đang quyết định gì, giới hạn nào cứng, khi nào chính sách phải đổi? |

Bạn chịu trách nhiệm tích hợp, nhưng không “làm hộ” kết luận của ba người còn lại. Mỗi người phải tự viết phần của mình, tự nêu một điểm phản biện và tự trả lời câu hỏi khi trình bày.

## 2. USMV và VTI là gì?

### ETF là gì?

ETF là một chiếc “giỏ đầu tư” được mua bán trên sàn như một cổ phiếu. Thay vì mua từng công ty riêng, quỹ mua một chứng chỉ ETF và gián tiếp sở hữu phần nhỏ của nhiều công ty. ETF vẫn có thể giảm giá; chữ “quỹ” hoặc “đa dạng hóa” không tạo ra bảo đảm vốn.

### VTI là gì?

VTI là mã giao dịch của **Vanguard Total Stock Market ETF**. Trong bối cảnh ngày 31/12/2022 của bài, nó đại diện cho thị trường cổ phiếu Mỹ rất rộng, từ công ty lớn đến công ty nhỏ, với tỷ trọng chủ yếu đi theo giá trị thị trường. Có thể hình dung VTI là “mua gần như cả khu chợ cổ phiếu Mỹ”.

VTI phù hợp làm benchmark vì nó trả lời câu hỏi: nếu Kappa không chọn chiến lược đặc biệt mà chỉ mua thị trường Mỹ rộng, kết quả sẽ ra sao?

### USMV là gì?

USMV là mã giao dịch của **iShares MSCI USA Min Vol Factor ETF**. Quỹ này theo một chỉ số chọn và phối hợp các cổ phiếu Mỹ nhằm làm cho **cả giỏ** có mức biến động dự kiến thấp hơn trong những ràng buộc nhất định. Nó không đơn giản chọn các cổ phiếu có biến động riêng lẻ thấp nhất; mô hình còn xét cách các cổ phiếu chuyển động cùng nhau.

Có thể hình dung USMV là một người xếp hàng hóa trong giỏ sao cho chiếc giỏ rung ít hơn. Chiếc giỏ vẫn là cổ phiếu, vẫn có thể giảm mạnh, và không có lời hứa rằng lợi nhuận hay Sharpe luôn cao hơn VTI.

### Khác nhau theo ngôn ngữ rất đơn giản

| Câu hỏi | VTI | USMV |
|---|---|---|
| Mục tiêu | Đại diện thị trường cổ phiếu Mỹ rộng | Giảm biến động dự kiến trong phần cổ phiếu Mỹ |
| Cách tạo tỷ trọng | Chủ yếu theo quy mô thị trường | Tối ưu theo rủi ro và tương quan, có các giới hạn xây dựng chỉ số |
| Lợi thế mong đợi | Tham gia rộng vào tăng trưởng thị trường, dễ hiểu | Có thể biến động và drawdown thấp hơn thị trường trong một số giai đoạn |
| Đánh đổi | Chịu gần đầy đủ rủi ro thị trường | Có thể bỏ lỡ một phần thị trường tăng mạnh; vẫn chịu rủi ro cổ phiếu |
| Vai trò trong bài | Benchmark cho phần tăng trưởng | Phương án tăng trưởng được khuyến nghị trong chính sách gốc |

Nguồn hiện hành của [MSCI](https://www.msci.com/indexes/index/139133/msci-usa-minimum-volatility-index-usd) mô tả chỉ số minimum volatility là tối ưu từ vũ trụ MSCI USA để giảm absolute risk trong các giới hạn. [iShares](https://www.ishares.com/us/products/239695/ishares-msci-usa-minimum-volatility-etf) mô tả USMV là ETF theo chiến lược cổ phiếu Mỹ có đặc tính biến động thấp hơn. Các trang hiện hành dùng để hiểu sản phẩm; bằng chứng về mandate đúng tại năm 2022 phải dùng tài liệu có ngày trước mốc cắt trong hồ sơ dự án.

### Vì sao chính sách gốc chọn USMV nhưng VTI lại thắng trong 2023-2025?

Trong dữ liệu huấn luyện 2015-2022, USMV có CAGR gần VTI nhưng biến động thấp hơn. Mô hình giả định risk aversion A=4 nên phạt biến động đủ mạnh để USMV có certainty equivalent cao hơn. Đây là lựa chọn theo **mức ưa thích rủi ro đã giả định**, không phải bằng chứng USMV có expected return cao hơn.

Trong đánh giá 2023-2025, VTI hưởng lợi nhiều hơn từ thị trường tăng. Kết quả sau chi phí giả định:

| Chỉ tiêu | USMV | VTI |
|---|---:|---:|
| Lợi nhuận lũy kế | 37,33% | 82,56% |
| CAGR | 11,15% | 22,22% |
| Biến động năm | 9,64% | 12,54% |
| Sharpe | 0,66 | 1,30 |
| Maximum month-end drawdown | -5,66% | -9,11% |

USMV đã giảm biến động và drawdown, nhưng phần lợi nhuận bị bỏ lỡ lớn hơn lợi ích giảm biến động nên Sharpe thấp hơn. Đây là bằng chứng bất lợi cần giữ trong bài. Ba năm chưa đủ để chứng minh VTI sẽ luôn tốt hơn; cũng không được dùng kết quả 2023-2025 để giả vờ rằng quyết định năm 2022 biết trước tương lai.

## 3. “Kiểm tra độc lập” nghĩa là gì?

Kiểm tra độc lập không đòi hỏi người thứ hai phải viết lại toàn bộ chương trình. Nó có nghĩa là **một người khác dùng nguồn hoặc cách tính riêng để xem kết luận có đứng vững không**. Người kiểm tra không chỉ đọc dòng “passed” do cùng chương trình tạo ra.

Có năm kiểu kiểm tra phù hợp:

1. **Tính lại:** dùng máy tính hoặc Excel tính lại một con số từ dữ liệu đầu vào.
2. **Đối chiếu nguồn:** mở tài liệu gốc để kiểm tra ngày, điều khoản, ticker hoặc định nghĩa.
3. **Kiểm tra logic:** xem tiền có bị tính hai lần, dùng sai kỳ hay đảo quan hệ nguyên nhân-kết quả không.
4. **Truy vết:** chọn một con số trong slide, lần ngược về memo, CSV và nguồn/mã.
5. **Red-team:** cố tìm trường hợp làm khuyến nghị thất bại và yêu cầu nhóm giải thích.

Mỗi phiếu kiểm tra phải ghi:

| Trường | Nội dung cần ghi |
|---|---|
| Claim được kiểm tra | Ví dụ: “Beta đủ trả USD 2,4m năm 2024” |
| Tệp/nguồn đầu vào | Tên PDF, CSV, trang hoặc dòng dữ liệu |
| Cách kiểm tra | Công thức hoặc các bước bằng lời |
| Kết quả riêng của người kiểm tra | Số tự tính hoặc kết luận từ nguồn |
| So với output chính | Khớp/không khớp; sai lệch bao nhiêu |
| Giới hạn | Phần nào chưa được kiểm tra |
| Tên và ngày | Người kiểm tra thật và ngày thực hiện |

Ví dụ đơn giản mà Thành viên B có thể làm không cần Python:

- Beta: 2.400 trái phiếu x USD 922,78 = USD 2.214.672 chi phí ban đầu; đến hạn nhận USD 2.400.000.
- Delta: cần mệnh giá `3.600.000 / 1,035 = 3.478.260,87`; chi phí là `3.478,26087 x 986,07 = 3.429.808,70`; coupon năm là `3.478.260,87 x 3,5% = 121.739,13`; năm 2027 principal + coupon = USD 3,6m.
- Tổng vốn: Beta + Delta + USMV + USD 9.168,59 chi phí phải bằng USD 12m.

Ví dụ Thành viên C có thể làm bằng Excel:

- Chọn hai tháng của VTI và USMV trong `data/processed/train_month_end_adjusted_prices.csv`.
- Tính `giá tháng này / giá tháng trước - 1`.
- So với đúng tháng trong `data/processed/train_monthly_returns.csv`.
- Ghi sai lệch do làm tròn nếu có. Không lưu đè dữ liệu gốc.

Ví dụ Thành viên D kiểm tra logic:

- Slide nói “mức lỗ 15% không thể được bảo đảm”.
- Mở `outputs/tables/whole_fund_stress.csv` và tìm kịch bản cổ phiếu -30%, lãi suất +100bp.
- Xác nhận loss fraction khoảng 17,53% nhưng cột payment cash flows vẫn không đổi trong giả định đề.
- Kết luận đúng phải gồm cả hai vế: giá trị thị trường có thể vượt ngưỡng lỗ, trong khi dòng tiền nghĩa vụ vẫn được bảo vệ theo giả định không vỡ nợ.

## 4. Thành viên A: Quant Lead & Integration Lead — bạn

### Trách nhiệm

Bạn là người duy nhất được giao chạy pipeline và sửa mã định lượng. Bạn quản lý phiên bản, giữ dữ liệu gốc, giải thích công thức và kết nối output của ba thành viên vào memo/slide. Bạn không tự chứng nhận rằng mọi giả định tài chính đều đúng.

### Cách làm

1. Đọc `README.md`, `CHECKPOINT.md`, `DECISION_LOG.md` và `EVIDENCE_MAP.md`.
2. Tạo một bản sao làm việc khi có mandate mới; không sửa `policy/frozen_policy.json`.
3. Dùng `analysis/rebuild.py` khi cần tái tạo từ dữ liệu đã lưu. Không tải dữ liệu mới chỉ để “làm lại”, vì dữ liệu gốc và evaluation đã được lưu riêng.
4. Lập bảng assumptions: case date, lạm phát, RF, ERP, A, chi phí, benchmark, constraints và quy tắc tái cân bằng.
5. Với mỗi claim quan trọng, ghi file output tạo ra nó và giới hạn diễn giải.
6. Khi mandate mới đến, thay đúng tham số bị ảnh hưởng trong scenario riêng, giữ cùng case date và cutoff, rồi so sánh với chính sách gốc.

### Output bắt buộc của A

| Mã | Output | Tiêu chuẩn hoàn thành |
|---|---|---|
| A1 | **Technical run log**, 1-2 trang | Lệnh chạy, thời điểm, input, output, lỗi/cảnh báo và hash policy trước/sau |
| A2 | **Assumption register**, 1 trang | Mỗi giả định có giá trị, lý do, nguồn, người sở hữu và sensitivity liên quan |
| A3 | **Evidence map cập nhật** | Mỗi bảng/biểu đồ/claim quan trọng trỏ đến đúng CSV hoặc JSON |
| A4 | **Scenario comparison sau mandate mới** | Original, revised, chênh lệch, nguyên nhân và giới hạn; không thay file frozen |
| A5 | **Teach-back 5 phút** | Giải thích pipeline: raw data → monthly returns → model → output → memo bằng lời đơn giản |

### Ai kiểm tra A?

- B kiểm tra lại ba phép tính trái phiếu và cash-flow.
- C tính lại hai monthly returns và kiểm tra nguồn/ticker.
- D truy vết ba claims từ slide về bảng nguồn và kiểm tra không vượt quá bằng chứng.

### Hướng chuyên sâu của A

- **Model-risk register:** với mỗi mô hình, ghi điều nó giả định, lỗi có thể xảy ra và quyết định nào bị ảnh hưởng.
- **Lifecycle risk:** lượng hóa việc tỷ trọng cổ phiếu tăng sau khi trái phiếu đáo hạn và quỹ trả nghĩa vụ; đây là điểm mạnh hơn việc chỉ nhìn allocation ban đầu.
- **Shortfall severity:** ngoài tần suất hụt mục tiêu, báo median shortfall hoặc các percentile thấp để Hội đồng biết “hụt bao nhiêu”.
- **Decision threshold:** tính điều kiện làm USMV/VTI đảo thứ hạng, như A hoặc equity risk premium, và giải thích theo ngôn ngữ Hội đồng.

## 5. Thành viên B: Liability & Fixed-Income Analyst

B không cần Python. B chịu trách nhiệm chứng minh quỹ có tiền trả đúng ngày và hiểu rủi ro của phần trái phiếu.

### Cách làm từng bước

1. Đọc trang 1-2 của đề và trang 2-3 của memo.
2. Viết hai nghĩa vụ trên một timeline: USD 2,4m năm 2024 và USD 3,6m năm 2027.
3. Tính lại Beta và Delta bằng công thức phía trên; ghi rõ mệnh giá, số “bond units”, giá trên mỗi USD 1.000 face và coupon.
4. Mở `outputs/tables/funding_cashflows.csv`; đi từng năm và kiểm tra coupon, principal, payment và cash tích lũy.
5. Mở `bond_metrics.csv` và `bond_stress.csv`; giải thích duration là độ nhạy gần đúng, convexity cải thiện phép gần đúng, exact repricing là kiểm tra trực tiếp.
6. Viết điểm phản biện: ví dụ rủi ro settlement/timing ngoài đời, rủi ro dùng coupon hai lần, hoặc giới hạn của giả định zero reinvestment/default-free.

### Output bắt buộc của B

| Mã | Output | Hình thức cụ thể |
|---|---|---|
| B1 | **Bond verification sheet** | 1 trang, có công thức Beta/Delta, số tự tính và so với output |
| B2 | **Liability timeline** | Một bảng hoặc sơ đồ 2023-2030, đánh dấu coupon, maturity và payment |
| B3 | **Interest-rate risk note** | 500-700 từ: YTM, duration, convexity, exact repricing và ý nghĩa đối với nghĩa vụ |
| B4 | **Independent critique** | 3-5 câu do B tự viết về điểm yếu của phương án |
| B5 | **Presentation ownership** | Chuẩn bị nói slide 2-5 và trả lời ít nhất 6 câu hỏi khó |

### Hướng nghiên cứu sâu của B

- **Asset-liability matching:** phân biệt “giá trái phiếu biến động” với “dòng tiền đáo hạn vẫn đủ”.
- **Curve risk:** giải thích parallel shift khác steepener ra sao; không cần tự fit curve bằng Python.
- **Operational liquidity:** nếu maturity/payment cùng ngày, settlement thực tế cần chuẩn bị gì? Ghi đây là mở rộng thực tế ngoài giả định đơn giản của đề.
- **Coverage covenant:** đề xuất quy tắc không dùng payment assets nếu chưa có dòng tiền thay thế đúng hạn.

Đây là contribution chuyên sâu vì nó chuyển bài từ “tính giá bond” sang “quản trị nghĩa vụ như một tổ chức”.

## 6. Thành viên C: Equity, ETF & Evidence Analyst

C không cần chạy mô hình. C sở hữu câu chuyện VTI/USMV, tính hợp lệ của chứng khoán ở mốc 2022 và nguồn dữ liệu.

### Cách làm từng bước

1. Đọc trang 4-7 của memo và mục eligibility/data trong `deliverables/Kappa_Requirements_and_Data_Guide.md`.
2. Đọc `data/raw/supporting/eligibility_checks.json`; lập bảng 10 tickers, loại tài sản, ngành/mandate, nguồn trước cutoff và điểm cần xác nhận.
3. Với VTI và USMV, viết riêng bốn mục: objective, construction intuition, expected behavior, failure modes.
4. Tính lại hai monthly returns bằng Excel như hướng dẫn ở mục 3.
5. Mở `evaluation_performance.csv`; so sánh return, volatility, Sharpe và drawdown. Không chọn ETF từ một chỉ tiêu đơn lẻ.
6. Mở `factor_regressions.csv`; giải thích beta/alpha/interval theo lời thường. Nếu khoảng alpha đi qua 0, không được nói alpha đã được chứng minh.
7. Kiểm tra mọi nguồn hiện hành có đang được dùng chỉ để giải thích, hay bị dùng sai để khẳng định trạng thái năm 2022.

### Output bắt buộc của C

| Mã | Output | Hình thức cụ thể |
|---|---|---|
| C1 | **VTI versus USMV explainer** | 2 trang, có bảng so sánh và phần “when each may disappoint” |
| C2 | **Eligibility and provenance matrix** | 10 dòng cho 8 stocks + 2 ETFs; ticker, sector/mandate, dated source, cutoff status, limitation |
| C3 | **Monthly-return check** | Excel hoặc bảng 1 trang, tính lại hai tháng và so với CSV |
| C4 | **Adverse-evidence note** | 500 từ giải thích vì sao USMV lag VTI nhưng chưa đủ để kết luận dài hạn |
| C5 | **Independent critique** | 3-5 câu của C về selection/survivorship/model risk |
| C6 | **Presentation ownership** | Chuẩn bị nói slide 6, 9 và 10 |

### Hướng nghiên cứu sâu của C

- **Strategic benchmark versus implementation benchmark:** VTI đo chi phí cơ hội của lựa chọn chiến lược; chỉ số USMV đo ETF có theo đúng mandate không.
- **Factor interpretation:** USMV có market beta thấp hơn; dùng FF3 để mô tả exposure, không biến regression thành dự báo chắc chắn.
- **Regime behavior:** giải thích low-volatility strategy có thể tham gia ít hơn khi thị trường tăng mạnh và bảo vệ phần nào khi thị trường giảm; kiểm tra bằng kết quả đã lưu, tránh causal claim khi thiếu holdings lịch sử.
- **Survivorship and selection bias:** candidate universe là danh sách sống sót được chọn hồi cứu; nêu rõ điều này làm yếu claim “unseen strategy”.
- **Methodology drift:** phương pháp chỉ số có thể đổi theo thời gian. Source hiện nay không được dùng thay cho prospectus/index method năm 2022.

## 7. Thành viên D: Investment Policy, Risk & Committee Analyst

D không cần Python. D biến các con số thành quyết định của Hội đồng và chịu trách nhiệm phản biện.

### Cách làm từng bước

1. Đọc toàn bộ đề và lập bảng “requirement → memo page → slide → output”.
2. Đọc `DECISION_LOG.md`, `TEAM_COMPLETION.md`, `MANDATE_REVISION.md` và white paper thảo luận.
3. Soạn một mini-IPS gồm: purpose, priority of objectives, eligible assets, liquidity, risk definitions, benchmarks, rebalancing, monitoring, authority và amendment process.
4. Phân biệt hard rules và dynamic rules. Ví dụ no borrowing là hard rule; inflation assumption là dynamic parameter.
5. Kiểm tra claim 15% bằng bảng stress và viết response ladder: warning, escalation, evidence, approver, expiry.
6. Viết “best case against our recommendation”: giả định nào sai, bằng chứng nào khiến Hội đồng đổi từ USMV sang VTI/cash/all-bond.
7. Xây câu chuyện slide theo dòng: mandate → funding → risk capacity → growth choice → adverse evidence → conditions for change.

### Output bắt buộc của D

| Mã | Output | Hình thức cụ thể |
|---|---|---|
| D1 | **Rubric and evidence matrix** | Mỗi yêu cầu/điểm số của đề nối với trang, slide, CSV và người sở hữu |
| D2 | **Mini Investment Policy Statement** | 2-3 trang, văn phong Hội đồng; các con số chưa duyệt phải ghi “proposed” |
| D3 | **Red-team memorandum** | 1 trang: ba lý do mạnh nhất để bác khuyến nghị và bằng chứng cần để đổi quyết định |
| D4 | **Mandate-change checklist** | Original requirement, revised wording, parameter affected, numerical output required, approver |
| D5 | **Q&A bank** | Tối thiểu 15 câu hỏi giảng viên có thể hỏi, phân công người trả lời |
| D6 | **Independent critique** | 3-5 câu của D về governance/risk/goal feasibility |
| D7 | **Presentation ownership** | Mở đầu, slide 1, 11-13 và kết luận |

### Hướng nghiên cứu sâu của D

- **Investment Policy Statement:** CFA Institute mô tả IPS là công cụ làm rõ objectives, constraints, governance, monitoring và accountability. D có thể dùng [khung IPS cho institutional investors](https://rpc.cfainstitute.org/policy/positions/elements-of-an-investment-policy-statement-for-institutional-investors) làm chuẩn cấu trúc; không sao chép các giới hạn số từ tổ chức khác.
- **Risk capacity versus risk willingness:** Kappa có thể sẵn lòng chịu rủi ro, nhưng nghĩa vụ gần hạn làm giảm khả năng chịu rủi ro của phần vốn dành cho payments.
- **Benchmark hierarchy:** payment delivery, real purchasing power, strategic benchmark và implementation benchmark trả lời bốn câu hỏi khác nhau.
- **Governance of exceptions:** nếu drawdown vượt 15% trong khủng hoảng, ai được quyết định giữ/bán, bằng chứng gì, thời hạn ngoại lệ bao lâu?
- **Decision under uncertainty:** trình bày điều chưa biết và condition for change; đây là dấu hiệu của judgment chuyên nghiệp.

## 8. Ma trận kiểm tra chéo

| Sản phẩm chính | Người làm | Người kiểm tra | Kiểm tra cái gì? |
|---|---|---|---|
| Pipeline, monthly returns, model outputs | A | C | Hai return tính tay, tháng/cutoff, định nghĩa adjusted price |
| Bond funding và interest-rate interpretation | B | A | Công thức, đơn vị, exact repricing và cash-flow coverage |
| VTI/USMV và source matrix | C | D | Claim có vượt nguồn không; current source có bị dùng cho 2022 không |
| IPS, risk trigger và rubric map | D | B | Nghĩa vụ có giữ ưu tiên không; policy có mâu thuẫn dòng tiền không |
| Final memo numerical claims | A tích hợp | B + C + D | Mỗi người kiểm phần mình, ký/ngày và ghi giới hạn |
| Final deck | D tích hợp nội dung | A kiểm số; B/C kiểm phần chuyên môn | Slide → memo → CSV/source; mở PPTX thật và tập Q&A |

Đây mới là “independent check”: người khác thực hiện một phép kiểm tra có thể nhìn thấy, chứ không chỉ nói “đã đọc và thấy ổn”.

## 9. Phần mở rộng nào gây ấn tượng với lecturer?

### Ưu tiên 1 — Liability-first governance

Trình bày quỹ thành ba “túi”: payment assets, liquidity reserve nếu có, và growth assets. Giải thích mỗi túi có mục tiêu, benchmark và risk measure riêng. Đây là cách tư duy gần với institutional asset-liability management và phù hợp trực tiếp với đề.

**Output:** một sơ đồ vốn ban đầu và timeline dòng tiền; một policy rule không được lấy tiền trong payment account để “buy the dip”.

### Ưu tiên 2 — Lifecycle risk sau mỗi payment

Allocation ban đầu có khoảng 52,9% equity, nhưng khi bonds đáo hạn và payments được trả, tài sản còn lại có thể trở nên gần như toàn equity. Bản phân tích advisory đã minh họa khoảng 94,3% equity sau payment 2027 trên một đường tăng trưởng xác định. Đây là một vấn đề chiến lược mạnh: mức 15% có còn hợp lý ở 2028-2030 không?

**Output:** bảng tỷ trọng theo năm hoặc theo các mốc trước/sau payment; đề xuất review/glide-path concept nhưng không dùng giá trái phiếu tương lai bịa đặt.

### Ưu tiên 3 — Benchmark architecture

Đừng dùng một benchmark cho mọi câu hỏi:

- Payment benchmark: trả đủ và đúng hạn.
- Mission benchmark: sức mua thực còn lại.
- Strategic benchmark: payment bonds + VTI growth comparator.
- Implementation benchmark: USMV có theo đúng index/chi phí dự kiến không.

**Output:** một bảng dashboard có bốn lớp và giải thích khi mỗi lớp cho tín hiệu xấu.

### Ưu tiên 4 — Model-risk and assumption register

Mỗi mô hình cần một “nhãn cảnh báo”: dữ liệu nào, giả định nào, giới hạn nào, quyết định nào phụ thuộc vào nó. Ví dụ simulation dùng lịch sử và return assumption; 68,48% là conditional modeled frequency, không phải calibrated probability.

**Output:** bảng 6-8 dòng gồm inflation, ERP, A, covariance, block simulation, transaction cost, cash reinvestment và survivor universe.

### Ưu tiên 5 — Adverse-evidence and pre-mortem

Giả sử năm 2030 kế hoạch thất bại. Viết trước ba nguyên nhân: inflation cao hơn, USMV return thấp, hoặc equity loss xảy ra sau khi bonds đã chi trả. Sau đó nêu indicator và action cho từng nguyên nhân.

**Output:** một trang “How this policy can fail” với trigger, evidence, response và owner.

### Ưu tiên 6 — Revised-mandate attribution

Khi mandate mới tới, tách tác động do trustee thay đổi yêu cầu khỏi thay đổi tự nguyện của mô hình. Giảng viên sẽ dễ thấy nhóm không dùng mandate mới làm cớ viết lại lịch sử.

**Output:** bảng original / revised / difference / why / decision effect, giữ cùng cutoff 31/12/2022.

### Ưu tiên 7 — Reproducibility plus human governance

Đã có code và hash. Giá trị tăng thêm là “ai chịu trách nhiệm”: ai chọn giả định, ai kiểm, ai phê duyệt, khi nào xem xét lại. Kết nối kỹ thuật với governance thường ấn tượng hơn thêm một optimizer.

**Output:** RACI nhỏ cho assumptions, data, model, policy, mandate response và final submission.

## 10. Những phần mở rộng nên tránh hoặc chỉ làm khi còn thời gian

- Thêm machine learning, Black-Litterman, neural network hoặc hàng chục ETF chỉ để bài trông phức tạp. Chúng mở thêm assumptions và dễ làm loãng yêu cầu chính.
- Dùng dữ liệu vĩ mô hoặc ETF holdings sau 2022 để biện hộ hồi tố cho quyết định ngày 31/12/2022.
- Tối ưu một blend mới bằng cách nhìn trước giai đoạn 2023-2025 rồi gọi đó là out-of-sample.
- Gọi simulation frequency là xác suất khách quan hoặc gọi stop-loss là bảo đảm tối đa 15%.
- Đưa các asset ngoài đề như international equity, derivatives, gold hoặc private markets vào original-case recommendation.
- Thêm chart mà không trả lời câu hỏi quyết định nào.

## 11. Thứ tự công việc thực tế từ 18 đến 22/10

| Khi nào | A | B | C | D |
|---|---|---|---|---|
| 18/10 | Giao file, giải thích pipeline 30 phút | Đọc đề trang 1-2; bắt đầu B1/B2 | Đọc memo 4-7; bắt đầu C1/C2 | Đọc đề; bắt đầu D1 |
| 19/10 | Hoàn thành A1/A2; trả lời câu hỏi dữ liệu | Tính Beta/Delta/coupon; kiểm cash flow | Tính hai returns; so USMV/VTI | Soạn mini-IPS và red-team outline |
| 20/10 | Cung cấp evidence map; sửa lỗi được chứng minh | Hoàn thành B3/B4 | Hoàn thành C4/C5 | Hoàn thành D2/D3/D5 |
| 21/10 | Tích hợp hồ sơ 2 trang và file nộp | Kiểm số phần bond | Kiểm nguồn và ETF claims | Kiểm rubric/format; tổ chức rehearsal |
| 22/10 trước 16:00 | Người được nhóm giao nộp và giữ receipt | Xác nhận phần mình | Xác nhận phần mình | Xác nhận package và contribution log tạm thời |

Ngày 23/10 sau 16:00, lưu mandate mới nguyên bản; A chạy scenario, B kiểm nghĩa vụ mới, C kiểm tác động đến growth universe/benchmark, D quản lý comparison và policy change log.

## 12. Câu hỏi giảng viên có thể hỏi và người trả lời

| Câu hỏi | Người chính | Ý trả lời phải có |
|---|---|---|
| Vì sao không mua toàn bonds? | B + D | All-bond bảo vệ nominal cash nhưng hụt real goal theo giả định; nêu trade-off, không nói equity chắc thắng |
| Vì sao chọn USMV thay vì VTI? | C + A | A=4 và risk estimates trước cutoff; threshold đảo chiều; adverse evaluation được giữ |
| 15% có thật sự được bảo đảm không? | D + B | Không; escalation threshold, stress 17,53%, payment cash flows vẫn được bảo vệ trong case assumptions |
| Alpha có chứng minh adviser đúng không? | C + A | Đọc confidence interval/p-value/model/sample; forecast alpha bằng 0 |
| Vì sao dùng 2,5% inflation? | D + A | Planning assumption + sensitivity; không phải fact; real goal và nominal translation tách biệt |
| Có data leakage không? | A + C | Policy frozen trước eval retrieval; 2023-2025 không re-estimate original policy |
| Thành viên không code đóng góp gì? | B/C/D tự trả lời | Chỉ đúng output thật, independent check thật và critique thật của mình |

## 13. Tiêu chuẩn một contribution tốt

Một contribution được coi là có chất lượng khi đáp ứng năm điều:

1. Có câu hỏi quyết định rõ ràng.
2. Có output cụ thể được lưu và có ngày.
3. Có nguồn hoặc phép tính để người khác kiểm tra.
4. Có một người khác kiểm tra độc lập và ghi kết quả.
5. Người làm có thể giải thích giới hạn và trả lời phản biện.

Số trang dài hoặc thuật ngữ phức tạp không tự tạo ra contribution tốt. Một trang kiểm tra dòng tiền đúng và giải thích rõ có thể giá trị hơn một mô hình mà nhóm không hiểu.

## 14. Thông tin cần điền để khóa phân công

Thay A/B/C/D bằng tên thật và ghi:

- Tên, mã sinh viên nếu cần.
- Mức độ thoải mái với Excel, đọc tiếng Anh và thuyết trình.
- Output được giao và ngày hoàn thành.
- Người kiểm tra chéo.
- Slide sẽ trình bày.
- Một critique tự viết.

Không ghi đóng góp ở thì quá khứ trước khi công việc thật sự hoàn thành.

## Handoff block

Đã hoàn thành: thiết kế lại phân công theo giả định chỉ A chạy Python; giải thích USMV/VTI; định nghĩa và ví dụ independent checks; quy định output cho bốn thành viên; ma trận kiểm tra chéo; danh sách extension có giá trị; lịch trước hạn 22/10 và Q&A ownership.

Việc tiếp theo: người dùng cung cấp tên/ký hiệu và năng lực B/C/D; cập nhật bảng phân công và contribution log. Sau đó nhóm thực hiện outputs và ghi bằng chứng thật. Course AI policy và actual revised mandate vẫn cần được cung cấp, không được suy đoán.

Prompt audit: đã trả lời các yêu cầu phân việc khi chỉ một người làm Python, công việc/cách làm/output cụ thể, USMV/VTI, independent check, hướng nghiên cứu sâu và cách tạo góc nhìn chuyên gia. Không thay allocation frozen, không tạo claim rằng thành viên đã thực hiện công việc, và không dùng dữ liệu post-2022 để viết lại quyết định ban đầu.
