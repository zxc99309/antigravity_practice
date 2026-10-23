# P02｜PostgreSQL、SQL、資料庫設計與效能

> 週次 W05–W08｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：能不用 Pandas 獨立在 SQL 中寫出正確指標、辨識 JOIN 倍增，並操作受控交易及資料約束。

**前置條件**：P01 Gate 通過；可以從 CLI 穩定讀取合成 CSV。

## 需要理解的原理

- 關聯式模型、資料正規化、PK/FK/UNIQUE/CHECK/NOT NULL、合成 key
- SELECT、JOIN、GROUP BY/HAVING、CASE/NULL、CTE、Window Function
- DML、UPSERT、ACID、transaction isolation、locking、rollback
- B-tree index、選擇性、EXPLAIN (ANALYZE, BUFFERS)、查詢成本與基數估算

## 每週教學與工作單

### W05｜模型與資料字典

**原理與研究**：設計 departments、employees、salary_history；指出員工姓名不是穩定 key。

**本人實作**：先提交 ERD、DDL、資料字典、Constraints，再匯入資料。

**應交證據**：建表 SQL、資料契約、反例 insert 被約束拒絕

### W06｜SQL 正確性

**原理與研究**：練習 JOIN、LEFT JOIN、NULL、GROUP BY、CASE、HAVING、存在性與去重。

**本人實作**：完成至少 10 題；包含刻意一對多 JOIN 膨脹的修正。

**應交證據**：每題 SQL、預期 row count、結果截取

### W07｜進階 SQL 與交易

**原理與研究**：練習 ROW_NUMBER/DENSE_RANK/LAG/SUM OVER、CTE、隔離層級、ROLLBACK。

**本人實作**：再完成至少 10 題；演示無效資料造成 Transaction rollback，避免半成品。

**應交證據**：Window 結果 + 前後 row count + rollback 記錄

### W08｜查詢計畫與 DB API

**原理與研究**：了解 Index 的寫入成本、查詢計畫、Connection pooling 基礎。

**本人實作**：以 Python 匯入 PostgreSQL；在同一資料量比較兩種查詢計畫，標註設備與測量限制。

**應交證據**：EXPLAIN 記錄、執行時間、結果一致性

## 階段專題

從既有 1,000 筆合成員工 CSV 建立合格匯入流程。**必須先補 `employee_id` 的合成規格**；來源快照列號僅能追蹤該次檔案，不能冒充跨批次人員身分。

## Acceptance Criteria（逐條勾核）

- [ ] 所有表具明確粒度、Key、Constraint；至少一個 FK violation 測試。
- [ ] 至少 20 題 SQL；其中各有 JOIN、Window、CTE、NULL 邊界題。
- [ ] 在一對多 JOIN 範例中先展示錯誤倍增，再修正並說明原因。
- [ ] 以交易測試成功 Commit 和失敗 Rollback，證明目標資料正確。
- [ ] 至少兩個 EXPLAIN 與查詢結果等價性證據；不以小表時間差斷言所有環境最佳。
- [ ] 可用 SQL 核對 Excel/Pandas 的統計結果，含 NULL 與四捨五入差異。

## 必須執行的故障/反例測試

- 員工姓名重複，若當 PK 應出現何種錯誤？設計修復。
- salary_history 一人三期資料導致員工計數三倍；修復 SQL。
- 在 Transaction 內故意插入違反 FK 的資料，證明 rollback。

## 導師現場追問（不可只複述 AI 答案）

- `COUNT(*)`、`COUNT(column)`、`COUNT(DISTINCT key)` 有何差別？
- Window 和 Group By 改變資料粒度有何不同？
- Index 為何不一定讓查詢更快？

## 常見誤區與邊界

效能測試必須保持結果相同，報告資料量與 buffer/cache；不能用 1,000 列的結果宣稱 index 效益。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
