# P11｜Parquet、DuckDB、Query Profiling 與 Spark 基礎

> 週次 W41–W44｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：理解單機與分散式運算的成本，能做公平的 Benchmark 並挑選合適工具。

**前置條件**：P02 已能讀查詢計畫、P03 資料結構穩定、P06 可重建環境。

## 需要理解的原理

- CSV vs Parquet；row vs column、compression、row group、predicate/column pushdown
- DuckDB SQL in-process、PostgreSQL index vs analytic scan、I/O 與記憶體
- Spark DataFrame、lazy evaluation、partition、shuffle、skew、local mode
- Benchmark 設計：相同資料/計算/硬體、warm-up、重複測量、結果等價

## 每週教學與工作單

### W41｜資料格式

**原理與研究**：測試 10 萬、100 萬、500 萬筆的 synthetic order_lines，控制 seed。

**本人實作**：CSV 與 Parquet 產出相同 schema；記錄檔案大小、讀取、欄投影。

**應交證據**：input hash、schema 一致性與格式測試報告

### W42｜DuckDB/Profile

**原理與研究**：了解 analytical query 與 OLTP query 的差別、profile 跟 index。

**本人實作**：同樣的 group-by/filter 在 pandas/DuckDB/Postgres 執行比較。

**應交證據**：命令、計畫、時間、peak memory、結果核對

### W43｜Spark local

**原理與研究**：了解 action/transform、shuffle、partition count、資料傾斜。

**本人實作**：用 Spark local mode 做同一 group-by，觀察 plan與 stage。

**應交證據**：Execution Plan、partition 實驗、功能測試

### W44｜公平比較與選型

**原理與研究**：比較初始啟動成本、記憶體、複雜度和部署維運成本。

**本人實作**：至少測 3 次、給中位數與波動範圍；提出「何時不用 Spark」結論。

**應交證據**：Benchmark Methodology + raw results + Recommendation

## 階段專題

用同一組合成資料完成「每月商品類別淨收款」；確保每種引擎都處理相同退款與 null 規則。

## Acceptance Criteria（逐條勾核）

- [ ] 資料量、欄位、seed、硬體、版本、cache 狀態完整列出。
- [ ] 不同引擎的查詢結果逐組一致；浮點誤差/排序差異有說明。
- [ ] 量測至少重複 3 次；不僅選最好的那一次。
- [ ] Parquet compression 與 column pruning 解釋正確。
- [ ] 能從 Spark Explain 說明 Shuffle 為何發生；Spark local 不宣稱已驗證真實多節點效能。
- [ ] 根據需求提供首選與替代方案，包含維運成本。

## 必須執行的故障/反例測試

- 將資料量縮至數千筆，看看 Spark 啟動成本是否反而較高。
- 只更改排序或 Null 處理造成結果不同，要求先修正語意再比較速度。
- 導入 highly skewed key，觀察 aggregation 或 shuffle 的影響。

## 導師現場追問（不可只複述 AI 答案）

- 為什麼 Parquet 對分析常有優勢卻不適合所有用途？
- Spark `repartition` 和 `coalesce` 的不同？
- 如何證明 benchmark 不是受 cache 或不公平 I/O 條件影響？

## 常見誤區與邊界

不為了作品集架設高費用 Spark Cluster；沒有數據支持時不可宣稱十倍加速。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
