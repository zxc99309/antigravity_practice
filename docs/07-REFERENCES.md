# 07｜官方學習資源與使用原則

> 下列連結為官方入口，文件內容與版本可能更新；執行指令前請確認當時穩定版。不得只因教學影片展示就將其視為 production best practice。

| 領域 | 官方文件 | 推薦用途 |
|---|---|---|
| Python | https://docs.python.org/3/tutorial/ | 語法、例外、I/O、模組 |
| Python packaging | https://packaging.python.org/en/latest/ | 虛擬環境與相依管理 |
| pytest | https://docs.pytest.org/en/stable/ | fixtures、parametrize、例外測試 |
| pandas | https://pandas.pydata.org/docs/ | DataFrame、清理、GroupBy、日期 |
| Git | https://git-scm.com/docs | Branch、Commit、Diff |
| PostgreSQL | https://www.postgresql.org/docs/current/ | DDL、JOIN、Window、Index、Transaction |
| Docker | https://docs.docker.com/ | Compose、Volume、Secret、Container |
| dbt | https://docs.getdbt.com/ | SQL 模型、Incremental、Test、Docs |
| Apache Airflow | https://airflow.apache.org/docs/ | DAG、Retry、Catchup、Backfill |
| Power BI | https://learn.microsoft.com/power-bi/ | 模型、資料刷新、權限、視覺化 |
| DAX | https://learn.microsoft.com/dax/ | Filter Context 與 Measure |
| Power Query | https://learn.microsoft.com/power-query/ | M、資料清理與查詢摺疊 |
| SciPy | https://docs.scipy.org/doc/scipy/ | 分布、假設檢定、統計方法 |
| statsmodels | https://www.statsmodels.org/stable/ | 統計模型與信賴區間 |
| DuckDB | https://duckdb.org/docs/ | Parquet SQL 與本地分析 |
| Parquet | https://parquet.apache.org/docs/ | 欄式檔案格式 |
| Spark | https://spark.apache.org/docs/latest/ | Shuffle、Partition、Spark SQL |
| GitHub Actions | https://docs.github.com/actions | CI 與 Workflow |
| GCP | https://cloud.google.com/docs | 選修 Cloud Run Jobs / Storage / BigQuery |
| AWS | https://docs.aws.amazon.com/ | 選修 S3 / RDS / ECS、IAM |

## 選資料集的原則

優先使用自行合成且可設定 `seed` 的資料，或具備合法使用條件且來源可驗證的公共資料。需能人工植入四種缺陷：重複、缺值、晚到、型別/Schema 變更。涉及人事與薪資時，僅使用合成資料；公開網頁爬蟲必須尊重使用條款、robots、頻率限制及個資規定。

## 閱讀方式

先由學習者在官方文件找出概念段落，寫 3–5 句摘要，再問 AI 反例與適用性；不以複製官方範例成功執行作為掌握的唯一標準。
