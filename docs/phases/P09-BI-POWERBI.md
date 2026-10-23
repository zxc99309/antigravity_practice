# P09｜Power BI、DAX、資料模型、交付與權限

> 週次 W33–W36｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：建立可被業務每天使用、能用 SQL 交叉驗證且有權限與刷新策略的 BI 報表。

**前置條件**：P08 的指標字典已通過審查；Mart 資料可信且可穩定刷新。

## 需要理解的原理

- Power Query / M 與資料來源清理、Query Folding 觀念
- Star Schema、Relationship cardinality、日期表、單向/雙向過濾的取捨
- DAX Measure vs Calculated Column、Row/Filter Context、CALCULATE
- Dashboard UX、RLS、refresh、incremental refresh 的條件與授權、發布與移交

## 每週教學與工作單

### W33｜資料模型

**原理與研究**：比較將所有資料攤平 vs 星型模型，說明 Fact/Dimension。

**本人實作**：使用可靠 Mart 建立 Power BI Model 和日期表，定義 relationship 方向。

**應交證據**：模型圖、資料來源、關聯基數核對

### W34｜DAX

**原理與研究**：學習 SUM、DIVIDE、CALCULATE、Filter Context；比較各種 Filter 互動。

**本人實作**：實作至少 8 個 measure：淨收款、訂單數、客單價、MoM、退款率等。

**應交證據**：逐項 SQL 預期 vs DAX 實際差異表

### W35｜報表與治理

**原理與研究**：練習卡片、趨勢、明細、切片器、資料新鮮度；最小必要權限。

**本人實作**：完成主管頁面、明細鑽取、異常/最後刷新時間，測試 RLS。

**應交證據**：畫面與敏感資訊檢查、RLS 測試紀錄

### W36｜驗收與交接

**原理與研究**：以業務視角測跨頁/日期/地區篩選，設定可靠刷新。

**本人實作**：交付使用者指南、SQL 對帳與刷新失敗處理方式。

**應交證據**：BI 驗收表、可重現截圖或本地 PBIX 說明

## 階段專題

建立「零售營運管理儀表板」，包含營運總覽、商品、顧客留存和退款頁。若無 Windows/Power BI，可先以另一 BI 工具完成共通能力，註明 Power BI 專項 NotRun，日後補驗。

## Acceptance Criteria（逐條勾核）

- [ ] 至少 8 個 measure 與指標字典一一對應。
- [ ] 切不同月份/商品/地區時，3 個重要 KPI 與 SQL 核對一致。
- [ ] 修正空分母與 NULL；保留日期表及正確時間關聯。
- [ ] 能以測試角色驗證 RLS；不能只憑「設定畫面」證明隔離。
- [ ] 明確顯示 Last Refresh 與資料時間上限；刷新失敗不靜默顯示舊數據為最新。
- [ ] 具備資料來源、刷新、權限、故障處理和業務操作文件。

## 必須執行的故障/反例測試

- DAX 計算客單價時忽略篩選造成所有部門/商品相同值，定位 Filter Context。
- 把商品與退款兩個事實表直接多對多相連，造成數字異常。
- 模擬 1 天未更新，報表應如何標示 stale data。

## 導師現場追問（不可只複述 AI 答案）

- Measure 與 Calculated Column 差異？
- RLS 為什麼不是依靠前端隱藏欄位？
- 如何測 SQL 與 DAX 的日期邊界一致？

## 常見誤區與邊界

使用 PBIX、公開分享、部署或刷新功能前先核對授權；不得發佈含敏感資訊的公開 Dashboard。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
