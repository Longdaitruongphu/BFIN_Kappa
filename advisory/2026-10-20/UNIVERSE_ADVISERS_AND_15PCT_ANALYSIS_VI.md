# So sánh universe, vai trò cổ phiếu, kết quả hai giai đoạn và tranh luận Eta–Theta

**Ngày phân tích:** 20/10/2026. **Quyết định gốc:** 31/12/2022. Tài liệu này dùng số liệu đã khóa trong dự án, giúp nhóm trình bày rõ mã nào chỉ là ứng viên nghiên cứu và mã nào thật sự được đề xuất nắm giữ. Nó không thay đổi chính sách gốc.

## 1. Có ba danh sách khác nhau, không phải một danh sách

| Nguồn | 8 cổ phiếu | 2 ETF | Số tháng | Đánh giá |
| --- | --- | --- | ---: | --- |
| Universe của dự án đã khóa | AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE | VTI, USMV | 96, 01/2015–12/2022 | Danh sách chính dùng để ước lượng, tối ưu và quyết định. Bao phủ 7 ngành cổ phiếu. |
| Role C `C1&2_eligibility` và `Returns_data` | MSFT, JNJ, UNH, JPM, PG, XOM, HD, NEE | VTI, USMV | 96, 01/2015–12/2022 | 6 cổ phiếu trùng danh sách dự án; đổi AAPL/CAT thành UNH/HD. Vẫn đủ 8 mã, 7 ngành (Healthcare có 2 mã), và đủ hai ETF. Các mã trùng khớp gần sát với dữ liệu dự án; UNH/HD không có dữ liệu raw cùng dự án để kiểm độc lập. |
| Role C `Stock Returns` và `Multifactor Regression` | AAPL, BAC, JNJ, JPM, KO, MSFT, PFE, PG | QQQ, SPY | 95, 02/2015–12/2022 | Một universe thứ ba. Có 5 cổ phiếu trùng với dự án, thêm BAC/KO/PFE, bỏ XOM/CAT/NEE và hai ETF VTI/USMV. Đủ 8 cổ phiếu nhưng chỉ 4 ngành, tuy vậy vượt mức tối thiểu 4 ngành của đề. Hai ETF có mandate khác: QQQ thiên Nasdaq-100, SPY là S&P 500. Đây không phải universe đã khóa cho khuyến nghị dự án. |

Vậy Role C không chỉ có “một list khác”. Eligibility và `Returns_data` là một universe thay AAPL/CAT bằng UNH/HD. `Stock Returns` và hồi quy là universe khác nữa, thay ETF VTI/USMV bằng QQQ/SPY và có 95 thay vì 96 tháng. QQQ theo Nasdaq-100, còn SPY theo S&P 500; mandate khác nhau rõ với USMV minimum-volatility và VTI total-market. Bảng FF3 của Role C khớp chính xác với dự án ở 96 tháng; hồi quy 95 tháng tính lại được từ `Stock Returns` sau khi căn tháng. Điều này cho thấy phép tính có thể hợp lý về số học, nhưng không làm các universe trở thành cùng một danh mục. Chưa có lý do được ghi nhận trong workbook cho hai lần đổi list. Các mô tả mandate hiện hành có thể kiểm tại [Invesco QQQ](https://www.invesco.com/us/en/financial-products/etfs/invesco-qqq-trust-series-1.html) và [SPY của State Street](https://www.ssga.com/library-content/products/factsheets/etfs/us/factsheet-us-en-spy.pdf); bằng chứng điều kiện tại cutoff 2022 vẫn phải có ngày phù hợp.

Trong `C1&2_eligibility`, cả 10 hàng có URL hồ sơ Yahoo hiện tại và ngày truy cập tháng 10/2026; cột file bằng chứng và người kiểm độc lập để trống. VTI có hàng riêng ở dòng 12, được ghi là benchmark; USMV ở dòng 11, được ghi là defensive factor sleeve. Vì vậy hai ETF có rationale, nhưng tài liệu gốc để chứng minh đủ điều kiện tại cutoff 2022 chưa được đính kèm ở các cột đó. Việc này là thiếu hồ sơ kiểm chứng, không tự nó chứng minh mã nào không hợp lệ.

## 2. Vì sao universe chính có các mã đó và mỗi mã làm gì trong nghiên cứu

Quỹ không mua tất cả cổ phiếu chỉ vì đã chọn chúng vào universe. Assignment yêu cầu một bộ ứng viên đa ngành để so sánh mô hình và xác định ETF growth đơn giản. Bảng dưới giải thích giả thuyết kinh tế và kết quả ước lượng 2015–2022. `Historical mean` là lợi suất số học bình quân tháng nhân 12; `Forecast` là đầu vào phán đoán `4% + beta × 4.5%`. Hai cột này không phải lợi suất CAGR và không phải dự báo đảm bảo.

| Mã | Vai trò/giả thuyết | Historical mean 2015–22 | Volatility năm | Beta CAPM | Forecast số học | Trọng số Sample A4 / Index A4 / Eta lịch sử |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| AAPL | Công nghệ, thiết bị/dịch vụ; growth exposure và kiểm tra liệu lợi suất lịch sử cao có thể dự báo được không | 25.01% | 29.13% | 1.208 | 9.44% | 0% / 0% / 10% |
| MSFT | Phần mềm/cloud; công nghệ nhưng biến động lịch sử thấp hơn AAPL, là mã trọng yếu để kiểm tra luận điểm alpha Theta | 24.88% | 22.50% | 0.959 | 8.32% | 2.21% / 0% / 10% |
| JPM | Ngân hàng, chu kỳ tín dụng và lãi suất; kiểm tra rủi ro tài chính theo chu kỳ | 15.57% | 25.39% | 1.146 | 9.16% | 2.88% / 0% / 0% |
| JNJ | Y tế/pharmaceuticals; cầu tương đối phòng thủ, beta thấp hơn thị trường | 10.48% | 15.61% | 0.525 | 6.36% | 6.67% / 10% / 0% |
| PG | Hàng tiêu dùng thiết yếu; cầu ổn định, thử vai trò phòng thủ | 10.54% | 15.95% | 0.368 | 5.66% | 10% / 10% / 0% |
| XOM | Năng lượng/giá hàng hóa; có thể hưởng lợi khi giá năng lượng tăng nhưng bản thân cổ phiếu vẫn biến động cao | 10.91% | 28.94% | 1.023 | 8.60% | 2.24% / 0% / 0% |
| CAT | Công nghiệp/thiết bị vốn; nhạy với đầu tư, chu kỳ kinh tế và chi phí đầu vào | 19.22% | 29.44% | 1.136 | 9.11% | 0% / 0% / 0% |
| NEE | Điện lực/utility; giả thuyết phòng thủ nhưng nhạy lãi suất do đặc tính giống tài sản duration dài | 18.71% | 18.84% | 0.391 | 5.76% | 6.00% / 10% / 10% |

| ETF | Vai trò | Historical mean 2015–22 | Volatility năm | Beta CAPM | Forecast số học | Trọng số Sample A4 / Index A4 / Eta lịch sử |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| VTI | Thị trường cổ phiếu Mỹ rộng; comparator có thể đầu tư cho growth sleeve | 10.52% | 16.31% | 0.988 | 8.45% | 18.10% / 11.34% / 0% |
| USMV | Danh mục cổ phiếu Mỹ tối thiểu hóa biến động tương đối; lựa chọn phòng thủ cho growth sleeve | 9.97% | 12.84% | 0.698 | 7.14% | 51.90% / 58.66% / 70% |

ETF vẫn là cổ phiếu. USMV có thể giảm biến động so với VTI nhưng không bảo toàn vốn, không phải trái phiếu và không khóa mức lỗ 15%. Các số lịch sử là 96 tháng đã chọn, gồm đại dịch và 2022 nhưng bỏ khủng hoảng tài chính 2008–09; danh sách cổ phiếu sống đến hiện tại cũng tạo survivorship/selection bias. Do đó lợi suất lịch sử rất cao của AAPL/MSFT/CAT/NEE không được đưa thẳng vào forecast. Model dùng beta và equity risk premium, forecast alpha bằng 0.

### 2015–2022, hai ETF và các cách tạo growth sleeve

| Chiến lược | CAGR lịch sử | Volatility | Sharpe lịch sử | Drawdown cuối tháng lớn nhất | Ý nghĩa |
| --- | ---: | ---: | ---: | ---: | --- |
| VTI | 9.59% | 16.31% | 0.59 | -24.82% | Tăng trưởng theo toàn thị trường; rủi ro cao hơn USMV trong cửa sổ mẫu. |
| USMV | 9.55% | 12.84% | 0.71 | -19.06% | Gần bằng CAGR nhưng biến động và drawdown lịch sử thấp hơn trong mẫu. Đây là lý do dữ liệu hỗ trợ xem USMV là lựa chọn thận trọng hơn tại cutoff. |
| Eta historical-Sharpe proxy | 13.71% | 13.65% | 0.95 | -18.83% | Trọng số chọn theo dữ liệu huấn luyện, đặt giới hạn 10% mỗi cổ phiếu/30% cổ phiếu trực tiếp; vẫn vượt 15% drawdown lịch sử. |

Eta proxy được chọn tối ưu hóa lợi suất lịch sử so với mốc RF kế hoạch 4%, không phải là phép ước lượng alpha bền vững. Hàng `historical_sharpe_definition_audit.csv` cho một biến thể trừ RF lịch sử theo tháng: biến thể đó có thay đổi tỷ trọng nhẹ (CAT 1.04%, AAPL 8.96% thay vì AAPL 10%), minh họa rằng lựa chọn Eta cũng phụ thuộc định nghĩa Sharpe. Cả hai đều khớp số liệu đã quan sát, nhưng tối ưu trên cùng một mẫu có thể chọn nhầm những người thắng do may mắn.

## 3. Sau khi mô hình chạy, quỹ thật sự chọn gì?

Chính sách đề xuất đóng băng năm 2022 **chỉ nắm USMV trong growth sleeve**, không nắm trực tiếp AAPL, MSFT, JPM hay các cổ phiếu khác trong bảng. Toàn quỹ đầu tư khoảng 52.89% vốn ban đầu vào USMV; 47.03% dành cho giá mua hai trái phiếu, phần còn lại là phí. Hai trái phiếu được khớp với nghĩa vụ. Quyết định dùng USMV xuất phát từ certainty equivalent dưới `A=4`: USMV 3.84% so với VTI 3.13%, và volatility mẫu 12.84% so với 16.31%.

Các mã cổ phiếu vẫn hữu ích theo bốn cách: (i) kiểm tra universe phủ nhiều ngành; (ii) ước lượng cùng ma trận covariance; (iii) cho thấy portfolio tối ưu thay đổi ra sao nếu cho phép cổ phiếu trực tiếp; (iv) kiểm tra lời Theta về factor/alpha ở MSFT, AAPL và JPM. Tuy nhiên, mô hình A4 và Eta proxy là **phương án so sánh**, không phải chính sách đã khuyến nghị. Sample A4 tăng certainty equivalent ước tính chỉ khoảng 0.12 điểm phần trăm so với USMV đơn giản; Sample A4 và Single-index A4 còn chênh 14.09% turnover một chiều. Nhóm chọn ETF đơn giản vì độ bất định của ước lượng lớn hơn lợi ích nhỏ từ optimizer.

ETF có thể tự nắm các công ty trong universe; phần look-through đó không giống mua riêng cổ phiếu, nhưng có nghĩa quỹ vẫn chịu các rủi ro doanh nghiệp. USMV là cổ phiếu Mỹ theo chỉ số minimum-volatility; VTI là thị trường Mỹ rộng. Cả hai là rủi ro thị trường, khác nhau về mandate và trọng số. Mô tả sản phẩm hiện hành của [iShares về USMV](https://www.ishares.com/us/products/239695/ishares-msci-usa-min-vol-etf) và [Vanguard về VTI](https://investor.vanguard.com/investment-products/list/all?filters=open&strategy=total_market_etfs) hỗ trợ cách phân biệt mandate; khi chứng minh điều kiện tại cuối 2022, dùng prospectus/tài liệu có ngày không muộn hơn cutoff, không lấy thông tin 2026 làm dữ kiện quyết định năm 2022.

## 4. Kiểm nghiệm 2023–2025: điều gì thực sự xảy ra

Quy tắc đã khóa là giữ tỷ trọng ban đầu và rebalance sau lợi suất tháng 12 hàng năm; kết quả growth sleeve có chi phí vào ban đầu và phí rebalance nếu có. Đây là **đánh giá danh mục cổ phiếu/ETF**, không phải báo cáo NAV toàn quỹ sau chi tiêu. Cột drawdown là drawdown từ đỉnh của wealth index tăng trưởng, sau phí, theo điểm định giá cuối tháng.

| Growth sleeve | Lũy kế 2023–25 | CAGR 3 năm | Volatility năm | Sharpe | Drawdown cuối tháng lớn nhất |
| --- | ---: | ---: | ---: | ---: | ---: |
| Khuyến nghị: USMV | 37.33% | 11.15% | 9.64% | 0.66 | -5.66% |
| Benchmark: VTI | 82.56% | 22.22% | 12.54% | 1.30 | -9.11% |
| Sample A4 | 43.50% | 12.79% | 9.86% | 0.80 | -6.34% |
| Single-index A4 | 35.55% | 10.67% | 10.24% | 0.59 | -6.76% |
| Eta historical-Sharpe proxy | 48.19% | 14.01% | 9.91% | 0.90 | -6.42% |

| Năm dương lịch | USMV | VTI |
| --- | ---: | ---: |
| 2023 | 10.22% | 25.92% |
| 2024 | 15.74% | 23.81% |
| 2025 | 7.65% | 17.10% |

Trong ba năm đánh giá, VTI thắng về lợi suất, Sharpe và cả ba năm dương lịch; USMV giữ đúng đặc tính đã tìm: biến động và drawdown nhỏ hơn. Khoảng cách lợi suất không được bù bởi phần volatility thấp hơn, nên Sharpe USMV thấp hơn. Eta proxy vượt USMV trong giai đoạn này, nhưng vẫn kém VTI; đây là bằng chứng thực nghiệm có lợi cho Eta's stock-selection rule trong đúng cửa sổ 36 tháng, không chứng minh quy tắc sẽ tiếp tục thắng. 2023–25 đã là dữ liệu quá khứ ở hiện tại; chúng dùng để kiểm chứng, không được dùng lại để tuyên bố đã biết trước khi quyết định 2022. Ba năm tăng mạnh cũng không cho biết mục tiêu 2030 đã đạt được.

## 5. Ai đúng: Eta hay Theta?

**Eta đúng ở bước khớp nghĩa vụ.** Trái phiếu Beta và Delta tạo dòng tiền đúng hai ngày phải chi, theo điều kiện trái phiếu giả định không vỡ nợ. Cách này giảm rủi ro phải bán cổ phiếu trong thời điểm xấu để lấy tiền trả học bổng/trung tâm. Phần yếu trong lời khuyên là “chọn danh mục có Sharpe lịch sử cao nhất” như thể đó là forecast. Eta proxy tăng Sharpe huấn luyện lên 0.95 so với USMV 0.71 và VTI 0.59, nhưng drawdown mẫu vẫn gần 19%; ngoài mẫu, Eta đạt 48.19%, tốt hơn USMV 37.33% nhưng kém VTI 82.56%. Kết quả này không bác bỏ Eta hoàn toàn, cũng không xác thực chiến lược cho 8 năm; nó cho thấy dữ liệu ngoài mẫu phải được báo công bằng và lựa chọn có trade-off.

**Theta đúng khi hỏi nguồn lợi suất và rủi ro là factor nào.** FF3 giải thích khoảng 84.8% biến động excess return USMV; beta thị trường FF3 xấp xỉ 0.74, SMB -0.30, HML -0.05 (không ý nghĩa). AAPL có market beta 1.27, HML -0.54; MSFT market beta 1.06, HML -0.36. Điều này giúp nhìn USMV là equity có market exposure thấp hơn VTI, và công nghệ nghiêng về growth. Factor regressions là giải thích lịch sử, không phải công thức tự động chọn danh mục.

Theta chỉ thuyết phục nếu có bằng chứng alpha **bền qua thời gian, sau rủi ro và chi phí**. Trong 96 tháng, USMV FF3 alpha 1.49%/năm, khoảng tin cậy 95% từ -2.09% đến +5.06%, p=0.415: dữ liệu không phân biệt được alpha với 0. JPM FF3 alpha 4.23%, CI -5.98% đến 14.43%, p=0.417. MSFT FF3 alpha 12.81%, CI +4.54% đến +21.08%, p=0.0024, là bằng chứng thuận lợi cho Theta trong toàn mẫu; nhưng nửa đầu 2015–18 ước lượng 13.23%, CI -0.53% đến +26.99%, p=0.0596; nửa sau 2019–22 là 12.72%, CI +2.86% đến +22.59%, p=0.0115. Hai nửa có dấu dương nhưng độ chắc khác nhau; chọn MSFT sau khi đã nhìn thấy thành công, thử nhiều mã, survivorship và dữ liệu sửa lại làm suy yếu khả năng diễn giải thành alpha tương lai. Vì vậy alpha dự báo vẫn bằng 0. Cách kết luận đúng: có một tín hiệu MSFT đáng nghiên cứu tiếp, chưa đủ để quỹ cam kết lợi suất alpha.

## 6. Định nghĩa 15% sao cho hội đồng dùng được

“Lỗ 15%” có ít nhất ba nghĩa. Lỗ từ **đầu kỳ** so sánh NAV hiện tại với 12 triệu ban đầu; **drawdown** so sánh với đỉnh gần nhất; lỗ theo năm đo riêng 12 tháng. Sau khi trả 6 triệu nghĩa vụ, NAV giảm là chi tiêu đã cam kết chứ không phải lỗ đầu tư. Tài liệu nghiên cứu về ngưỡng đã đề xuất dùng 15% làm trigger drawdown của growth sleeve, trong khi theo dõi payment coverage riêng. Đó là một đề xuất quản trị hữu ích nếu trustees xác nhận như vậy; vì câu chữ đề nói “quỹ” lỗ, hội đồng vẫn phải quyết định có thực sự muốn nói toàn fund hay phần growth.

Stress trên toàn quỹ lúc khởi đầu định nghĩa lỗ là thay đổi giá trị tài sản từ 12 triệu trước chi tiêu. Kết quả cho thấy:

| Stress thị trường | Thay đổi toàn quỹ trên 12 triệu |
| --- | ---: |
| Equity -20%, đường cong +100bp | -12.25% |
| Equity -30%, đường cong +100bp | -17.53% |
| Equity -40%, đường cong +100bp | -22.82% |

Do đó, nếu trustees muốn 15% áp dụng cho **toàn fund tại điểm đầu tư**, danh mục cơ sở vượt ngưỡng trong stress -30%/+100bp dù hai nghĩa vụ vẫn được khớp. Model tính chuyển khoảng **1.014 triệu USD** từ USMV sang tiền mặt sẽ đưa riêng kịch bản này về 15%; required equity CAGR tăng từ **4.84% lên khoảng 5.60%**. Đây không phải cách giữ được mục tiêu mà không trade-off; cũng không bảo đảm mọi lỗ thực tế dưới 15%.

Nếu trustees xác nhận 15% áp dụng cho **growth sleeve**, thì 15% của vốn USMV ban đầu 6,346,351 USD khoảng **952,000 USD**; nên đo drawdown từ high-water mark trên chuỗi total-return đã điều chỉnh dòng tiền vào/ra sleeve. Lịch sử 2015–22 có drawdown USMV -19.06%, nên mức này vẫn sẽ bị vượt trong một số khủng hoảng. Nó làm trigger cảnh báo/hành động quản trị, không phải cam kết ceiling. Whole-fund stress -17.53% vẫn cần công bố riêng.

Đề xuất để hội đồng thảo luận, chưa phải luật được duyệt:

1. **Red lines cứng:** không dùng margin/short/derivatives; giữ coverage ≥100% cho hai khoản đến hạn; không bán trái phiếu earmarked trừ khi nguồn dự phòng/thay thế được duyệt và coverage vẫn nguyên.
2. **Trigger 15% có phạm vi rõ:** phương án khuyến nghị để thảo luận là drawdown của growth sleeve, đo từ đỉnh bằng chuỗi total-return sau phí và điều chỉnh dòng tiền vào/ra. Đồng thời báo cả whole-fund mark-to-market stress. Nếu trustees muốn whole-fund limit, phải lượng hóa giảm equity và chấp nhận required return cao hơn.
3. **Ngưỡng hành động, không lệnh bán tự động:** cảnh báo ở -10%; -15% bắt buộc committee review; -20% hoặc nguy cơ thiếu coverage gọi trustees khẩn. Ghi biên bản việc giữ nguyên, rebalance theo rule hay xin đổi IPS. Đây khớp mẫu quy trình đã nghiên cứu trong `LOSS_LIMITS_RESEARCH_AND_DESIGN_VI.md`.
4. **Systemic-risk exception:** có thể hoãn giao dịch discretionary trong tối đa 30 ngày nếu thanh khoản/giá không đáng tin hoặc bán sẽ ép khóa lỗ, miễn coverage nghĩa vụ còn ≥100%; Chair + Treasurer đề xuất, trustees có thẩm quyền duyệt, giải thích lý do/ngày hết hạn, rà soát hàng tuần và xin duyệt mới trước khi gia hạn.
5. **Không hứa mức lỗ tối đa được bảo đảm:** gap thị trường, thanh khoản và tương quan có thể làm mức lỗ vượt ngưỡng. “Maximum stop-loss” chỉ có thể là trigger quản trị. Muốn giảm stress loss phải hạ equity risk budget và nhận mục tiêu 2030 yếu đi.

## 7. File để tự kiểm

- Universe và lý do chọn: `analysis/config.json`, `deliverables/Kappa_Committee_Memo_Editable.md` trang 4–6, `data/raw/supporting/eligibility_checks.json`.
- Kết quả mỗi cổ phiếu/ETF: `outputs/tables/expected_return_inputs.csv`, `training_performance.csv`.
- Tỷ trọng chính sách và đối chứng: `policy/frozen_policy.json`, `outputs/tables/portfolio_candidates.csv`, `risk_preference.csv`.
- Factor/alpha và độ ổn định: `outputs/tables/factor_regressions.csv`, `alpha_stability.csv`, `factor_variance_decomposition.csv`.
- Performance 2023–25 và từng năm: `outputs/tables/evaluation_performance.csv`, `evaluation_calendar_years.csv`, `evaluation_wealth.csv`.
- Ngưỡng 15%: `outputs/tables/whole_fund_stress.csv`, `risk_limit_sensitivity.json`.
- Chênh lệch workbook: `outputs/role_c_audit/role_c_independent_audit.json`, `reference/role_c/BFIN_Part_C_original.xlsx`.

Kết quả kiểm 2023–25 được tính bằng cùng chính sách đã khóa, nhưng chỉ là 36 tháng và dùng dữ liệu lịch sử hiện đã có, với hạn chế chọn mã sống đến hiện tại và vintage Yahoo/FF đã sửa. Dùng nó để đánh giá sự lựa chọn và cập nhật quyết định kể từ hiện tại; không dùng nó như bằng chứng khiến quyết định ngày 31/12/2022 trở nên hiển nhiên.
