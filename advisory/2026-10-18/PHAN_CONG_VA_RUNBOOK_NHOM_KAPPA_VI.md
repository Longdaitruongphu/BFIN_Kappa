# Kappa Foundation: chia việc và hướng dẫn làm bài cho nhóm

**Ngày lập:** 18/10/2026, giờ Việt Nam  
**Đối tượng:** bốn thành viên trong nhóm; có thể điều chỉnh nếu chỉ một hoặc hai người chạy được Python.  
**Mục đích:** hướng dẫn nội bộ bằng tiếng Việt. Các sản phẩm chính thức vẫn phải viết bằng tiếng Anh.

## 1. Bài này đang yêu cầu nhóm làm gì?

Hãy tưởng tượng Kappa có một chiếc két chứa 12 triệu USD. Quỹ đã hứa trước hai khoản giáo dục: 2,4 triệu USD vào cuối năm 2024 và 3,6 triệu USD vào cuối năm 2027. Hết năm 2030, quỹ muốn số tiền còn lại mua được lượng hàng hóa tương đương 8 triệu USD vào tháng 12/2022.

Nhiệm vụ của nhóm là nói với Hội đồng: nên giữ tài sản gì, giữ bao nhiêu, làm sao có sẵn tiền trả hai lời hứa, cơ hội và rủi ro của mục tiêu 2030 là gì, và Hội đồng sẽ thay đổi quyết định theo quy tắc nào.

Hai khoản chi năm 2024 và 2027 là **nghĩa vụ bắt buộc trong đề gốc**. Mục tiêu sức mua 8 triệu USD là **mục tiêu đầu tư**, không phải lời hứa chắc chắn sẽ đạt. Đề không nói phải chọn USMV, lạm phát 2,5%, hệ số rủi ro A=4 hay phải giới hạn lỗ đúng 15%; đó là các giả định và quyết định phải giải thích. Đề cấm vay, bán khống và phái sinh.

Thông tin để tái tạo quyết định gốc phải có ngày không muộn hơn 31/12/2022. Năm 2023-2025 dùng để đánh giá riêng chính sách đã đóng băng; không được xem kết quả rồi sửa câu chuyện để làm như thể nhóm biết kết quả ấy từ năm 2022. Đề yêu cầu 8-12 cổ phiếu Mỹ thuộc ít nhất bốn ngành, cộng hai ETF khác chiến lược; phân tích trái phiếu, danh mục, CAPM và ít nhất một mô hình đa nhân tố Lecture 7; nguồn dữ liệu và mã Python có thể tái lập; memo không quá tám trang cộng tối đa một trang tài liệu tham khảo; PDF và bản sửa được của slide; cùng đóng góp thật của từng thành viên và người kiểm tra độc lập.

Lịch trong đề, tất cả theo giờ TP. Hồ Chí Minh: **22/10 lúc 16:00** nộp hồ sơ quyết định ban đầu, file Python đang làm việc và hồ sơ dữ liệu có ngày; **23/10 lúc 16:00** Hội đồng công bố mandate sửa đổi; **29/10 lúc 16:00** nộp toàn bộ bài cuối. Ngày 23/10 còn ở tương lai vào thời điểm lập hướng dẫn này nên chưa thể phân tích nội dung sửa đổi.

## 2. AI đã làm những gì, và kết quả đang nằm ở đâu?

AI đã hỗ trợ đọc đề, tổ chức phân tích, viết và chạy mã Python, truy xuất dữ liệu qua `yfinance`, lấy bộ nhân tố Fama-French từ thư viện Kenneth French, tính dòng tiền trái phiếu, phân tích danh mục, tạo bảng và biểu đồ, rồi soạn các tài liệu. Dữ liệu thô, thời điểm lấy, cài đặt và dấu vân tay tệp được lưu. AI còn dựng sẵn hồ sơ phần đóng góp và câu hỏi; phần đó **không chứng minh sinh viên đã tự làm hay đã kiểm tra**.

| Sản phẩm hiện có | Đã tạo được gì? | Thành viên cần làm tiếp |
|---|---|---|
| [Memo hội đồng PDF](../../deliverables/Kappa_Committee_Memo.pdf) và [bản sửa được](../../deliverables/Kappa_Committee_Memo_Editable.md) | 9 trang: 8 trang nội dung và một trang tài liệu tham khảo. Có khuyến nghị, phân bổ, tài trợ nghĩa vụ, trái phiếu, danh mục, mô hình nhân tố, kết quả đánh giá, giới hạn rủi ro và điều kiện xem xét lại. | Đọc, kiểm tra con số trọng yếu, hiểu được lập luận và rà lại với yêu cầu môn học. |
| [Hồ sơ quyết định ban đầu PDF](../../deliverables/Kappa_Initial_Decision_Record.pdf) và [bản sửa được](../../deliverables/Kappa_Initial_Decision_Record_Editable.md) | Đúng 2 trang; ghi danh mục, giả định và quy tắc đánh giá ban đầu. Trạng thái là “prepared for submission”; chưa có bằng chứng đã nộp. | Đối chiếu tên thành viên, định hướng thật của nhóm, quy định AI môn học và xác nhận quy tắc trước khi nộp. |
| [Bài trình bày PDF](../../deliverables/Kappa_Committee_Presentation.pdf) và [PowerPoint sửa được](../../deliverables/Kappa_Committee_Presentation.pptx) | 13 slide, có bảng và hai biểu đồ. Kiểm tra cấu trúc, khả năng nhập slide và hình ảnh slide đã được ghi nhận. Phiếu kiểm tra nêu rõ **chưa xác nhận chạy bằng Microsoft PowerPoint bản gốc**. | Chia người trình bày, tập trả lời câu hỏi và mở thử PPTX trên máy nhóm để kiểm tra phông, biểu đồ, bố cục. |
| [Hướng dẫn yêu cầu và dữ liệu PDF](../../deliverables/Kappa_Requirements_and_Data_Guide.pdf) và [bản sửa được](../../deliverables/Kappa_Requirements_and_Data_Guide.md) | 7 trang; giải thích nguồn, cấu trúc dữ liệu, cách tái chạy và cách đọc một số bảng. | Dùng làm tài liệu tra cứu khi nhóm kiểm tra; không thay thế việc từng người phải hiểu phần mình trình bày. |
| `analysis/` và `data/raw/` | Có mã lấy dữ liệu riêng, mã phân tích và mã dựng báo cáo; có dữ liệu Yahoo và bộ nhân tố gốc. Khoảng 96 tháng dùng để ước lượng (2015-2022) và 36 tháng đánh giá (2023-2025). | Một người kỹ thuật quản lý mã và không để người khác cùng chạy ghi đè đầu ra. Người thứ hai kiểm tra độc lập phép tính đã chọn. |
| `outputs/tables/` và `outputs/figures/` | Bảng vốn đầu tư, dòng tiền, định giá và stress trái phiếu, hiệu suất, beta/alpha, giả định dự báo và độ nhạy mục tiêu. | Kiểm tra đúng bảng nào đang hỗ trợ mỗi câu trong memo/slide; phát hiện giải thích quá mức dữ liệu. |
| `policy/frozen_policy.json` | Chính sách gốc được đóng băng trước khi tách dữ liệu đánh giá; mã băm SHA-256 đã lưu. | Không sửa trực tiếp. Nếu có mandate mới, tạo phương án và bản ghi riêng, giữ nguyên phương án gốc. |

Phương án gốc dành khoảng 2,215 triệu USD cho Beta, 3,430 triệu USD cho Delta, 6,346 triệu USD cho USMV và khoảng 9.169 USD chi phí giả định. Beta tài trợ 2,4 triệu USD năm 2024; Delta tài trợ 3,6 triệu USD năm 2027; coupon dư khoảng 486.957 USD được tính vào tiền cuối kỳ.

Một mô phỏng cho ra tần suất đạt mục tiêu 2030 là 68,48% ở kịch bản lạm phát 2,5%. Hãy gọi đây là **tần suất mô phỏng có điều kiện**, không gọi là xác suất đã được xác thực ngoài đời, lời hứa hay bảo đảm. Kiểm tra đạt 28 phép kiểm tra số học là kiểm tra chương trình chạy đúng theo cách viết; nó chưa chứng minh giả định dự báo đúng, chính sách tốt nhất hay bài tuân thủ chính sách AI của môn học.

## 3. Chia bốn vai trò: mỗi người phải có việc thật và người kiểm tra khác

Hãy thay “Bạn 1” bằng tên thật và ghi công việc mà người đó thực sự hoàn tất. Đừng điền trước rằng ai đã kiểm tra hoặc đóng góp việc họ chưa làm.

| Vai trò | Việc chính | Sản phẩm bằng chứng | Người kiểm tra gợi ý |
|---|---|---|---|
| **Bạn 1 — Trưởng phần dữ liệu và Python** | Giữ mã nguồn, dữ liệu thô, cài đặt và dấu vân tay tệp. Giải thích cách tạo lợi nhuận tháng và bảo đảm dữ liệu đánh giá không bị đưa ngược vào quyết định năm 2022. Chỉ một người quản lý lần chạy đầy đủ. | Ghi chép mã/tệp đã chạy, bảng kiểm dữ liệu, câu trả lời miệng về một hàng dữ liệu. | Bạn 2 kiểm tra độc lập hai phép tính và số tháng; không chỉ xem dòng chữ “passed”. |
| **Bạn 2 — Kiểm tra định lượng độc lập** | Tự tính lại một lợi nhuận tháng từ giá đã điều chỉnh; tính lại Sharpe hoặc phép so sánh USMV/VTI; kiểm tra một số liệu stress/độ nhạy. Có thể không biết viết Python để làm phần này, nhưng phải biết công thức, máy tính/bảng tính cơ bản và cách dò dữ liệu. | Bảng tính kiểm tra, phép tính có đơn vị và giải thích chỗ nào khớp/khác. | Bạn 1 giải thích cách script làm; một người khác xác nhận rằng phép kiểm tra độc lập thật sự. |
| **Bạn 3 — Trái phiếu và nghĩa vụ** | Tự đọc đề, vẽ lịch tiền vào/ra, kiểm tra Beta/Delta, coupon, ngày đến hạn và stress lãi suất. Giải thích vì sao hai khoản bắt buộc được che phủ mà không cần bán cổ phiếu. | Bảng dòng tiền theo năm và một trang giải thích bằng lời của chính mình. | Bạn 2 kiểm tra lại công thức và số; Bạn 4 đối chiếu số tiền/ngày trong memo. |
| **Bạn 4 — Chính sách, phản biện và trình bày** | Đối chiếu câu hỏi bắt buộc trong đề với memo/slide; kiểm tra lạm phát, benchmark, mức lỗ, bất lợi của USMV; thu thập đúng quy định AI môn học; biên tập trình bày và chuẩn bị câu hỏi Hội đồng. | Bảng “yêu cầu đề → trang/bảng minh chứng”, ghi nguồn quy định AI, bản phân công thuyết trình và phản biện cá nhân. | Bạn 3 đọc chéo dòng tiền; Bạn 1 xác nhận mô tả phương pháp/mã không sai. |

**Nếu chỉ có hai người chạy Python:** Bạn 1 giữ vai trò quản lý mã và chạy; Bạn 2 kiểm tra phép tính độc lập. Bạn 3 và Bạn 4 vẫn làm sâu phần trái phiếu, đề bài, chính sách và phản biện. Cả hai người kỹ thuật vẫn phải tự hiểu một phần tài chính; hai người còn lại vẫn phải tự kiểm tra một con số thay vì giao hết phần định lượng cho AI.

**Nếu chỉ bạn chạy Python:** bạn giữ mã và chạy; chọn một thành viên khác làm người kiểm tra số học độc lập bằng một phép tính có thể tự tái tạo. Ba thành viên còn lại nhận trách nhiệm rõ về trái phiếu, yêu cầu đề/chính sách AI, phản biện USMV/VTI và tập trình bày. Người kiểm tra không cần biết lập trình để kiểm tra, nhưng cần được bạn chỉ cho biết dữ liệu đầu vào, công thức, đơn vị và con số ở đâu.

**Vòng kiểm tra chéo quan trọng:** người tạo phép tính không tự ghi mình là người kiểm tra độc lập phép tính đó. Sau khi kiểm tra, mỗi người tự viết 3-5 câu phê bình khuyến nghị cuối cùng và giải thích bằng lời. Phần đóng góp nhóm trong `TEAM_COMPLETION.md` hiện là gợi ý; chỉ sửa thành sự thật sau khi từng việc được làm xong.

## 4. Lộ trình gấp cho hồ sơ 22/10

### Bước 1 — 18/10: chốt sự thật đầu vào

Nhóm điền tên thật, mã sinh viên nếu môn yêu cầu, ai có thể chạy Python, ai có thể kiểm tra bảng tính, ai thuyết trình được. Tìm **chính sách AI thật của môn học** và quy định thuyết trình trong tài liệu môn học. Nếu không tìm thấy, ghi rõ đang chờ xác nhận; đừng đoán rằng giảng viên cho phép mọi cách dùng AI. Chốt người chịu trách nhiệm mỗi vai trò và người kiểm tra riêng.

### Bước 2 — 19/10: ai cũng đọc đề; kỹ thuật viên không chạy lại để cho có

Đọc đề trang 1-4 và đánh dấu nghĩa vụ, giới hạn đầu tư, dữ liệu và hạn nộp. Xem [hồ sơ hai trang](../../deliverables/Kappa_Initial_Decision_Record_Editable.md) và [log quyết định](../../DECISION_LOG.md). Nếu nhóm chấp nhận phân bổ gốc, kiểm tra nó còn phản ánh lựa chọn của nhóm không. Đừng gọi là “đã nộp” khi chưa nộp thật.

### Bước 3 — 20/10: người trái phiếu và người kiểm tra số làm việc độc lập

Bạn 3 vẽ trục thời gian: 2023, 2024 trả 2,4 triệu; 2025-2026 coupon; 2027 trả 3,6 triệu; 2028-2030 giữ phần còn lại. Bạn 2 dùng máy tính tái tạo ít nhất hai con số, chẳng hạn chi phí trái phiếu = mệnh giá x giá niêm yết / 1.000 hoặc Sharpe từ lợi nhuận vượt RF và độ lệch chuẩn hàng tháng. Ghi đủ công thức, kỳ đo, đơn vị và nguồn số ban đầu.

### Bước 4 — 21/10: đọc chéo và tập giải thích

Mỗi thành viên giải thích một bảng/slide của mình mà không đọc nguyên văn. Người nghe hỏi: “Con số này từ tệp nào? Đơn vị gì? Điều gì làm nó sai? Nó chứng minh được gì, không chứng minh được gì?” Sửa lỗi có bằng chứng, thống nhất bản hồ sơ, chuẩn bị cách công bố hỗ trợ AI. Chỉ một người ghi nhận bản nộp sau khi nhóm xác nhận.

### Bước 5 — 22/10 trước 16:00: nhóm xác nhận và nộp đúng nơi

Đề yêu cầu hồ sơ ban đầu tối đa hai trang, candidate universe, cửa sổ dữ liệu, benchmark, số tiền ban đầu, giả định quan trọng, quy tắc đánh giá/tái cân bằng; kèm file Python đang làm và hồ sơ dữ liệu có ngày. Kiểm lại dung lượng và nội dung đúng yêu cầu môn học, giữ biên nhận thực tế. Bản PDF hiện tại có hai trang nhưng còn phải rà thông tin nhóm, chính sách AI và sự hiểu biết của từng người.

### Bước 6 — 23/10 sau khi mandate mới được phát hành

Lưu nguyên bản đúng như được phát hành và ghi ngày/nguồn. So từng câu yêu cầu mới với đề gốc. Giữ bản gốc và chính sách năm 2022 riêng; tính ảnh hưởng của thay đổi theo một kịch bản mới. Đừng đoán nội dung trước khi đọc. Quy trình chi tiết ở `MANDATE_REVISION.md`.

### Bước 7 — 24-29/10: hoàn thiện bài cuối

Chạy các sửa đổi được cả nhóm duyệt, giữ log phiên bản; kiểm tra lại bảng trong memo khớp CSV, memo đúng giới hạn trang, slide PDF khớp PPTX, nguồn có thể truy xuất và ai cũng giải thích được phần ghi tên mình. Hoàn thành bảng đóng góp, check chéo và phản biện từng người bằng sự thật. Trước 16:00 ngày 29/10, xác nhận archive cuối thực sự được nộp.

## 5. Giải thích kỹ thuật như làm theo một công thức nấu ăn

**Nguyên liệu là dữ liệu thô.** `data/raw/train/` giữ giá thị trường trong giai đoạn xây dựng quyết định; `data/raw/eval/` giữ giá đánh giá riêng; `data/raw/supporting/` giữ tài liệu phương pháp và ghi chú nguồn. Có dữ liệu thô nghĩa là giữ nguyên nguyên liệu trước khi cắt, nấu; đừng thay bằng bảng tải từ bạn khác.

**Phiếu công thức là cài đặt và cách tải.** `analysis/retrieve_data.py` là mã lấy dữ liệu; `analysis/config.json` ghi mã chứng khoán, ngày và giả định. Không chạy phần lấy dữ liệu mới khi chưa có lý do và chưa ghi lại ngày/phiên bản. Phần đánh giá 2023-2025 đã được lấy sau khi chính sách được đóng băng.

**Bước sơ chế là `analysis/analyze.py`.** Mã kiểm tra ngày, dựng giá tháng/lợi nhuận, nối bộ nhân tố, tính trái phiếu và danh mục rồi ghi bảng. Lợi nhuận điều chỉnh dùng thay đổi giá cùng tác động cổ tức/phân chia theo dữ liệu vendor; người kiểm tra cần hiểu phép biến đổi, không chỉ tin con số đầu ra.

**Khâu nấu lại là `analysis/rebuild.py`.** Khi Python 3.12 và gói đã ghim đã sẵn sàng, từ thư mục gốc chạy trong PowerShell:

```powershell
.\.venv\Scripts\python.exe analysis\rebuild.py
```

Đây là dựng lại từ tệp đã lưu, không tải internet. Biên nhận cũ cho biết lần chạy trước tắt mạng và vượt 28 kiểm tra số. Nếu thư mục `.venv` chưa có, đừng vội tạo hoặc cài gói; hỏi người đang quản lý máy và làm theo `README.md`. Chỉ một thành viên chạy một lần tại một thời điểm, tránh hai người cùng ghi vào bảng và báo cáo.

**Đĩa thức ăn là CSV/JSON trong `outputs/tables/`.** Mỗi dòng thường là một chứng khoán, tháng hay kịch bản; cột cho biết giá trị, kỳ đo và đơn vị. Mở bằng Excel được, nhưng không lưu đè tệp gốc. Ví dụ `evaluation_performance.csv` so hiệu suất USMV với VTI; `funding_cashflows.csv` cho thấy tiền vào/ra theo năm; `factor_regressions.csv` cho beta, alpha và khoảng tin cậy. Luôn đọc tiêu đề cột trước, tìm định nghĩa trong memo hoặc guide rồi mới diễn giải.

**Món ăn bày ra là memo, slide và biểu đồ.** Chúng phải khớp bảng gốc. Nếu slide ghi 82,56% nhưng bảng không thấy, dừng lại và truy vết trước khi trình bày.

Phép kiểm tra trẻ nhỏ có thể hiểu là: **mọi con số phải trả lời được ba câu “lấy ở đâu?”, “tính thế nào?”, “nó có nghĩa gì?”**. Thêm câu thứ tư cho người kiểm tra: **“Nếu đổi một giả định hoặc có một lỗi, kết luận có đổi không?”**

## 6. Cách kiểm tra con số trọng yếu

| Câu hỏi | Nơi xem | Cách nói dễ hiểu |
|---|---|---|
| Đã dùng đủ 12 triệu USD chưa? | `outputs/tables/initial_allocation.csv` | Cộng Beta + Delta + USMV + chi phí, đối chiếu 12 triệu. |
| Có tiền trả đúng hai ngày không? | `outputs/tables/funding_cashflows.csv` | Tại mỗi năm, cộng tiền trái phiếu đến hạn và coupon; trừ khoản phải trả; số còn lại không âm. |
| Trái phiếu đổi giá khi lãi suất đổi thế nào? | `bond_metrics.csv`, `ytm_duration_validation.csv`, `bond_stress.csv` | Duration/convexity là phép ước tính; bảng repricing kiểm tra lại bằng định giá chính xác. Đừng gọi thay đổi giá là thay đổi dòng tiền hợp đồng. |
| USMV hơn hay kém VTI trong giai đoạn đã chọn? | `outputs/tables/evaluation_performance.csv` | Đọc đồng thời tổng lợi nhuận, CAGR, biến động, Sharpe và drawdown; nói rõ chỉ có 36 tháng. |
| Alpha có chứng minh kỹ năng không? | `outputs/tables/factor_regressions.csv` | Đọc hệ số cùng khoảng tin cậy, sai số chuẩn và số tháng. Alpha ước lượng không tự động là lợi nhuận tương lai. |
| Mục tiêu 2030 chắc đến đâu? | `mission_simulation.csv`, `goal_sensitivity.csv` | Đây là kết quả theo giả định; hỏi độ sâu thiếu hụt và điều gì xảy ra khi lạm phát cao. Tần suất mô phỏng không phải lời bảo đảm. |
| Cú sốc có làm mất tiền trả nghĩa vụ không? | `outputs/tables/whole_fund_stress.csv` | So giá trị tài sản thị trường với dòng tiền hợp đồng; đề giả định không vỡ nợ trái phiếu nhưng giá bán trước hạn vẫn có thể đổi. |

### Ví dụ kiểm tra Sharpe

Sharpe hỏi: “Mỗi đơn vị dao động của danh mục, nhà đầu tư được bù bao nhiêu lợi nhuận vượt tiền gần như phi rủi ro?” Cách tính trong bài: trung bình lợi nhuận tháng trừ lãi suất phi rủi ro tháng, chia cho độ lệch chuẩn của chuỗi vượt lãi suất ấy, rồi quy đổi năm bằng căn bậc hai của 12.

Kết quả 2023-2025: Sharpe USMV 0,66, VTI 1,30. USMV biến động thấp hơn nhưng lợi nhuận vượt RF thấp hơn nhiều; nó **không thắng** chỉ vì sụt giảm tối đa nhỏ hơn. Giai đoạn chỉ có 36 tháng và thị trường tăng mạnh; kết quả bất lợi này cần được trình bày đầy đủ, không dùng để tuyên bố chắc chắn ETF nào sẽ thắng tương lai.

## 7. Việc con người phải tự xác nhận trước khi ghi tên nộp bài

1. Chính sách AI của môn học và quy tắc trích dẫn/trình bày. Gói hiện tại đã công bố AI có hỗ trợ, nhưng nhóm vẫn phải đối chiếu đúng yêu cầu của giảng viên.
2. Mỗi thành viên biết và giải thích được phần mình làm; ghi công việc thật và tệp/bảng minh chứng.
3. Một thành viên khác đã thật sự kiểm tra lại việc đó; ghi kết quả và lỗi đã sửa.
4. Mỗi thành viên viết phản biện riêng, chẳng hạn: mục tiêu quá tham vọng, USMV có chi phí cơ hội, 15% chưa thể coi là sàn bảo đảm, hay giả định lạm phát thiếu chắc chắn. Người viết phải giải thích được ý của mình.
5. Nhóm tự quyết định có còn chấp nhận khuyến nghị trái phiếu thanh toán + USMV hay chưa. Việc AI đã tối ưu không thay cho lựa chọn và chịu trách nhiệm của nhóm.
6. Không bịa tên, mã sinh viên, kiểm tra độc lập, nội dung mandate sửa đổi hoặc trạng thái đã nộp.

## 8. Trạng thái cần biết hôm nay

- Phân tích đề gốc và các sản phẩm được tạo; bản dựng ngoại tuyến trước đây đạt 28 kiểm tra số học, và gói lưu trữ đã được đối chiếu lại. Đây là bằng chứng tính nhất quán kỹ thuật, không thay kiểm tra người và tuân thủ môn học.
- Memo PDF: 9 trang gồm một trang tham khảo; hồ sơ ban đầu: 2 trang; data guide: 7 trang; slide PDF: 13 trang. PPTX đã qua kiểm tra cấu trúc và bản render slide, nhưng chưa xác nhận mở trực tiếp bằng PowerPoint.
- Quyết định đã ghi nhận trước đây là trái phiếu Beta + Delta để trả nghĩa vụ, USMV cho phần tăng trưởng, benchmark VTI, chấp nhận có thể hụt mục tiêu. Người dùng đang yêu cầu cùng tư duy lại triết lý; chưa có quyết định thay allocation.
- Chưa có bằng chứng hồ sơ ngày 22/10 đã được nộp; ngày hiện tại là 18/10 nên hạn nộp vẫn ở phía trước.
- Còn cần nhóm cung cấp: chính sách AI thật, tên và đóng góp thật của thành viên, kết quả kiểm tra thật, và sau ngày 23/10 là văn bản mandate sửa đổi.
- Dữ liệu năm 2023-2025 đã đóng vai trò đánh giá; không dùng lại để giả lập rằng nhóm năm 2022 biết tương lai.

Sau buổi phân công, ghi tên người thật và trả lời ngắn ba câu: **ai chạy Python, ai kiểm tra một phép tính độc lập, ai phụ trách nghĩa vụ trái phiếu?** Sau đó nhóm có thể dùng sáu vòng trong `advisory/2026-10-16/Board_Consultation_Questions.md` để chốt triết lý đầu tư trước khi thay chính sách.
