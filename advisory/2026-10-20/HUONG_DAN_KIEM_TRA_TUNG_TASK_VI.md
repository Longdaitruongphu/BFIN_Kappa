# Hướng dẫn tự kiểm từng phần bài Kappa (bản nội bộ, 20/10/2026)

**Đọc theo thứ tự này:** đề gốc `reference/BFIN-WS2026-Group_Assignment.pdf` → quyết định đã khóa `policy/frozen_policy.json` → dữ liệu gốc `data/raw/` → phép tính `analysis/` → kết quả `outputs/tables/` → bài trình bày `deliverables/`. Không sửa bản gốc `reference/role_c/BFIN_Part_C_original.xlsx`. Báo cáo đối chiếu tiếng Anh là `advisory/2026-10-20/INDEPENDENT_ASSIGNMENT_AND_ROLE_C_AUDIT.md`.

## 0. Hiểu đề trước khi bấm máy

Mốc ra quyết định là **31/12/2022**. Quỹ có **12 triệu USD tiền mặt**. Hai hóa đơn bắt buộc là **2,4 triệu cuối 2024** và **3,6 triệu cuối 2027**, cố định bằng USD danh nghĩa. Sau khi trả hai hóa đơn, quỹ *muốn* còn sức mua bằng **8 triệu USD tại cuối 2022** vào cuối 2030; đây là mục tiêu, không phải bảo đảm. “Không thoải mái với lỗ gần 15%” chưa nói lỗ từ đỉnh đến đáy, trong một năm hay trên vốn đầu kỳ, nên nhóm phải tự định nghĩa, kiểm stress và nói rõ giới hạn. Trang 2 giới hạn loại tài sản, buộc 8–12 cổ phiếu Mỹ ít nhất 4 ngành cùng 2 ETF cổ phiếu Mỹ khác chiến lược. Trang 3 buộc mọi phần tính toán và trang 4 buộc hồ sơ nộp, đóng góp thật, đánh giá mandate sửa đổi.

Một cách hình dung: trước tiên bỏ riêng tiền để trả hai hóa đơn đúng hạn; phần còn lại mới đi “trồng cây” đến năm 2030. Vốn phải trả hóa đơn là 6/12 = **50%** vốn ban đầu. Nếu *chỉ chia đều để giải thích* cho năm năm 2023–2027 thì là 1,2 triệu USD/năm = **10% vốn đầu kỳ/năm**; thực tế quỹ chỉ trả đúng hai mốc, không phải 1,2 triệu mỗi năm.

## 1. Kiểm bộ quy ước, tránh trộn các loại lãi suất

Mở `analysis/config.json`. Bảng sau là quy ước dùng xuyên suốt:

| Thời gian / chỉ số | Dùng số nào | Dùng để làm gì | Tuyệt đối không hiểu thành |
| --- | --- | --- | --- |
| 2015–2022, huấn luyện | Lợi suất cổ phiếu/ETF theo từng tháng và **RF theo từng tháng** trong FF3 | Ước lượng beta, phương sai, Sharpe lịch sử, hồi quy CAPM/FF3; 96 tháng kết thúc 12/2022 | Dùng lãi suất dự báo 4% để thay cho mọi RF lịch sử |
| 2023–2025, kiểm nghiệm | Lợi suất và **RF FF3 theo đúng từng tháng 2023–2025** | Đánh giá danh mục và VTI đã khóa; 36 tháng, không chọn lại chứng khoán từ kết quả này | Thành tích 2030 hoặc dữ liệu “biết trước” ở 2022 |
| Quyết định/dự phóng từ cuối 2022 đến 2030 | `inflation=2.5%`/năm trong kịch bản cơ sở; stress 2–5% | Quy đổi 8 triệu sức mua 2022 thành mục tiêu USD 2030 và đổi tài sản tương lai về sức mua 2022 | Lãi phi rủi ro, lãi được bảo đảm, hay chiết khấu hai hóa đơn danh nghĩa |
| Quyết định/dự phóng | `forecast_rf=4%`/năm và `forecast_erp=4.5%`/năm | Đầu vào *kỳ vọng* `E[R_i]=4%+beta_i×4.5%`, tính certainty equivalent và các ngưỡng đảo chiều | Lãi tiền mặt chắc chắn thu được trong 8 năm |
| Dòng tiền coupon dư | 0% tái đầu tư cơ sở | Giữ thận trọng: 486.956,52 USD vào 2030 | Lãi phi rủi ro 4% tự động cộng vào coupon |

Lý do chọn 2,5%: đây là *giả định quản trị tại cuối 2022*, cao hơn lạm phát PCE dài hạn 2% trong dự báo Fed tháng 12/2022 và sát dự báo 2024; chưa phải ước lượng chi phí giáo dục chính xác. Lý do chọn 4%: mốc kế hoạch xấp xỉ lợi suất trái phiếu trong đề tại cuối 2022. Thay đổi cả hai phải ghi lý do, ngày biết tin và bảng độ nhạy; không âm thầm lấy trung bình RF hoặc CPI của 2023–2025 để biện minh cho quyết định năm 2022. Xem lời giải thích và nguồn ở `deliverables/Kappa_Committee_Memo_Editable.md`, mục Mandate / Portfolio.

## 2. Kiểm tiền trái phiếu và nghĩa vụ (task funding + bond)

Mở `outputs/tables/funding_summary.json`, `initial_allocation.csv`, `funding_cashflows.csv`.

1. Beta là trái phiếu zero-coupon 2 năm, giá 922,78 USD trên 1.000 face. Mua **2.400** đơn vị: `2.400 × 922,78 = 2.214.672 USD`. Đến 31/12/2024 nhận `2.400 × 1.000 = 2,4 triệu`, trả ngay hóa đơn.
2. Delta coupon 3,5% nên năm 2027 mỗi đơn vị trả `1.000 + 35 = 1.035 USD`. Cần `3.600.000/1.035 = 3.478,26086957` đơn vị (đề cho phép phần lẻ), giá mua `×986,07 = 3.429.808,70 USD`. Coupon 2023–2026 là `3.478,26086957×35 = 121.739,13 USD/năm`; bốn khoản = **486.956,52 USD** dư.
3. Cộng Beta + Delta + USMV + phí = **12 triệu USD**. Cột `cumulative_cash_zero_reinvestment` không được âm. Đừng chiết khấu hai khoản phải trả bằng inflation: đề nói nghĩa vụ USD danh nghĩa cố định.
4. Mở `bond_metrics.csv` kiểm năm, coupon, giá của **cả năm** trái phiếu Alpha–Epsilon so với trang 2 đề. Kiểm YTM, duration, convexity. `bond_curve.csv` nói rõ đường cong suy ra chưa đầy đủ; `bond_stress.csv` đặt giá tính lại chính xác cạnh giá xấp xỉ duration/convexity ở +/-100bp, +200bp và đổi độ dốc. Giá shock là đánh dấu thị trường trước đáo hạn; bond giữ đến hạn vẫn trả dòng tiền đề bài, theo giả định không vỡ nợ.

Đầu ra để giải thích cho giảng viên: trang 1–3 memo, `analysis/bonds.py` và 5 file CSV trên. Người kiểm độc lập nên tự bấm máy tính công thức Beta, Delta và ít nhất một giá bond từ dòng tiền, rồi ghi tên/ngày, không chỉ nhìn ô `passed`.

## 3. Kiểm mục tiêu 2030 và khả năng chịu rủi ro

Từ `goal_sensitivity.csv`, tại inflation 2,5% và coupon cash 0%: `8.000.000×1,025^8 = 9.747.223,18 USD` danh nghĩa; sức mua 2022 của USD 2030 là `USD_2030/1,025^8`. Với USMV đầu kỳ 6.346.350,71 USD, giải phương trình `6.346.350,71×(1+g)^8 + 486.956,52 = 9.747.223,18`; được **g=4,8365%/năm CAGR**. Điều này không có nghĩa quỹ chỉ cần sinh lời 4,84% trên *toàn bộ* 12 triệu: nửa vốn đã gắn với hai nghĩa vụ.

Mở `risk_preference.csv`: `CE = lợi suất kỳ vọng số học − A×phương sai năm/2`. Chạy mắt các hàng `A=2,4,8`; `A=4` chọn USMV, nhưng `A<2,5803` sẽ nghiêng sang VTI (với cùng inputs và hai ETF này). `decision_summary.json` chứa ngưỡng ERP 6,9759%. Đây là tính *ưu tiên* của hội đồng, không phải “risk aversion thật” đã đo từ đề. Mở `whole_fund_stress.csv`: shock cổ phiếu -30% cùng +100bp tạo lỗ 17,53% của **12 triệu vốn đầu kỳ**, dù hai hóa đơn vẫn có dòng tiền trả. Vì thế 15% là ngưỡng gọi họp / xem lại chính sách, không phải stop-loss cứng được bảo đảm.

Mở `mission_scenarios.csv` và `mission_simulation.csv`: 20.000 đường mô phỏng khối tháng 12, cơ sở USMV 68,48% đường đạt mục tiêu, stress inflation 4% chỉ 48,05%. Gọi đây là xác suất *trong mô hình có điều kiện*, không phải xác suất thực được hiệu chuẩn. So sánh phương án toàn trái phiếu ở `all_bond_summary.json`: chắc dòng tiền hơn nhưng thiếu sức mua mục tiêu ở 2,5% inflation.

## 4. Kiểm Yahoo có thật, không cộng dividend hai lần

Mở `analysis/retrieve_data.py` và `data/raw/retrieval_manifest.jsonl`. Dữ liệu đã lưu từ Yahoo qua Python `yfinance.Ticker.history`, `interval=1d`, `auto_adjust=False`, `back_adjust=False`, `actions=True`, `repair=False`, `keepna=True`. Chương trình lấy từ 12/2014 để có mẫu số tính lợi suất **tháng 1/2015**, nhưng giai đoạn ước lượng chỉ từ 1/2015. Dữ liệu đánh giá được tải riêng. Mỗi tải thành công ghi URL, timestamp, version, file, số dòng và SHA-256. Dữ liệu raw nằm ở `data/raw/train/*_daily.csv` và `data/raw/eval/*_daily.csv`, kèm `.pkl` gốc.

Cách kiểm bằng tay cho MSFT: ở `data/processed/train_month_end_adjusted_prices.csv`, giá `Adj Close` cuối 2/2020 = **153,273239135742**, cuối 3/2020 = **149,205139160156**. Tính `149,205139160156/153,273239135742−1 = −0,0265414889` (−2,65415%). Tìm cùng ô ở `train_monthly_returns.csv`. `Adj Close` đã phản ánh điều chỉnh corporate action của Yahoo; `train_corporate_actions.csv` chỉ để kiểm tra, **không cộng dividend thêm lần hai**. Dữ liệu Yahoo được tải năm 2026, có thể là lịch sử đã được vendor sửa lại; đây là bài retrospective, không phải backtest live thật vào năm 2022.

Để kiểm máy độc lập từ thư mục gốc, chạy PowerShell:

```powershell
python analysis\audit_inventory.py --verify
.\.venv\Scripts\python.exe analysis\verify_source_chain.py
.\.venv\Scripts\python.exe analysis\verify_core_equations.py
.\.venv\Scripts\python.exe analysis\verify_factor_portfolio.py
.\.venv\Scripts\python.exe analysis\rebuild.py
```

Lệnh đầu kiểm hash trạng thái folder **trước khi dựng lại**. Lệnh thứ hai đọc raw: hash 22 file thị trường/FF3 cùng 4 tài liệu phụ trợ, tự gom ngày giao dịch cuối mỗi tháng, tính lại 1.320 lợi suất và 528 factor. Lệnh thứ ba tự tính lại năm giá bond, tổng vốn, nghĩa vụ, mục tiêu 2030, certainty equivalent và performance/Sharpe 36 tháng. Lệnh thứ tư kiểm độc lập 10 hồi quy CAPM/FF3, hai ma trận covariance và 11 hàng danh mục. Lệnh cuối tái tạo toàn bộ output mà **không truy cập internet**, ghi 28 phép kiểm trong `outputs/tables/reproduction_checks.csv`. Một lần rebuild mới có thể đổi hash PDF do metadata và log chạy; manifest là ảnh chụp có ngày, muốn lưu trạng thái mới thì dùng `python analysis/audit_inventory.py --create` sau khi kiểm kết quả. Nếu hash raw, tháng hoặc giá trị số không khớp, dừng và điều tra, không điền số giả để làm cho bảng đẹp. *Không chạy `retrieve_data.py` lần nữa chỉ để “refresh” bài gốc*: làm vậy đổi vintage và cần hồ sơ/kịch bản mới.

## 5. Kiểm FF3 và đơn vị phần trăm

File gốc là `data/raw/train/F-F_Research_Data_Factors_CSV.zip` (và bản `eval`), tải từ Kenneth French; cùng SHA-256 `593f4fbef03181bc0b22ff6292f217689dd1fb79355049ca905d95b262040a66`. Mở ZIP và xem hàng tháng dạng `YYYYMM, Mkt-RF, SMB, HML, RF`. Chẳng hạn FF3 tháng 1/2015 có `Mkt-RF = -3.10` **đơn vị phần trăm**, khi đưa vào model thành `-0.031` **đơn vị thập phân**; SMB = `-0.0061`, HML = `-0.0348`, RF = `0`. `analysis/analyze.py:load_factors` chia **cả bốn cột** cho 100 và gắn cùng tháng với lợi suất Yahoo. `data/processed/train_factors.csv` và `eval_factors.csv` là phần cắt cho hai giai đoạn. Vì cùng một ZIP full-history được tải trong cả hai pha, SHA giống nhau là hợp lý; không phải hai quan sát độc lập. Kiểm định nhân tố dùng `R_asset,t−RF_t`, rồi hồi quy lên `Mkt-RF`, SMB, HML; không trừ RF lần nữa khỏi factor market.

## 6. Kiểm chọn cổ phiếu, ETF, mô hình và evaluation

Đề yêu cầu *lập universe* chứ không bắt mua hết. `analysis/config.json` liệt kê 8 stocks AAPL, MSFT, JPM, JNJ, PG, XOM, CAT, NEE, trải 7 ngành; VTI (thị trường Mỹ rộng) và USMV (cổ phiếu Mỹ thiên biến động thấp). `data/raw/supporting/eligibility_checks.json` lưu ngày của tài liệu trước 2023; một số SEC file không lưu toàn văn do HTTP 403, đã ghi thật trong `source_register.json`. Rủi ro chọn trước các mã hiện còn sống vẫn phải nói ra. Mở `expected_return_inputs.csv` để xem beta và forecast `4%+beta×4,5%` của từng mã. Mở `portfolio_candidates.csv`, hai hàng `Sample_A4` và `Single_index_A4`: chung universe, giới hạn tối đa 10% một cổ phiếu và 30% tổng cổ phiếu, nhưng covariance khác nhau. Đó là phần đề yêu cầu; sheet `Optimization` rỗng trong Role C không thay thế được.

`factor_regressions.csv` có CAPM và FF3 cho USMV, VTI, AAPL, MSFT, JPM; `alpha_low`/`alpha_high` là khoảng 95%, không nên gọi alpha tương lai được bảo đảm chỉ vì một p-value nhỏ. Mặc định forecast alpha=0. `evaluation_performance.csv` ghi **36 tháng** 1/2023–12/2025. USMV tăng lũy kế **37,33%**, Sharpe **0,66**; VTI **82,56%**, Sharpe **1,30** sau giả định phí vào vị thế. USMV có volatility và drawdown nhỏ hơn. Kiểm `evaluation_summary.json`: SHA policy trước/sau giống nhau. Nếu giảng viên hỏi “tại sao Sharpe chênh lệch”, trả lời: Sharpe = trung bình lợi suất vượt RF hằng tháng / độ lệch chuẩn của lợi suất vượt RF × căn 12; trong ba năm này lợi suất vượt RF của VTI cao lên nhiều hơn mức tăng volatility. Xem bảng năm và đường tài sản ở `evaluation_calendar_years.csv`, `evaluation_wealth.csv`; không đổi lựa chọn ở 2022 sau khi xem 2023–25.

## 7. Đối chiếu workbook Role C theo thứ tự dễ hiểu

Mở bản sao chỉ đọc `reference/role_c/BFIN_Part_C_original.xlsx`:

1. `Returns_data` có 10 mã nhưng khác frozen universe; 8 mã trùng với dự án cho số gần khớp (làm tròn). `Stock Returns` lại dùng thêm một danh sách 10 mã khác, 95 tháng. Hỏi Role C phiên bản nào là cuối cùng và tại sao lại thay universe; không tự nhập các hồi quy của danh sách sau vào memo chính.
2. `Fama-French Factors` khớp đúng 96 tháng project. `Multifactor Regression` tính lại được từ bảng 95 tháng, nên **không kết luận dữ liệu giả**. Nhưng không hồi quy USMV là tăng trưởng đề xuất, không cho khoảng tin cậy alpha.
3. `C3_return check!G27:H36`: ở row 27 hai giá đã làm tròn tạo lợi suất **−2,64892%**, còn bảng returns ghi khoảng **−2,65413%**; hiệu khoảng 0,00521 điểm phần trăm, nhưng cột chênh lệch ghi 0 và báo `PASSED`. Rows 28–36 chưa có giá, ra `#DIV/0!`, vẫn báo `PASSED`. Đây là lỗi quy trình kiểm, cần làm lại từ raw với công thức và ngưỡng sai số thực.
4. `C4_source record`: đường dẫn `raw/yahoo_monthly_raw.csv` với hash được ghi **không có file đính kèm để băm lại**; hai nguồn tổng hợp cũng thiếu hash. Trước khi coi Role C là lần tải độc lập, yêu cầu file raw đúng hash, code tải, settings, nhật ký lỗi và người xác nhận.
5. `C1&2_eligibility` thiếu tệp minh chứng và người kiểm trong các ô M:N; `Optimization` trống. Lấy phần đã chứng minh trong project chính, không dùng nhãn `PASSED` của workbook để thay bằng chứng.

Phép so sánh định lượng Role C nằm tại `outputs/role_c_audit/role_c_independent_audit.json`; trên máy này chạy lại bằng `python analysis\audit_role_c.py`. Script này cần `openpyxl` (Python hệ thống hiện có 3.1.5; `.venv` phân tích gốc chưa cài), `numpy` và `pandas`. Trên máy mới, cài các thư viện đó vào môi trường audit trước khi chạy. Sau đó một **thành viên khác** phải tự mở nguồn gốc, tính lại mẫu riêng, ghi ngày/cách làm/kết luận/điểm chưa đồng ý. Đây mới là “kiểm độc lập” theo nghĩa đóng góp nhóm, không phải AI chạy lại cùng code.

## 8. Đóng gói/nộp bài: điểm nào chưa thể xác nhận hôm nay

`deliverables/Kappa_Committee_Memo.pdf` là tám trang nội dung + một trang tài liệu; có slide PDF và PPTX chỉnh sửa được. `EVIDENCE_MAP.md` nối từng trang tới bảng. Đề còn yêu cầu **bản nộp ban đầu thực tế** trước 22/10 16:00, **mandate sửa đổi** công bố 23/10 16:00 và phân tích chênh lệch, nộp cuối 29/10 16:00, statement đóng góp và critique thật của từng bạn, khai báo AI theo nội quy khóa học. Tệp chuẩn bị sẵn không chứng minh đã upload. As of 20/10, mandate sửa đổi chưa thể tính; khi có, giữ nguyên bản frozen và theo `MANDATE_REVISION.md`. Mọi file đem nộp phải bằng tiếng Anh; tài liệu tiếng Việt này chỉ để bạn kiểm và phân việc.
