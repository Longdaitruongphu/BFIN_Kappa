# So sánh danh mục tăng trưởng tại ngày 31/12/2022

**Trạng thái:** Phân tích tư vấn để thảo luận; không sửa chính sách đã đóng băng.  
**Cutoff quyết định:** chỉ thông tin đến 31/12/2022. Dữ liệu 2023–2025 được trình bày riêng làm kiểm định ngoài mẫu; không được dùng để chọn danh mục hồi tố. Dự án hiện không có chuỗi hoàn chỉnh đến 2026 cho quyết định này.

## Kết luận để trình bày

Không có một danh mục “tối ưu” nếu chưa nói rõ tối ưu theo tiêu chí nào. Trong các danh mục ứng viên đã chạy:

- **Tối đa certainty equivalent theo covariance mẫu, A=4:** `Sample_A4`, CE 3,962%/năm; chỉ hơn `USMV` (3,845%) khoảng **0,117 điểm phần trăm/năm**, tức khoảng 12 điểm cơ bản. Danh mục này dùng 30% cổ phiếu trực tiếp và hai ETF.
- **Tối đa certainty equivalent theo single-index covariance, A=4:** `Single_index_A4`, CE 4,258%/năm theo đúng covariance single-index; khi chấm cùng covariance mẫu thì CE là 3,890%, thấp hơn `Sample_A4`. Kết quả thay đổi theo cách ước lượng rủi ro.
- **Chính sách dự án đã đóng băng:** 100% USMV trong growth sleeve. Đây là lựa chọn đơn giản để vận hành, ít phụ thuộc vào một nghiệm tối ưu hóa nhiều tham số; **không phải** nghiệm có CE cao nhất trong toàn bộ universe.

Vì vậy, cách nói chính xác trước hội đồng là: “USMV là lựa chọn chính sách thận trọng, dễ giám sát đã được chốt trong hồ sơ gốc. Tối ưu hóa cho thấy có phương án cổ phiếu–ETF có CE cao hơn, nhưng lợi thế dưới covariance mẫu chỉ khoảng 12 điểm cơ bản và thứ hạng đổi theo mô hình covariance. Đây là đánh đổi giữa hiệu quả điểm ước tính và độ bền/đơn giản khi triển khai, không phải bằng chứng USMV là danh mục toán học tốt nhất.”

## Quỹ đang tối ưu điều gì?

Mô hình trước hết tách **nghĩa vụ** khỏi **growth sleeve**. Hai khoản chi 2024 và 2027 được cấp vốn bằng trái phiếu Beta/Delta theo giả định đề bài; phần tăng trưởng được so sánh trên 6.346 triệu USD. Do đó, biểu đồ dưới đây không cho phép lấy tiền ở phần nghĩa vụ để tăng rủi ro cổ phiếu.

Ở tầng danh mục tăng trưởng, tiêu chí định lượng là certainty equivalent:

`CE = lợi suất kỳ vọng số học − (A/2) × phương sai năm`, với `A=4`.

Đầu vào lợi suất là CAPM theo bộ quy ước đã chốt: RF dự phóng 4%, ERP 4,5%, alpha dự phóng bằng 0. Rủi ro được tính cả từ covariance mẫu 2015–2022 và covariance single-index. Đây là **xếp hạng theo mô hình và giả định**, không phải lợi suất kép được hứa hẹn.

Để gọi một danh mục là tối ưu cho cả quỹ, chưa đủ chỉ tối đa CE của growth sleeve. Cần thêm tiêu chí toàn quỹ như xác suất đạt 8 triệu USD sức mua 2022, mức thiếu hụt khi không đạt, rủi ro mất vốn và thanh khoản, trong khi bảo đảm coverage nghĩa vụ. Simulation hiện hành chỉ so sánh USMV/VTI; vì vậy kết quả mới xác định được nghiệm tối ưu theo CE, chưa chứng minh danh mục nào tối ưu nhất cho xác suất hoàn thành mục tiêu 2030.

## Các danh mục nổi bật và tỷ trọng growth sleeve

| Danh mục | AAPL | MSFT | JPM | JNJ | PG | XOM | CAT | NEE | VTI | USMV |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Chính sách USMV | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 100% |
| Đối chứng VTI | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 100% | 0% |
| 50/50 ETF | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 0% | 50% | 50% |
| Sample A=4 | 0% | 2,21% | 2,88% | 6,67% | 10% | 2,24% | 0% | 6,00% | 18,10% | 51,90% |
| Single-index A=4 | 0% | 0% | 0% | 10% | 10% | 0% | 0% | 10% | 11,34% | 58,66% |
| Eta: Sharpe huấn luyện | 10% | 10% | 0% | 0% | 0% | 0% | 0% | 10% | 0% | 70% |

Các giới hạn tối ưu hóa: không bán khống, tổng tỷ trọng cổ phiếu trực tiếp tối đa 30%, mỗi cổ phiếu tối đa 10%, còn lại có thể phân bổ vào VTI/USMV. Các tỷ trọng trên là phần trăm của **growth sleeve**, không phải toàn bộ 12 triệu USD. Trái phiếu nghĩa vụ được giữ cố định ngoài bảng này.

Với Sample A=4, ví dụ quy đổi phần growth sleeve 6,346,351 USD: khoảng 140 nghìn MSFT, 183 nghìn JPM, 424 nghìn JNJ, 635 nghìn PG, 142 nghìn XOM, 380 nghìn NEE, 1,149 nghìn VTI và 3,294 nghìn USMV. Beta/Delta không đổi. Bảng toàn bộ danh mục và số USD từng mã nằm trong `outputs/tables/portfolio_weights_and_full_fund_bridge.csv`.

## Biểu đồ cần đọc như thế nào?

- `outputs/figures/portfolio_frontier_decision_2022.png`: trục ngang là biến động năm ước tính từ covariance mẫu; trục dọc là lợi suất CAPM dự phóng. Đường CE cho biết với cùng A=4, danh mục nằm cao hơn đường có CE cao hơn. Các điểm xám là những nghiệm khác nhau của A=1,2,4,6,8 cùng Eta; chúng giúp thấy đánh đổi rủi ro/lợi suất, không phải tất cả đều là danh mục tối ưu cùng lúc.
- `outputs/figures/portfolio_weights_growth_sleeve.png`: xem tiền trong growth sleeve được chia vào từng mã ra sao. Cổ phiếu riêng lẻ chạm trần 10% ở các danh mục optimizer.
- `outputs/figures/portfolio_radar_training_2022.png`: radar dùng năm trục minh họa: lợi suất dự phóng, CE A=4, biến động thấp, Sharpe huấn luyện và drawdown nông. Điểm 0–100 là min–max trong sáu danh mục được vẽ, không phải điểm tuyệt đối.
- `outputs/figures/portfolio_oos_2023_2025.png`: tách riêng lợi suất kép và biến động ngoài mẫu sau khi quyết định đã đóng băng. VTI dẫn đầu giai đoạn này; kết quả không được đưa ngược vào quyết định 2022.

### Radar có nên cộng tổng điểm để chọn không?

Radar **hợp lý để nhìn nhanh** mỗi danh mục mạnh/yếu ở mặt nào, nhưng không nên cộng điểm tùy tiện hoặc chọn danh mục có diện tích lớn nhất. CE đã kết hợp lợi suất và phương sai; thêm lợi suất, biến động và drawdown vào tổng điểm sẽ tính lặp các khía cạnh liên quan nhau. Sharpe cũng dùng lợi suất vượt RF trên độ lệch chuẩn, nên có giao nhau với CE và volatility. Min–max còn phụ thuộc các danh mục nào được đưa vào hình: thêm/bớt một ứng viên sẽ làm điểm của các danh mục khác đổi.

Nếu hội đồng vẫn muốn một composite score, phải định nghĩa trước từng trục, hướng tốt/xấu, chuẩn hóa, trọng số, lý do trọng số, ngưỡng loại và xử lý dữ liệu thiếu; đồng thời kiểm tra danh mục thắng có đổi khi đổi trọng số hay không. Trong initial record nên trình bày **CE A=4 là tiêu chí xếp hạng chính**, radar là dashboard phụ trợ, và hiển thị song song các chỉ số thô. Không dùng tổng điểm radar thay cho luận cứ đầu tư.

## Kết quả quan sát và giới hạn

Trong 2015–2022, Sample A=4 có CAGR 10,81%, biến động 12,65%, Sharpe 0,81 và drawdown cuối tháng lớn nhất -17,96%; Single-index A=4 lần lượt 10,56%, 12,24%, 0,81 và -16,87%; USMV 9,55%, 12,84%, 0,71 và -19,06%. Tất cả các danh mục này từng vượt drawdown 15% trong mẫu. Vì vậy ngưỡng 15% nên tiếp tục là trigger quản trị/họp rà soát, không thể diễn đạt như mức lỗ tối đa được bảo đảm.

Trong 2023–2025, Sample A=4 có CAGR 12,79% và Sharpe 0,80; Single-index A=4 10,67% và 0,59; USMV 11,15% và 0,66; VTI 22,22% và 1,30. Đây chỉ là 36 tháng đánh giá ngoài mẫu. Nó cho thấy VTI thắng trong giai đoạn cụ thể này, không chứng minh rằng nên chọn VTI vào năm 2022 hoặc rằng kết quả tương lai sẽ lặp lại.

Danh sách cổ phiếu là universe chọn trước từ hiện tại và dữ liệu lịch sử của các mã sống sót, nên còn survivorship/selection bias. Covariance 96 tháng nhạy với cửa sổ và cú sốc từng xảy ra; CAPM return là giả định theo beta, không phải dự báo được hiệu chỉnh xác suất. Mô hình không đảm bảo trần drawdown, không xóa rủi ro cổ phiếu chung, và chưa tối ưu hóa trực tiếp xác suất mục tiêu 2030 cho tất cả các danh mục.

## Tái lập và kiểm tra từng bước

1. Mở `analysis/config.json`: xác nhận ngày quyết định 2022-12-31, cửa sổ huấn luyện kết thúc 2022-12, A=4, RF=4%, ERP=4,5%, giới hạn từng mã 10% và tổng cổ phiếu trực tiếp 30%.
2. Mở `outputs/tables/portfolio_candidates.csv`: kiểm tra trọng số từng phương án; tổng mỗi hàng bằng 100%, không có tỷ trọng âm, cổ phiếu trực tiếp không vượt các giới hạn.
3. Mở `outputs/tables/portfolio_comparison_decision_2022.csv`: kiểm tra forecast return, hai loại volatility/covariance, CE A=4 và hiệu quả 2015–2022.
4. Mở `outputs/tables/portfolio_comparison_and_weights.csv` và `portfolio_weights_and_full_fund_bridge.csv`: đối chiếu tỷ trọng tăng trưởng và quy đổi USD; Beta/Delta phải không đổi giữa các phương án.
5. Mở riêng `outputs/tables/portfolio_comparison_decision_2022.csv` các cột `oos_...`, hoặc `portfolio_oos_2023_2025.png`: đây là đánh giá sau cutoff; không dùng các cột này để chọn danh mục năm 2022.
6. Tái tạo kết quả từ dữ liệu đã lưu: `.venv\Scripts\python.exe analysis\portfolio_choice_visuals.py`. Script chỉ đọc dữ liệu cục bộ và ghi các bảng/biểu đồ comparison; không sửa `policy/frozen_policy.json`.

Trước khi sửa policy, hội đồng cần chốt một câu hỏi định hướng: ưu tiên giữ cấu trúc USMV đơn giản, hay cho phép tối ưu hóa cổ phiếu trực tiếp để đổi lấy lợi thế CE theo một covariance model? Nếu chọn phương án sau, cần đánh giá lại độ nhạy với cửa sổ, tham số, turnover và mô phỏng mục tiêu 2030 trước khi thay đổi chính sách.
