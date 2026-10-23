# SQL-DRILLS｜20 題階段性 SQL 工作訓練

**資料來源**：P02 的 `employees/departments/salary_history`，P03 的 `orders/order_lines/products/payments/refunds/customers`。建立資料時先記錄 grain、key、nullability。每題需提交 SQL、用途、預期筆數、實際筆數、手工算得的微型 fixture 預期值。題目不提供完整標準 SQL，以保留獨立思考空間。

| # | 題目 | 必須驗證的陷阱 |
|---:|---|---|
| 01 | 查出每部門員工數 | `COUNT(*)` vs distinct |
| 02 | 查出沒有部門的員工 | LEFT JOIN + NULL |
| 03 | 每部門平均/中位月薪 | 忽略 NULL 或錯誤轉型 |
| 04 | 每部門前 3 高薪者 | ROW_NUMBER vs DENSE_RANK |
| 05 | 月薪高於部門平均的員工 | Correlated subquery/CTE |
| 06 | 某員工最近一次薪資 | 多筆同日期 tie-breaker |
| 07 | 計算連續兩期薪資差 | LAG + partition/order |
| 08 | 找出重複的姓名但不同 ID | name 不是 key |
| 09 | 比較 JOIN 前後人數 | 一對多膨脹 |
| 10 | 用 transaction 保證批次載入 | 失敗 rollback |
| 11 | 訂單明細總金額 | line grain vs order grain |
| 12 | 每日完成付款訂單數 | event_time / paid_time |
| 13 | 各通路退款率 | 分母與退款定義 |
| 14 | 有訂單但尚未付款的顧客 | NOT EXISTS vs NULL |
| 15 | 同訂單多筆付款與退款核對 | 先聚合後 JOIN |
| 16 | 每月 MoM 淨收款變動 | LAG / 零值分母 |
| 17 | 顧客首次購買月份 | MIN window / group |
| 18 | 30 天回購留存 | observation window |
| 19 | 來源版本最新事件去重 | `(updated_at, id)` / 唯一 key |
| 20 | 以 EXPLAIN 比較查詢計畫 | input size/cache/result 同等 |

## 硬性要求

- 至少 5 題含 NULL，至少 5 題含重複／一對多，至少 3 題 Window，至少 2 題交易/效能。
- 由導師在驗收當下改變日期界線、增加同一人的第二筆薪資或更改退款事件，學習者能獨立調整查詢。
- 不因執行成功就宣稱正確；**需要 expected vs actual，且解釋 grain 與分母**。
