# Giải thích quyết định policy và kế hoạch xử lý mandate 23/10

**Ngày:** 20/10/2026. Tài liệu tư vấn nội bộ. Không thay thế mandate gốc, policy đã freeze, hoặc văn bản revised mandate chưa được phát hành.

## Những gì bạn vừa xác nhận

- Nghĩa vụ 2024/2027 được ưu tiên trước mục tiêu sức mua $8m năm 2030.
- Inflation giữ base 2.5% và chạy sensitivity.
- Risk aversion giữ baseline A=4; sensitivity theo đề xuất.
- Giữ lựa chọn USMV của quyết định gốc năm 2022 và dùng VTI làm comparator. Kết quả 2023–25 là phần đánh giá sau, không được dùng để viết lại quyết định 2022.

Đây là xác nhận cho hướng tư vấn. Chúng không sửa `policy/frozen_policy.json` hay thay thế initial submission.

## Giải thích các câu hỏi còn chưa rõ

### 2. “Lập thêm kịch bản” coupon là gì?

Delta trả bốn coupon sớm, mỗi coupon khoảng **$121,739**, tổng khoảng **$486,957** trong 2023–2026. Coupon này không cần để khớp khoản phải trả 2027 vì coupon cuối cộng gốc đã đủ $3.6m.

Có hai cách xử lý cần so sánh:

| Kịch bản | Làm gì với coupon sớm? | Ý nghĩa |
|---|---|---|
| A — baseline đã freeze | Giữ tiền mặt, giả định sinh lời 0% | Thận trọng, dễ giải thích; đây là quy ước hiện tại của model. |
| B — đầu tư lại | Mỗi coupon nhận được thì đầu tư vào growth sleeve theo một quy tắc đã viết trước | Tăng khả năng tăng trưởng, nhưng coupon cũng chịu rủi ro cổ phiếu và có thể mất giá đúng lúc cần thanh khoản. |

“Lập thêm kịch bản” chỉ có nghĩa là chạy cả A và B để thấy terminal wealth, biến động, drawdown và khả năng đạt mục tiêu thay đổi ra sao. Nó **không** có nghĩa là đã chọn B. Nếu chưa rõ, giữ A làm base và chỉ dùng B như sensitivity. Không được cho rằng coupon đầu tư lại chắc chắn kiếm được lợi suất như dự báo.

### 3. Ngưỡng 15% biểu trưng cho điều gì?

Trước hết cần phân biệt ba khái niệm:

- **Mức lỗ tối đa được bảo đảm:** quỹ không thể lỗ quá con số này trong bất kỳ tình huống nào. Với cổ phiếu và gap khủng hoảng, không thể hứa điều đó; lệnh stop cũng có thể khớp thấp hơn mức đặt.
- **Ngưỡng cảnh báo/xem xét:** khi thước đo lỗ chạm 15%, phải họp, kiểm tra nghĩa vụ và quyết định có giữ nguyên chính sách không. Không tự động bán.
- **Ngưỡng hành động tự động:** chạm 15% thì bắt buộc giảm/bán tài sản. Cách này có nguy cơ bán sau khi giá đã giảm mạnh và không bảo đảm giá bán.

**Đề xuất cho quỹ:** gọi 15% là *ngưỡng kích hoạt rà soát*, không gọi là maximum stop-loss. Đo trên growth sleeve bằng chuỗi lợi suất đã điều chỉnh dòng tiền (để khoản chi $2.4m/$3.6m không bị hiểu nhầm thành investment loss); khi chạm ngưỡng thì kiểm tra lại luận điểm, thanh khoản, độ phủ nghĩa vụ và dự báo. Không có bán tự động. Việc bảo đảm các khoản phải trả được theo dõi riêng bằng cash-flow coverage, là redline cứng hơn.

Cần phân biệt thêm: “15% từ đỉnh gần nhất” là drawdown; “giảm 15% so với ngày đầu” là loss từ mốc đầu. Hai số có thể khác nhau. Với quỹ đã chi tiền cho chương trình, không nên so NAV hiện tại thẳng với $12m ban đầu vì các khoản chi hợp lệ làm NAV giảm. Chuỗi growth sleeve hoặc NAV được điều chỉnh dòng tiền sẽ tránh nhầm lẫn đó.

### 4. Ngoại lệ khủng hoảng cần quyết định gì?

Ngoại lệ không có nghĩa là được bỏ qua nghĩa vụ. Nó là quy trình để tránh một chính sách máy móc buộc quỹ bán tài sản ngay giữa thị trường rối loạn. Một quy trình có thể viết như sau:

1. **Ai được kích hoạt?** Ví dụ Chủ tịch ủy ban đầu tư cùng thủ quỹ, hoặc đa số trustees; chọn đúng cơ quan có thẩm quyền của case.
2. **Điều gì được tạm dừng?** Ví dụ chỉ tạm dừng rebalance bán tài sản rủi ro; không được tạm dừng trả nghĩa vụ đến hạn.
3. **Ngoại lệ kéo dài bao lâu?** Ví dụ hết hạn trong 30 ngày, sau đó phải tái phê duyệt. Đây chỉ là mẫu để thảo luận, chưa phải quy tắc đã chọn.
4. **Điều kiện bảo vệ nào không được miễn?** Đủ tiền/tài sản đáo hạn cho khoản phải trả kế tiếp, thanh khoản vận hành, và không vi phạm hard rules của đề.
5. **Hồ sơ phải ghi gì?** Sự kiện, số liệu, người quyết định, hành động tạm dừng, rủi ro chấp nhận và ngày rà soát tiếp theo.

Để bắt đầu đơn giản: 15% là trigger để họp; một ngoại lệ chỉ trì hoãn quyết định giao dịch trong thời gian ngắn, có người phê duyệt và ngày hết hạn; nghĩa vụ gần nhất vẫn phải được giữ đủ.

### 6. A=4 liên quan thế nào với inflation và câu hỏi 4?

Ba thứ này trả lời ba câu hỏi khác nhau:

- **Inflation** quyết định $8m sức mua hôm nay tương đương bao nhiêu đô la danh nghĩa năm 2030, từ đó ảnh hưởng mức tăng trưởng cần có.
- **Risk aversion A** thể hiện trustees đánh đổi lợi suất kỳ vọng lấy biến động/rủi ro như thế nào khi so sánh USMV với VTI. Trong model hiện tại, ngưỡng chuyển lựa chọn là A≈2.58: A=2 nghiêng VTI; A=4,6,8 nghiêng USMV theo quy ước model. A không tự động tăng khi inflation tăng.
- **Crisis-exception governance** quy định ai được gọi họp, có thể tạm dừng điều gì và trong bao lâu nếu ngưỡng rủi ro bị chạm.

Sensitivity gọn và rõ có thể là hai bảng song song:

| Planning inflation | Nominal target 2030 | Growth-sleeve CAGR cần thiết* |
|---:|---:|---:|
| 2.0% | $9.373m | 4.30% |
| 2.5% base | $9.747m | 4.84% |
| 4.0% | $10.949m | 6.45% |
| 5.0% | $11.820m | 7.52% |

\* Dùng cùng quy ước gốc: vốn USMV $6.346m, giữ $0.487m coupon tích lũy ở cash không sinh lời đến 2030; đây là required CAGR, không phải forecast.

Bảng A-sensitivity giữ inflation ở base 2.5%: A=2/4/6/8. Sau đó có thể làm một ma trận nhỏ inflation × A nếu muốn xem *vừa* yêu cầu sức mua *vừa* preference ảnh hưởng kết luận ra sao. Không cần gộp thành một “A biến thiên theo CPI”; đó sẽ là hai giả định khác bản chất.

### 8. Câu hỏi “revised mandate” nghĩa là gì?

Đây không phải câu hỏi bạn phải tự nghĩ nội dung. Đề gốc nói trustees sẽ phát hành một mandate sửa đổi lúc **16:00 ngày 23/10/2026**. Khi văn bản được phát hành, cần nhận đúng nội dung, giữ bản gốc và ghi nguồn/ngày. Hiện tại dự án chưa có văn bản đó; từ “revised mandate” chưa đủ để suy ra thay đổi nào.

## Những thay đổi có thể xảy ra và cách chuẩn bị

Đây là **nhóm kịch bản để chuẩn bị**, không phải dự đoán mandate thật sẽ chọn nhóm nào.

| Nếu văn bản mới yêu cầu… | Tác động cần chạy lại | Hướng giải pháp/đánh đổi cần báo trustees |
|---|---|---|
| Đổi số tiền hoặc ngày hai nghĩa vụ | Sizing Beta/Delta, cash-flow coverage, capital còn lại, required CAGR | Khớp lại ngày/số tiền bằng bond cash flows; nếu thiếu tiền, báo vốn bổ sung hoặc giảm mục tiêu growth, không lờ nghĩa vụ. |
| Biến $8m real goal thành cam kết cứng hoặc nâng mục tiêu | Required return, shortfall/scenario table, danh mục all-bond đối chiếu | Giải thích không thể bảo đảm mục tiêu real bằng tài sản rủi ro; cân nhắc vốn góp thêm, thời hạn dài hơn hoặc mục tiêu thấp hơn. All-bond so sánh hiện tại khoảng $7.471m real ở 2.5%, thiếu khoảng $529k so với mục tiêu; cần khoảng $480k vốn đầu vào bổ sung theo cấu trúc gốc để đạt mục tiêu all-bond. |
| Đặt giới hạn lỗ 15% thành hard cap | Kiểm tra tính khả thi với equity, stress gap, quyền đầu tư được phép | Nêu rõ hard cap không thể hứa với equity thường; nếu trustee thật sự yêu cầu sàn bảo vệ, cần đổi công cụ/mandate hoặc chấp nhận giảm tăng trưởng, nhưng đề cấm derivatives/borrowing/shorting. Không được viết rằng một stop order bảo đảm sàn. |
| Đổi mức chịu rủi ro/benchmark/ETF | Tái lập preference table, return/risk, stress, turnover, benchmark architecture | Giữ nguyên dữ liệu cutoff 2022; so sánh cùng universe và cùng giả định. Không dùng kết quả 2023–25 để chọn lại chính sách 2022. |
| Yêu cầu tiền mặt dự phòng hoặc chi vận hành mới | Deduct reserve/spending khỏi vốn growth, tính lại CAGR và payment coverage | Tách reserve khỏi khoản chi nghĩa vụ và terminal assets; không đếm một đô la hai lần. |
| Mở/đóng loại tài sản hoặc thêm giới hạn | Xác nhận có nằm trong universe đề cho phép không; làm lại nguồn eligibility và model | Đề gốc chỉ cho cash, case bonds, cổ phiếu thường Mỹ, ETF Mỹ chủ yếu đầu tư cổ phiếu Mỹ; không borrowing/shorting/derivatives. Một mandate lớp học mới không tự động sửa các hard rule của đề trừ khi văn bản đề/giảng viên nói rõ. |
| Không đổi số tiền nhưng đổi cách hiểu “15%” hoặc governance | Viết lại định nghĩa đo, người phê duyệt, thời hạn, báo cáo | Đây có thể chỉ là thay đổi policy process; không nhất thiết đổi allocation, nhưng phải định lượng nếu nó kích hoạt giao dịch/rebalance. |

## Quy trình 23/10 đến 29/10

### 23/10, ngay khi nhận mandate mới

1. Lưu file/email nguyên bản, ghi đúng thời gian/nguồn; tạo hash; không chép lại theo trí nhớ.
2. Giữ riêng snapshot initial submission 22/10, frozen policy, dữ liệu và decision log. Không ghi đè.
3. Chia từng câu mới thành “thay đổi bắt buộc”, “làm rõ”, hoặc “không thay đổi”; trích nguyên văn và ghi điều khoản/đoạn liên quan.
4. Lập scenario copy của config. Mỗi trường thay đổi phải có giá trị cũ, giá trị mới, nguồn mới và lý do; policy gốc vẫn nguyên.

### 24–26/10: định lượng tác động

5. Dùng cùng case date 31/12/2022 và thông tin có đến ngày đó để thiết kế phương án mới. Không để giá, lãi suất hay kết quả 2023–25 lọt vào quyết định “như thể biết trước”.
6. Chạy lại phần bị ảnh hưởng: allocation/fees, nghĩa vụ và coverage, cash reserve/coupons, nominal 2030 goal/inflation, required CAGR, return-risk preference, sample vs single-index, factor evidence, curve/equity stress, turnover và constraints.
7. So bảng original vs revised: USD từng sleeve, phí, coverage năm 2/5, terminal goal, required CAGR, risk/shortfall diagnostics, stress loss, A, exposures và rule thay đổi. Giải thích chênh lệch do mandate mới riêng với chênh lệch do lựa chọn mô hình.

### 27–28/10: đánh giá và hoàn thiện

8. Đánh giá policy gốc và policy mới trên cùng giai đoạn 2023–25 theo đúng quy tắc đã freeze. Đây là **evaluation riêng sau khi thiết kế**, không phải bằng chứng được dùng để chọn policy 2022. Nếu mandate sửa tiêu chí evaluation, ghi thêm tiêu chí mới nhưng vẫn giữ kết quả đánh giá ban đầu.
9. Cập nhật memo, slides, decision log, scenario config và evidence map; giữ nội dung bất lợi. Mỗi thành viên ghi việc thật đã làm, một thành viên khác kiểm tra, và critique riêng. Không điền thay phần đóng góp thực tế.
10. Kiểm tra AI-use policy môn học, giới hạn 8 trang memo cộng tối đa 1 trang references, slide PDF + editable source, raw data/scripts, rebuild, manifest và archive.

### Trước 29/10, 16:00 HCMC

11. Khóa bản final mới; chạy rebuild/checks, kiểm tra các file và trang/slides; lưu archive và receipt. Giữ lại bản 22/10 và log mọi quyết định bị thay thế. Không tuyên bố đã nộp nếu chưa có biên nhận upload.

## Câu hỏi còn cần bạn xác nhận

1. Coupon: dùng A làm baseline (giữ cash, 0%) và B chỉ làm sensitivity đầu tư coupon vào USMV? Đây là cách an toàn nhất để phản ánh workbook B mà không âm thầm đổi policy.
2. 15%: có đồng ý cách diễn giải đề xuất—ngưỡng kích hoạt họp/rà soát trên growth sleeve, dòng tiền điều chỉnh, không tự bán—còn coverage nghĩa vụ là redline riêng?
3. Ngoại lệ: bạn muốn ví dụ quy trình 30 ngày với phê duyệt của Chủ tịch ủy ban + thủ quỹ/đa số trustee, hay muốn để authority theo đúng cấu trúc board trong mandate mới?
4. Revised mandate: hiện chưa có văn bản trong folder. Hãy gửi/paste đúng nguyên văn khi nhận ngày 23/10; nếu đã nhận được rồi thì cung cấp file/nguồn cụ thể.

## Nguồn số

Các required CAGR trên được tính lại từ `policy/frozen_policy.json` và `outputs/tables/funding_summary.json`, giữ nguyên vốn growth $6,346,350.71 và cash coupon $486,956.52. Các nghĩa vụ, ngày case, hard rules và ngày phát hành revised mandate được trích từ `reference/BFIN-WS2026-Group_Assignment.pdf`, trang 1–4. Các số all-bond là kết quả gốc đã lưu trong handoff, không phải ước tính mới cho mandate chưa biết.
