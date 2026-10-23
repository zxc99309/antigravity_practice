# 02｜能力矩陣、深度標準與求職方向

## 以能力證據評級，不以學過的工具名稱評級

| 等級 | 描述 | 驗證方式 |
|---|---|---|
| L0 | 尚不熟悉 | 無法定義概念 |
| L1 | 能辨識 | 可用自己的話說明用途與限制 |
| L2 | 有提示能完成 | AI 提供提示後可自行實作、測試 |
| L3 | 獨立交付 | 不依賴 AI 解題，有可重現證據 |
| L4 | 能排錯比較 | 故障注入、討論 trade-off，能定位修復 |
| L5 | 能設計帶人 | 能根據約束設計方案、Review 他人、留下維運文件 |

| 職能 | 最低求職目標 | 直接證據 | Phase |
|---|---|---|---|
| SQL / Relational / Window | L4 | 20 題 SQL + EXPLAIN + 對帳 | P02、P08 |
| Python / Pandas / CLI | L4 | CLI、tests、Profile、錯誤處理 | P01、P07 |
| ETL / ELT / Incremental | L4 | 多來源、唯一鍵、水位、Backfill | P03、P04 |
| Data Quality / Contract | L4 | Schema 測試、拒絕資料、資料對帳 | P04、P12 |
| Data Modeling | L3 | ERD、Star Schema、SCD | P02、P03 |
| Statistics / EDA | L3 | 假設與限制完整的可重現分析 | P07 |
| Business KPI / Analytics | L4 | 指標字典、Funnel/Cohort、管理摘要 | P08 |
| Excel / BI / DAX | L3 | 樞紐、Power BI Measures、SQL 核對 | P01、P09 |
| Orchestration / dbt | L3 | DAG、tests、docs、重跑 | P05 |
| Git / Docker / CI / Cloud | L3 | PR、Compose、Workflow、Cost/IAM | P01、P06 |
| AB Testing / Forecasting | L2–L3 | 實驗評估、Baseline 對照 | P10 |
| Parquet / DuckDB / Spark | L2 | 可重現 Benchmark 與適用性分析 | P11 |
| 溝通、需求、文件、維運 | L4 | ADR、Runbook、Incident、Demo | 全階段 |

## 典型職缺對應（非就業市場統計）

- **Data Analyst**：SQL、Excel、Python EDA、統計、KPI、業務解讀與報告；能理解資料來源及限制。
- **BI Engineer / BI Analyst**：SQL、星型模型、指標統一定義、Power BI/DAX、刷新、權限、管理報表。
- **Junior Data Engineer / ETL Engineer**：SQL、Python、DB、ETL/ELT、工作流、資料品質、監控與恢復。
- **混合型資料職缺**：上述三條線共用 SQL + Python + Schema + 指標口徑；依公司選擇雲端、SSIS/SSRS、dbt 等工具。

## 求職範圍檢核

亦可使用 [台灣混合型職缺橋接課](08-TAIWAN-HYBRID-ROLE.md) 補強 T-SQL、Excel、Power BI 與日常運維。

投遞之前選 5–10 則近期真實 JD，在個人學習記錄中建立「要求 → 證據連結 → 差距 → 補強優先順序」表；沒有看到的需求不可憑想像硬塞課程。職缺工作內容各異，切勿因單一 JD 宣稱全台灣都一樣。
