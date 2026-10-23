# DE-002｜每日增量訂單與晚到退款

**角色**：某電商每天有新訂單、訂單狀態變更、部分付款和退款，客服要求報表能在隔天更新。
**輸入**：自行生成（固定 seed）的 `orders`、`order_lines`、`payments`、`refunds` 合成資料，加上模擬 HTTP API 或 CSV 一種來源；有穩定 ID 與來源版本時間。
**目標**：增量處理正確，而不是速度最快。

## 業務契約

- 訂單狀態包含 created/paid/cancelled/refunded（可再細分，但需定義合法轉移）。
- Event Time、Source Updated Time、Ingested Time 分開記錄，統一明確時區。
- 實作 Full Load、Incremental Load、重新處理日期區間；說明 cursor 使用 `(updated_at, stable_id)` 或 overlap/reconciliation 的取捨。
- 訂單、付款與退款的事實表粒度不同，禁止直接多對多 JOIN 相乘。

## 測試資料組

- T1：第 1 天 1,000 筆訂單，第 2 天新增加 100 筆。
- T2：同一秒更新 2 個不同 ID 的訂單。
- T3：已付款訂單第 3 天被取消或第 5 天部分退款。
- T4：兩筆支付、兩筆退款屬同一訂單；需要先各自聚合再 JOIN。
- T5：第 4 天才收到第 1 天產生的更新（晚到）。

## AC 與可檢查輸出

- [ ] 每批紀錄來源窗口、cursor、run id、row counts、checksum/版本。
- [ ] Raw 與 Staging 有正確粒度、版本規則、型別、日期，失敗列可定位。
- [ ] 重跑 T1–T5，鍵、筆數與金額一致，不會多列/漏列。
- [ ] 提供 `gross_order_amount`、`paid_amount`、`refund_amount`、`net_paid_revenue` 的**教學口徑**，明確指出它們不是正式財報營收。
- [ ] SQL、Python（或 dbt）兩套獨立方法核對每日結果。
- [ ] Backfill 不使用無界刪除；只影響指定日期/批次且有變更記錄。

## 導師追問

如果只看 `updated_at > watermark`，同一秒更新會漏哪筆？如果資料源沒有 updated_at，增量要怎麼辦？為什麼報表「昨天」需要說明時間區域和退款歸屬？
