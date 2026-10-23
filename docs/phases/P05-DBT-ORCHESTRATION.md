# P05｜dbt、工作流編排、排程、回補

> 週次 W17–W20｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：把已有的 SQL Transform 與 Python Extract 按相依關係自動執行，失敗時可以定位、重試與回補。

**前置條件**：P04 已完成品質規則與故障復原基本操作。

## 需要理解的原理

- dbt source、ref、staging/intermediate/mart、generic/singular tests
- dbt incremental model、documentation、lineage、不同 SQL warehouse adapter 的差異
- DAG、task idempotency、schedule interval、logical date、catchup/backfill
- retry/timeout、failure callback、task boundary、依賴重算、每日 SLA

## 每週教學與工作單

### W17｜dbt 基礎

**原理與研究**：了解 ELT 在資料庫執行轉換，區分 SQL 模型與 Python extraction。

**本人實作**：將 P03 的 staging/mart SQL 搬入 dbt，設定 source freshness、unique、not_null、relationships tests。

**應交證據**：dbt run/test 及失敗案例

### W18｜增量與文件

**原理與研究**：了解 dbt incremental 策略與 unique_key 並非萬能保證。

**本人實作**：建立一個 incremental model，文件化 lineage、口徑與變更策略。

**應交證據**：docs 和重複/晚到輸入結果核對

### W19｜DAG

**原理與研究**：理解 DAG 與 cron 的差別；先以最小單機部署。

**本人實作**：建立 extraction→raw→dbt→quality→report 的依賴 DAG。

**應交證據**：成功執行、失敗 task 與依賴跳過證據

### W20｜追溯與恢復

**原理與研究**：理解排程時間、資料時間、手動觸發不完全相同。

**本人實作**：讓前一日工作失敗，演練 retry/補跑，確認不重複資料且下游更新正確。

**應交證據**：時間線、回補命令、最終對帳

## 階段專題

建立每日零售資料流程並用 DAG 視覺化依賴；使用本機 PostgreSQL 和合法的 dbt adapter；外部服務依賴須可用本機 fake/fixture 取代。

## Acceptance Criteria（逐條勾核）

- [ ] dbt 至少 3 類模型、4 類 tests 且可刻意讓一項失敗。
- [ ] DAG 獨立 Task、符合依賴、可控 timeout/retry，Log 具有 run id。
- [ ] 能區分 DAG run 時間、實際來源資料日期與業務報表日期。
- [ ] 重跑指定日期不造成重複，回補後報表及品質測試重新核對。
- [ ] 能說明小型簡單排程何時用 cron 就夠了、何時才值得用 Airflow。
- [ ] 紀錄 Airflow/dbt 使用版本、部署方式、資源限制。

## 必須執行的故障/反例測試

- 刻意讓 quality check 失敗：下游不得把錯誤資料發成正式指標。
- 模擬前一天失敗、今天成功：手動補跑前一天，證明不覆寫今天。
- dbt incremental model 資料更新導致錯誤，判斷增量策略與回補範圍。

## 導師現場追問（不可只複述 AI 答案）

- DAG task 為何應冪等？
- Airflow task retry 跟資料庫 transaction 的邊界如何設計？
- dbt tests 與 P04 的來源資料契約差別在哪？

## 常見誤區與邊界

Airflow 不是用來承載任意長時間的資料處理程式的唯一方案；先有可測的 pipeline，再談 orchestrator。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
