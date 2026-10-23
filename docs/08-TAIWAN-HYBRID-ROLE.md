# 台灣混合型資料職缺橋接課｜SQL Server / Excel / Power BI / ETL

> 此文件是加強實際辦公室環境的**選修橋接課**，不是台灣所有公司統一技術規範。依實際應徵的 JD 選擇，避免為了追求工具清單拖慢必修主線。建議在 P08–P09 完成後，另用 2–4 週或融入每週選修。

## 常見混合型日常情境（需求到交付）

| 日常需求 | 真正要問的事 | 主力能力 | 要留的證據 |
|---|---|---|---|
| 早上營收報表少了昨天資料 | 排程、時區、資料來源、晚到與刷新 | SQL、ETL、Ops | Job run、source/mart 對帳、補跑 |
| 業務臨時要三個月銷售明細 | 指標口徑、權限、客戶識別、輸出格式 | SQL、Excel/BI、保密 | 查詢、權限確認、匯出範本 |
| 財務說付款總金額和報表對不起來 | 退款、取消、部分支付、JOIN grain | SQL、對帳、溝通 | 差異表、可重現個案、決議 |
| 主管希望每週自動寄管理報表 | SLA、排程、失敗通知、接收權限 | ETL、BI、Ops | Runbook、重試、脫敏通知 |
| 欄位/主檔改版導致報表跑錯 | Schema Contract、上下游影響、版本 | Modeling、Test、協作 | 影響分析、測試、回滾 |
| Excel 與 Power BI 數字不同 | 日期、Null、Measure、資料刷新 | Excel、DAX、SQL | 三方對帳、口徑字典 |

## A. SQL Server / T-SQL 橋接（建議 1 週）

- 認識 SQL Server 常見資料型別、`datetime2`、`decimal`、`nvarchar`、clustered/nonclustered indexes、transaction isolation、execution plan。把 P02 其中 6 題移植到 T-SQL。
- 對照 PostgreSQL 的 `LIMIT` vs T-SQL `TOP/OFFSET FETCH`、字串/日期處理、序列/IDENTITY、UPSERT 策略等，記錄語意差異，不只做語法替換。
- 實作：SQL Server Express/Developer（先確認個人與使用條款）或可取得的安全實驗環境；如果無法合法安裝，先寫設計對照和 T-SQL 草稿，**標記 NotRun**。
- 驗收：同組資料與同組問題、SQL 結果一致，提供至少一個執行計畫解讀；禁用真實公司帳密或來源。

## B. Excel / Power Query / BI 操作（建議 3–5 天）

- Excel Tables、Power Query 清理、PivotTable、Power Pivot（如環境支援）、查找函式、日期格式、資料驗證、常見編碼。
- 以 1,000 筆員工資料和 100,000 筆交易資料驗證不同工具的計數/金額；超出 Excel 行數上限時不可硬塞工作表，改讓 SQL/Power Query 聚合後再消費。
- 驗收：同一份 KPI 用 SQL、Excel 和 Power BI 顯示一致；每個工具使用的 Null、四捨五入、時區定義寫清楚。

## C. SSIS / SQL Agent / SSRS / Power BI（選修）

- 認識 SSIS 的控制流、資料流、參數、錯誤輸出；用 P03 管線說明如何映射，不必為了「會操作」重新做三套相同商業邏輯。
- SQL Server Agent（若合法授權且可用）與 Airflow/Cron 對照：Job 歷史、重試與通知、依賴、回補。
- SSRS Paginated Report 與 Power BI 互動儀表板的用途比較：列印格式與互動分析不同。
- 驗收：對兩種工具提出運維、費用、權限、替換難度及部署可行性比較；環境不可用時以具體對照與案例演練替代。

## D. 資料需求與溝通能力（每週持續）

請學習者扮演接案者，導師扮演業務方，對每個需求問出：

1. 這個 KPI 的**正式定義與 Owner** 是誰？
2. 時間範圍、時區、來源延遲與資料有效日是什麼？
3. 明細是否涉及客戶/員工資訊？要遮罩、限制下載嗎？
4. 報表需一次性、每天固定產出，還是需要可回補歷史？
5. 如何知道結果正確，與哪份來源對帳？
6. 排程失敗誰被通知？多久恢復、怎樣不重複？

## E. 對應求職 JD 的練習方法

在 P12 前收集 5–10 則實際當期職缺，取關鍵需求建立表格：`職缺 | SQL | Python | ETL | BI | Cloud | 分析 | 目前證據 | 缺口`。若目標偏 BI，就強化 P08/P09 + T-SQL；若偏 DE，就強化 P03/P04/P05/P06；若偏 Analyst，就強化 P07/P08/P10 + Excel。不可簡化成「台灣所有職缺都不分工」。
