# P06｜Docker、CI/CD、基礎雲端、權限與成本

> 週次 W21–W24｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：在乾淨環境重建、測試、執行資料平台；理解最小權限與運行成本，不依賴個人筆電。

**前置條件**：P05 有可重現的完整本地管線與測試。

## 需要理解的原理

- 容器、映像、volume、network、healthcheck、持久性、不同環境
- GitHub Actions 的 CI gates、依賴快取、整合測試、artifact retention
- Secrets 與最小權限、公開資料庫風險、資料備份/還原、PII 遮罩
- 雲端 storage、Job、資料倉儲、IAM、成本/費用上限

## 每週教學與工作單

### W21｜Compose

**原理與研究**：說明 image/container/volume/network 不同；畫資料持久化邊界。

**本人實作**：Compose 啟動 Python + PostgreSQL（Airflow 可做選修）；清除容器後重建。

**應交證據**：重建步驟、schema 初始化、資料恢復證據

### W22｜CI

**原理與研究**：理解 unit/integration/schema test 分工、CI 不應依賴真實付費服務。

**本人實作**：GitHub Actions 執行 lint、pytest、必要的 PostgreSQL integration test。

**應交證據**：PR Check 結果與一個故意失敗的 run

### W23｜安全

**原理與研究**：建立 threat model：token、DB、Log、Dashboard、CI permissions。

**本人實作**：以環境變數/Secrets 注入、做 secret scan 與 backup/restore 演練。

**應交證據**：安全檢查清單與恢復證據

### W24｜雲端選修

**原理與研究**：比較本地、Cloud Run Jobs/BigQuery 或 S3/RDS/ECS 等服務的可用性與成本。

**本人實作**：選擇一個 bounded job 上線或產出等價本地設計與驗證；避免常駐付費。

**應交證據**：成本表、停止/刪除方式、部署或替代驗證

## 階段專題

一位同學或 Reviewer 在乾淨環境依 README 重建本地全套系統並跑完整測試；若使用雲端，明確保留費用、IAM、刪除資源的證據。

## Acceptance Criteria（逐條勾核）

- [ ] Compose 或等價方案可從零啟動，資料存續與清除邊界寫清楚。
- [ ] PR 自動跑測試；故意注入失敗能讓 CI 紅燈。
- [ ] 至少一次 DB 備份/還原，核對資料筆數與指標。
- [ ] 明確禁止 `.env`、個資、資料庫認證進 Git；日誌可遮罩敏感欄位。
- [ ] 雲端操作不得承諾零成本；有預估、限制與 teardown；無雲端權限時明列 NotRun，完成等價本地 Gate。
- [ ] 可解釋 DEV/TEST/PRD 的差異及部署回滾概念。

## 必須執行的故障/反例測試

- 刪除容器但保留 volume，確認資料是否仍存在。
- CI 用錯密鑰權限，需在不洩漏 token 的前提下診斷。
- 改環境變數造成連不上 DB；依 Log 排查與修復。

## 導師現場追問（不可只複述 AI 答案）

- Docker volume 與 image 的用途有何不同？
- 為什麼測試成功不能證明部署安全？
- 如何估算每天跑 10 分鐘批次 job 的固定/變動費用？

## 常見誤區與邊界

禁止開啟公網 PostgreSQL、提交真實資料、沒有費用限制的常駐雲端資源。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
