# 01｜48 週 Roadmap、依賴與完成定義

> Phase = 4 週的里程碑，不是 4 週後自動通關。每個週次結束至少留下一份 Git PR、SQL/Notebook/測試成果或調查報告。完成定義以 [評量規範](04-ASSESSMENT.md) 為準。

| 週 | Phase | 核心任務 | 可檢查交付 |
|---|---|---|---|
| W01 | P01 | 讀懂現有程式與 Git 工作流 | 呼叫流程圖、環境紀錄、初始測試報告 |
| W02 | P01 | CLI、檔案格式、編碼與資料型別 | 非 UI 的 CSV 處理指令 |
| W03 | P01 | Python 例外、logging、模組分離 | 可追蹤錯誤的程式與單元測試 |
| W04 | P01 | Linux/CLI、Excel 校驗、重構驗收 | 跨環境操作手冊與 Demo |
| W05 | P02 | Relational Model、DDL、Constraint | ERD、Schema、資料字典 |
| W06 | P02 | JOIN、聚合、NULL、去重 | SQL 練習及預期結果 |
| W07 | P02 | Window、CTE、Transaction | 分析 SQL、交易演示 |
| W08 | P02 | Index、EXPLAIN、Python→DB | 查詢計畫與匯入 SQL 證據 |
| W09 | P03 | 多來源與 Raw Contract | 原始檔版本、來源清單 |
| W10 | P03 | Extract/Load 與全量匯入 | 可重跑的基本 ingest |
| W11 | P03 | 增量、水位、晚到資料 | 增量與缺漏回補演示 |
| W12 | P03 | Star Schema / SCD | Fact/Dimension DDL 與數據驗算 |
| W13 | P04 | 品質規則與 Quarantine | 契約驗證、錯誤資料隔離 |
| W14 | P04 | 冪等、交易、部分失敗 | 重跑不重複、恢復測試 |
| W15 | P04 | Retry、限流、排他 | 來源故障與併發演練 |
| W16 | P04 | Backfill、Runbook、對帳 | Incident Report 與復原證據 |
| W17 | P05 | dbt Model、Sources、Tests | dbt Staging / Mart |
| W18 | P05 | Incremental、Docs、Lineage | dbt 關聯圖、測試失敗案例 |
| W19 | P05 | Airflow DAG 與依賴 | 本地排程 DAG |
| W20 | P05 | Retry、Catchup、Backfill | 排程失敗重跑與證據 |
| W21 | P06 | Docker Compose、Vol/Network | 可重建本地堆疊 |
| W22 | P06 | GitHub Actions、Lint/Test | 自動檢查 Pipeline |
| W23 | P06 | 密鑰、IAM、部署成本 | 威脅模型、成本表 |
| W24 | P06 | 免費/低成本雲端 Job 選修 | 部署 Demo 或等價本地驗證 |
| W25 | P07 | 描述統計、資料品質、視覺 | EDA Notebook + 問題定義 |
| W26 | P07 | 抽樣、分布、偏差、離群 | 方法選擇與敏感度分析 |
| W27 | P07 | 相關、區間估計、假設檢定 | 含效果量與假設的分析 |
| W28 | P07 | 可重現報告與同儕答辯 | EDA 分析報告 |
| W29 | P08 | 業務需求、KPI 口徑 | Metric Dictionary |
| W30 | P08 | 營收、退款、毛利、時間維度 | 對帳 SQL、指標模型 |
| W31 | P08 | Funnel、Cohort、RFM | 不同分母下的比較 |
| W32 | P08 | 敘事、建議、限制、決策 | 管理摘要與反事實提問 |
| W33 | P09 | Power Query 與星型模型 | 可追溯 Data Model |
| W34 | P09 | DAX 與 Filter Context | 可核對的 Measures |
| W35 | P09 | 儀表板 UX、刷新、RLS | 互動式報表與權限測試 |
| W36 | P09 | BI 數據驗證、移交 | 業務驗收紀錄 |
| W37 | P10 | A/B 需求、設計、樣本偏差 | 實驗計畫書 |
| W38 | P10 | 假設檢定、效果量、校正 | A/B 分析與風險聲明 |
| W39 | P10 | 時間序列與資料洩漏 | Baseline、切分策略 |
| W40 | P10 | 預測驗證與業務行動 | 模型比較與簡報 |
| W41 | P11 | CSV/Parquet、Row/Column Store | 格式比較與數據驗證 |
| W42 | P11 | DuckDB、Index、Query Profiling | 查詢瓶頸報告 |
| W43 | P11 | Spark local、Partition、Shuffle | 同題多引擎比較 |
| W44 | P11 | 可重複 Benchmark 與選型 | 效能/成本/限制報告 |
| W45 | P12 | 需求訪談、契約、ADR、Plan | Capstone Scope 與驗收規則 |
| W46 | P12 | E2E 整合與維運 | 可重建資料系統 |
| W47 | P12 | 故障注入、對帳、BI 與分析 | Incident + 驗收證據 |
| W48 | P12 | 交接、Demo、面試挑戰 | Portfolio、Runbook、答辯 |

## 前置關係與教學原則

- P01 → P02 → P03 → P04 為**強依賴主線**；未達最低正確性與復原標準不可進 P05。
- P05/P06 可以先用最小化設備示範；P07–P10 共用 P03 的業務資料集，但不能用未通過品質檢查的資料直接報表。
- P11 可以將 Spark 只做 local mode，不為了學習啟動雲端集群。P12 整合之前的產物，不從零造新平台。
- 逢遇技術重大變更，導師先查官方版本文件，再提出更動；教材中的工具名稱不是永遠固定的部署推薦。

## 能力里程碑

- **M1 (W12)**：能從 CSV/API 擷取、存入 PostgreSQL、用 SQL 建立基本 Mart；理解欄位口徑。
- **M2 (W24)**：能讓工作按時執行、發現品質問題、對帳、重跑與部署；有 PR + CI 證據。
- **M3 (W36)**：能提出統計分析與 KPI 定義，完成資料一致的 Power BI Dashboard。
- **M4 (W48)**：能獨立做端到端系統、故障復原、業務解讀與交接答辯。

## 時間調整機制

每週低於 6 小時時，建議一個「週任務」延長成兩週；遇到卡關先產出問題紀錄（輸入、預期、實際、Log、已嘗試方案），再尋求分層提示。追求理解和證據，不追求打卡速度。
