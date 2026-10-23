# CAPSTONE-001｜零售營運資料平台（工程 × 分析 × BI）

## 模擬業務需求

公司有 CSV 商品資料、模擬訂單 API、付款與退款資料。營運主管希望每日查看淨收款、退款率、顧客留存與商品趨勢；資訊部門希望來源變更或夜間工作失敗時可以識別、隔離、回補、通知及對帳。

**現實約束**：免費／低成本、單機可重建、合成資料、無公開資料庫、若雲端資源不適合可改以本地部署，但需說明差異。每週時間有限，因此先做安全 MVP 再做擴展。

## 交付範圍與架構

1. **Data Source**：2 種以上取得方式（本地 CSV + 模擬 API），穩定 source IDs、可重播缺陷注入。
2. **Raw / Staging / Mart**：原始版本、轉換規則、Quality Check、拒絕列、Fact/Dimension、可追溯的 Lineage。
3. **Pipeline**：Full、Incremental、Idempotency、限次 Retry、Backfill、Batch Run metadata、進度指標。
4. **Analytics**：至少 10 個 KPI、營收變化分解、Cohort 或 Funnel、可重現 EDA Notebook，統計限制說明。
5. **BI**：至少一個互動 Dashboard，包含資料新鮮度與失敗狀態，3 項 SQL↔BI 核對。
6. **Ops**：Docker/CI、Secrets、最低權限、備份/還原、Incident Runbook、部署回滾概念。

## 最低非功能要求

- 同樣來源和相同版本重跑三次，key 與核心指標保持一致。
- API 429、source schema 變化、兩天晚到資料三種故障可被測試且可恢復。
- SQL 與 BI 實際結果具對帳表；資料品質異常不靜默進正式 Mart。
- 有限資源下記錄執行時間/記憶體/成本與部署選型原因。
- 沒有任何真實顧客資料與 Secret，公開展示前進行安全檢查。

## 四階段驗收

| 週 | Gate | 證據 |
|---|---|---|
| W45 | 需求凍結 | PRD、資料契約、KPI Dictionary、ERD、ADR、AC |
| W46 | E2E 正常流程 | Clean-room rebuild、CI、Raw→Mart、BI 草稿 |
| W47 | 故障／回補 | 未預告注入、Incident、Backfill、SQL/BI 對帳 |
| W48 | 交接／求職 Demo | Architecture、Runbook、30+30 分鐘展示／提問、Portfolio |

## 技術面試情境（臨場不靠 AI）

1. 兩個一模一樣的 source event 抵達系統，哪一層去重？為什麼？
2. 退款今天入帳但訂單在上月，月報採什麼口徑？何時須重算？
3. 如果資料表成長 100 倍，你先測量哪三項指標，再考慮 Spark？
4. 一個 DAX Measure 與 SQL 算出不同客單價，怎樣追查 Filter Context？
5. 若下週只能維運 1 個人，哪些組件可以簡化？哪些正確性門檻絕不能省？

## 禁止捷徑

只有 Streamlit UI、只有套模板的 Dashboard、只有「跑過成功」或 AI 自述測試成功，都不能算通關。必須具備真實執行證據、失敗案例、復原結果與本人答辯。
