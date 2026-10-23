# Metric Dictionary｜[專案/版本]

> 業務指標應由資料 Owner 與 Consumer 確認，不是只由報表作者默認。

| Metric ID | 名稱 | 定義（分子/分母） | 粒度 | 時區/歸屬日期 | 包含/排除 | SQL/model | Owner | 驗證方式 |
|---|---|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

## 每個重要指標的邊界案例

- 0 分母如何呈現？NULL / 0 / 不適用如何區分？
- 多筆付款/退款是否已在各自粒度先聚合？
- 取消訂單、部分退款、跨月退款、跨時區事件怎麼處理？
- 來源晚到導致歷史數字改變時，是否保留版本/更正紀錄？
- BI Measure 是否能用獨立 SQL 重算並一致？

## 發布與版本

- Version：`TODO`
- 生效日期：`TODO`
- 定義更動：`TODO`
- 受影響的 Mart / BI / 分析報告：`TODO`
- 核准紀錄：`TODO`
