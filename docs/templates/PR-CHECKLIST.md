# 培訓任務 PR Checklist

- [ ] PR 只處理當前 Issue/工作單，沒有未經授權的重構。
- [ ] 需求、輸入、輸出、非目標與 AC 明確。
- [ ] 資料 grain、key、NULL、版本、時間區域與指標口徑說明。
- [ ] 新增/修改測試含錯誤與邊界；只寫實際執行結果。
- [ ] 同一批重跑與異常恢復的行為符合當前 Phase 要求。
- [ ] SQL / BI / 分析數值提供 expected vs actual 對帳。
- [ ] 無 token、DB 密碼、真實個資、企業機密或敏感 Log。
- [ ] README/Runbook 能讓另一人重建、操作與排錯。
- [ ] 本人能解釋任意一段新增邏輯與設計權衡。
- [ ] 已知限制與 NotRun 清楚註記。
- [ ] 無自動合併 main；交由 Repo 維護者 Review。
