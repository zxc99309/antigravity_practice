# 最初 14 天｜可直接開始的逐日教學流程

> 每天建議 45–90 分鐘；若當日沒完成可延後。前 14 天不是把所有功能寫完，而是確立「自己能理解、自己能測」的工作習慣。每個工作日請由 AI 先問學習者想法，不得自動整批完成。

| Day | 核心知識點 | 本人必做 | 可驗證證據 |
|---:|---|---|---|
| 01 | 專案全貌、學習契約 | 完成基準題目與技能自評 | 初始回答（不貼個資） |
| 02 | DataFrame 與模組 | 畫出 UI → analyzer → exporter 呼叫流程 | 流程圖、3 個設計問題 |
| 03 | Git / Branch / Diff | 建立任務分支、做一個小修改 | Commit + diff + revert 演示 |
| 04 | Python 型別/錯誤 | 對 load_csv 加一個測試邊界 | pytest 真實輸出 |
| 05 | CSV encoding | 說明 cp950/utf-8-sig、補一個反例 | fixture 與預期/實際差異 |
| 06 | pandas missing | 比較 dropna、fillna、preserve | 數值變化與業務風險 |
| 07 | 週驗收 1 | 不靠 AI 重現 1–6 天成果 | 小測 + 反思 |
| 08 | CLI 設計 | 寫輸入/輸出/錯誤的介面規格 | CLI 設計筆記，不必先寫碼 |
| 09 | argparse | 實作 input / output / strategy | `--help` 與正確命令 |
| 10 | 日誌/退出碼 | 區分成功、輸入錯誤、系統錯誤 | 失敗範例與 log |
| 11 | 共用核心 | CLI 與 UI 都 import `src.analyzer` | 依賴圖、同輸入輸出一致 |
| 12 | 測試與重構 | 增加正常/錯誤各至少一測試 | 失敗先行/修復後差異 |
| 13 | Excel 校驗 | 使用樞紐或公式核對 Pandas 統計 | Excel vs Python 比較表 |
| 14 | 週驗收 2 | 不靠 AI 改一個 CLI 條件、展示結果 | PR + Demo + 反思 |

## AI 開局對話

1. 問今天是哪個 Day、昨天的成果在哪裡。
2. 只發今日一小題；先問學習者自行提出設計或猜測結果。
3. 根據測試輸出提供 H0–H3 分層提示；必要時才提供完整示範。
4. 用 [Phase Submission](templates/PHASE-SUBMISSION.md) 複製當日證據，不要直接把 demo 程式碼判定為本人學會。

第 14 天後回到 [P01](phases/P01-PYTHON-FOUNDATIONS.md) 剩餘週次及 [48 週表](01-ROADMAP-48-WEEKS.md)。
