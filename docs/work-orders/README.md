# 工作單（實務任務）總表

> 工作單是模擬「需求 → 實作 → 驗證 → 故障 → 交付」的工程 Ticket。先自己設計再求助 AI；每張工作單用一個 Branch/PR 交付。導師可依學習者能力調整資料規模，不得刪去該單必要正確性門檻。

| ID | 建議 Phase | 工作情境 | 必交成果 |
|---|---|---|---|
| [DE-001](DE-001-CSV-POSTGRES.md) | P01–P02 | CSV 匯入 PostgreSQL | Schema、CLI、重跑、安全驗證 |
| [DE-002](DE-002-INCREMENTAL-ORDERS.md) | P03 | 每日新增／更新訂單 | Watermark、Late Data、對帳 |
| [DE-003](DE-003-INCIDENT-BACKFILL.md) | P04–P05 | 缺兩天資料的復原 | Incident、Backfill、驗證 |
| [AN-001](AN-001-EDA-KPI.md) | P07–P08 | 營收與顧客分析 | EDA、Metric Dictionary、分析報告 |
| [BI-001](BI-001-DASHBOARD.md) | P09 | 高階主管 Dashboard | DAX / SQL 驗證、RLS、刷新 |
| [CAPSTONE-001](CAPSTONE-001-RETAIL-PLATFORM.md) | P12 | 綜合零售平台 | 系統、分析、BI、演練與交接 |
| [SQL-DRILLS](SQL-DRILLS.md) | P02 起反覆練 | 20 題 SQL 實戰 | SQL、預期值、邊界測試 |

**相依**：DE-001 → DE-002 → DE-003 → AN-001 → BI-001 → CAPSTONE-001。SQL-DRILLS 在所有階段持續練。每張工作單先建立含答案與未來資料的 `expected` fixture，但不要先把 AI 解答直接複製到實作。
