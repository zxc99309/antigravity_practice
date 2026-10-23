# 資料工程 × 資料分析 × BI｜48 週實務培訓計畫

> 適用對象：已完成 `antigravity_practice` CSV 資料分析助手、希望在台灣尋找初階資料工程／資料分析／BI 相關工作的初學者。
> 狀態：課程設計文件，**不是**已完成訓練或已通過驗收的證明。
> 時程：12 個 Phase、48 週；以每週 10–15 小時估算。依完成證據調整速度，**不得按日曆自動畢業**。
> 原則：先正確、再可靠、再自動化、再優化、最後規模化。

## 先從這裡開始

1. 學習者讀 [入學盤點](00-ONBOARDING.md)，建立自己的學習目標、時間與基準測驗紀錄。
2. 學習者或 AI 導師讀 [48 週總覽](01-ROADMAP-48-WEEKS.md) 及 [能力矩陣](02-COMPETENCY-MATRIX.md)。
3. **Antigravity 等 AI 導師務必先讀** [導師操作規約](03-AI-MENTOR-PROTOCOL.md)、[AI 啟動提示](MENTOR_START_PROMPT.md) 和 [評估規範](04-ASSESSMENT.md)。
4. 每週只開啟一張任務單；週末依 [交付流程](06-DELIVERY-WORKFLOW.md) 提交證據，不以「AI 說完成」為準。
5. 每階段查閱 `phases/Pxx-*.md`，完成任務、故障演練、答辯與資料品質證據後才能進下一階段。
6. 所有題目必須使用**合成或合法公開**資料；不得把真實個資、密鑰、公司資料放進 public repository。

## 為什麼是複合型課程？

企業常有一人跨越資料擷取、SQL 查詢、儲存、清理、數據口徑、儀表板及分析解讀的工作需求。課程將三條職能結合，但仍分清輸出：

| 職能 | 解決問題 | 實際交付 |
|---|---|---|
| Data Engineering | 如何穩定、可追溯地供應資料 | 來源整合、ETL/ELT、資料表、排程、測試、故障復原 |
| Data Analytics | 數字代表什麼、有哪些證據與限制 | 指標定義、探索分析、統計推論、洞察與建議 |
| BI / Analytics Engineering | 如何讓跨部門持續使用一致的數字 | Mart、Semantic Model、Power BI／替代報表、刷新與權限 |

**總畢業標準**：別人交付「每天更新的訂單與退款資料，請提供可靠淨營收報表」的需求時，學習者能自行提出合理問題、建立管線、核對指標、製作報表、維運與復盤。AI 允許協助，學習者必須能離線／不依賴 AI 解釋及修改重要邏輯。

## 既有專案如何銜接

目前已存在 `app.py`、`src/analyzer.py`、`src/charts.py`、`src/exporter.py`、`tests/test_analyzer.py`、`scripts/generate_sample_data.py`。保留它們，不應為學習一個新工具直接推倒重寫。

- 現有 1,000 筆員工 CSV 是 P01–P02 的練習材料；沒有穩定的員工主鍵，**姓名不可視為唯一識別碼**。可先以 `(file_sha256, source_row_number)` 標識「來源快照中的一列」，但不能用來追蹤員工跨批次身分。正式跨批次資料應新增穩定 `employee_id`。
- P03 開始另增合成電商事件／訂單／退款，保留原分析 App 作為 downstream consumer。
- `docs/` 僅為教學與驗收規範，**不代表實作路徑已存在**；使用者驗收各 Phase 後才逐步新增 `pipeline/`、`sql/`、`dbt_project/`、`dags/` 等程式碼。

## 文件導覽

- [前 14 天動手流程](FIRST-14-DAYS.md)
- [課程進度與 Session Handoff](PROGRESS.md)
- [入學盤點](00-ONBOARDING.md)
- [48 週路線與依賴](01-ROADMAP-48-WEEKS.md)
- [能力矩陣與求職職能](02-COMPETENCY-MATRIX.md)
- [AI 導師操作規約](03-AI-MENTOR-PROTOCOL.md)
- [評分、補考、升級規則](04-ASSESSMENT.md)
- [目標架構、資料模型與風險](05-TARGET-ARCHITECTURE.md)
- [每週工作、PR 與證據流程](06-DELIVERY-WORKFLOW.md)
- [官方參考資源](07-REFERENCES.md)
- [台灣混合型職缺橋接課](08-TAIWAN-HYBRID-ROLE.md)
- [練習工作單總表](work-orders/README.md)
- [文件模板](templates/README.md)

### Phase 清單

| Phase | 主題 | 主要作品 |
|---|---|---|
| [P01](phases/P01-PYTHON-FOUNDATIONS.md) | Python、Git、Linux、Excel | CLI CSV pipeline |
| [P02](phases/P02-SQL-POSTGRES.md) | SQL、關聯式資料庫 | 具約束的 PostgreSQL Schema + SQL 查詢 |
| [P03](phases/P03-ETL-MODELING.md) | ETL/ELT、維度建模 | 多來源 Raw→Staging→Mart |
| [P04](phases/P04-RELIABILITY.md) | 品質與恢復 | Idempotent pipeline + Backfill |
| [P05](phases/P05-DBT-ORCHESTRATION.md) | dbt、排程 | 測試化 SQL Models + DAG |
| [P06](phases/P06-DEVOPS-CLOUD.md) | Docker、CI、雲端 | 可重建環境與部署說明 |
| [P07](phases/P07-STATISTICS-EDA.md) | 統計、EDA | 可重現統計分析報告 |
| [P08](phases/P08-BUSINESS-ANALYTICS.md) | KPI、營運分析 | 指標字典 + Cohort/Funnel 分析 |
| [P09](phases/P09-BI-POWERBI.md) | BI、Power BI | 銷售／退款管理儀表板 |
| [P10](phases/P10-EXPERIMENTS-FORECAST.md) | A/B、預測 | 實驗設計與預測比較 |
| [P11](phases/P11-PERFORMANCE-SPARK.md) | 儲存與效能、Spark | 有效的 Benchmark |
| [P12](phases/P12-CAPSTONE.md) | 企業交付模擬 | 零售資料平台、交接與面試展示 |

## 明確不承諾的事

- 48 週只是**學習節奏**，不是薪資、職位或錄取保證；台灣職缺的技術組合依公司而異。
- 只有小樣本練習不能推斷正式環境安全或效能；測試環境與證據必須寫清楚。
- 學習不等於多安裝工具。Airflow、Spark、Cloud 等必須能說明成本、替代選項與不適用的條件。
