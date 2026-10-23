# BI-001｜主管用 Power BI 銷售／退款儀表板

**需求**：主管早上 9 點前需要看前一日資料（時間與刷新頻率僅供教學，請將實際範例與系統時區明確記錄），可依產品、通路、地區篩選，還能辨識資料是否過期。

## 交付頁面

- **Overview**：付費金額、退款金額、淨收款、訂單數、客單價；趨勢與比較期間。
- **Product / Region**：商品、地區、通路變化，含篩選與 Drill Through。
- **Customer**：新客、回購、Cohort 留存（觀察窗與分母明示）。
- **Quality**：最後資料時間、Last Refresh、批次成功/失敗、品質告警。

## 模型與安全

- 優先連 Mart / 清楚界定的 SQL view；建立 Date Dimension、Fact 與 Dimension 關聯，說明 Cardinality 與方向。
- 至少建立 8 個 DAX measures；每個 measure 對應上一階段的 Metric Dictionary。
- 使用測試角色驗證 RLS；不得在 Public Repo 公開企業秘密或真實客戶個資。

## AC

- [ ] 3 個跨日期/商品/地區篩選案例的 DAX 與獨立 SQL 完全對帳，考慮 rounding。
- [ ] 日期/時區/期間/退款歸屬有明確定義，避免前後數字口徑不同。
- [ ] 重新整理成功與失敗都可看出；不能把舊資料誤標為今天最新。
- [ ] 不同身份的 RLS 檢查有模擬角色證據。
- [ ] 提供使用者指南、模型圖、Refresh Runbook；Power BI 專有功能若未實測，清楚標記 NotRun。

## Reviewer 反例

1. 切一個只含退款、沒有付款的新期間，考慮負值與 NULL。
2. 商品某分類完全沒有訂單，卡片數字、分母及互動是否合理。
3. RLS 用測試角色 A 訪問 B 的資料，必須被阻擋。
