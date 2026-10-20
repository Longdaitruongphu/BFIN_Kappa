# Kappa Portfolio Lab v2 — hướng dẫn sử dụng và tư duy phân tích

Ngày cập nhật: 20/10/2026. Đây là công cụ thảo luận giả định, không tự sửa IPS hay quyết định đã đóng băng. Giao diện và hình xuất dùng tiếng Anh; giải thích dùng tiếng Việt.

## 1. Công cụ đang giải bài toán nào?

Hình dung quỹ có hai ngăn tiền:

- **Ngăn nghĩa vụ:** mua Beta và Delta để trả 2.4 triệu USD cuối 2024 và 3.6 triệu USD cuối 2027 theo đề. Không lấy ngăn này ra tối ưu cổ phiếu.
- **Ngăn tăng trưởng — growth sleeve:** khoảng **6.346 triệu USD** còn lại sau trích lập trái phiếu và chi phí ban đầu. Lab phân bổ ngăn này giữa AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI, USMV.

Trong lab, tổng tỷ trọng 100% là **100% ngăn tăng trưởng**, không phải 100% toàn bộ 12 triệu USD. VTI là ETF thị trường cổ phiếu Mỹ rộng; USMV là ETF theo chiến lược cổ phiếu Mỹ biến động thấp. Cả hai vẫn có thể lỗ.

Lab hiện tối ưu danh mục **100% cổ phiếu/ETF**. Cash không phải biến tối ưu. Đường CAL minh họa kết hợp tiền phi rủi ro với một danh mục rủi ro; nó không có nghĩa app đã tối ưu tỷ trọng cash. Nếu muốn tăng mức phòng thủ bằng cash, cần một bài toán phân bổ bổ sung và quy ước tái đầu tư tiền mặt.

**Không thể đọc “σ = 15%” thành “lỗ tối đa 15%”.** σ đo mức phân tán lợi suất, drawdown đo sụt giảm từ đỉnh, còn cú sốc −30% là kịch bản giả định. Ba con số khác nhau. Không áp ngưỡng quản trị 10/15/20% của toàn quỹ trực tiếp vào graph của riêng growth sleeve.

Đề không bắt chọn Sharpe cao nhất và không quy định cap 10%/cổ phiếu hay 30% cổ phiếu trực tiếp. Hai ô cap trong bản này mặc định trống. Mọi cap bạn nhập chỉ là kịch bản để kiểm tra.

## 2. Mở app và sử dụng trong lần đầu

Đóng cửa sổ phiên bản cũ. Trong PowerShell ở thư mục dự án:

```powershell
.\.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py
```

Hoặc nhấp đúp `OPEN_PORTFOLIO_LAB.cmd` ở thư mục gốc. Không cần tải lại dữ liệu hay cài thêm thư viện cho bản nâng cấp nếu môi trường `.venv` hiện có vẫn hoạt động.

1. Đợi phép tính đầu tiên hoàn tất. Giao diện dùng dữ liệu đã lưu, không truy cập Yahoo/French khi bạn thay tham số.
2. Bên trái có ba tab: **Inputs**, **Stress**, **Portfolios**. Có thể cuộn từng tab; kéo vạch chia hai vùng nếu muốn tăng diện tích graph.
3. Giữ mặc định CAPM, Sample, 96 tháng, RF 4%, ERP 4.5%, A=4, lạm phát 2.5%, không thêm caps. Đây là kịch bản làm việc, không phải các hằng số đúng trong mọi hoàn cảnh.
4. Trong **Portfolios**, bấm **Core**: chọn GMV, Max Sharpe, Max Utility A=4, USMV, VTI. Chỉ nên xem 3–6 đường cùng lúc.
5. Chọn loại graph ở thanh phía trên vùng hình. Di chuột gần điểm trên Risk/return để đọc số chính xác ở thanh trạng thái.
6. Bấm **Pin baseline** để ghi nhớ tỷ trọng và giả định đang hiển thị.
7. Đổi **một** tham số, bấm **Apply & recalculate**, rồi xem graph, Scorecard và Baseline comparison.
8. Bấm **Export** và chọn thư mục cha. App tạo thư mục con mới; chỉ các danh mục được tick có trong bảng và 8 graph. Riêng sensitivity map/grid luôn chứa đầy đủ 30 tổ hợp A–ERP.

**Sửa ô chưa đồng nghĩa đã tính lại.** Hình, baseline và export luôn dùng kết quả của lần Apply hoàn tất gần nhất. Nếu phép tính thất bại, app giữ hình cũ và thông báo lỗi, không âm thầm dùng giả định khác.

**Pin baseline không phải freeze policy.** Nó chỉ là mốc so sánh trong phiên app. Khi tắt app, hãy export để giữ settings/weights. Load JSON phục hồi inputs, xóa baseline trong bộ nhớ; cần Apply rồi Pin nếu muốn dùng cấu hình vừa nạp làm mốc.

## 3. Bốn khâu cần phân biệt: dự báo, rủi ro, tối ưu, kiểm chứng

```text
2015–2022 → ước lượng beta / factor exposure / covariance
                     ↓
Giả định RF, premiums → lợi suất kỳ vọng từng tài sản
                     ↓
Lợi suất + covariance + A + constraints → tỷ trọng danh mục
                     ↓
Giữ quy tắc đầu tư để kiểm chứng riêng trong 2023–2025
```

Không dùng kết quả 2023–2025 để chỉnh rồi gọi đó là quyết định đã có vào cuối 2022. Nếu thử nhiều lần sau khi thấy kết quả đánh giá, đó là nghiên cứu hồi cứu.

### CAPM và FF3: hai cách tạo expected return

CAPM trong lab:

`E(Ri) = RF + beta_i × ERP + return_shift`

Ví dụ RF=4%, beta=0.70, ERP=4.5% → E(Ri)=7.15% trước return shift. Beta đo độ nhạy với thị trường, không phải xác suất lời/lỗ. CAPM dùng beta từ hồi quy lợi suất tháng vượt RF lịch sử.

FF3:

`E(Ri) = RF + b_market × ERP + b_SMB × premium_SMB + b_HML × premium_HML + return_shift`

SMB là chênh lệch lợi suất nhóm công ty nhỏ và lớn; HML là chênh lệch nhóm value và growth theo cách dựng nhân tố French. [Mô tả chính thức của Kenneth French](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html).

Hồi quy FF3 lịch sử giúp giải thích lợi suất đã xảy ra; bản thân nó không quyết định premium tương lai. Vì vậy SMB/HML bắt đầu **để trống**. Chọn FF3 phải điền cả hai, kể cả khi chủ động thử 0%. Alpha dự báo luôn bằng 0; không coi alpha lịch sử là lợi nhuận chắc chắn lặp lại.

FF3 không mặc nhiên tốt hơn CAPM: có thêm cách giải thích nhưng cũng thêm giả định và sai số. Nên giữ CAPM làm mốc, dùng FF3 với các premium có lý do để kiểm tra lựa chọn có bền không.

### Sample và Single-index: hai cách ước lượng covariance

Covariance trả lời: “Hai tài sản thường tăng/giảm cùng nhau đến mức nào?” Cùng biến động riêng lẻ nhưng tương quan khác nhau thì rủi ro rổ khác nhau.

- **Sample:** trực tiếp tính covariance của lợi suất tháng trong cửa sổ đã chọn, nhân 12 thành covariance năm.
- **Single-index:** phần chung đến từ thị trường, cộng phương sai riêng của từng tài sản; giả định các phần dư không tương quan chéo. Cấu trúc đơn giản hơn nhưng có thể bỏ sót liên hệ cùng ngành/phong cách.

Tên `Sample Max Utility` cho biết matrix dùng **tạo tỷ trọng**. Ô **Common scoring covariance** quyết định matrix dùng **chấm tất cả danh mục trong bảng** và vẽ frontier. Điều này giúp so sánh trên cùng thước đo. Danh mục tối ưu bằng Single-index có thể không nằm trên frontier Sample.

Đổi cửa sổ từ 96 xuống 60 tháng sẽ tính lại **cả beta CAPM, exposure FF3, sample covariance và single-index covariance** trên cùng cửa sổ. Không giữ beta cũ rồi ghép matrix mới.

### GMV, Max Sharpe và Max Utility: ba định nghĩa “tối ưu”

| Danh mục | Câu hỏi nó trả lời | Điều nó chưa bảo đảm |
|---|---|---|
| GMV | Tổ hợp có variance nhỏ nhất trong tập tài sản và giới hạn đang xét? | Không đồng nghĩa giữ được vốn hay đạt mục tiêu 2030 |
| Max Sharpe | Tổ hợp có phần bù kỳ vọng trên mỗi đơn vị volatility lớn nhất? | Không tự phản ánh mức sợ rủi ro A; không chắc lợi suất thực tế cao nhất |
| Max Utility | Tổ hợp cân bằng expected return và variance tốt nhất theo A? | Phụ thuộc A và đầu vào; không phải bảo hiểm chống lỗ |
| Equal-weight 1/N | Nếu không tin vào sự chính xác của optimizer, chia đều thì sao? | Không tự bảo đảm đa dạng hóa rủi ro |
| 100% VTI / USMV | So với một lựa chọn ETF đơn giản, tối ưu phức tạp có đáng không? | Hai ETF có mục tiêu khác nhau; phải nhìn cả lãi lẫn rủi ro |

Công thức chung, lợi suất dùng dạng số thập phân:

`E(Rp) = w'μ`

`Variance = w'Σw; σp = sqrt(Variance)`

`Sharpe = [E(Rp) − RF] / σp`

`U = E(Rp) − 0.5 × A × Variance`

Ví dụ lợi suất 8%, σ=15%, A=4 → U=0.08−0.5×4×0.15²=3.5%. Utility là thước đo lựa chọn theo mô hình, **không phải tiền lãi ròng 3.5%**.

Mọi dòng của Scorecard dùng **cùng A đang nhập** để chấm U. Một dòng `Utility A=8` dùng A=8 để xây tỷ trọng, nhưng vẫn được chấm lại theo A chung trong bảng. Không so utility tính với A khác nhau như thể cùng thang điểm.

Đối với bối cảnh quỹ trường học, tôi đề xuất dùng Max Utility làm **khung so sánh ưu tiên**, GMV làm đối chứng phòng thủ, Max Sharpe làm đối chứng hiệu quả, và VTI/USMV để kiểm tra tính thực dụng. Đây là đề xuất phương pháp; không có quy định ngành “mọi quỹ trường học phải A=4”. Quan hệ giữa mục tiêu, giới hạn và chính sách là nội dung của IPS — Investment Policy Statement. [CFA Institute, IPS cho tổ chức](https://rpc.cfainstitute.org/policy/positions/elements-of-an-investment-policy-statement-for-institutional-investors).

## 4. Từng tham số chỉnh cái gì?

| Ô giao diện | Nhập thế nào | Có thể làm thay đổi gì? |
|---|---|---|
| Expected-return model | CAPM hoặc FF3 | Công thức dự báo μ; tỷ trọng nếu expected returns đổi |
| Common scoring covariance | Sample / Single-index | Rủi ro, U, Sharpe, frontier và sensitivity map; vẫn giữ các ứng viên tạo bởi cả hai matrix |
| Training months | 96/84/72/60 | Tương ứng bắt đầu Jan2015/2016/2017/2018; tất cả kết thúc Dec2022 |
| Forecast risk-free | 4 nghĩa là 4%/năm | Expected return và CAL; không thay chuỗi RF lịch sử trong hồi quy |
| Market risk premium | 4.5 nghĩa là 4.5%/năm | Phần bù thị trường kỳ vọng; khác lợi suất toàn thị trường |
| SMB / HML expected premium | 0, 1, −1… theo %/năm | Chỉ có tác dụng với FF3; 0 phải là lựa chọn có chủ ý |
| Risk aversion A | 1,2,4,6,8,12 để so sánh | A tăng thường ưu tiên variance thấp hơn; không trực tiếp quy định stop-loss |
| Planning inflation | 2.5 nghĩa là 2.5%/năm | Mục tiêu nominal 2030 và sức mua dự phóng; không tự thay μ hoặc optimal weights |
| Volatility multiplier | 1.25 | σ từng tài sản tăng 25%; covariance nhân 1.5625 |
| Correlation stress | 50 nghĩa là 50% | Kéo mọi tương quan nửa đường về +1; không có nghĩa đặt mọi hệ số tương quan bằng 0.5 |
| Diagonal shrinkage | 20 nghĩa là 20% | Kéo matrix tương quan 20% về identity, giảm hệ số chéo; giữ variance riêng trước vol stress |
| Return shift | −2 nghĩa là −2 điểm %/năm | Trừ cùng mức khỏi μ mọi tài sản; không thay dữ liệu lịch sử |
| Cost per dollar traded | 10 bps =0.1% | Chi phí mua+bán trong kiểm chứng rebalance; không đưa vào objective hiện tại |
| Historical rebalance rule | Annual/Quarterly/Monthly/Buy and hold | Lịch đưa về tỷ trọng mục tiêu sau lợi suất cuối kỳ; thay CAGR/DD thực hiện |
| Optional max any asset | Trống hoặc 20 | 20%=cap cho mọi mã, kể cả ETF |
| Optional direct-stock total | Trống hoặc 30 hoặc 0 | Tổng tỷ trọng 8 cổ phiếu trực tiếp; không tính cổ phiếu nằm trong ETF |
| 2030 real goal | 8 nghĩa là $8m | Mục tiêu sức mua; đổi số là sensitivity, không đổi nghĩa vụ đề |
| Asset price shocks | −30 nghĩa là giảm 30% ngay | Loss giả định của tỷ trọng hiện tại và tỷ trọng baseline |
| Custom weights | Tick Include custom; điền % | Thêm danh mục do bạn chọn; bắt buộc tổng 100%, không tự chuẩn hóa |

Một ví dụ về cap bất khả thi: tối đa 20% mỗi mã và tối đa 10% cổ phiếu trực tiếp chỉ cho phép 2 ETF ×20% +10% =50%; không thể đầu tư đủ 100%. App báo lỗi thay vì tự nới quy tắc.

**Đổi RF nhưng weights không đổi có thể hoàn toàn đúng.** Trong CAPM, nếu giữ ERP, beta, covariance: tăng RF cùng một lượng làm μ tất cả tài sản tăng cùng lượng. Với tổng weights=1, thứ hạng utility và phần bù trong Sharpe có thể giữ nguyên.

Tương tự, return shift chung không đổi tổ hợp Max Utility/GMV khi các yếu tố còn lại giữ nguyên, nhưng có thể đổi Max Sharpe. Inflation chỉ đổi đích sức mua nên không tự làm optimizer trở nên thận trọng hơn. Muốn kiểm tra một chế độ lạm phát tác động lên thị trường, phải khai báo thêm tác động lên μ, σ, correlation.

**Không dùng shrinkage như “thuốc giảm rủi ro”.** Đây là giả định thống kê cần thử độ nhạy; matrix đẹp hơn không chứng minh estimate đúng hơn. App áp dụng theo thứ tự: diagonal shrinkage → correlation stress → volatility multiplier.

## 5. Chọn graph nào cho câu hỏi nào?

| Graph | Cách đọc và mục đích |
|---|---|
| Risk / return | Sang phải=rủi ro cao hơn, lên trên=lợi suất kỳ vọng cao hơn. Điểm ghi ID và (σ; E[R]); di chuột đọc số. Dùng để thấy trade-off, không chọn chỉ vì nằm cao nhất |
| Radar profile | Điểm 0–100 tương đối trong cùng kịch bản. Chọn 3–5 danh mục để nhìn đặc tính. Không cộng các trục hoặc xếp hạng diện tích |
| Allocation weights | Mỗi hàng là danh mục; mỗi cột là mã; ô hiện %. Phát hiện 2 danh mục tên khác nhưng tỷ trọng gần giống hoặc tập trung một mã |
| Risk contributions | Tỷ trọng đóng góp vào variance. 10% vốn không đồng nghĩa 10% rủi ro; các ô trong một hàng cộng 100% |
| Shock losses | Mỗi danh mục chịu vector cú sốc hiện đang nhập. Có baseline thì so tỷ trọng cũ với tỷ trọng mới; hiển thị % và dollar trên vốn dư |
| Sensitivity map | Trục A và ERP; mỗi ô tối ưu lại utility. Màu là volatility được chọn; số nhỏ không tự có nghĩa “tốt hơn”. Export có weights từng ô |
| 2023–25 wealth | Giá trị $1 đầu kỳ; tick 100% VTI để hiện benchmark nét đứt. Đây là kiểm chứng hồi cứu |
| 2023–25 drawdown | Độ giảm từ đỉnh trước đó; đường gần 0 hơn mất ít hơn. Đo theo tháng nên bỏ sót tổn thất nội tháng |
| Scorecard | Số liệu và weights đầy đủ, có thanh cuộn ngang; U/Sharpe là forecast còn CAGR/DD có nhãn giai đoạn riêng |
| Baseline comparison | Giữ weights cũ trong assumptions mới so với candidate hiện tại; turnover và chi phí đổi danh mục ước tính |

Radar cũ có lỗi đảo chiều drawdown. **Đã sửa:** −5% được điểm tốt hơn −25%. Các graph cũ đã xuất trước bản sửa vẫn là output cũ; dùng hình trong `outputs/figures/portfolio_lab_v2/` hoặc export lại.

Radar chuẩn hóa theo tất cả ứng viên khả thi của **kịch bản hiện tại**, không theo những dòng vừa tick. Tick/bỏ tick không đổi thang trong cùng kịch bản. Nhưng khi đổi giả định/thêm custom portfolio, tập ứng viên thay đổi nên không so “radar 80” của hai kịch bản như cùng đơn vị vật lý.

Để trình lecturer, tôi ưu tiên **Risk/return + Allocation weights + Drawdown**, thêm **Risk contributions** và **Sensitivity map** nếu cần giải thích cơ chế. Radar dùng phụ trợ. Một kết luận có sức thuyết phục cần trade-off và bằng chứng phản bác, không cần thật nhiều đa giác.

## 6. Làm sensitivity test từng bước

Sensitivity: đổi một yếu tố để biết điều gì gây ra kết quả.

1. Reset inputs → Apply → Core → Pin baseline → Export mốc.
2. **A:** thử 2,4,6,8,12; giữ các ô khác. Xem Max Utility đổi weights, volatility và expected return thế nào.
3. **ERP:** quay về mốc; thử 2%,4.5%,6%; xem Max Utility, Max Sharpe; quan sát tập trung có tăng không.
4. **Risk estimate:** quay về mốc; Sample sang Single-index. So các danh mục trên cùng scoring matrix và xem Risk contributions.
5. **Cửa sổ:** 96 xuống 60. Nếu weights đổi rất lớn, đó là tín hiệu estimate không ổn định, không phải bằng chứng cửa sổ nào đúng.
6. **Inflation:** 2.5% →4%→5%; expected weights có thể y nguyên nhưng Required CAGR tăng. Đó là sức ép lên mục tiêu, không phải tăng expected return tự động.
7. **Trading rule:** annual →quarterly/monthly với cost 0/10/25 bps. Xem lợi ích rebalance có bị chi phí ăn mòn. Không chọn lịch mới bằng hindsight rồi ghi ngược vào 2022.
8. **FF3:** khai báo các premium và chạy từng cái riêng; ví dụ SMB=0/HML=0, sau đó chỉ đổi HML từ −1% đến +1%. Các mức này là lưới thử nghiệm, không phải estimate đã được xác nhận.

Ghi cho mỗi test: thay đổi gì, vì sao có thể xảy ra, weights cũ/mới, turnover, rủi ro, kỳ vọng, ảnh hưởng mục tiêu, quyết định có đảo chiều không.

## 7. Làm stress test đúng nghĩa

Stress: ghép những thay đổi có câu chuyện kinh tế nhất quán. Không gán xác suất nếu chưa có mô hình hiệu chỉnh.

**Bài tập A — cú sốc tức thời với danh mục đang giữ**

- Pin baseline. Trong Stress điền AAPL −40, MSFT −35, JPM −30, JNJ −15, PG −15, XOM −25, CAT −35, NEE −30, VTI −30, USMV −22 (%).
- Giữ inputs thị trường khác; Apply → Shock losses.
- App tính `loss = Σ wi × shock_i`. Với cả 10 tài sản cùng −30%, mọi danh mục long-only 100% equities đều lỗ đúng −30%. Đây là kết quả đúng, không phải bug.
- Dollar loss tính trên $6.346m; không phải loss toàn bộ quỹ.

**Bài tập B — đổi chế độ rủi ro**

- Pin mốc rồi dùng preset Recession/risk-off: volatility×1.5, correlation stress50%, ERP3%, return shift−2pp, inflation2.5%, shrink0; shocks −30% cho mọi tài sản.
- RF, A, caps, model và costs giữ nguyên. Chỉnh thêm nếu muốn nhưng phải ghi rõ.
- Baseline comparison cho biết rủi ro của **weights cũ** trong matrix mới, rồi mới so với **weights tối ưu lại**.
- Không giả định quỹ đã có danh mục tối ưu mới trước khi khủng hoảng đến.

**Bài tập C — áp lực lạm phát**

- Preset Inflation pressure: inflation5%, volatility×1.25, correlation stress25%, return shift−1pp, ERP4.5%, shrink0.
- Vector shocks mang tính minh họa, có XOM +10% và các mã khác giảm; đây không phải khẳng định ngành năng lượng chắc thắng trong lạm phát.
- Đọc cả Required CAGR và rough real terminal amount. “Còn đủ tiền danh nghĩa” không đồng nghĩa “còn đủ sức mua”.

**A không phải nhiệt kế thị trường.** Thử A khác để tìm mức lựa chọn phù hợp khả năng chịu lỗ của quỹ. Trong một stress kinh tế, thường giữ A để thấy cùng một hội đồng sẽ chọn gì khi input đổi. Chỉ đổi A khi thảo luận thay đổi thật về sở thích/khả năng chịu rủi ro, không tăng/giảm A tùy kết quả muốn có.

## 8. Những điều quan trọng về số liệu và cách kiểm tra

Sức mua 2030:

`Target_nominal = Real_goal × (1 + inflation)^8`

`Required_sleeve_CAGR = [(Target_nominal − surplus_coupons) / initial_surplus]^(1/8) − 1`

Mốc mặc định 2.5% → yêu cầu CAGR xấp xỉ **4.84%/năm** cho vốn dư, với $486,956.52 coupons dư nằm tiền mặt theo bridge đã lưu. RF không thay thế inflation để tính sức mua.

Ô projected 2030 của Scorecard chỉ là:

`g_rough = expected_return − 0.5 × variance`

`Real_terminal_rough = [surplus × (1+g_rough)^8 + coupons] / (1+inflation)^8`

Đây là **xấp xỉ phục vụ so sánh**, không phải expected terminal wealth chính xác, không phải xác suất đạt mục tiêu, không có mô hình đường đi/shortfall và không tích hợp phí giao dịch tương lai. Không lấy E[R] arithmetic so trực tiếp với CAGR compound để tuyên bố đã đạt mục tiêu.

Về chi phí: gốc $6.346m đã trừ chi phí ban đầu theo funding bridge cũ. Trong các đường lịch sử của lab, $1 bắt đầu **sau mốc phân bổ**, chỉ thu phí rebalance. Vì vậy CAGR của lab có thể lệch nhẹ với báo cáo cũ có trừ entry cost. Không âm thầm coi hai convention là một. Initial bond funding/cost không được tính lại khi đổi ô cost này.

Baseline comparison lưu return/vol/U dạng số thập phân; ví dụ 0.15=15%. One-way turnover là `0.5×Σ|w_new−w_old|`; switch cost minh họa là `cost×Σ|Δw|×surplus`, không phải giao dịch đã thực hiện. Chưa có trạng thái holdings đã drift hay chi phí tối ưu trong bài toán này.

Các điểm kiểm tra bằng tay:

1. `selected_metrics_weights.csv`: tổng 10 weights=1; utility=return−0.5A×variance; volatility²=variance.
2. Tìm một hàng 100% VTI/USMV: expected return và variance phải bằng riêng tài sản đó.
3. Set mọi shock=−30%: mọi loss phải là −30%.
4. Set vol multiplier=2, correlation/shrink giữ nguyên: với **cùng weights**, volatility gấp2 và variance gấp4. Danh mục được tối ưu lại không nhất thiết có volatility gấp2 vì weights đổi.
5. Đổi inflation, giữ các input khác: weights không đổi; Required CAGR và real terminal đổi.
6. Giữ sample, 96 tháng và mặc định: beta/covariance phải khớp bảng đã lưu; log kiểm tra ghi sai lệch trong sai số làm tròn.
7. Hai ô cap trống không có cap tự thêm; benchmark có thể vi phạm cap bạn thử và được đánh dấu, không tự bị bỏ.

## 9. File nào chứa gì?

| File/thư mục | Vai trò |
|---|---|
| `analysis/interactive_surplus_portfolio_lab.py` | Điểm khởi chạy, hàm tối ưu và dữ liệu chung |
| `analysis/portfolio_lab_scenarios.py` | Settings, estimate, stress covariance, sensitivity, baseline, export |
| `analysis/portfolio_lab_desktop.py` | Giao diện, checkbox, tooltips, tác vụ tính toán nền |
| `analysis/portfolio_lab_charts.py` | 8 loại graph và chú thích |
| `analysis/test_portfolio_lab_v2.py` | Kiểm tra số học, giao diện Tk và xuất hình mẫu |
| `data/processed/train_monthly_returns.csv` / `train_factors.csv` | Lợi suất và factors 2015–2022, nguồn đã lưu |
| `data/processed/eval_monthly_returns.csv` | Kiểm chứng 2023–2025, không đưa vào estimation |
| `outputs/figures/portfolio_lab_v2/` | Hình mẫu và bảng/settings mặc định mới |
| `logs/portfolio_lab_v2_checks.json` | Kết quả kiểm tra bản nâng cấp |

Export tạo 8 hình PNG và SVG, `selected_metrics_weights.csv`, `baseline_comparison.csv`, `sensitivity_grid_all.csv`, `scenario.json`. JSON chứa inputs, ID map, portfolio được tick, weights baseline nếu có, và hashes dữ liệu/policy để truy xuất. ID có thể đổi giữa cấu hình; đối chiếu bằng tên danh mục và ID map của **chính export đó**.

Chạy kiểm tra:

```powershell
.\.venv\Scripts\python.exe analysis\test_portfolio_lab_v2.py
```

Kiểm tra lập trình không chứng minh đầu tư sẽ thành công hoặc giả định được hội đồng chấp thuận. Dữ liệu gốc và frozen policy không bị thay đổi bởi lab.

## 10. Cách đưa kết quả vào quyết định

Một câu kết luận tốt có dạng:

> “Tại A=…, với expected-return model…, covariance…, danh mục X có weights…, expected return…, volatility…. Chúng tôi chọn/không chọn X vì…. Khi thay giả định… sang…, lựa chọn đảo chiều/không đổi và turnover là…. VTI là benchmark đã chọn trước. Đánh giá 2023–2025 cho thấy…. Điều chưa được mô hình hóa là….”

Đừng viết “radar tổng điểm cao nhất nên tối ưu”. Hãy trả lời: tối ưu theo **mục tiêu nào**, trong **tập tài sản nào**, dưới **giả định nào**, với **giới hạn nào**, và **còn đứng vững khi đầu vào sai đến mức nào**.

Nguồn phương pháp: đề gốc `reference/BFIN-WS2026-Group_Assignment.pdf`; [French factor definitions](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html); [CFA, Portfolio Risk and Return II](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/portfolio-risk-return-part-2); [CFA, IPS cho tổ chức](https://rpc.cfainstitute.org/policy/positions/elements-of-an-investment-policy-statement-for-institutional-investors). Các nguồn web được xem ngày 20/10/2026 để giải thích phương pháp, không dùng làm dữ liệu dự báo mới cho quyết định 2022.
