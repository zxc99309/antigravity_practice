# DE-001｜將既有員工 CSV 載入 PostgreSQL

**角色**：你是企業資訊部門的初階資料工程師。業務需要把每週一批的合成員工資料存入資料庫供查詢，不希望重覆手動匯入。
**輸入**：`sample_data/sample.csv`（1,000 筆合成資料；6 欄），與 `scripts/generate_sample_data.py`；不可使用真實人事資料。
**非目標**：不用先做 Airflow、Spark、雲端 DB 或複雜的 Streamlit 新 UI。

## 要先想清楚

- 員工姓名可能重複，檔案沒有穩定 `employee_id`；需要定義「來源快照中一列」和「同一名員工跨週版本」是不同概念。
- 可以先存入 Raw Snapshot + staging 表做匯入流程；若要識別跨週人員，必須修改**合成資料契約**，添加穩定 ID。
- 哪些欄位允許 NULL？年齡 0/200、月薪負值是否應警告或拒絕？

## 子工作單與完成條件

- [ ] A. 畫出原始檔到 DB 的流程圖；建立 `load_runs`、`raw_employee_rows` 與目標表（名稱可變）Schema、PK、FK、Constraints。
- [ ] B. 寫一個 CLI 能接 `--input`、`--dsn-env`、`--batch-id`，密碼來自環境變數，不進版控。
- [ ] C. 對原始檔計 SHA-256，紀錄來源名稱、checksum、ingested_at、row_number、run_id、row count。
- [ ] D. 同一 snapshot 重跑三次，Raw 的事件記錄策略與業務目標的唯一性都有文件，不產生重複員工。
- [ ] E. 至少設計 5 個驗證規則：型別、數值範圍、姓名 NULL、主鍵/來源唯一性、row count。
- [ ] F. 用 SQL 證明目標 rows/unique-key/avg salary 與 Pandas 在相同 NULL 處理下相等。
- [ ] G. 模擬一筆無效年齡與一筆重覆來源，需見明確拒絕或 Quarantine 紀錄。
- [ ] H. 更新 README：PostgreSQL 初始化、env 變數名稱（僅名稱）、匯入與驗證指令。

## 故障演練

1. 相同檔案連續載入 3 次；保存每次 run 的 row count、key distinct、薪資總和。
2. 讀到一半破壞一列 CSV；應有明確失敗訊號，保留前面資料的原子性/檢查點設計說明。
3. 同名員工出現在兩列；必須解釋不能靠姓名去重。

## 驗收證據

ERD/DDL、CLI 使用範例、SQL 對帳、pytest（含 DB integration 或說明測試隔離）、Log（不含 PII/密碼）、反例結果與 PR。只要資料變少，必須解釋哪些列及為何被拒絕。導師請選一個新欄位臨時改題，讓學習者自行處理。
