# P03｜ETL/ELT、多來源擷取、增量與維度建模

> 週次 W09–W12｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：把單次手動分析轉為多來源、可追蹤的 Raw → Staging → Mart 管線，能建立增量與更新歷史。

**前置條件**：P02 Gate 通過；已理解 key、transaction、JOIN 基數。

## 需要理解的原理

- Extract 與 Load 的邊界、全量/增量、Watermark、Source Cursor、rate limit
- Raw snapshot、checksum、source metadata、Schema Registry/Contract 觀念
- 合成訂單與退款的業務鍵、event_time/updated_at/ingested_at、Late Arriving Data
- Star Schema、fact grain、dimension、surrogate key、SCD Type 1/2、Aggregation

## 每週教學與工作單

### W09｜來源與契約

**原理與研究**：設計合成 order、order_line、payment、refund、product、customer，定義 row grain 與鍵。

**本人實作**：新增可設定 seed 的資料產生器、Raw 契約及來源 manifest。

**應交證據**：Schema + 欄位字典 + 來源與修訂歷史

### W10｜完整匯入

**原理與研究**：用 Python 讀合成 CSV 與模擬 API（可用本地 fixture）；區分 Extract/Load。

**本人實作**：建立 Raw ingestion 與批次資訊表；保留檔 checksum、run_id、rows。

**應交證據**：同輸入兩次批次的原始可追溯證據

### W11｜增量與晚到

**原理與研究**：學習嚴格大於 `updated_at` 會漏同秒資料；比較 tie breaker/overlap。

**本人實作**：設計 incremental cursor + UPSERT；模擬已處理日期的更新與晚到退款。

**應交證據**：首次/增量/重跑/晚到資料對帳

### W12｜資料建模

**原理與研究**：明確區分訂單行粒度、退款粒度與付款粒度；介紹 SCD1/2。

**本人實作**：建立日期維度、產品維度、訂單明細事實表；驗算淨收款教學口徑。

**應交證據**：ERD + DDL + SQL 三組指標核對

## 階段專題

建立「每日電商交易資料」管線，包含至少兩種來源方式（CSV、模擬 HTTP API），同一組來源可設計漏資料、晚到資料與版本更新。

## Acceptance Criteria（逐條勾核）

- [ ] Raw 可追溯來源/批次與檔案雜湊；來源資料在清理時不被覆蓋。
- [ ] Staging 明確型別轉換、資料拒絕策略及留存原始列定位。
- [ ] 同筆訂單更新後採明確版本規則，不憑列順序決定勝出版本。
- [ ] 支援 Full Load + Incremental + 指定日期回補的基本設計；可說明 watermark 缺陷。
- [ ] Fact/Dimension 明確 grain、key、關聯，避免付款與退款 JOIN 導致倍增。
- [ ] 可用獨立 SQL 驗證 Raw→Staging→Mart 筆數與教學淨收款。

## 必須執行的故障/反例測試

- 兩筆具有相同 `updated_at` 但不同 `order_id` 的更新，檢驗 cursor 遺漏。
- 訂單付款隔天退款；比較依付款日期或退款日期計算的差異。
- 同訂單兩次部分付款 + 兩次退款造成 JOIN 4 列；修正聚合粒度。

## 導師現場追問（不可只複述 AI 答案）

- 何時使用 SCD Type 2，而不是每次直接覆寫 master？
- Raw 與 Staging 的資料丟失責任如何界定？
- ELT 與 ETL 的選擇與數據治理有何關係？

## 常見誤區與邊界

不要用真實公開顧客資料來做訓練；不要用自動補平均值處理缺失交易金額。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
