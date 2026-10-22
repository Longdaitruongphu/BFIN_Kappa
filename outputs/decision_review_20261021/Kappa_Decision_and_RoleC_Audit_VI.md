# Kappa: kiểm toán danh mục tăng trưởng và quyết định 22/10

**Trạng thái:** tài liệu tư vấn nội bộ ngày 21/10/2026; ngày thông tin của quyết định đầu tư là 31/12/2022. Không dùng kết quả 2023–2025 để chọn ngược danh mục tại 2022. File Role C mới được giữ nguyên byte ở `reference/role_c/BFIN_Part_C_Verified_Expanded_original_20261021.xlsx` (SHA-256 `d575f3722438d744d364cbc35056c03bdb50d202b201006f5c01978a9474f286`). Các phát biểu trong workbook là đối tượng kiểm tra, không phải chính sách được phê duyệt.

## 1. Quyết định cần tối ưu cái gì?

Đề giao **hai bài toán nối tiếp**. Trước hết, dùng trái phiếu case để khớp *đúng ngày, đúng số tiền danh nghĩa* USD 2.4m cuối 2024 và USD 3.6m cuối 2027. Beta 2,400 đơn vị tốn USD 2,214,672; Delta 3,478.26087 đơn vị tốn USD 3,429,808.70. Phí giả định 5 bp cho trái phiếu làm chi phí của nhánh nghĩa vụ USD 5,647,302.94. Nếu đầu tư phần còn lại vào ETF/cổ phiếu với phí vào lệnh 10 bp, giá trị chứng khoán tăng trưởng ban đầu là **USD 6,346,350.71**; phí toàn bộ giao dịch ban đầu USD 9,168.59. Bốn coupon Delta trước đáo hạn, USD 486,956.52, vào tiền mặt với lãi tái đầu tư 0% trong base case. Cách này không cần bán cổ phiếu hoặc bán trái phiếu trước hạn để trả hai nghĩa vụ.

Sau đó, tối ưu *phần vốn tăng trưởng*, không tối đa hóa một tỷ số Sharpe riêng lẻ. Tiêu chí ra quyết định đang đề xuất là: (i) không phá kế hoạch nghĩa vụ; (ii) phù hợp mức chịu lỗ của trustees, nơi 10/15/20% trên **growth sleeve** là ngưỡng xem xét chứ không phải lệnh stop; (iii) trong các phương án đáp ứng điều kiện trên, so sánh lợi suất kỳ vọng và rủi ro bằng `U_A = E[R] - 0.5 A σ²` với **A = 4 tạm thời**, kiểm độ nhạy A=2/6/8; (iv) không nhận thêm phức tạp và chi phí nếu cải thiện mô hình quá nhỏ hoặc không vững. Mục tiêu USD 8m sức mua tháng 12/2022 là mục tiêu cần theo dõi, không là bảo đảm. CPI 2.5% đưa nó lên USD 9.747m danh nghĩa năm 2030; growth cần 4.836% CAGR nếu bốn coupon ở cash 0%. Kịch bản lạm phát chi phí giáo dục 3.0% nâng mục tiêu lên USD 10.134m và hurdle lên 5.374%.

**Ba định nghĩa “tối ưu” trả lời ba câu khác nhau.** GMV hỏi danh mục có phương sai thấp nhất; nó không hỏi đủ lợi suất để đạt mục tiêu. Max Sharpe hỏi phần bù lợi suất trên mỗi đơn vị biến động; nó không biết trustees ngại mức lỗ 15% thế nào. Max Utility hỏi đánh đổi lợi suất/rủi ro theo A đã công bố; nó phù hợp hơn với lựa chọn chính sách, nhưng rất nhạy với đầu vào. Vì vậy “tối ưu toán học” là một *ứng viên*, không tự động thành quyết định ủy thác. Radar có thể dùng để trình bày các trục khác nhau, song không cộng điểm tùy ý: Sharpe, volatility, utility cùng chứa thông tin rủi ro và cộng lại sẽ đếm hai lần.

## 2. Danh mục nào dùng để so sánh?

Tất cả số ở bảng này dùng cùng **10 ứng viên được lưu nguồn** (AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, VTI, USMV), 96 tháng 2015–2022, CAPM `4% + beta × 4.5%`, alpha dự báo bằng 0, covariance sample chung để chấm Utility A=4, long-only và tổng trọng số 100%. **Không áp trần 10%/mã hay 30% cổ phiếu trực tiếp** vì trustees chưa duyệt. Kết quả 2023–2025 ở cột cuối chỉ là kiểm định sau quyết định; có 10 bp phí đầu vào và phí tái cân bằng hằng năm khi phát sinh giao dịch. Bảng máy đọc: `outputs/decision_review_20261021/growth_candidate_comparison.csv` và `growth_candidate_weights.csv`.

| Vai trò so sánh | E[R] | σ năm | U(A=4) | 2015–22 max DD | 2023–25 CAGR sau phí |
|---|---:|---:|---:|---:|---:|
| USMV 100% – phương án chính sách 22/10 | 7.14% | 12.84% | 3.84% | −19.06% | 11.15% |
| VTI 100% – benchmark, phương án bác có cơ sở | 8.45% | 16.31% | 3.13% | −24.82% | 22.22% |
| 50% USMV / 50% VTI – điểm trung gian dễ thực thi | 7.79% | 14.24% | 3.74% | −21.09% | 16.69% |
| 1/N mười ứng viên – đối chứng đơn giản | 7.80% | 14.76% | 3.44% | −17.51% | 18.93% |
| Historical Max Sharpe – đúng đề xuất của Eta | 7.16% | 14.93% | 2.71% | −18.63% | 15.88% |
| Sample GMV – sàn biến động trong mẫu | 6.49% | 11.91% | 3.65% | −15.12% | 7.25% |
| CAPM Max Sharpe – phần bù kỳ vọng / σ | 8.46% | 16.35% | 3.11% | −24.87% | 22.40% |
| Sample Max Utility A=4 – đối thủ toán học của USMV | 7.19% | 12.70% | **3.96%** | −17.74% | 12.76% |
| Single-index Max Utility A=4 – đổi mô hình rủi ro | 6.76% | 12.11% | 3.83% | −16.20% | 9.83% |

Danh mục Sample Max Utility A=4 phân bổ **46.18% USMV, 17.89% VTI, 11.62% PG, 7.46% JNJ, 7.45% NEE, 3.52% JPM, 2.96% XOM, 2.92% MSFT** (AAPL/CAT bằng 0). Nó hơn USMV **0.119 điểm phần trăm utility** trong mô hình sample. Tuy nhiên nếu chỉ thay cửa sổ 96 tháng bằng 60 tháng, danh mục tối ưu A=4 thay **34.76% vốn theo một chiều**; đó là dấu hiệu độ nhạy ước lượng, không phải bằng chứng danh mục 96 tháng sẽ sai. USMV giữ vai trò lựa chọn chính sách dễ giải thích, thanh khoản và không đặt cược vào alpha từng mã. Quyết định này có giá: VTI vượt USMV trong 2023–2025. Cần trình trustees cả kết quả bất lợi đó. Nếu nhóm muốn chuyển sang danh mục nhiều mã trước hạn 22/10, phải thay rõ record, tái lập lợi ích sau phí và kiểm tra lại nguồn cùng phương pháp; không lặng lẽ đổi sau khi thấy giai đoạn 2023–2025.

Eta đúng ở việc khóa nghĩa vụ bằng trái phiếu. Nhưng *historical* max Sharpe dồn khoảng 33.2% vào MSFT và 41.3% vào NEE; Sharpe quá khứ không biến thành kỳ vọng chắc chắn. Danh mục này có 2023–25 CAGR 15.88%, cao hơn USMV, song drawdown −13.90% (USMV −5.66%) và utility A4 theo forecast 2022 thấp hơn. Vì vậy không được viết rằng Eta “thua” mọi tiêu chí; kết luận đúng là **phương pháp chọn bằng Sharpe lịch sử không đủ để xác định khẩu vị rủi ro và nghĩa vụ của Kappa**. Theta đúng khi dùng FF3 để giải thích exposure; 5/39 alpha trong Expanded có p<0.05 đơn lẻ, nhưng không có mã nào qua hiệu chỉnh 39 phép thử ở 5%, nên không đủ bằng chứng để đưa alpha dương vào dự báo 2023–2030.

**Vai trò của từng loại ứng viên:** tám cổ phiếu là bộ mẫu để kiểm sector, CAPM/FF3 và khả năng đa dạng hóa; không phải danh sách bắt buộc mua. AAPL/MSFT đại diện tăng trưởng công nghệ; JPM tài chính; JNJ y tế; PG tiêu dùng thiết yếu; XOM năng lượng; CAT công nghiệp; NEE tiện ích. USMV là exposure cổ phiếu Mỹ thiên về rủi ro thấp; VTI là exposure thị trường rộng. Đây là *giả thuyết vai trò tại 2022*, không chứng minh cổ phiếu nào sẽ thắng. Không dùng alpha lịch sử làm phần bù lợi suất dự báo khi chưa có lý do để tin nó bền vững.

## 3. Đọc stress test, trigger và quyền đổi quyết định

Ví dụ cơ học: nếu growth sleeve giảm ngay sau khởi tạo, giá trị toàn quỹ giảm ít hơn vì trái phiếu nghĩa vụ được giữ để trả đúng hạn. Đây là đánh dấu giá trị trong kịch bản, không phải dự báo xác suất hay mức lỗ tối đa. Giả sử giá trị trái phiếu không đổi ở thời điểm minh họa và cash coupon vẫn 0%, ta có:

| Growth giảm | Mất USD growth | Tương đương % vốn USD 12m ban đầu | CAGR growth mới cần cho mục tiêu CPI 2.5%* | Hành động |
|---:|---:|---:|---:|---|
| 10% | 634,635 | 5.29% | 6.23% | Kiểm dữ liệu, nghĩa vụ, thanh khoản và stress; chưa tự bán. |
| 15% | 951,953 | 7.93% | 6.99% | Ủy ban họp, quyết định giữ, tái cân bằng theo rule, hoặc đề nghị đổi policy. |
| 20% | 1,269,270 | 10.58% | 7.80% | Báo trustees khẩn, dừng tăng rủi ro tùy ý, không mặc định bán ở đáy. |
| 30% | 1,903,905 | 15.87% | 9.62% | Kịch bản sốc cho kiểm tra tính khả thi và nguyên tắc khóa goal khi lên giá. |

`*` Minh họa sốc tức thì tại đầu 2023 rồi tính lại 8 năm; không thể diễn giải cùng con số cho cú sốc xảy ra ở 2026 hay 2028. Drawdown được đo bằng chuỗi *unitized total-return* của growth sleeve từ đỉnh gần nhất; bỏ ảnh hưởng tiền chuyển vào/ra, kể cả coupon sweep. Mốc 10/15/20 là tín hiệu quản trị đã thống nhất, không là giới hạn thua lỗ được bảo hiểm. Nghĩa vụ 2024/2027 có kiểm tra độ phủ riêng ở mọi mức.

**Upside:** không bán chỉ vì lời x%. Trong đợt xem xét hằng năm, định giá lại nghĩa vụ và mục tiêu thực, lấy giá có thể giao dịch của công cụ hợp lệ, rồi tính liệu sau sốc growth −30% còn đủ để khóa *phần tối thiểu* của goal hay không. Nếu có, trình trustees bảo vệ phần tối thiểu đó; phần vượt tiếp tục theo growth policy. Không tự thêm mục tiêu chi thường niên. Phải ghi ngày quyết định và không viết lại backtest đã đóng băng.

**Một ngưỡng đảo chiều định lượng:** chỉ trong cặp USMV/VTI với CAPM và sample variance 2015–22, khi A giảm dưới khoảng **2.58**, VTI có utility cao hơn USMV; nếu A=4 cố định thì ERP giả định phải tăng từ 4.5% lên khoảng **6.98%** để VTI vượt. Đây là ngưỡng *xem xét lại* cặp ETF, không tự động giao dịch, và không áp cho danh mục nhiều mã hoặc mandate mới. Nếu lịch/số tiền nghĩa vụ thay đổi, bước đầu tiên phải tính lại trái phiếu và vốn dư; không được chữa hụt funding bằng cách tăng beta growth. Đề revised mandate thực tế chưa được phát hành tại ngày 21/10/2026, nên chưa thể tuyên bố phản ứng số cuối cùng.

## 4. Kiểm toán ba workbook và nguồn dữ liệu

### Đã kiểm được

1. **Role B gốc:** `reference/BFIN_Part_B_original.xlsx`, các ô `Bond_Assumptions!B18:B23` tái lập đúng số trái phiếu và chi phí quote. Nó trình vốn dư **trước phí**; cần dùng budget sau phí ở quyết định Kappa. Đầu ra kiểm: `outputs/role_b_audit/role_b_independent_audit.json`.
2. **Role C gốc:** `reference/role_c/BFIN_Part_C_original.xlsx` có nhiều universe không thống nhất, tab tối ưu trống và không kèm raw files. Đầu ra kiểm: `outputs/role_c_audit/role_c_independent_audit.json`.
3. **Role C Expanded:** 39 asset series x 133 giá tháng; 96 lợi suất train và 36 lợi suất eval có thể tính lại từ các ô giá. Bốn cột FF3, 96 tháng, **khớp chính xác** file processed French đã truy từ ZIP gốc. Tam giác dưới sample covariance 10 mã tại `Optimization!B55:K64` khớp tính lại (sai số lớn nhất 1.11e−16). Ba danh mục 24 tài sản tại `Optimization!D5:F28` cộng đúng 100%; các CAGR/volatility/max DD của ba hàng `Optimization!C34:F36,J34:K36` tái tạo được khi giả định **tái cân bằng hằng tháng và chưa trừ phí**. 39 hồi quy FF3 cũng tính lại được từ các chuỗi giá trong chính workbook (sai số alpha tối đa 1.11e−16). Đầu ra: `outputs/role_c_audit/expanded/expanded_workbook_audit.json`, các CSV so sánh và `outputs/decision_review_20261021/role_c_ff3_independent_recalculation.csv`.
4. **Nguồn Kappa riêng:** `analysis/verify_source_chain.py` kiểm 22 file Yahoo/French saved, SHA-256, 1,320 return và 528 factor values, PASS; `analysis/verify_core_equations.py` kiểm budget, bonds, goal, preference và OOS, PASS. Dữ liệu train/eval chính có bản raw, manifest thời gian UTC, yfinance 1.7.0 và cài đặt tải. Đây là *retrospective vendor history* tải năm 2026, không là tape lưu tại đúng năm 2022.

### Không được coi là đã verify hoặc không khớp policy

| Nơi kiểm | Phát hiện và ảnh hưởng |
|---|---|
| `C4_source record!D3:F42,M3:N42`, `Raw_Adjusted_Prices!B2:AN3` | Link Yahoo/Digrin/SEC chung không phải bản tải gốc; chưa có raw response, timestamp, settings, phiên bản hoặc cách tạo checksum cho 30 mã thêm. Cột N chỉ kiểm số dòng. Không thể chứng nhận nguồn 39 mã theo Exhibit 2. |
| Toàn workbook Expanded | Có **10,292 ô công thức nhưng 0 giá trị cache** trong file đã lưu. Excel có thể tính khi mở, nhưng chữ “PASS/VERIFIED” chưa là chứng cứ đã chạy lại; file kiểm của chúng tôi tính ngoài Excel. |
| `Raw_Adjusted_Prices!I101:I137` và `Returns_data!I98:I135` | **USMV 2023–25 không khớp raw Yahoo đã lưu.** Tháng 03/2023 Role C cho −0.387%, raw Yahoo cho +3.446%; chênh 3.834 điểm %. Gross CAGR Role C 7.724%, raw Yahoo 11.189%. Trong 8 mã overlap còn lại, sai số return lớn nhất dưới 0.015 điểm %. Do đó OOS của danh mục Role C có USMV không dùng để quyết định trước khi truy lại nguồn và tính lại. |
| `0_Audit_&_Endowment_IPS!B14:B18`, `Optimization!B35`, `Optimization!G34:I38` | File đưa vào spending 4.5–5% rolling NAV, HEPI 2.6% + hurdle 7.7–8.2%, ba tier 35/35/30, 65/35 total-fund stress và λ=3.5. Đề chỉ có hai khoản chi cố định và goal 2030; bộ quy ước hiện tại CPI2.5/HEPI3 stress, A=4, đo 15% chủ yếu ở growth sleeve. Các dòng này là **mandate khác**, không là Kappa đã chốt. |
| `C1&2_eligibility!A1:R45`, `Optimization!D5:F28`, `Optimization!B54:K64` | File dùng 39 candidates và 24 holdings (sáu ETF); Exhibit 1 yêu cầu vũ trụ 8–12 cổ phiếu và 2 ETF. Ma trận sample/SIM in ra chỉ 10 tài sản trong khi danh mục có 24; chưa có đối chiếu 24 mã cùng universe. |
| `Optimization!D5:F28`, `Optimization!B34:B36` | Trọng số nhập cứng, không có công thức/solver hoặc đầu ra code chứng minh chúng giải bài toán Utility λ=2/3.5/6. Nhãn “optimal” chưa có căn cứ. |
| `Optimization!F37:G37` | Đối chứng 1/N 10 mã có max DD in-sample báo −19.42%, nhưng tính độc lập theo monthly-rebalance từ chính giá workbook cho **−17.75%**. CAGR 15.56% và vol 13.49% của hàng này đúng; max DD/65-35 DD cần sửa và ghi cách tính. |
| `Multifactor Regression!D5:J43` | 5/39 alpha có p<0.05 riêng lẻ; 0/39 qua mức Bonferroni 0.05/39. Hồi quy số học đúng nhưng p nhỏ không chứng minh alpha bền vững hoặc forecast alpha dương. Chọn mã sau khi nhìn lịch sử làm bằng chứng càng yếu. |

Giá USMV train trong Expanded và raw Kappa khác mức tuyệt đối do vendor adjustment/chuẩn hóa, nhưng *return* train chênh tối đa dưới 0.0001 điểm phần trăm và không đủ giải thích sai lệch OOS lớn. Cần truy đúng Yahoo response hoặc log nguồn của Role C cho USMV năm 2023–25; không được thay số bằng suy đoán. Với 30 mã mới không có bản raw tương ứng ở gói Kappa, đánh giá hiện tại là **không chứng minh được provenance**, không tuyên bố số giả.

## 5. Thiếu gì theo trang 3 của đề và hạn nộp nào?

**22/10, tối đa hai trang + Python + dated data record:** record đã sửa ở `submission_2026-10-22/deliverables/`; có 10 ứng viên, 96 tháng, VTI benchmark, USD 12m đầy đủ, growth weights, assumptions và rule đánh giá/rebalance. `submission_2026-10-22/analysis/run_initial.py` chạy offline từ raw training; `data/DATA_RECORD.md` và manifest giải thích source. Chưa được tuyên bố là đã nộp.

**29/10, memo tối đa tám trang:** cần trình đủ năm dòng bằng chứng của trang 3: (1) preference A đổi quyết định, funding & real goal; (2) bond yield, spot curve khuyết, duration/convexity so exact repricing dưới parallel và curve-shape shocks; (3) sample/SIM trên cùng 10 candidates, tỷ trọng, forecast inputs, phí và độ nhạy; (4) CAPM vs FF3 cho USMV/growth và ≥2 mã, beta, alpha CI/p, kinh tế của exposures; (5) chiến lược/benchmark đóng băng 2023–25, ngưỡng đảo chiều, kết quả bất lợi. Mỗi bảng/đồ thị cần tên output sinh từ code. Ngoài ra archive cuối cần slide PDF + nguồn chỉnh sửa, 22/10 submission, decision log, statement đóng góp và kiểm độc lập của thành viên, disclosure AI theo quy định môn học. Các phần này **không nên ép vào record hai trang** nhưng phải có trong final package.

## 6. Quy trình để tự kiểm, từng bước

1. **Mở đề:** xem `reference/BFIN-WS2026-Group_Assignment.pdf` trang 1–2 để gạch chân hai khoản chi, tài sản được phép và vũ trụ 8–12+2; trang 3 là checklist evidence cho final; trang 4 định nghĩa rõ mốc 22/10 và 29/10.
2. **Mở record 22/10:** trang 1 kiểm tổng 2,214,672 + 3,429,809 + 6,346,351 + 9,169 ≈ 12m (số trên PDF làm tròn USD); trang 2 kiểm CPI 2.5, HEPI stress 3, A4, signal 10/15/20, ngày cutoff.
3. **Kiểm nguồn:** đọc `submission_2026-10-22/data/DATA_RECORD.md`, `data/raw/retrieval_manifest.jsonl`; đối chiếu ticker, ngày tải UTC, `auto_adjust=False`, `actions=True`, mã băm và raw CSV/ZIP. Chạy `python analysis/verify_source_chain.py` ở project root để tính lại giá cuối tháng, 1,320 returns và 528 factors. Với FF3, 1.25 trong file nguồn là **1.25% = 0.0125** trong mô hình.
4. **Kiểm Excel Expanded:** không sửa file gốc. Chạy Python bundled `analysis/audit_expanded_c.py`; mở `outputs/role_c_audit/expanded/evaluation_source_comparison.csv`, lọc USMV. Tại `Raw_Adjusted_Prices!I104` (03/2023; xác định bằng cột ngày) đối chiếu file raw saved; kiểm `C4_source record!N3:N42` là công thức COUNT chứ không là nguồn.
5. **Kiểm portfolio:** chạy `.venv/Scripts/python.exe analysis/compare_growth_options_20261021.py`; mở hai CSV `growth_candidate_comparison` và `growth_candidate_weights`. Đọc *cột U(A=4)* chỉ như điểm mô hình tại 2022; *cột OOS* là kiểm nghiệm riêng. Đổi A, ERP hoặc Σ chỉ trong phiên bản phân tích có ngày, không sửa `policy/frozen_policy.json` để hợp thức hóa kết quả tương lai.
6. **Người kiểm độc lập:** một thành viên khác kiểm lại ít nhất một giá→return tháng, một hàng FF3 sau chia 100, tổng USD 12m, một dòng weights=100% và một max DD; ghi tên, ngày, file/cell và kết luận. Đây là kiểm số và nguồn, không đơn thuần đọc lại phần giải thích.

**Giới hạn quan trọng:** `yfinance`/Yahoo là nguồn mà đề yêu cầu, không là dữ liệu điểm thời gian hoàn hảo; French có thể sửa lịch sử phương pháp; 2023–25 không chứng minh goal 2030. “No drawdown approaching 15%” không thể hứa bằng stop order cổ phiếu. Quyết định sửa lại sau revised mandate phải có bản before/after, số và hiệu lực mới.
