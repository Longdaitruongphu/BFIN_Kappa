# Giải thích mô hình danh mục và sửa nhầm lẫn về giới hạn tỷ trọng

## Những câu trong tài liệu đang nói về gì?

**Beta ở đây là hệ số beta của cổ phiếu/ETF, không phải trái phiếu Beta.** Với từng tài sản, mô hình CAPM hồi quy lợi suất vượt lãi suất phi rủi ro của tài sản theo phần bù lợi suất thị trường trong 96 tháng từ 01/2015 đến 12/2022. Hệ số dốc cho biết tài sản thường nhạy với biến động thị trường đến mức nào. Dùng hệ số này để dự phóng lợi suất CAPM: `Rf dự phóng + beta × phần bù rủi ro thị trường`; alpha dự phóng được đặt bằng 0.

**FF3 là mô hình ba nhân tố Fama–French.** Ngoài thị trường, nó đo độ nhạy lịch sử với SMB (cổ phiếu nhỏ trừ lớn) và HML (giá trị trừ tăng trưởng). Hồi quy giúp giải thích tài sản từng có các exposure nào; bản thân hồi quy không cho biết phần bù tương lai của SMB/HML. Muốn biến nó thành dự báo lợi suất, cần quyết định trước `E(SMB)` và `E(HML)`, cùng với `Rf` và `E(Mkt-RF)`. Nhóm chưa chốt hai phần bù SMB/HML; vì vậy CAPM là forecast cơ sở đơn giản, còn FF3 là kiểm tra độ nhạy nếu và khi nhóm đưa ra các giả định rõ ràng. FF3 alpha lịch sử cũng không tự động là alpha tương lai.

**Covariance (ma trận hiệp phương sai)** đo các tài sản cùng tăng/giảm với nhau ra sao. Từ cùng 96 quan sát lợi suất tháng, sample covariance ước lượng trực tiếp mức biến động và đồng biến động; nhân 12 để quy đổi sang đơn vị năm theo quy ước mô hình. Khi tính danh mục, `σ²p = w′Σw`; độ lệch chuẩn danh mục là căn bậc hai của phương sai. Single-index covariance là một ước lượng cạnh tranh để kiểm tra quyết định có phụ thuộc mạnh vào cách đo rủi ro hay không. Đây là giả định ổn định theo thời gian, không phải lời bảo đảm rằng tương quan tương lai y hệt 2015–2022.

## IPS là gì, và điều gì thật sự bắt buộc?

IPS là **Investment Policy Statement** — văn bản chính sách đầu tư của quỹ: mục tiêu, nghĩa vụ, thời hạn, cách chấp nhận rủi ro, tài sản được phép, tiêu chuẩn so sánh, giới hạn do trustees chấp thuận, quy tắc giám sát và thẩm quyền đổi chính sách. IPS không phải tên của một công thức tối ưu hóa.

Đề bài không chọn sẵn một danh mục tối ưu, hàm mục tiêu, risk aversion, risk limits hay model ưu tiên. Đề yêu cầu nhóm đề xuất một phân bổ, một phương án thay thế đáng tin cậy, lượng hóa risk-return, cho thấy giả định ngại rủi ro ảnh hưởng lựa chọn thế nào, và so sánh sample covariance với single-index covariance. Đề cũng yêu cầu nhóm **đề xuất và giải thích** mọi giới hạn danh mục và chi phí giao dịch bổ sung. Các giới hạn này là lựa chọn của nhóm/trustees, không được trình bày như rule có sẵn.

Đề cấm vay, bán khống và phái sinh; vì vậy công cụ khóa long-only. Nhưng đề **không** đặt trần 10% cho từng cổ phiếu hay trần 30% cho tổng cổ phiếu trực tiếp. Hai con số đó xuất hiện trong `analysis/config.json` và bản policy lưu trước đây với trạng thái “working assumptions awaiting the group's confirmation”; chúng là giả định phân tích chưa được trustees/người dùng xác nhận. Tôi đã sai khi gọi chúng là giới hạn IPS bắt buộc. Tệp cũ được giữ nguyên để bảo toàn lịch sử; công cụ mới mặc định để trống các trần bổ sung, và chỉ áp dụng chúng khi người dùng tự nhập để kiểm tra kịch bản.

## Tối ưu thế nào cho quỹ này?

Tách quyết định làm hai tầng. Tầng 1 là đảm bảo các khoản chi 2024 và 2027 bằng trái phiếu phù hợp dòng tiền như đã tính. Tầng 2 là phân bổ phần dư USD 6.346m cho mục tiêu thực năm 2030. Không dùng vốn đã dành trả nghĩa vụ để chạy optimizer tăng trưởng.

Đề bài không bắt buộc GMV, Max Sharpe, CAPM hay utility. Bộ so sánh dễ giải thích và đáp ứng trực tiếp đề là:

1. **Mean–variance utility làm chuẩn quyết định:** `U = E(Rp) − 0.5 × A × σ²p`. A phải được trustees/nhóm biện minh; chạy nhiều A để chỉ ra nó đổi tỷ trọng thế nào. A=4 trước đây chỉ là working assumption, chưa phải lựa chọn người dùng đã phê duyệt.
2. **GMV và maximum Sharpe làm phương án đối chiếu:** GMV chỉ giảm phương sai; maximum Sharpe tối đa hóa phần bù lợi suất trên mỗi đơn vị biến động. Không phương án nào tự động là lựa chọn phù hợp nhất cho quỹ có mục tiêu sức mua và nghĩa vụ.
3. **Liability/goal-aware kiểm tra tính phù hợp:** sau khi khóa khoản trả, so sánh xác suất đạt mục tiêu thực 2030, mức hụt trung vị/đuôi xấu và tổn thất toàn quỹ dưới stress. Đây là lớp kiểm tra quyết định; không được gọi là xác suất đáng tin cậy nếu chưa hiệu chỉnh mô hình và giả định phân phối.

Baseline nên báo cả mô hình sample và single-index trên cùng tài sản, cùng giả định lợi suất và cùng các giới hạn; tiếp đó chạy kịch bản có giới hạn bổ sung và không có giới hạn. Khi không có giới hạn, optimizer có thể dồn tỷ trọng vào một vài tài sản do sai số dự phóng. Đây là bằng chứng để nhóm cân nhắc đề xuất giới hạn/regularization, không phải lý do để lén coi 10%/30% là đã được phê duyệt.

Benchmark growth-sleeve đơn giản, có thể đầu tư và phù hợp yêu cầu đề là **VTI**. Báo USMV như phương án/chính sách được cân nhắc và báo riêng mức đạt nghĩa vụ/mục tiêu sức mua. Benchmark đo opportunity cost của cổ phiếu/ETF; coverage trái phiếu đo khả năng trả nghĩa vụ; không gộp cả ba thành một điểm Sharpe.

## Câu hỏi để nhóm chốt trước khi gọi một phương án là “tối ưu”

1. **Mục tiêu chính:** bạn muốn tối đa hóa utility với A đã biện minh (khuyến nghị làm tiêu chí quyết định dễ kiểm toán), hay tối đa hóa khả năng đạt mục tiêu sức mua 8m năm 2030 sau khi nghĩa vụ được bảo đảm? Nếu chọn mục tiêu, mức hụt nào là không chấp nhận được?
2. **Ngại rủi ro:** A=4 có thể giữ làm điểm giữa tạm thời rồi so sánh A=1, 2, 4, 6, 8; bạn có muốn chọn A=4 làm base để trình bày không, hay muốn base thận trọng hơn? A là khẩu vị chính sách, không suy ra máy móc từ mức giảm 15%.
3. **Giới hạn tập trung:** để trống trần mỗi tài sản/tổng cổ phiếu trong kịch bản cơ sở, rồi trình bày các giới hạn như kịch bản để trustees chọn? Nếu có, lý do nào khiến giới hạn cụ thể hợp với quỹ (rủi ro tập trung, quản trị, thanh khoản), thay vì chọn chỉ vì optimizer cần constraint?
4. **Tiền mặt và benchmark:** sau khi mua Beta/Delta, có cho phép phần dư giữ T-bills/tiền mặt trong growth sleeve không? Tạm dùng VTI làm benchmark growth allocation và USMV là phương án đối chiếu có phù hợp ý bạn không?
5. **FF3 dự phóng:** bạn muốn chỉ dùng FF3 để giải thích lịch sử (an toàn hơn khi chưa có view factor), hay đề xuất kịch bản phần bù SMB/HML rõ nguồn và kiểm tra CAPM vs FF3 forecast? Nếu chưa có luận cứ riêng, để factor premia 0 chỉ là sensitivity, không phải kết luận trung lập.

## Công cụ Python mới

`analysis/interactive_surplus_portfolio_lab.py` đọc dữ liệu đã lưu cục bộ, mặc định không đặt trần cổ phiếu, cho chỉnh CAPM/FF3, RF, ERP, phần bù SMB/HML, A, lựa chọn covariance, hệ số stress covariance, lạm phát, chi phí tái cân bằng và hai trần tập trung tùy chọn. Có thể tick chọn danh mục hiển thị riêng trên đồ thị điểm/radar và xuất từng hình hoặc bảng CSV.

Chạy GUI: `.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py`.

Kiểm tra tính toán/biểu đồ, không mở cửa sổ: `.venv\Scripts\python.exe analysis\interactive_surplus_portfolio_lab.py --self-test`.

Đồ thị và dự phóng là kịch bản, không phải cam kết. Mô hình chưa mô phỏng phân phối đuôi dày, phí ban đầu của từng combination, dòng tiền thực tế từ cash/Treasury hoặc sai số dự báo. Hãy đối chiếu bảng weights/metrics xuất CSV và giữ benchmark VTI, khoảng mẫu 2015–2022 và evaluation 2023–2025 tách biệt.
