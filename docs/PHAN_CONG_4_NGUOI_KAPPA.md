# KAPPA FOUNDATION — PHÂN CÔNG CÔNG VIỆC NHÓM 4 NGƯỜI

## Từ đề bài PDF đến sản phẩm nộp 29/10/2026

**Prepared for:** Minh — Python Lead & Overall Lead  
**Version:** 1.0 — 18/10/2026  
**Status:** Kế hoạch làm việc nội bộ. Không phải bằng chứng rằng công việc đã hoàn thành.

> **Nguyên tắc xuyên suốt:** Một người làm Python, ba người làm phân tích. Không ai chỉ “đọc và thấy ổn”. Mỗi kết luận phải có người tạo, người kiểm, bằng chứng và ngày.

---

## MỤC LỤC

1. Phần I — Executive chia việc
2. Phần II — Quy trình chung và cách kiểm
3. Phần III — Chi tiết từng người
4. Phần IV — Ma trận check, cross-check, verify
5. Phần V — Go further extra theo từng mảng
6. Phần VI — Deliverables, deadline, mẫu biểu
7. Phụ lục — Check card, glossary, nguồn

### Document control

| Item | Value |
|---|---|
| Version | 1.0 — 18/10/2026 |
| Owner | Minh — Python Lead & Overall Lead |
| Review | 21/10/2026 nội bộ; 22/10/2026 trước deadline initial record |
| Distribution | Nội bộ nhóm 4 người; không công bố ngoài |
| Related | White Paper, IPS, Scenario Workbook, Committee Memo 8 trang |
| Source of truth | `reference/BFIN-WS2026-Group_Assignment.pdf` |

> **Cách đọc:** Minh đọc Part I và Part IV trước. Mỗi thành viên đọc Part III của mình, sau đó đọc phần của người sẽ kiểm mình. Part V dùng để chọn extra; Part VI dùng để chốt deadline.

---

# PHẦN I — EXECUTIVE CHIA VIỆC

## 1.1. Bài toán trong 8 dòng

- Kappa có **12 triệu USD** tiền mặt vào **31/12/2022**; không có tài sản, nợ hay khoản tài trợ nào khác.
- Phải trả **2,4 triệu USD** ngày **31/12/2024** và **3,6 triệu USD** ngày **31/12/2027**. Đây là nghĩa vụ cố định, không được đổi trong case gốc.
- Sau khi trả, mục tiêu là còn **sức mua 8 triệu USD** tính theo giá tháng 12/2022 vào cuối 2030. Đây là **mục tiêu**, không phải lời hứa lợi nhuận.
- Hội đồng “không thoải mái” với lỗ gần **15%**, nhưng chưa định nghĩa đo thế nào, trong bao lâu, đánh đổi ra sao.
- Được dùng cash, 5 trái phiếu fictional, cổ phiếu Mỹ, ETF cổ phiếu Mỹ; **cấm vay, bán khống, phái sinh**.
- Phải có **8–12 cổ phiếu thuộc ít nhất 4 ngành + 2 ETF khác mandate**; được giữ một phần; phải có bằng chứng eligibility tại 31/12/2022.
- Dữ liệu thị trường phải tự lấy bằng Python qua **yfinance**; factor data tự lấy từ **Kenneth French**; phải lưu raw, hash, ngày, settings, versions; phải rebuild offline.
- Deadline: **22/10 16:00** initial record 2 trang + Python + data record; **23/10 16:00** revised mandate; **29/10 16:00** final archive.

### Baseline allocation đang được phân tích

| Use | USD | Vai trò |
|---|---:|---|
| Beta bond | 2.214.672,00 | Trả 2,4 triệu USD năm 2024 |
| Delta bond | 3.429.808,70 | Trả 3,6 triệu USD năm 2027 |
| USMV | 6.346.350,71 | Phần tăng trưởng cho mục tiêu 2030 |
| Chi phí | 9.168,59 | 5bp trái phiếu + 10bp cổ phiếu |
| **Tổng** | **12.000.000,00** | |

> Đây là **baseline để chia việc**, không phải quyết định cuối cùng. Revised mandate 23/10 có thể đổi nghĩa vụ, mục tiêu hoặc ràng buộc; khi đó tạo scenario riêng, không sửa bản gốc.

## 1.2. Nguyên tắc phân việc

1. **Chia theo câu hỏi quyết định, không chia theo công cụ.** Ai không code vẫn làm phân tích thật, không chỉ đọc và sửa câu chữ.
2. **Minh giữ “single source of truth” về số.** Mọi con số cuối cùng phải đi qua pipeline của Minh hoặc được Minh đối chiếu.
3. **Mỗi output có đúng một owner.** Một người có thể support, nhưng không có “ai cũng làm”.
4. **Không tự kiểm bài mình.** Người tạo phép tính không được là người kiểm độc lập duy nhất.
5. **Kiểm bằng cách tái tạo hoặc đối chiếu nguồn, không kiểm bằng cách đọc.** “Em thấy hợp lý” không phải check.
6. **Mỗi tuần một lần freeze.** Số nào đã lên memo/slide thì không sửa nếu không có log và người kiểm.
7. **Không bịa tên, không bịa việc, không bịa check.** Contribution statement chỉ điền sau khi làm thật.

## 1.3. Bảng executive 4 vai

| Thành viên | Vai trò | Câu hỏi trung tâm | Sở hữu chính | Output bắt buộc | Rubric | Người kiểm |
|---|---|---|---|---|---|---|
| **Minh (A)** | Quant & Integration Lead | “Các con số có đúng, tái lập được, và thực sự chứng minh điều gì?” | Python, data, bond repricing, portfolio, factor, evaluation, scenario, memo integration | A1–A11 | Data 15 + Portfolio 15 + Factor 15 + integration | B, C, D |
| **B** | Liability & Fixed Income Analyst | “Quỹ có chắc tiền trả đúng ngày không, và trái phiếu chịu rủi ro gì?” | Bond valuation, funding cash flow, rate risk, liquidity, covenant | B1–B8 | Bond & funding 20 | Minh, D |
| **C** | Equity/ETF & Provenance Analyst | “Đang mua cái gì, nguồn có đúng 2022, benchmark có hợp lý?” | Universe, VTI/USMV, eligibility, data provenance, evaluation narrative, factor readout | C1–C8 | Data 15 + Market/factor 15 | Minh, D |
| **D** | Mandate, Risk & Committee Analyst | “Hội đồng quyết định gì, 15% là gì, khi nào phải đổi?” | Assumptions, risk policy, IPS, memo, slides, revised mandate, Q&A | D1–D9 | Mandate 10 + Evaluation/mandate 15 + Memo/slides 10 | B, C |

## 1.4. Bản đồ rubric → người phụ trách

| Vùng chấm điểm | Điểm | Lead | Support | Bằng chứng chính |
|---|---:|---|---|---|
| Mandate, assumptions & judgement | 10 | D | Minh, B | Initial record, assumption register, risk note, memo pages 1–2, 8 |
| Bond valuation & funding risk | 20 | B | Minh, D | Bond metrics, curve, stress, funding cash flow, rate note |
| Data integrity & reproducibility | 15 | Minh | C, D | Raw manifest, hash, return note, rebuild receipt, evidence map |
| Portfolio construction & robustness | 15 | Minh | B, D | Expected returns, covariance, constraints, candidates, sensitivity |
| Market & factor interpretation | 15 | Minh | C, D | CAPM/FF3, beta, alpha CI, variance decomposition, factor note |
| Evaluation & mandate response | 15 | Minh (numbers), D (response) | C, B | Frozen evaluation, adverse evidence, reversal threshold, revision table |
| Committee memo & presentation | 10 | D | Minh, B, C | Memo 8+1, slides 13, Q&A, rehearsal |

## 1.5. Chuỗi verify một dòng

**Minh → C** kiểm returns/data; **Minh → B** kiểm bond/cash-flow; **Minh → D** kiểm claims/evidence.  
**B → Minh** kiểm bond math; **B → D** kiểm memo consistency.  
**C → Minh** kiểm data/cutoff; **C → D** kiểm source claims.  
**D → B** kiểm cash-flow priority; **D → C** kiểm evidence.  
**Final memo:** D đọc lần cuối; Minh khóa số; B/C ký phần mình.

## 1.6. Timeline tổng

| Thời điểm | Việc phải xong | Owner |
|---|---|---|
| 18/10 | Chốt vai, đọc PDF, data pack, assumption register | Minh + D |
| 19/10 | Data/model nền; bond pack; universe; rubric/IPS | Minh, B, C, D |
| 20/10 | Portfolio/factor/evaluation; funding/rate; ETF/adverse; 15%/red team | Minh, B, C, D |
| 21/10 | Cross-check, sửa lỗi, initial record, rehearsal | All |
| 22/10 16:00 | Nộp initial record + Python + data record; giữ receipt | Minh + D |
| 23/10 16:00 | Nhận revised mandate; lưu nguyên bản; tạo scenario | Minh + D |
| 24–28/10 | Memo/slides final; scenario comparison; Q&A | All |
| 29/10 16:00 | Final archive; page limit; PDF/PPTX; contribution | Minh + D |

## 1.7. Sáu quyết định phải khóa trước khi làm sâu

1. Kappa có tiếp tục sau 2030 hay 2030 là mốc kết thúc?
2. 8 triệu USD thực có phải mục tiêu ràng buộc, hay có thể đổi nếu có trade-off?
3. 15% là **ngưỡng hành động** hay **sàn kinh tế**?
4. Mức hụt mục tiêu nào hội đồng chấp nhận: 5%, 10%, 20%?
5. Chi phí vận hành thực tế là bao nhiêu: custody, audit, reporting, consultant?
6. Chính sách AI của môn học và revised mandate là gì?

> Nếu chưa có câu trả lời, ghi rõ **“proposed”** trong mọi tài liệu. Không biến giả định của nhóm thành yêu cầu của đề.

## 1.8. Definition of done

Một phần được coi là xong khi có đủ 5 thứ:

- **Đúng người:** có owner và checker khác người làm.
- **Đúng file:** output nằm trong `docs/` hoặc `outputs/`, có tên và version.
- **Đúng số:** có thể tái tạo từ raw data hoặc nguồn gốc.
- **Đúng lời:** giải thích được bằng tiếng Việt đơn giản, không đọc nguyên văn.
- **Đúng dấu:** có ngày, người kiểm, kết quả, và giới hạn.

## 1.9. Cách dùng tài liệu này

1. **Minh đọc toàn bộ** và chốt tên thật của B/C/D, năng lực Excel/tiếng Anh/thuyết trình.
2. **Mỗi người đọc phần của mình** trước, sau đó đọc phần của người sẽ kiểm mình.
3. **In bảng output của mình** và đánh dấu: chưa làm, đang làm, xong, đã kiểm.
4. **Không chờ đến 21/10 mới check.** Mỗi output xong là gửi checker ngay.
5. **Mọi con số lên memo/slide** phải có dòng trong evidence map.
6. **Mọi thay đổi sau 22/10** phải vào decision log, không sửa lặng lẽ.
7. **Mỗi người tự viết critique 3–5 câu**, không nhờ AI viết hộ nguyên văn.

---

# PHẦN II — QUY TRÌNH CHUNG VÀ CÁCH KIỂM

## 2.1. Kiến trúc tài liệu

| Tài liệu | Trả lời câu hỏi | Độ dài | Ai chịu |
|---|---|---|---|
| White Paper | Quỹ tồn tại để làm gì, tin gì, hành xử thế nào? | 12–16 trang | D + Minh |
| IPS | Nhà quản lý được làm gì, không được làm gì? | 4–6 trang | D + Minh |
| Scenario Workbook | Nếu điều này xảy ra thì sao? | Excel 6–8 tab | Minh |
| Committee Memo | Hôm nay quyết định gì? | 8 trang + 1 ref | D + Minh |
| Slides | Kể câu chuyện trong 12–15 phút | 13 slide | D + all |
| Code/Data | Chứng minh tái lập | Repo + archive | Minh |

> White paper và IPS là tài liệu nền. **Memo 8 trang mới là sản phẩm chấm điểm chính.** Đừng để white paper làm chậm deadline 22/10.

## 2.2. Quy trình 10 bước

1. **Khóa facts:** đọc PDF, chốt nghĩa vụ, mục tiêu, ràng buộc, deadline.
2. **Khóa assumptions:** inflation, RF, ERP, A, costs, benchmark, rebalancing.
3. **Lấy dữ liệu:** Yahoo/yfinance + Kenneth French; lưu raw, hash, manifest.
4. **Dựng returns:** month-end adjusted close; 96 tháng train, 36 tháng eval; không fill missing.
5. **Định giá bonds & funding:** cash flow, YTM, duration, convexity, exact repricing, stress.
6. **Dựng portfolio:** expected returns, covariance, constraints, candidates, CE, sensitivity.
7. **Factor models:** CAPM + FF3; beta, alpha, CI, R², variance decomposition.
8. **Freeze & evaluate:** khóa policy trước eval; chạy 2023–2025; giữ adverse evidence.
9. **Scenario & revised mandate:** S0–S9; original vs revised; không viết lại lịch sử.
10. **Đóng gói & verify:** memo, slides, code, data, decision log, contribution, archive.

## 2.3. Evidence hierarchy

Khi có mâu thuẫn, thứ tự tin cậy là:

1. **Raw download** + hash + manifest.
2. **Processed data** được tạo từ raw bằng code.
3. **Output table/JSON** được tạo từ processed data.
4. **Memo/slide** trích từ output.

Nếu slide khác CSV, **CSV thắng**. Nếu CSV khác raw, **raw thắng**. Nếu raw không khớp nguồn, **nguồn gốc thắng**. Không được sửa ngược từ slide xuống CSV.

## 2.4. Bốn mức kiểm

| Mức | Tên | Ai làm | Có phải independent check? |
|---|---|---|---|
| 0 | Self-check | Người làm | Không |
| 1 | Reproduce cùng code | Người làm/máy | Chỉ là reproducibility |
| 2 | Peer recompute bằng Excel/máy tính | Người khác | Có, mức cơ bản |
| 3 | Independent source/method | Người khác, khác đường tính | Có, mức tốt |
| 4 | Red team | Người khác cố bác bỏ | Có, mức cao nhất |

## 2.5. Khung 5C cho mỗi phiếu kiểm

| Thành phần | Câu hỏi |
|---|---|
| **Claim** | Kết luận chính xác là gì? |
| **Calculation** | Tính lại bằng cách nào? |
| **Consistency** | Có khớp giữa slide, memo, CSV, raw không? |
| **Caveat** | Kết luận này **không** chứng minh điều gì? |
| **Confirmation** | Ai kiểm, ngày nào, khớp/lệch bao nhiêu? |

## 2.6. Quy trình khi phát hiện lệch

1. **Dừng:** không sửa số ngay, không “làm tròn cho khớp”.
2. **Ghi:** log claim, input, cách tính, kết quả hai bên, chênh lệch.
3. **Truy:** lỗi ở raw, processing, formula, unit, timing hay copy?
4. **Sửa:** sửa ở tầng thấp nhất; chạy lại toàn bộ output bị ảnh hưởng.
5. **Cập nhật:** memo/slide/evidence map; ghi version.
6. **Ký:** owner + checker xác nhận lại.

## 2.7. Sign-off log

| Item | Owner | Checker | Kết quả | Ngày | Version |
|---|---|---|---|---|---|
| Bond pack | B | Minh | Pass/Fix | | |
| Returns | Minh | C | Pass/Fix | | |
| Evaluation | Minh | C | Pass/Fix | | |
| Risk note | D | B | Pass/Fix | | |
| Memo | D | Minh + B + C | Pass/Fix | | |

## 2.8. AI use và disclosure

- AI được dùng để hỗ trợ đọc, code, kiểm tra, draft.
- **Không** để AI tự quyết định allocation, risk limit hay conclusion.
- Mọi output AI phải có người đọc, hiểu, kiểm.
- Ghi rõ AI đã hỗ trợ gì và người kiểm đã làm gì.
- Tuân thủ chính sách AI thật của môn học; nếu chưa có, hỏi giảng viên và lưu email.

## 2.9. File naming và version

- `A1_run_log.md`, `B2_bond_verification.xlsx`, `C3_return_check.xlsx`, `D3_risk_note.md`.
- Version: `v01`, `v02`, `final`; không dùng `final_final`.
- Mỗi lần đổi số: ghi `CHANGELOG.md` hoặc decision log.
- Không sửa `policy/frozen_policy.json`, raw data, hay file của người khác mà không báo.

## 2.10. Nhịp họp

| Cuộc họp | Thời lượng | Nội dung | Output |
|---|---|---|---|
| Daily stand-up | 15 phút | Hôm qua, hôm nay, blocker | 3 dòng |
| Mid-week check | 60 phút | Số nào đã khóa, số nào lệch | Sign-off log |
| Pre-submission | 90 phút | Đọc chéo, rehearsal, page limit | Checklist |
| Post-mortem | 30 phút | Học gì, sửa gì | Notes |

---

# PHẦN III — CHI TIẾT TỪNG NGƯỜI

## 3.1. MINH — Quant & Integration Lead

### 3.1.1. Vai trò và câu hỏi trung tâm

Minh là **người duy nhất chạy pipeline Python**, giữ “single source of truth” về số, và là **tổng phụ trách** kết nối B/C/D vào memo/slide. Minh không làm hộ kết luận của người khác và không tự chứng nhận mọi giả định tài chính là đúng.

Câu hỏi Minh phải trả lời được:

- Con số này được tạo từ file nào, bằng công thức nào?
- Nếu đổi một giả định, kết luận nào đổi?
- Kết quả này chứng minh được gì, không chứng minh được gì?
- Nếu ngày mai dữ liệu được tải lại, kết quả có tái lập được không?

### 3.1.2. Phạm vi

**Minh sở hữu:**

- Data retrieval, raw files, manifest, hash, environment.
- Monthly returns, sample alignment, data quality.
- Bond repricing, cash-flow engine, stress math.
- Expected returns, covariance, optimization, constraints, CE.
- CAPM/FF3, alpha CI, factor variance.
- Frozen evaluation, performance metrics.
- Scenario workbook, goal sensitivity, all-bond alternative.
- Evidence map, integration, final numeric QA.

**Minh không sở hữu:**

- Nội dung chính sách/risk (D).
- Cách trình bày bond risk bằng lời (B).
- Cách chọn universe/ETF và source audit (C).
- Quyết định cuối cùng của hội đồng (D + cả nhóm).

### 3.1.3. Đầu vào

- `reference/BFIN-WS2026-Group_Assignment.pdf`
- `README.md`, `CHECKPOINT.md`, `DECISION_LOG.md`, `EVIDENCE_MAP.md`
- `deliverables/Kappa_Requirements_and_Data_Guide.md`
- `analysis/`, `data/raw/`, `data/processed/`, `outputs/tables/`
- `policy/frozen_policy.json`

### 3.1.4. Quy trình từng bước

1. **Đọc PDF 4 trang** và đánh dấu 7 vùng rubric; đối chiếu với memo hiện có.
2. **Khóa môi trường:** Python 3.12, requirements, hash policy; chạy `analysis/rebuild.py` một lần, ghi log.
3. **Dựng data manifest:** ticker, source URL, retrieval UTC, requested dates, rows, first/last date, settings, package versions, SHA-256.
4. **Dựng returns:** month-end adjusted close; kiểm 96 tháng train, 36 tháng eval; kiểm missing, corporate actions, overlap Dec 2022.
5. **Dựng bond pack:** cash flow từng bond; YTM; duration; convexity; exact repricing; parallel ±100bp; steepener; +200bp; liquidity note.
6. **Dựng portfolio pack:** forecast return = 4% + beta × 4.5%; zero alpha; sample covariance; single-index covariance; constraints; A=1..8; CE; candidates.
7. **Dựng factor pack:** CAPM/FF3; HAC 3 lags; alpha CI; R²; variance decomposition; alpha stability.
8. **Freeze & evaluate:** policy đã frozen; chạy 2023–2025; CAGR, vol, Sharpe, drawdown, calendar years, costs; giữ adverse.
9. **Dựng scenario workbook:** S0–S9; outputs; dashboard; decision triggers.
10. **Dựng evidence map:** mỗi số trên memo/slide trỏ về CSV/JSON + script + owner + limitation.
11. **Tích hợp:** cập nhật memo/slides; kiểm page limit, số khớp, PDF/PPTX, archive.
12. **Ngày 23/10:** lưu revised mandate nguyên bản; tạo scenario copy; chỉ đổi tham số bị ảnh hưởng; so sánh original/revised/difference/cause.

### 3.1.5. Output bắt buộc

| Mã | Output | Hình thức | Tiêu chuẩn hoàn thành |
|---|---|---|---|
| A1 | Technical run log | 1–2 trang | Lệnh, thời điểm, input/output, lỗi, hash trước/sau |
| A2 | Data manifest | CSV/JSON | Ticker, source, ngày, settings, version, SHA-256 |
| A3 | Return construction note | 1–2 trang | Adjusted close, month-end, missing, corporate actions, 96/36 |
| A4 | Bond & funding pack | Excel | Cash flow, YTM, duration, convexity, exact repricing, stress |
| A5 | Portfolio pack | Excel | Forecast, covariance, constraints, candidates, CE, sensitivity |
| A6 | Factor pack | Excel | CAPM/FF3, beta, alpha, CI, p-value, R², variance |
| A7 | Frozen evaluation pack | Excel | 2023–2025 metrics, calendar years, costs, drawdown |
| A8 | Scenario workbook | Excel | S0–S9, outputs, dashboard, triggers |
| A9 | Evidence map | 1–2 trang | Mỗi claim → CSV/JSON → script → owner → limitation |
| A10 | Integration checklist | 1 trang | Page limit, số khớp, PDF/PPTX, hash, archive |
| A11 | Teach-back note | 1 trang | Giải thích pipeline trong 5 phút |

### 3.1.6. Minh kiểm ai, kiểm gì

| Người | Minh kiểm gì | Cách kiểm |
|---|---|---|
| B | Bond math, cash flow, exact repricing, units | Tính lại Beta/Delta; so `bond_metrics.csv`; kiểm ngày/đơn vị |
| C | Data/cutoff, ticker, 2 monthly returns | Mở raw + processed; tính tay 2 tháng; kiểm source date |
| D | 3 claims trọng yếu trong memo/slide | Trace slide → memo → CSV → script; kiểm caveat |

### 3.1.7. Go further của Minh

1. **Model risk register:** 8 dòng, mỗi model một “nhãn cảnh báo”: giả định gì, sai thế nào, quyết định nào bị ảnh hưởng.
2. **Shortfall severity:** ngoài 68,48%, tính median shortfall, 5th percentile, P(hụt >10%/20%).
3. **Lifecycle/glidepath:** sau 2027, equity ~94,29%; stress 30% mất 28,29% tài sản còn lại; đề xuất review/glidepath.
4. **Decision threshold map:** A × ERP; inflation × required CAGR; điều kiện đảo USMV/VTI/all-bond.
5. **Reverse stress test:** tìm combination inflation 4–5%, equity return thấp, shock 2028 làm kế hoạch thất bại.
6. **Vintage audit:** so dữ liệu tải tháng 10/2026 với giả định 2022; ghi rõ revised vendor history.
7. **Covariance robustness:** sample vs single-index, resampling, turnover, cost; kết luận “simple is defensible”.
8. **Multiple testing:** alpha của nhiều mã; điều chỉnh diễn giải, không biến p-value thành kỹ năng.

### 3.1.8. Câu hỏi bảo vệ Minh phải trả lời

- Vì sao 96 tháng, không phải 60?
- Vì sao zero forecast alpha?
- Vì sao USMV ở A=4? Đảo chiều ở đâu?
- 68,48% có phải xác suất không? Vì sao không?
- Làm sao chứng minh không có look-ahead?
- Vì sao sample covariance khác single-index? Kết luận nào đổi?
- Nếu inflation 4% thì sao?
- Nếu revised mandate đổi payment thì sao?
- Nếu dữ liệu Yahoo được revise thì sao?
- Rủi ro model lớn nhất là gì?

### 3.1.9. Lỗi thường gặp

- Chạy lại data mới rồi lẫn với data cũ, không ghi version.
- Sửa số trên slide mà không sửa CSV.
- Để người khác chạy cùng lúc, ghi đè output.
- Trả lời “68,48% là xác suất” — sai bản chất.
- Dùng 2023–2025 để chọn lại portfolio 2022 — hindsight.
- Ôm quá nhiều việc, không kịp viết memo.

### 3.1.10. Thời gian

| Ngày | Giờ | Việc |
|---|---|---|
| 18/10 | 2h | Đọc PDF, chốt data pack, chạy rebuild |
| 19/10 | 4h | Returns, bond pack, portfolio skeleton |
| 20/10 | 4h | Factor, evaluation, scenario skeleton |
| 21/10 | 3h | Cross-check, sửa, evidence map |
| 22/10 | 2h | Initial record, freeze, submit |
| 24–28/10 | 2h/ngày | Memo/slides, scenario, QA |

---

## 3.2. B — Liability & Fixed Income Analyst

### 3.2.1. Vai trò và câu hỏi trung tâm

B chịu trách nhiệm **chứng minh quỹ có tiền trả đúng ngày** và **giải thích trái phiếu chịu rủi ro gì**. B không cần Python; B cần Excel/máy tính, đọc hiểu, và kỷ luật ghi nguồn.

Câu hỏi B phải trả lời:

- Năm 2024 và 2027, tiền đến từ đâu, đúng ngày không?
- Nếu lãi suất đổi, giá trị trái phiếu đổi bao nhiêu, nhưng dòng tiền có đổi không?
- Nếu phải bán trước hạn, rủi ro gì?
- Nếu settlement/payment cùng ngày, vận hành cần gì?

### 3.2.2. Phạm vi

**B sở hữu:**

- Liability timeline 2023–2030.
- Beta/Delta verification bằng tay.
- Funding cash-flow coverage.
- YTM, duration, convexity, exact repricing, parallel/steepener.
- Liquidity/settlement checklist.
- Coverage covenant.
- Bond slides 2–3.

**B không sở hữu:**

- Chọn universe/ETF (C).
- Portfolio optimization (Minh).
- 15% policy ladder (D).
- Python pipeline (Minh).

### 3.2.3. Đầu vào

- PDF trang 1–3, đặc biệt Exhibit 1.
- Memo trang 1–3.
- `outputs/tables/funding_cashflows.csv`
- `outputs/tables/bond_metrics.csv`
- `outputs/tables/bond_stress.csv`
- `outputs/tables/ytm_duration_validation.csv`
- `outputs/tables/bond_curve.csv`
- `outputs/tables/curve_interpolation_sensitivity.csv`

### 3.2.4. Quy trình từng bước

1. **Đọc PDF trang 1–3** và memo trang 1–3; gạch chân 2,4m/3,6m, ngày, coupon, mệnh giá.
2. **Vẽ liability timeline 2023–2030:** coupon Beta, coupon Delta, principal, payment, cash balance.
3. **Tính Beta bằng tay:** 2.400 bonds × 922,78 = 2.214.672; đáo hạn 2.400 × 1.000 = 2.400.000.
4. **Tính Delta bằng tay:** 3.600.000 / 1,035 = 3.478.260,87 mệnh giá; cost = 3.478,26087 × 986,07 = 3.429.808,70; coupon = 121.739,13; final = 3.600.000.
5. **Kiểm funding_cashflows.csv từng năm:** coupon, principal, payment, cumulative; không âm; không double count.
6. **Kiểm bond_metrics.csv:** YTM, modified duration, convexity; so với tính tay.
7. **Kiểm bond_stress.csv:** +100bp, −100bp, steepener; so exact repricing; giải thích duration/convexity là approximation.
8. **Kiểm ytm_duration_validation.csv:** sai số duration/convexity; xác nhận exact repricing.
9. **Viết rate risk note 500–700 từ:** YTM vs spot; price risk vs funding risk; hold-to-maturity; curve shape.
10. **Viết liquidity/settlement checklist:** ai chuyển tiền, ngân hàng nào, cut-off, dual approval, reconciliation.
11. **Viết coverage covenant:** không release payment asset nếu không có replacement cash flow đúng hạn.
12. **Viết critique:** zero reinvestment, default-free assumption, settlement risk, mark-to-market vs cash flow.

### 3.2.5. Output bắt buộc

| Mã | Output | Hình thức | Tiêu chuẩn |
|---|---|---|---|
| B1 | Liability timeline | Excel/PDF 1 trang | 2023–2030, coupon, principal, payment, cash |
| B2 | Bond verification | Excel 1 trang | Công thức, số tự tính, so output, sai lệch |
| B3 | Funding coverage | 1–2 trang | Từng năm, cumulative ≥0, không double count |
| B4 | Rate risk note | 500–700 từ | YTM, duration, convexity, exact repricing, parallel/steepener |
| B5 | Liquidity/settlement checklist | 1 trang | 10 bước, role, cut-off, dual approval |
| B6 | Coverage covenant | 1 trang | Rule, replacement test, exception |
| B7 | Independent critique | 3–5 câu | Điểm yếu của phương án |
| B8 | Slide 2–3 script | 1 trang | Speaking notes + 6 Q&A |

### 3.2.6. B kiểm ai, kiểm gì

| Người | B kiểm gì | Cách kiểm |
|---|---|---|
| Minh | Bond math, cash flow, exact repricing | Tính lại 2 bonds; so công thức; kiểm unit/ngày |
| D | 15% policy có mâu thuẫn dòng tiền không | Đọc risk ladder; kiểm payment priority |
| D | Memo/slide bond consistency | So 2,4m/3,6m/486.957 với CSV |

### 3.2.7. Go further của B

1. **ALM/funding ratio:** phân biệt price risk và funding risk; funding ratio theo năm.
2. **Key rate duration/curve shape:** steepener, flattener, twist; tác động Beta/Delta.
3. **Cash-flow matching vs immunization:** vì sao hold-to-maturity đơn giản hơn duration matching.
4. **Liquidity/settlement stress:** payment date holiday, bank cut-off, operational failure.
5. **Cost of conservatism:** all-bond 7,471m real vs 8m; thiếu 6,62%; cần thêm 480.443 USD.
6. **Coverage covenant:** rule đề xuất, replacement test, board approval.
7. **Bond accounting:** amortized cost vs fair value; mark-to-market không phải cash loss.

### 3.2.8. Câu hỏi bảo vệ B phải trả lời

- Vì sao chọn Beta và Delta, không phải Alpha/Gamma/Epsilon?
- Vì sao Delta mệnh giá 3.478.260,87 mà không phải 3,6 triệu?
- Nếu lãi suất +200bp, giá trị giảm bao nhiêu? Dòng tiền có đổi không?
- Nếu payment date là ngày nghỉ, làm sao trả đúng hạn?
- Nếu bond default? Case nói default-free, nhưng thực tế?
- Nếu coupon tái đầu tư >0 thì sao?
- Duration và convexity khác nhau thế nào?
- Vì sao hold-to-maturity là hợp lý?
- Rủi ro lớn nhất của payment account là gì?
- Nếu revised mandate đổi ngày/amount thì sao?

### 3.2.9. Lỗi thường gặp

- Tính coupon trên mệnh giá 3,6m thay vì 3.478m.
- Cộng coupon hai lần vào terminal cash.
- Nhầm YTM duration với spot duration.
- Nói “trái phiếu an toàn” mà bỏ qua price risk.
- Không kiểm ngày payment và settlement.
- Viết quá dài, không có bảng.

### 3.2.10. Thời gian

| Ngày | Giờ | Việc |
|---|---|---|
| 18/10 | 1h | Đọc PDF/memo; timeline skeleton |
| 19/10 | 2h | Beta/Delta; funding check |
| 20/10 | 2h | Rate note; liquidity; covenant |
| 21/10 | 1h | Cross-check; slide script |
| 22/10 | 1h | Initial record bond section |

---

## 3.3. C — Equity/ETF & Provenance Analyst

### 3.3.1. Vai trò và câu hỏi trung tâm

C sở hữu **câu chuyện VTI/USMV**, **tính hợp lệ của universe tại 2022**, **nguồn dữ liệu**, và **cách diễn giải evaluation/factor**. C không cần chạy mô hình; C cần Excel, đọc tài liệu, và hoài nghi đúng chỗ.

Câu hỏi C phải trả lời:

- VTI là gì, USMV là gì, khác nhau ở đâu?
- Vì sao USMV được chọn dù VTI thắng 2023–2025?
- 10 mã có thật sự eligible tại 31/12/2022?
- Nguồn hiện tại có bị dùng sai để chứng minh trạng thái 2022?
- Alpha có chứng minh kỹ năng không?

### 3.3.2. Phạm vi

**C sở hữu:**

- Eligibility matrix 10 mã.
- VTI/USMV explainer.
- 2 monthly return check.
- Evaluation/adverse evidence note.
- Factor readout.
- Benchmark architecture.
- Slides 4–6, 9.

**C không sở hữu:**

- Python pipeline (Minh).
- Bond math (B).
- 15% policy (D).
- Final allocation decision (Minh + D).

### 3.3.3. Đầu vào

- PDF trang 2–3.
- Memo trang 4–7.
- `data/raw/supporting/eligibility_checks.json`
- `data/processed/train_month_end_adjusted_prices.csv`
- `data/processed/train_monthly_returns.csv`
- `outputs/tables/evaluation_performance.csv`
- `outputs/tables/evaluation_calendar_years.csv`
- `outputs/tables/factor_regressions.csv`
- `outputs/tables/factor_variance_decomposition.csv`

### 3.3.4. Quy trình từng bước

1. **Đọc PDF trang 2–3** và memo trang 4–7; ghi lại yêu cầu 8–12 stocks, ≥4 sectors, 2 ETFs.
2. **Lập eligibility matrix 10 dòng:** ticker, loại, sector/mandate, nguồn trước cutoff, ngày, cutoff status, limitation.
3. **Viết VTI/USMV explainer 2 trang:** objective, construction, expected behavior, failure modes, when each may disappoint.
4. **Tính 2 monthly returns bằng Excel:** chọn 2 tháng; lấy adjusted close; `giá tháng này / giá tháng trước − 1`; so CSV; ghi sai lệch.
5. **Kiểm 96/36 tháng:** đếm, kiểm first/last date, missing, overlap Dec 2022.
6. **Đọc evaluation_performance.csv:** CAGR, vol, Sharpe, drawdown, calendar years; so USMV/VTI.
7. **Viết adverse evidence note 500 từ:** vì sao USMV lag; 36 tháng; survivor universe; không kết luận dài hạn.
8. **Đọc factor_regressions.csv:** beta, alpha, CI, p-value, R²; giải thích alpha CI đi qua 0.
9. **Viết benchmark architecture 4 lớp:** payment, mission, strategic, implementation.
10. **Viết critique:** survivorship, selection, data vintage, low-vol crowding, ETF look-through.

### 3.3.5. Output bắt buộc

| Mã | Output | Hình thức | Tiêu chuẩn |
|---|---|---|---|
| C1 | Eligibility matrix | Excel 10 dòng | Ticker, sector/mandate, source, date, cutoff, limitation |
| C2 | VTI/USMV explainer | 2 trang | Objective, construction, behavior, failure modes |
| C3 | Return check | Excel 1 trang | 2 tháng, formula, so CSV, sai lệch |
| C4 | Adverse evidence note | 500 từ | USMV vs VTI, calendar years, limits |
| C5 | Factor readout | 1–2 trang | Beta, alpha, CI, R², interpretation |
| C6 | Benchmark architecture | 1 trang | 4 lớp, dashboard |
| C7 | Independent critique | 3–5 câu | Selection/survivorship/data |
| C8 | Slide 4–6, 9 script | 1 trang | Speaking notes + 8 Q&A |

### 3.3.6. C kiểm ai, kiểm gì

| Người | C kiểm gì | Cách kiểm |
|---|---|---|
| Minh | 2 monthly returns, 96/36, ticker, cutoff | Excel; so raw/processed; kiểm source date |
| Minh | Factor interpretation | Đọc CI/p-value; kiểm claim “alpha” |
| D | Source claims, current vs 2022 | Mở source; kiểm ngày; kiểm wording |
| D | Benchmark consistency | Payment/mission/strategic/implementation |

### 3.3.7. Go further của C

1. **Benchmark architecture:** 4 lớp; tránh một benchmark cho mọi câu hỏi.
2. **Factor/regime behavior:** rolling beta; upside/downside capture; low-vol trong bull/bear.
3. **Tracking difference/implementation shortfall:** expense ratio, bid-ask, premium/discount, rebalancing.
4. **Survivorship/selection bias:** 10 mã sống sót; ảnh hưởng đến kết luận.
5. **ETF look-through:** USMV/VTI cùng nắm mega-cap; concentration ẩn.
6. **Methodology drift:** index method có thể đổi; current source không thay prospectus 2022.
7. **Adverse evidence:** USMV lag 45 điểm % cumulative; giữ nguyên, không tô hồng.

### 3.3.8. Câu hỏi bảo vệ C phải trả lời

- VTI là gì? USMV là gì? Khác nhau thế nào?
- Vì sao USMV được chọn nếu VTI thắng?
- USMV có phải “low risk” không?
- Vì sao 2015–2022, không phải 2010–2022?
- Universe có bias không?
- Alpha có chứng minh kỹ năng không?
- Vì sao không mua direct stocks?
- Benchmark nào dùng để đánh giá gì?
- Nếu USMV đổi index thì sao?
- Nếu VTI concentration cao thì sao?

### 3.3.9. Lỗi thường gặp

- Nói “USMV an toàn” — sai.
- Dùng current ETF holdings để giải thích 2023–2025.
- Đọc alpha mà bỏ CI/p-value.
- Chọn universe toàn mã nổi tiếng rồi nói “unbiased”.
- So sánh return mà bỏ risk.
- Dùng 36 tháng để kết luận dài hạn.

### 3.3.10. Thời gian

| Ngày | Giờ | Việc |
|---|---|---|
| 18/10 | 1h | Đọc memo; eligibility skeleton |
| 19/10 | 2h | Eligibility matrix; return check |
| 20/10 | 2h | VTI/USMV; adverse note; factor readout |
| 21/10 | 1h | Cross-check; slide script |
| 22/10 | 1h | Initial record universe/benchmark |

---

## 3.4. D — Mandate, Risk & Committee Analyst

### 3.4.1. Vai trò và câu hỏi trung tâm

D biến con số thành **quyết định của hội đồng**, giữ cho bài có **governance và phản biện**, và là người bảo đảm memo/slides trả lời đúng câu hỏi của đề. D không cần Python.

Câu hỏi D phải trả lời:

- Hội đồng đang quyết định gì, với giả định nào?
- 15% là gì, đo thế nào, vượt thì ai làm gì?
- Chính sách nào là hard rule, cái nào là parameter?
- Revised mandate đổi gì, và quyết định nào phải đổi?
- Nếu khuyến nghị sai, vì sao?

### 3.4.2. Phạm vi

**D sở hữu:**

- Rubric map.
- Assumption register (với Minh).
- Risk/15% note.
- Mini-IPS.
- Red-team memo.
- Revised mandate checklist.
- Q&A bank.
- Memo/slide integration, final read.
- Slides 1, 10, 12, 13.

**D không sở hữu:**

- Python/model (Minh).
- Bond math (B).
- ETF/source (C).
- Final numbers (Minh).

### 3.4.3. Đầu vào

- PDF 4 trang.
- `DECISION_LOG.md`, `TEAM_COMPLETION.md`, `MANDATE_REVISION.md`
- `deliverables/Kappa_Committee_Memo_Editable.md`
- `deliverables/Kappa_Initial_Decision_Record_Editable.md`
- `outputs/tables/whole_fund_stress.csv`
- `outputs/tables/risk_limit_sensitivity.json`
- `outputs/tables/mission_simulation.csv`
- `outputs/tables/all_bond_alternative.csv`

### 3.4.4. Quy trình từng bước

1. **Đọc PDF 4 trang**; lập rubric map 7 dòng: requirement → memo page → slide → CSV → owner.
2. **Lập assumption register** với Minh: case date, inflation, RF, ERP, A, costs, benchmark, rebalancing, no default, zero reinvestment.
3. **Viết risk/15% note:** metric (month-end unitized NAV, peak-to-trough, exclude programme payments), horizon, 12% review, 15% escalate, approver, expiry, limitation.
4. **Viết mini-IPS 2–3 trang:** purpose, objectives, constraints, eligible assets, liquidity, risk, benchmarks, rebalancing, monitoring, authority, amendment.
5. **Viết red-team memo 1 trang:** 3 lý do mạnh nhất để bác; evidence cần để đổi.
6. **Lập revised mandate checklist:** original requirement, revised wording, parameter affected, output required, approver.
7. **Xây Q&A bank 15–20 câu:** câu hỏi, owner, answer outline.
8. **Tích hợp memo/slides:** kiểm page limit, story, numbers, source; final read.
9. **Viết critique:** goal ambition, inflation, governance, liquidity, behavioral bias.

### 3.4.5. Output bắt buộc

| Mã | Output | Hình thức | Tiêu chuẩn |
|---|---|---|---|
| D1 | Rubric map | Excel 7 dòng | Requirement → page/slide/CSV/owner |
| D2 | Assumption register | Excel 10 dòng | Value, reason, source, owner, sensitivity |
| D3 | Risk/15% note | 1–2 trang | Metric, ladder, approver, expiry, limitation |
| D4 | Mini-IPS | 2–3 trang | Purpose, objectives, constraints, governance, benchmarks |
| D5 | Red-team memo | 1 trang | 3 lý do, evidence to change |
| D6 | Revised mandate checklist | 1 trang | Original/revised/parameter/output/approver |
| D7 | Q&A bank | 15–20 câu | Question, owner, answer outline |
| D8 | Memo/slide integration | 1 trang | Map, page limit, final read |
| D9 | Independent critique | 3–5 câu | Governance/risk/goal |

### 3.4.6. D kiểm ai, kiểm gì

| Người | D kiểm gì | Cách kiểm |
|---|---|---|
| Minh | 3 claims trọng yếu | Trace slide → memo → CSV → script |
| B | Bond/funding consistency | So 2,4m/3,6m/486.957; kiểm ngày |
| C | Source/benchmark claims | Mở source; kiểm current vs 2022 |
| All | Memo page limit và story | Đọc to; kiểm 8+1; kiểm decision-led |

### 3.4.7. Go further của D

1. **Risk capacity vs risk willingness:** 15% là “không thoải mái”, không phải “không thể chịu”.
2. **Governance of exceptions:** ai được giữ risk sau breach, evidence gì, expiry bao lâu.
3. **Pre-mortem:** 3 cách kế hoạch thất bại; indicator/action/owner.
4. **Mandate attribution:** tách thay đổi do trustee vs thay đổi tự nguyện của model.
5. **IPS/RACI:** ai chọn assumption, ai kiểm, ai phê duyệt.
6. **Board dashboard:** 1 trang, 10 tiles, traffic light.
7. **Behavioral risk:** anchoring vào 8m; recency bias sau 2023–2025; action bias khi drawdown.

### 3.4.8. Câu hỏi bảo vệ D phải trả lời

- 15% là gì? Có phải guarantee không?
- Vì sao không all-bond?
- Vì sao 2,5% inflation?
- Ai quyết định? Ai kiểm?
- Nếu revised mandate đổi payment thì sao?
- Nếu drawdown 18% thì làm gì?
- Nếu USMV lag 3 năm nữa thì sao?
- Có nên đổi goal không?
- Rủi ro lớn nhất là gì?
- Điều gì làm nhóm đổi ý?

### 3.4.9. Lỗi thường gặp

- Viết policy chung chung, không có metric/trigger.
- Nói “15% là max loss” — sai.
- Trộn hard rule với parameter.
- Memo quá 8 trang.
- Không có red team.
- Không có owner cho Q&A.

### 3.4.10. Thời gian

| Ngày | Giờ | Việc |
|---|---|---|
| 18/10 | 1h | Đọc PDF; rubric map |
| 19/10 | 2h | Assumption register; IPS skeleton |
| 20/10 | 2h | Risk note; red team; Q&A |
| 21/10 | 2h | Memo integration; rehearsal |
| 22/10 | 1h | Initial record; submit |
| 24–28/10 | 2h/ngày | Final memo/slides; revised mandate |

---

# PHẦN IV — MA TRẬN CHECK, CROSS-CHECK, VERIFY

## 4.1. Ma trận đầy đủ

| Sản phẩm | Owner | Checker chính | Checker phụ | Kiểm gì | Bằng chứng |
|---|---|---|---|---|---|
| Raw data & manifest | Minh | C | D | 2 tickers, ngày, hash, settings | Manifest, raw CSV |
| Monthly returns | Minh | C | B | 2 tháng, 96/36, missing | Excel, processed CSV |
| Bond valuation | B | Minh | D | Beta/Delta, YTM, duration, exact repricing | B2, bond_metrics |
| Funding cash flow | B | Minh | D | Từng năm, cumulative, double count | B1, funding_cashflows |
| Portfolio optimization | Minh | B | D | Constraints, cash, CE, sensitivity | A5, portfolio_candidates |
| Factor regressions | Minh | C | D | Beta, alpha, CI, R², interpretation | A6, factor_regressions |
| Evaluation | Minh | C | D | CAGR, vol, Sharpe, drawdown, adverse | A7, evaluation_performance |
| Universe/eligibility | C | Minh | D | Ticker, source date, cutoff | C1, eligibility_checks |
| VTI/USMV/benchmark | C | D | Minh | Source claims, current vs 2022 | C2, C6 |
| Risk/15%/IPS | D | B | C | Cash-flow priority, evidence, metric | D3, D4, whole_fund_stress |
| Revised mandate | Minh + D | B | C | Payment impact, growth impact, attribution | Scenario, table |
| Memo | D | Minh | B, C | Page limit, numbers, story, source | Memo, evidence map |
| Slides | D | Minh | B, C | Numbers, charts, flow, Q&A | PPTX/PDF |
| Contribution statement | Minh | D | B, C | Work, check, critique, truth | Statement |

## 4.2. Chi tiết từng check

### 4.2.1. B kiểm Minh: bond math và funding

- Mở `A4_bond_pack.xlsx`; chọn Beta và Delta.
- Tính lại cost, face, coupon, final payment bằng máy tính.
- So với `bond_metrics.csv` và `funding_cashflows.csv`.
- Kiểm đơn vị: USD, bond units, face value 1.000.
- Kiểm ngày: 2024, 2027, coupon annual.
- Kiểm exact repricing: +100bp, −100bp, steepener.
- Ghi check card C-02, C-03, C-04.

### 4.2.2. C kiểm Minh: returns và data

- Chọn 2 tháng bất kỳ trong 2015–2022.
- Lấy adjusted close từ `train_month_end_adjusted_prices.csv`.
- Tính `giá tháng này / giá tháng trước − 1`.
- So với `train_monthly_returns.csv`.
- Đếm 96 tháng; kiểm first/last; kiểm missing.
- Kiểm ticker/date/cutoff trong manifest.
- Ghi check card C-05, C-11.

### 4.2.3. D kiểm Minh: claims và evidence

- Chọn 3 số trên slide: 2,4m; 37,33%; 17,53%.
- Trace slide → memo → CSV/JSON → script.
- Kiểm wording: “68,48% là frequency, không phải probability”.
- Kiểm caveat: 36 tháng, survivor universe, revised data.
- Ghi check card C-07, C-08, C-10.

### 4.2.4. Minh kiểm B: bond và funding

- Mở B2; kiểm công thức Beta/Delta.
- Kiểm Delta face: 3,6m / 1,035 = 3.478.260,87.
- Kiểm coupon: 3.478.260,87 × 3,5% = 121.739,13.
- Kiểm funding: 2024, 2027; cumulative không âm.
- Kiểm rate note: YTM vs spot; duration vs convexity; exact repricing.
- Ghi check card C-02, C-03, C-04.

### 4.2.5. D kiểm B: memo/slide consistency

- So 2,4m/3,6m/486.957 trên memo và slide.
- Kiểm ngày 31/12/2024 và 31/12/2027.
- Kiểm “bonds cover payments without equity sale”.
- Kiểm “surplus coupons retained”.
- Ghi check card C-04.

### 4.2.6. Minh kiểm C: data/cutoff

- Mở C1; kiểm 10 tickers, sector, type.
- Kiểm source date ≤31/12/2022.
- Kiểm AAPL/MSFT fiscal year logic.
- Kiểm USMV source: July 2022 SEC-filed description; not current page.
- Kiểm 2 monthly returns.
- Ghi check card C-05, C-11.

### 4.2.7. D kiểm C: source claims

- Đọc C2/C5/C6; đánh dấu claim về 2022.
- Kiểm current source không được dùng làm bằng chứng 2022.
- Kiểm alpha CI: có đi qua 0 không.
- Kiểm benchmark: 4 lớp, không trộn.
- Ghi check card C-09.

### 4.2.8. B kiểm D: cash-flow priority

- Đọc D3/D4.
- Kiểm hard rule: payment trước growth.
- Kiểm 15% không được làm mất nghĩa vụ.
- Kiểm exception: không release payment asset.
- Ghi check card C-07.

### 4.2.9. C kiểm D: evidence

- Đọc D1/D5.
- Kiểm mỗi claim có source/output.
- Kiểm red team có evidence.
- Kiểm Q&A owner.
- Ghi check card C-10.

### 4.2.10. Final memo sign-off

- D đọc toàn bộ, kiểm page limit 8+1.
- Minh kiểm mọi số, evidence map.
- B kiểm bond/funding sections.
- C kiểm universe/ETF/evaluation sections.
- Mỗi người ký tên, ngày, phần mình.
- Không nộp nếu còn “TODO” hoặc “fix later”.

## 4.3. Mười check card trọng yếu

| ID | Claim | Owner | Checker | Cách kiểm | Kết quả kỳ vọng |
|---|---|---|---|---|---|
| C-01 | Tổng allocation = 12m | Minh | B | Cộng 4 dòng initial_allocation | 12.000.000 |
| C-02 | Beta trả 2,4m năm 2024 | B | Minh | 2.400 × 922,78; đáo hạn 2,4m | 2.214.672; 2.400.000 |
| C-03 | Delta trả 3,6m năm 2027 | B | Minh | 3,6m / 1,035; coupon 3,5% | 3.478.260,87; 121.739,13 |
| C-04 | Funding không âm mọi năm | B | Minh | Từng năm funding_cashflows | Cumulative ≥0 |
| C-05 | USMV CAGR 11,15%; VTI 22,22% | Minh | C | Tính từ evaluation path | Khớp |
| C-06 | Sharpe USMV 0,66; VTI 1,30 | Minh | C | Mean excess / sd × sqrt(12) | Khớp |
| C-07 | Stress −30% equity +100bp = 17,53% | Minh | D | Đọc whole_fund_stress; tính lại | 17,53% |
| C-08 | 68,48% là conditional frequency | Minh | D | Đọc mission_simulation; wording | Không gọi probability |
| C-09 | All-bond real 7,471m; thiếu 6,62% | Minh | B | Đọc all_bond_summary; tính | 7,471m; 6,62% |
| C-10 | A=4: USMV CE 3,84; VTI 3,13 | Minh | C | Đọc risk_preference; tính CE | Khớp |
| C-11 | 96 tháng train; 36 tháng eval | Minh | C | Đếm sample; first/last | 96; 36 |

## 4.4. Check card template

| Trường | Nội dung |
|---|---|
| Check ID | C-XX |
| Claim | Kết luận được kiểm |
| Owner | Người tạo |
| Checker | Người kiểm độc lập |
| Input | File/nguồn/dòng |
| Method | Công thức hoặc bước |
| Checker result | Số/kết luận tự tính |
| Difference | Khớp/lệch bao nhiêu |
| Caveat | Điều chưa kiểm |
| Decision | Pass/Fix |
| Date | Ngày thực hiện |

## 4.5. Lỗi check thường gặp

- “Em đọc rồi, thấy đúng” — không phải check.
- Chạy lại đúng script của Minh — reproducibility, không phải independent.
- Kiểm slide khớp memo, nhưng cả hai cùng sai từ CSV.
- Kiểm số mà không kiểm đơn vị/ngày.
- Kiểm kết quả mà không kiểm caveat.
- Ký tên nhưng không ghi ngày/người kiểm.
- Sửa số sau khi check mà không check lại.

---

# PHẦN V — GO FURTHER EXTRA THEO TỪNG MẢNG

## 5.1. Bảng ưu tiên

| Vùng | Extra | Câu hỏi nghiên cứu | Output | Vì sao ấn tượng | Công sức | Owner |
|---|---|---|---|---|---|---|
| Mandate | Funding ratio + shortfall severity | “Nếu hụt, hụt bao nhiêu?” | 1 trang + chart | Đi từ probability sang severity | TB | Minh |
| Mandate | Decision threshold map | “Điều gì làm đảo quyết định?” | Heatmap A × ERP | Decision architecture | TB | Minh + D |
| Bond | Key rate/curve shape | “Steepener ảnh hưởng gì?” | Bảng 3 kịch bản | Beyond parallel shift | TB | B |
| Bond | Liquidity/settlement | “Có trả đúng ngày không?” | Checklist 10 bước | Operational realism | Thấp | B |
| Data | Vintage audit | “Dữ liệu 2026 có giống 2022?” | Data lineage map | Reproducibility maturity | TB | Minh + C |
| Portfolio | Covariance robustness | “Optimizer có ổn định?” | Sample vs single-index + turnover | Model risk | TB | Minh |
| Factor | Alpha multiple testing | “Alpha có thật hay do search?” | Rolling alpha + CI | Statistical honesty | TB | Minh + C |
| Evaluation | Adverse evidence + reversal | “USMV lag thì sao?” | Threshold table | Intellectual honesty | Thấp | C + D |
| Mandate response | Original vs revised bridge | “Đổi vì trustee hay vì model?” | Attribution table | No hindsight | TB | D + Minh |
| Memo | Board dashboard 1 trang | “10 phút hiểu gì?” | 10 tiles | Communication | Thấp | D |
| Memo | Pre-mortem/reverse stress | “Kế hoạch fail thế nào?” | 1 trang failure map | Risk maturity | Thấp | D + B |
| Slides | Q&A bank + mock viva | “Ai trả lời câu nào?” | 20 Q&A | Accountability | Thấp | D |

## 5.2. Minimum viable vs stretch

| Mức | Phải có | Nên có | Có thì tốt |
|---|---|---|---|
| 22/10 | Initial record 2 trang; Python; data record; freeze | Assumption register; bond pack | White paper outline |
| 29/10 | Memo 8+1; slides PDF/PPTX; code/data; contribution | Dashboard; red team; Q&A | Lifecycle; shortfall severity; decision map |
| Research highlight | 1–2 extra có số | 3–4 extra | 5+ extra |

## 5.3. Những thứ không nên làm

- Thêm machine learning, Black-Litterman, neural network chỉ để trông phức tạp.
- Copy allocation của Yale/Harvard khi mandate không cho phép.
- Dùng dữ liệu 2023–2025 để thiết kế lại quyết định 2022.
- Gọi 68,48% là xác suất; gọi 15% là guarantee.
- Đưa private equity, hedge fund, vàng, quốc tế vào original case.
- Viết white paper 40 trang trong khi memo 8 trang chưa xong.
- Để AI viết conclusion mà không ai hiểu.

---

# PHẦN VI — DELIVERABLES, DEADLINE, MẪU BIỂU

## 6.1. Checklist 22/10 — initial record

- [ ] Đúng 2 trang, có universe, estimation window, benchmark, dollar allocation, assumptions, evaluation/rebalancing rule.
- [ ] Allocation cộng đủ 12 triệu USD, gồm costs.
- [ ] Nêu rõ 2,4m/3,6m/8m real.
- [ ] Nêu rõ 15% là vấn đề chưa định nghĩa, có proposed metric.
- [ ] Python file đang làm việc, chạy được.
- [ ] Data record có ngày, ticker, source, settings.
- [ ] Policy frozen, hash lưu.
- [ ] Receipt nộp bài.

## 6.2. Checklist 23/10 — revised mandate

- [ ] Lưu nguyên bản, ngày, nguồn.
- [ ] Không sửa bản 22/10.
- [ ] Liệt kê từng yêu cầu đổi.
- [ ] Xác định parameter bị ảnh hưởng.
- [ ] Tạo scenario copy, không overwrite frozen policy.
- [ ] Tính lại payment coverage, growth, risk, goal.
- [ ] Bảng original/revised/difference/cause.
- [ ] Ghi rõ đâu là thay đổi của trustee, đâu là model.
- [ ] Cập nhật decision log.

## 6.3. Checklist 29/10 — final archive

- [ ] Memo ≤8 trang + ≤1 reference.
- [ ] Slides PDF + editable PPTX.
- [ ] Python scripts/notebook, environment, rebuild instructions.
- [ ] Raw downloads, processed data, outputs, source record.
- [ ] 22/10 submission + decision log.
- [ ] Contribution statement + another member’s check + each critique.
- [ ] AI disclosure.
- [ ] Page limit, font, charts, tables.
- [ ] Archive hash, receipt.

## 6.4. Page limit và file name

| File | Limit | Ghi chú |
|---|---|---|
| `Kappa_Committee_Memo.pdf` | 8 trang + 1 ref | Không nhét white paper vào |
| `Kappa_Initial_Decision_Record.pdf` | 2 trang | Đúng yêu cầu |
| `Kappa_Committee_Presentation.pdf` | 13–15 slide | PDF + PPTX |
| `A4_bond_pack.xlsx` | Không limit | Nguồn cho B |
| `A8_scenario_workbook.xlsx` | Không limit | S0–S9 |
| `D7_QA_bank.md` | 2–3 trang | 20 câu |

## 6.5. Daily plan

| Ngày | Minh | B | C | D |
|---|---|---|---|---|
| 18/10 | Đọc PDF, data pack, rebuild | Đọc PDF/memo, timeline | Đọc memo, eligibility | Đọc PDF, rubric |
| 19/10 | Returns, bond pack, portfolio skeleton | Beta/Delta, funding | Eligibility, 2 returns | Assumption, IPS |
| 20/10 | Factor, evaluation, scenario | Rate note, liquidity | VTI/USMV, adverse | 15%, red team, Q&A |
| 21/10 | Cross-check, evidence map | Cross-check bond | Cross-check source | Memo integration |
| 22/10 | Initial record, submit | Bond section | Universe/benchmark | Final read, submit |
| 23/10 | Revised scenario | Payment impact | Growth impact | Attribution |
| 24–28/10 | Memo/slides, QA | Bond slides | ETF slides | Memo/slides, rehearsal |
| 29/10 | Archive, hash | Sign-off | Sign-off | Sign-off |

## 6.6. Group risk register

| Rủi ro | Khả năng | Tác động | Giảm thiểu | Owner |
|---|---|---|---|---|
| Minh quá tải | Cao | Cao | Timebox; B/C/D viết phần mình; không làm hộ | Minh |
| B/C/D không quen Excel | TB | TB | Template; 1:1; video 10 phút | Minh |
| Data Yahoo/French lỗi | TB | Cao | Lưu raw; log; rebuild offline | Minh |
| Revised mandate đến muộn | TB | Cao | Chuẩn bị checklist; không đoán | D |
| AI policy chưa rõ | Cao | Cao | Hỏi giảng viên; disclose; lưu email | D |
| Memo quá trang | TB | Cao | Viết decision-led; cắt exhibit | D |
| Số lệch giữa slide/memo | Cao | Cao | Evidence map; freeze; sign-off | Minh |
| Contribution không khớp | TB | Cao | Log hàng ngày; checker ký | All |
| File hỏng/merge lỗi | TB | Cao | Version; backup; zip | Minh |

## 6.7. Contribution statement template

| Member | Substantive work | Evidence file | Checked by | Check result | Critique | Can explain? |
|---|---|---|---|---|---|---|
| Minh | | | B/C/D | | | Yes/No |
| B | | | Minh/D | | | Yes/No |
| C | | | Minh/D | | | Yes/No |
| D | | | B/C | | | Yes/No |

> Chỉ điền sau khi việc đã làm. Không ghi “đã kiểm” nếu chưa kiểm. Không ghi critique hộ người khác.

## 6.8. Decision log template

| Ngày | Decision | Evidence | Owner | Approver | Reversal condition |
|---|---|---|---|---|---|
| | | | | | |

## 6.9. Q&A bank 20 câu

| # | Câu hỏi | Người trả lời | Ý chính |
|---:|---|---|---|
| 1 | Vì sao không all-bond? | B + D | All-bond đủ nominal nhưng thiếu real goal 6,62%; trade-off |
| 2 | Vì sao USMV thay vì VTI? | C + Minh | A=4; CE 3,84 vs 3,13; đảo ở A<2,58/ERP>6,98% |
| 3 | 15% có được bảo đảm? | D + B | Không; stress 17,53%; threshold not floor |
| 4 | Alpha có chứng minh kỹ năng? | C + Minh | CI; zero forecast alpha; multiple testing |
| 5 | Vì sao 2,5% inflation? | D + Minh | Planning assumption; 2–5% sensitivity |
| 6 | Có data leakage không? | Minh + C | Policy frozen trước eval; 2023–2025 không re-estimate |
| 7 | Vì sao 96 tháng? | Minh | ≥60; 96 common; 60-month sensitivity |
| 8 | Vì sao không mua direct stocks? | Minh + D | CE gain nhỏ; concentration; model error |
| 9 | Vì sao Delta face 3,478m? | B | 3,6m / 1,035; coupon 3,5% |
| 10 | Nếu rates +200bp? | B | Price fall; cash flow unchanged; hold-to-maturity |
| 11 | Nếu payment date holiday? | B | Settlement checklist; pre-fund |
| 12 | Nếu inflation 4%? | Minh + D | Target 10,949m; required CAGR 6,45%; frequency 48,05% |
| 13 | Nếu revised mandate đổi? | D + Minh | Scenario copy; original/revised/difference/cause |
| 14 | Benchmark nào? | C + D | 4 layers: payment, mission, strategic, implementation |
| 15 | Rủi ro lớn nhất? | D | Mission failure; payment/liquidity; model risk |
| 16 | Điều gì làm đổi ý? | D + Minh | A, ERP, inflation, mandate, USMV behavior |
| 17 | Người không code đóng góp gì? | B/C/D | Bond, universe/source, policy/risk, checks |
| 18 | Làm sao biết data sạch? | C + Minh | Raw, hash, manifest, 96/36, no fill |
| 19 | Vì sao không đổi goal? | D | Có thể, nhưng phải quantified trade-off |
| 20 | AI đã làm gì? | Minh + D | Assist; human check; disclose; no autonomous decision |

## 6.10. Cách dùng Q&A bank

- Mỗi câu có **một owner chính** và **một người support**; không để “cả nhóm cùng trả lời”.
- Trả lời theo 3 câu: **kết luận → bằng chứng → giới hạn**. Không đọc slide.
- Tập nói 60–90 giây mỗi câu; câu nào quá 2 phút là chưa hiểu.
- Nếu không biết: “Em sẽ kiểm lại trong file X và trả lời sau” — không đoán.
- Câu 17–20 dùng cho contribution statement và AI disclosure; cả nhóm phải trả lời được.
- Rehearsal 2 vòng: vòng 1 mỗi người 10 câu; vòng 2 random 5 câu, người khác phản biện.

---

# PHỤ LỤC

## A. Glossary

| Thuật ngữ | Nghĩa | Thuật ngữ | Nghĩa |
|---|---|---|---|
| ETF | Giỏ chứng khoán mua bán như cổ phiếu | VTI | ETF thị trường cổ phiếu Mỹ rộng |
| USMV | ETF cổ phiếu Mỹ theo chiến lược biến động thấp | YTM | Lợi suất nội bộ nếu giữ đến đáo hạn |
| Duration | Độ nhạy giá trái phiếu với lãi suất | Convexity | Điều chỉnh phi tuyến của duration |
| bp | Basis point, 0,01% | CE | Certainty equivalent |
| A | Risk aversion | Sharpe | Excess return / volatility |
| Drawdown | Mức giảm từ đỉnh | Funding ratio | Assets / nghĩa vụ |
| Shortfall | Thiếu hụt so với mục tiêu | IPS | Investment Policy Statement |
| RACI | Responsible, Accountable, Consulted, Informed | ALM | Asset-liability management |
| LDI | Liability-driven investment | Tracking error | Độ lệch so với benchmark |
| Survivorship bias | Chỉ nhìn mã sống sót | Look-ahead bias | Dùng thông tin tương lai |
| Data vintage | Phiên bản dữ liệu tại thời điểm tải | | |

## B. Nguồn nội bộ

- `reference/BFIN-WS2026-Group_Assignment.pdf`
- `README.md`, `CHECKPOINT.md`, `DECISION_LOG.md`
- `EVIDENCE_MAP.md`, `TEAM_COMPLETION.md`, `MANDATE_REVISION.md`
- `deliverables/Kappa_Requirements_and_Data_Guide.md`
- `deliverables/Kappa_Committee_Memo_Editable.md`
- `deliverables/Kappa_Initial_Decision_Record_Editable.md`
- `policy/frozen_policy.json`
- `outputs/tables/`

## C. Câu chốt cho cả nhóm

> Chúng ta không cố chứng minh mình thông minh. Chúng ta cố chứng minh rằng **mọi khuyến nghị đều có thể truy vết, có người kiểm, có giới hạn, và có điều kiện đảo chiều**. Đó là thứ một hội đồng đầu tư thực sự cần.
