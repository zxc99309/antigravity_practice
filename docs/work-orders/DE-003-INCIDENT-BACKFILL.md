# DE-003｜ETL 故障、資料缺漏與安全回補

**情境**：星期三早上，主管發現星期一/二的訂單數下降 40%，昨天的排程顯示成功，但來源 API 其實只回傳部分分頁。維運工程師必須在不製造重複的前提下修正。

## 事前準備

先用固定種子建立 7 天完整來源資料，產出 expected row count、`COUNT(DISTINCT order_id)`、付款、退款與淨收款參考值；再用測試開關讓其中 2 天的某些 page 被漏取。預期值不得於事故發生後才回推改寫。

## 處置任務

1. **偵測**：藉由 row count volume threshold / source page cursor 對帳找到異常；不要只相信 Scheduler 綠燈。
2. **定界**：列出影響批次、日期、資料表、報表；保存 run id、request id（合成）、來源摘要與 DB 狀態。
3. **止血**：避免下游刷新錯誤 KPI，或明確標示 stale/unverified。
4. **修復**：用有範圍的 backfill job 重取資料；若需交易或去重，先列不變條件。
5. **驗證**：以獨立來源 expected set 和至少四項指標核對；在同一日期重跑兩次仍不變。
6. **復盤**：寫 incident timeline、根因、監測缺口、短期/長期改善、負責人與驗收期。

## AC

- [ ] 不以「重新跑過」當作正確性的證明，必須有 expected vs actual 對帳表。
- [ ] Backfill 範圍有日期上下界，能證明其他日期未被改動。
- [ ] 重跑至少兩次不產生重複；影響下游資料與報表的刷新範圍明確。
- [ ] 具備可查的 failure logs、incident report、改善措施與回歸測試。

## 第二輪考題

改成「來源 API 第三頁永遠回 429」、「部分退款的來源 schema 改名」、「兩個工作同時補同日」擇一，要求學習者單獨定位，不提前公布解答。

請使用 [Incident 模板](../templates/INCIDENT-REPORT.md) 交付。
