**Rà soát gợi ý IPS và câu hỏi cần chốt cùng trustees**

Ngày 21/10/2026. Bản này dùng để tư duy và hoàn thiện đề xuất cho initial record; chưa phải mandate thực của thầy. Ngày case giữ 31/12/2022, không dùng thông tin sau cutoff để dựng lại lựa chọn gốc.

**Quy tắc 10/15/20 bạn đã duyệt để đưa vào IPS đề xuất**

Thước đo chính là drawdown của growth sleeve, tính trên giá trị một đơn vị đã gồm tổng lợi suất, so với đỉnh lịch sử. Tiền mặt thu được khi bán tài sản trong growth sleeve vẫn thuộc sleeve; tiền nộp/rút ngoài được xử lý như thay đổi số đơn vị. Không đặt lại đỉnh vì chuyển từ USMV sang tài sản khác.

| Tín hiệu | Hành động đã chọn để ghi vào IPS đề xuất | Giao dịch |
|---|---|---|
| 10% đến dưới 15% | Trong 2 ngày làm việc kiểm dữ liệu, cổ tức, cash flow, độ phủ nghĩa vụ, stress và mục tiêu; báo Investment Committee | Không tự động giao dịch |
| 15% đến dưới 20% | Investment Committee họp trong 5 ngày làm việc; lập biên bản giữ nguyên, thực hiện một quy tắc rebalance đã duyệt riêng, hoặc kiến nghị trustees đổi policy | Chạm mốc buộc review, không buộc bán |
| Từ 20% | Báo trustees cùng ngày hoặc ngày làm việc kế tiếp; tạm ngưng các quyết định tùy nghi làm tăng rủi ro trong lúc review | Không mặc định bán hết growth assets |
| Rủi ro thiếu bất kỳ khoản bắt buộc nào | Escalate ngay, dù sleeve chưa lỗ 10%; lập dòng tiền và phương án bù đúng hạn | Xử lý nghĩa vụ trước |

Nếu giá gap từ dưới 10% xuống quá 20%, áp dụng cấp cao nhất đã chạm. Cả 10/15/20 là **mốc trách nhiệm và hành động quản trị**, không phải bảo đảm giới hạn kinh tế của khoản lỗ. Dữ liệu lịch sử 2015–2025 theo tháng chỉ cho phép kiểm tra drawdown cuối tháng; không tuyên bố backtest đầy đủ trigger hằng ngày.

Đây là rule người dùng đã duyệt **để đưa vào policy nhóm đề xuất**; chưa phải trustees phê duyệt và chưa sửa `policy/frozen_policy.json`. Phiên bản lưu trong `policy/IPS_addendum_selected_drawdown_rules_2026-10-21.json`.

**Rà soát đề xuất lạm phát và TIPS**

Ngày giao dịch cuối năm 2022 là 30/12/2022 vì 31/12/2022 là thứ Bảy. Treasury công bố par yield danh nghĩa 10 năm 3.88% và par real yield TIPS 10 năm 1.58%; chênh lệch xấp xỉ 2.30%. Ở nút 7 năm, hai mức là 3.96% và 1.61%; nội suy đơn giản tới 8 năm cho chênh lệch quanh 2.33%. Đây là **chênh lệch par-yield xấp xỉ**, chưa phải breakeven zero-coupon chính xác 8 năm. Treasury nói các mức này là par yield nội suy từ chỉ báo bid-side. Breakeven có thêm inflation-risk premium và liquidity effects, nên không gọi nó là kỳ vọng CPI thuần hay lợi suất chắc chắn. [Treasury danh nghĩa](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202212&type=daily_treasury_yield_curve), [Treasury TIPS thực](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?field_tdr_date_value_month=202212&type=daily_treasury_real_yield_curve), [Federal Reserve study về inflation compensation](https://www.federalreserve.gov/pubs/feds/2008/200805/200805pap.pdf).

HEPI là chỉ số chi phí hoạt động cho trường cao đẳng/đại học theo năm tài khóa tháng 7–tháng 6. Bảng Commonfund có dữ liệu FY2015–FY2022: trung bình HEPI khoảng 2.74%, CPI khoảng 2.34%, chênh lệch **0.40 điểm phần trăm/năm** trong đúng cửa sổ tám năm này. Nhưng ở FY2022, HEPI 5.2% thấp hơn CPI 7.2% tới 2 điểm %. Commonfund báo chênh lệch trung bình 60 năm khoảng +0.8 điểm. Vì vậy “HEPI cộng đều 0.3–0.5%” không phải quy luật hằng năm. HEPI đo chi phí vận hành của đại học; nó có thể không khớp trực tiếp chi phí học bổng hoặc learning centre của Kappa. [Commonfund 2022 HEPI report, Table A](https://www.commonfund.org/hubfs/00%20Commonfund.org/04%20Institute/HEPI/Reports/2022-Commonfund-Higher-Education-Price-Index.pdf), [Commonfund methodology and purpose](https://www.commonfund.org/blog/hepi-defines-college-inflation).

Đề ghi mục tiêu bằng sức mua USD tháng 12/2022 nhưng không chỉ rõ chỉ số giảm phát. Quy ước hiện tại là CPI 2.5% base và thử 2–5%. Chọn HEPI làm thước đo mục tiêu sẽ tạo một câu hỏi kinh tế thật sự, không chỉ thay 2.5% thành 3%: phải xác định chi phí giáo dục nào quỹ đang cố duy trì và thống nhất chỉ số base-year/terminal-year. Có thể giữ CPI làm mục tiêu danh nghĩa so sánh với tài sản tài chính và dùng HEPI 3% làm stress mission-cost, hoặc trustees có thể xác định chính HEPI là thước đo purchasing power.

**Rà soát cash-flow dedication và tiền coupon**

Delta face $3,478,260.87, coupon mỗi năm **$121,739.13**, final principal + coupon $3.6m năm 2027. Gợi ý của bạn dùng **một** coupon Delta cho khoản năm 2024, nên Beta face còn $2,278,260.87; Beta cost theo quote $922.78 là $2,102,333.57. Bond cost là $5,532,142.26, tiết kiệm $112,338.43 so với Beta face đủ $2.4m. Cách này chính xác theo dòng tiền nếu coupon 2024 được nhận đúng ngày trả.

Nhưng code cũ `analysis/bonds.py` có phương án khác: trừ **hai** coupon khỏi Beta obligation, tức Beta face $2,156,521.74, vì coupon Delta 2023 có thể được giữ riêng và dùng năm 2024 cùng coupon 2024. Phương án này dùng thêm một nguồn coupon, tiết kiệm thêm khoảng $112,338 giá Beta so với phương án một coupon; tiền coupon dư tới 2030 còn hai coupon thay vì ba. Hai phương án đều khớp dòng tiền trong quy ước cùng ngày của case. Chọn coupon 2023 để dành trước giúp không phụ thuộc vào nhận và chuyển coupon cùng ngày 2024.

Phí cũng phải nhất quán. Con số $6,467,857.74 trong gợi ý là `$12m - bond cost`, nên chưa trừ phí trái phiếu hay cổ phiếu. Với **một** coupon dùng trả 2024, giả định hiện hành 5bp trái phiếu và 10bp cổ phiếu cho vốn growth sleeve đầu kỳ khoảng **$6,458,633.03**. Nếu ba coupon dư giữ ở cash 0%, CAGR sleeve cần khoảng **4.78%**. Nếu coupon 2023, 2025, 2026 được đầu tư vào cùng sleeve theo đúng ngày nhận và tăng cùng CAGR với sleeve, hurdle khoảng **4.64%**. Đây là hai tính toán khác nhau; coupon đầu tư vào cổ phiếu sẽ có rủi ro giá. Mô hình cơ sở hiện tại giữ coupon cash 0% và không đem chúng đi đầu tư.

Forward rate tính từ curve là một mức implied theo cấu trúc lãi suất, không đảm bảo là lãi suất tái đầu tư thực tế. Phương án 2% là sensitivity lợi suất tiền gửi/trái phiếu ngắn hạn; 0% là stress không nhận lãi. Không gọi hai mức này là “hedged” nếu không mua công cụ khóa được dòng tiền đó.

Nắm trái phiếu default-free tới hạn khóa dòng tiền danh nghĩa của case, nhưng không khóa sức mua nếu CPI/HEPI cao hơn giả định và không xóa biến động mark-to-market nếu phải bán trước hạn. Gọi cách này “cash-flow dedication/hold-to-maturity”; chỉ gọi immunization duration nếu đã khớp độ nhạy lãi suất của tài sản và nghĩa vụ.

**Tách drawdown trigger với VaR**

Bạn đã chọn drawdown high-water growth sleeve cho 15%. Không cần đổi nó thành `VaR95 <=15%`. Với μ=7.14%, σ=12.84% của USMV, giả định chuẩn một năm cho VaR95 xấp xỉ `1.645×12.84% − 7.14% = 13.98%`. Đây là phân vị lợi suất một năm dưới giả định phân phối chuẩn, không phải peak-to-trough drawdown. USMV đã có month-end historical drawdown khoảng −19.06% trong 2015–2022, nên cả hai phép đo có thể cho câu trả lời khác nhau.

Nếu giảng viên thêm VaR, lưu nó như **ràng buộc phụ** và nêu phân phối, horizon, alpha và cập nhật tham số. Không trình bày VaR95 như “maximum loss”. Công thức dấu trong gợi ý thể hiện đúng lower-tail loss khi phân phối chuẩn, nhưng con số vẫn nhạy với giả định chuẩn, covariance và mean estimate.

Các con số `π*=3.65%`, `λ*=6.8`, xác suất dưới 50%, ngưỡng alpha shrinkage γ=0.45, và mục tiêu σ=9.2% chưa được hỗ trợ bởi các đầu vào/mô phỏng đã lưu. Không đưa chúng vào IPS hiện tại. Cần quy định chính xác mục tiêu hàm, ràng buộc, dữ liệu và xác suất nào rồi mới giải lại để tìm threshold. Dữ liệu hiện tại chỉ có FF3; tuyên bố RMW/FF5 và alpha persistence cần tải đúng factor files, thống nhất cutoff và kiểm định riêng. CAPM/FF3 cùng alpha forecast bằng 0 vẫn là baseline đã chốt.

Trong FF3 2015–2022 đã lưu, alpha MSFT là khoảng **12.81%/năm**, khoảng tin cậy 95% là khoảng **4.54–21.08%**, p≈0.0024. Alpha AAPL là khoảng 11.04%, nhưng khoảng tin cậy chứa 0 (p≈0.085); alpha USMV và VTI cũng không khác 0 rõ ràng. Kết quả MSFT thay đổi theo hai nửa cửa sổ: 2015–2018 p≈0.060, 2019–2022 p≈0.0115. Vì vậy không được viết chung rằng “mọi/hầu hết alpha không có ý nghĩa”; cũng không nên gọi hệ số MSFT là alpha bền vững đã được chứng minh. Chưa hiệu chỉnh nhiều mã/cửa sổ, universe được chọn hồi cứu, n=96 tháng và kết quả qua subperiods không đồng nhất. Giữ forecast alpha=0 là lựa chọn thận trọng có lý do, nhưng phải trình bày kết quả dương của MSFT như phản chứng nghiêm túc với Theta. Xem `outputs/tables/factor_regressions.csv` và `alpha_stability.csv`.

Đường cong spot mà bạn tính (`z4=3.85%, z6≈3.833%, z7≈3.867%`) khớp với sensitivity **linear-in-zero-yield** sẵn trong `analysis/bonds.py`. Curve cơ sở của project nội suy log discount factor và cho spot xấp xỉ `3.8377%, 3.8444%, 3.8759%` tại các nút 4/6/7 năm; cả hai khớp giá case ở nút nhưng khác giả định nội suy. Đề để term structure thiếu nên đây là hai giả định hợp lý để trình song song, không khẳng định một curve là duy nhất. Implied forward tính từ curve cũng không phải cam kết coupon sẽ tái đầu tư được đúng mức đó.

Danh sách bổ sung UNH/COST/BRK-B/HON/QUAL/VOO/SPY làm thay đổi candidate universe và/hoặc benchmark đã đóng băng (8 cổ phiếu hiện tại + VTI/USMV). Chưa được dùng cho quyết định gốc: phải cập nhật ngày-dữ-liệu/eligibility theo cutoff, lấy lại raw Yahoo, factor joins, 60/96 tháng chung và chạy lại portfolio với benchmark và policy mới ghi version. Yêu cầu 2015-2022 không thể được “chứng minh không có survivorship bias” chỉ bằng việc chọn mã còn tồn tại tại 2022; phải mô tả tiêu chí chọn và giới hạn suy luận.

**Upside: nguyên tắc đã chọn, thủ tục thực thi cần chốt**

Không dùng mức “tăng 20%” hay một mức return mới để tự động chốt lời. Lợi suất tốt một quý có thể là nhiễu; nếu 100% sleeve vẫn là USMV thì tái cân bằng nội bộ không tồn tại. Phương án IPS gợi ý:

1. Mỗi năm, sau khi xác nhận cashflow nghĩa vụ, cập nhật phần sức mua $8m theo chỉ số inflation mà trustees đã chọn và quy đổi thành mục tiêu danh nghĩa tại ngày review.
2. Tính **funding ratio được bảo vệ** từ giá trị tài sản ít rủi ro có thật tại ngày đó và coupon chắc chắn, sau phí, theo đúng ngày đáo hạn. Không tính expected equity return như tài sản đã khóa.
3. Chạy stress đã được duyệt lên growth assets. Nếu tài sản được chuyển sang danh mục bảo vệ đủ tài trợ 100% mục tiêu thực sau stress, quỹ có thể chốt phần cần thiết vào trái phiếu maturity-matched/cash; không bán toàn bộ growth assets.
4. Giữ phần tăng trưởng dư trên mục tiêu trong growth sleeve theo risk budget hiện có, trừ khi trustees đổi mục tiêu chi tiêu hoặc thời hạn. Không tự nâng spending vì đã có năm tốt.
5. Nếu funding ratio chưa đủ để khóa goal, chỉ rebalance theo calendar/band đã được duyệt. Ưu tiên coupon, tiền mới và phần overweight để tiến về target; không mua thêm chỉ vì asset vừa tăng.
6. Sau 2027 bắt buộc review risk drift. Minh họa 5% equity growth làm equities khoảng 94.3% NAV còn lại sau khi trả các nghĩa vụ; do đó upside và downside đều phải xem theo NAV còn lại, không chỉ cơ cấu ngày 2022.

Bạn đã chọn nguyên tắc sau: **khóa phần mục tiêu nếu còn đủ sau stress −30%**. Bạn cũng đã chọn CPI 2.5% làm chỉ số chính cho goal test và HEPI 3.0% là stress chi phí giáo dục riêng. Quy trình cụ thể được ghi vào `policy/IPS_addendum_selected_drawdown_rules_2026-10-21.json`: kiểm nghĩa vụ trước; tính goal danh nghĩa theo CPI; dùng giá và công cụ thực sự khả dụng tại ngày review; stress growth sleeve −30%; nếu vẫn đủ tài trợ thì chỉ chuyển đúng phần tối thiểu cần thiết sang tài sản hợp lệ khớp kỳ hạn, phần dư giữ theo growth policy. Không dùng quote Epsilon 2022 cho lệnh mua trong tương lai. Đây không bảo đảm sức mua vì lạm phát sau ngày khóa vẫn có thể khác giả định.

**Thực hành ở endowment đại học: điều gì áp dụng được cho Kappa**

Các chính sách chính thức cho thấy không có một “công thức quỹ đại học” duy nhất, và không có bằng chứng các quỹ lớn đều đặt A=4 hoặc trigger drawdown 10/15/20. Điểm chung hữu ích hơn là: xác định nghĩa vụ/chi tiêu; bảo vệ khả năng chi trả qua thời gian; đặt mục tiêu lợi suất thực sau chi tiêu/chi phí; so hiệu quả với benchmark; quy định quyền hạn, giám sát và đánh giá định kỳ.

| Tổ chức / tài liệu chính thức | Thực hành được tài liệu nêu | Bài học cho Kappa và giới hạn |
|---|---|---|
| Yale, spending policy hiện hành | Công thức làm mượt payout kết hợp phần chi trước với phần dựa trên giá trị quỹ; có mục tiêu payout và biên kiểm soát. | Có thể học cách giảm giật cục của các khoản chi tùy nghi kéo dài. Không áp dụng công thức này lên hai khoản cố định 2024/2027; trang policy hiện hành sửa sau cutoff 2022. |
| Harvard, payout FAQ | Payout thường trong vùng 5–5.5% market value; công thức giúp ổn định chi, Hội đồng có quyền phê duyệt. | Payout là quyết định ngân sách/quản trị riêng, không phải “risk-free withdrawal rate” áp được cho Kappa. Phải tránh rút theo một năm NAV cao/thấp. |
| Stanford, endowment payout process | Chính sách smoothing giới hạn biến động payout năm này qua năm khác; mục tiêu payout và guardrails hướng tới ổn định chi và sức mua. | Nếu Kappa sau này có học bổng vận hành hằng năm, hãy xây payout rule riêng, dùng trung bình NAV nhiều năm và trần/sàn. Không thay cash-flow dedication của nghĩa vụ theo ngày. |
| University of California GEP / foundation portfolio | Đặt mục tiêu real return dài hạn, benchmark theo danh mục chính sách, theo dõi rủi ro/phân bổ/chi phí và cân nhắc chi phí giao dịch khi tái cân bằng. | Phù hợp để thiết kế monitoring của growth sleeve. Quỹ Kappa có hạn 2030 và nghĩa vụ lớn gần hạn nên phải ưu tiên độ phủ liabilities và stress-path, không chỉ rolling benchmark return. |

Nguồn chính thức: [Yale spending policy](https://your.yale.edu/policies-procedures/2202-endowment-spending-and-distributions), [Harvard payout FAQ](https://finance.harvard.edu/faq/how-does-harvard-determine-its-endowment-payout), [Stanford payout process](https://fingate.stanford.edu/managing-funds/endowment-payout-process), [UC GEP Investment Policy Statement](https://www.ucop.edu/investment-office/gep-investment-policy-statement.pdf), [UC FY2021–22 endowment report](https://ucop.edu/investment-office/investment-reports/annual-reports/uc-investments-annual-endowment-report-fy-2021-2022-public-final.pdf). Các trang hiện hành chỉ dùng để minh họa governance; không được đưa thông tin công bố sau 31/12/2022 vào rationale cho quyết định ngày case.

**CPI 2.5% và HEPI 3.0%: nên dùng thế nào**

Đề dùng khái niệm “sức mua” nhưng không định nghĩa giỏ hàng giáo dục. Khuyến nghị làm việc là dùng **một chỉ số chính** cho pass/fail của mục tiêu để tránh đổi thước đo tùy kết quả: CPI 2.5% làm base vì mục tiêu đang ghi giá trị USD tháng 12/2022 và CPI khớp với cách báo real return của danh mục tài chính; HEPI 3.0% là kịch bản mission-cost stress vì Kappa phục vụ giáo dục. FY2015–22, HEPI trung bình 2.74%, CPI 2.34%; HEPI cao hơn 0.40 điểm/năm, nhưng FY2022 HEPI 5.2% còn CPI 7.2%. Vì thế 3.0% là planning stress được chọn để thử độ nhạy, không phải dự báo đã xác thực.

Bạn đã chọn CPI 2.5% làm tiêu chí chính và HEPI 3.0% làm stress riêng. Phép tính có thể tái tạo bằng `analysis/goal_inflation_sensitivity.py`; kết quả nằm ở `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`. Mục tiêu 2030 lần lượt **$9.747m** và **$10.134m**; hurdle growth sleeve khoảng **4.84%** và **5.37% CAGR**. HEPI stress làm mục tiêu danh nghĩa cao hơn **$386,937**. Nếu sleeve kiếm ròng 5%/năm và coupon không sinh lãi, terminal wealth xấp xỉ **$9.863m**: vượt CPI-base target khoảng **$116k**, nhưng thấp hơn HEPI-stress target khoảng **$271k danh nghĩa** (khoảng **$214k theo sức mua 2022**). Đây là đường lợi suất minh họa, không phải xác suất.

HEPI được công bố theo FY kết thúc tháng 6 và phản ánh rổ chi phí vận hành giáo dục đại học; nó không mặc nhiên bằng lạm phát của học bổng hoặc learning centre Kappa. Để chạy stress HEPI, dùng **mức 3% hình học hằng năm từ cùng base date** như một scenario rõ ràng, hoặc nếu muốn đo chỉ số thực thì phải đồng bộ FY base/end dates. Không lấy CPI 2.5% và HEPI 3.0% rồi cộng, lấy trung bình, hay nhân chồng trong cùng goal. Nếu trustees xác nhận mục tiêu là giữ sức mua riêng của chương trình giáo dục, hãy thay CPI bằng chỉ số được họ lựa chọn cho pass/fail và báo CPI như comparator.

Nếu chọn nhiều ETF/cổ phiếu, rebalance upside theo trọng số policy đã duyệt, không đổi mục tiêu theo giá. Chọn **một** corridor trước khi backtest: ±5 điểm phần trăm cho các sleeve lớn, hoặc ±25% tương đối so với target cho tài sản riêng; không vừa chọn cái thuận hơn sau khi nhìn return. Kiểm tra chi phí giao dịch: chỉ trade khi phí dự kiến và rủi ro giảm lớn hơn lợi ích sửa drift. Giới hạn 12–15% mỗi stock và ETF floor 30% trong gợi ý là lựa chọn policy mới, chưa được duyệt; giữ ở sensitivity cho đến khi nhóm thống nhất.

**Các quy ước đã chốt trong tham vấn**

1. **Chốt chỉ số cho goal — đã chọn:** CPI 2.5% là chỉ số pass/fail chính; HEPI 3.0% là stress phụ, không gộp hai chỉ số. Nếu trustees sau này xác định $8m là sức mua của một rổ chi phí giáo dục cụ thể, cần sửa định nghĩa goal có hiệu lực về sau và tính lại, không âm thầm thay CPI bằng HEPI.

2. **Phí giao dịch — đã chốt quy ước:** bạn chọn 5bp bonds và 10bp equity làm base nhất quán với file đang dùng; sensitivity riêng là 0bp bonds, 5bp ETF và 10bp direct stocks. Đây là mức friction giả định vì đề không cho đầy đủ bảng phí, không khẳng định là báo giá broker thực tế. Với portfolio chỉ mua USMV, dùng bộ sensitivity làm vốn growth ròng tăng khoảng **$5,992** (từ $6.346m lên $6.352m); hurdle CPI giảm **0.0124 điểm %** (4.8365% xuống 4.8241%), hurdle HEPI giảm tương tự (5.3743% xuống 5.3619%). Kết luận mục tiêu không đổi đáng kể. Chi tiết tính toán trong `outputs/mandate_preparedness/inflation_goal_sensitivity.csv`.

Coupon đã chốt: giữ Beta đủ $2.4m face để tự trả khoản 2024, tách coupon Delta làm tiền dư, base cash reinvestment 0%. Phương án dùng một hoặc hai coupon chỉ là sensitivity. Danh sách cap cổ phiếu, VaR/CVaR và cổ phiếu đề xuất thêm cũng chỉ được chạy dưới dạng sensitivity cho tới lúc được xác nhận; không thay hard rules của đề.
