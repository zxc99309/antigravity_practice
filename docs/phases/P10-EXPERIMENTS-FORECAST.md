# P10｜A/B 實驗、因果意識、時間序列與預測

> 週次 W37–W40｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：在清楚假設和限制下評估營運活動；建立可比較 Baseline 的預測，不以模型複雜度當成品質。

**前置條件**：P07 統計報告與 P08 指標定義都已過關。

## 需要理解的原理

- Randomization、control/treatment、unit of analysis、sample ratio mismatch
- confidence interval、effect size、power/sample size、multiple comparison
- time series trend/seasonality、time-based split、data leakage
- naive seasonal baseline、MAE/MAPE（零值限制）/RMSE、rolling evaluation

## 每週教學與工作單

### W37｜實驗設計

**原理與研究**：定義要改善的業務 KPI、受測單位、隨機化方式與觀察期。

**本人實作**：編寫促銷 A/B Experiment Plan；註明停止規則與可能偏差。

**應交證據**：設計書、合成資料方案與樣本量假設

### W38｜實驗分析

**原理與研究**：理解統計與商業顯著性不同；A/A 與樣本比失衡檢查。

**本人實作**：分析合成 A/B：差異、效果量、區間、p-value 與分層。

**應交證據**：完整計算、假設限制、決策建議

### W39｜時間序列

**原理與研究**：討論模型使用未來資料的 Data Leakage；固定 train/validation 時間切分。

**本人實作**：訂單數建立 naive 和 seasonal naive 兩種 Baseline。

**應交證據**：time split、資料準備、Baseline 預測

### W40｜預測與決策

**原理與研究**：比較簡單線性/樹模型與 Baseline，重視誤差與運營用途。

**本人實作**：以 rolling origin 驗證，分析異常節日和概念漂移；寫建議。

**應交證據**：預測評估報告、同圖比較、部署與否理由

## 階段專題

「促銷是否改善轉換率？」與「下月訂單量多少？」兩份小型決策報告；至少一份結論應誠實呈現證據不足，而不是一定產生正面結論。

## Acceptance Criteria（逐條勾核）

- [ ] A/B 計畫在看結果前事先指定主 KPI、假設、樣本量與排除條件。
- [ ] 有 sample ratio mismatch 或等價資料品質檢查。
- [ ] 記錄效果量、信賴區間與商業判準，不只看 p-value。
- [ ] 資料切分遵守時間先後；明確檢查 target leakage。
- [ ] 預測與 naive/seasonal Baseline 同條件比較，公布 error metric 的限制。
- [ ] 商業建議列出因果推論假設與需要補充的驗證。

## 必須執行的故障/反例測試

- 將同一用戶每次點擊當獨立樣本，診斷獨立性問題。
- 拿含有下一個月營收欄位的特徵來預測下一個月。
- 對 10 種指標重複檢定只報顯著的一項，討論多重比較。

## 導師現場追問（不可只複述 AI 答案）

- 觀察到促銷後的數據變好，是否足以證明促銷造成？
- 時間序列為何不能直接 shuffle train/test？
- 若 Baseline 優於複雜模型，應如何報告？

## 常見誤區與邊界

本階段只學有實務價值的預測基礎，不應把轉型目標擴張成 ML Engineer / Data Scientist。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
