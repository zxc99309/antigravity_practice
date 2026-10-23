# P04｜資料品質、容錯、冪等、重跑與事件復原

> 週次 W13–W16｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：讓一條成功過的管線能在失敗、重複、延遲與不完整資料下保持一致性。

**前置條件**：P03 可跑通 Full / Incremental，且已產生可查證批次資訊。

## 需要理解的原理

- Data Contract：schema/unique/null/referential/range/freshness/volume
- Idempotent processing、transaction boundary、dedupe、quarantine
- Retryable vs non-retryable error、exponential backoff、HTTP 429、timeout
- Backfill、Checkpoint、lock/concurrency、data reconciliation、incident report

## 每週教學與工作單

### W13｜品質契約

**原理與研究**：將 P03 的欄位定義變成可執行的資料驗證。

**本人實作**：做 schema、null、unique、FK、range、freshness、volume rule；隔離拒絕的列。

**應交證據**：規則表、錯誤樣本、警告/拒絕策略

### W14｜冪等與交易

**原理與研究**：區分 at-least-once、atomic commit、exactly-once 的宣稱限制。

**本人實作**：相同批次重跑三次、在寫入途中強制中斷，證明最終一致。

**應交證據**：前後 hash/count/key 唯一性與 transaction log

### W15｜網路與併發

**原理與研究**：將 429、502、timeout、永久 4xx 分類，設計 bounded retry。

**本人實作**：模擬 429 Retry-After、來源超時與兩次排程重疊；用 lock/唯一鍵等策略。

**應交證據**：retry 次數/間隔/最終告警與鎖競爭結果

### W16｜回補與事故

**原理與研究**：制定 backfill window、依賴表刷新順序、影響分析。

**本人實作**：刪除 TEST 中某日資料，按 runbook 安全回補並寫 Postmortem。

**應交證據**：資料對帳 + 事故時間線 + 預防措施

## 階段專題

實施 [DE-003 故障與回補](../work-orders/DE-003-INCIDENT-BACKFILL.md)；導師必須事先固定預期 row-count/hash 與故障注入範圍，不可事後調整答案。

## Acceptance Criteria（逐條勾核）

- [ ] 資料品質至少六類規則可測且有明確 fail/warn/quarantine 政策。
- [ ] 相同來源重跑三次，業務唯一鍵、筆數、金額不變。
- [ ] 半途失敗後可恢復，不產生無主資料；日誌可追溯失敗 run。
- [ ] 遇到 429 有限次退避並遵守 Retry-After；非重試錯誤不無限循環。
- [ ] 手動 backfill 可選日期並對帳；記錄何時須重新計算 Mart/BI。
- [ ] 有一次實際故障注入報告、復原前後證據與 Runbook。

## 必須執行的故障/反例測試

- 在 DB commit 之前 kill process，查看 Raw 與 Mart 是否半成品。
- 讓 API 前兩次回傳 429、第三次成功；再讓連續錯誤超過上限。
- 重疊執行同一日期的兩個工作，確認不產生雙倍。
- 人工加入不合法退款（負值、未知訂單）看 quarantine。

## 導師現場追問（不可只複述 AI 答案）

- 為何只是加 `ON CONFLICT DO NOTHING` 不等於整條管線冪等？
- 重試何時會造成重複外部副作用？
- 要如何證明「資料補齊」不等於「資料全對」？

## 常見誤區與邊界

不能只檢查輸出存在；至少核對 row count、key 集合、數值總和與資料版本。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
