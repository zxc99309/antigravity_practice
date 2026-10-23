# P01｜Python 工程化、Git、CLI、Linux、Excel

> 週次 W01–W04｜學習主線：工程 × 分析 × BI｜必修 Phase。

## 目的與入口條件

**學習成果**：把「手動上傳 CSV 的工具」轉為可重用、可追蹤且可驗證的 Python CLI；懂得與 Excel 的結果交叉驗證。

**前置條件**：既有程式可執行；完成 00-ONBOARDING 基準盤點。

## 需要理解的原理

- 函式的契約：輸入、輸出、型別、例外；mutable / copy / side effect
- pathlib、encoding、csv、JSON、datetime、context manager、generator；pandas dtype 與 memory
- Git branch/commit/diff/rebase 的基本用途；venv 與依賴版本；pytest、Ruff
- CLI argument、stdout/stderr、exit code、logging；Windows 與 Linux 差異；Excel 篩選、樞紐、公式核對

## 每週教學與工作單

### W01｜讀懂程式

**原理與研究**：繪製 `app.py` 到 `src/analyzer.py` / `charts.py` / `exporter.py` 的依賴圖；說明 DataFrame copy、不變更原始資料的理由。

**本人實作**：自行執行現有 pytest，記錄環境與真實輸出；增加一個錯誤格式的測試。

**應交證據**：學習筆記 + 可追溯的測試 log + 一個小 PR

### W02｜CLI 與檔案契約

**原理與研究**：理解檔案路徑與 encoding fallback；說明 UTF-8-SIG、CP950、dtype 推斷的局限。

**本人實作**：新增獨立 CLI：input/output/strategy，與 Streamlit 共用核心，不複製清理邏輯。

**應交證據**：正常/不存在/空 CSV/錯編碼案例的命令與輸出

### W03｜錯誤與品質

**原理與研究**：理解例外分類、logging、配置與程式退出碼；Ruff/pytest/fixtures。

**本人實作**：新增結構化 Run ID 與錯誤訊息；寫單元測試，確認失敗時不生成假成功輸出。

**應交證據**：pytest、lint、CLI exit code 證據

### W04｜可維護與跨環境

**原理與研究**：Linux 檔案權限、相對路徑、環境變數；Excel Power Query/樞紐表基本驗算。

**本人實作**：在另一個乾淨虛擬環境依文件執行；與 Excel 的筆數、缺失值、分組平均比較。

**應交證據**：README、輸入種子、兩種工具交叉核對結果

## 階段專題

完成 `python -m pipeline.cli --input sample_data/sample.csv --output output/clean.csv --strategy preserve`（參數格式可自行設計並記錄），保留原 Streamlit 功能；不應讓 CLI 反向 import Streamlit。

## Acceptance Criteria（逐條勾核）

- [ ] CLI 無需開瀏覽器可處理 CSV，與既有 UI 使用相同核心邏輯。
- [ ] 輸入空檔、二進位、錯誤路徑、缺欄時回傳可辨識的錯誤；失敗 exit code 非 0。
- [ ] 不覆蓋來源；輸出位置、覆寫策略與例外清楚。
- [ ] 不把「合法解碼」誤當「語意正確」；提供至少一個亂碼或推斷 dtype 反例。
- [ ] pytest 包含正常與例外路徑，記錄真實結果與版本。
- [ ] Excel 和 Pandas 統計結果核對並解釋浮點數/缺失值差異。

## 必須執行的故障/反例測試

- 把 `.xlsx` 改名 `.csv` 後要求辨識或拒絕，不能悄悄產出奇怪資料。
- 來源路徑不存在、output 權限不足、含千分位數的薪資被推為文字。
- 模擬不可重現的套件更新，說明如何用鎖版或受控版本策略修復。

## 導師現場追問（不可只複述 AI 答案）

- 為何 DataFrame 的 `copy()` 不能取代資料庫交易？
- stdout、stderr 與 Logging 各適合放哪些內容？
- 何時不該用 Pandas 一次 `read_csv` 讀完整檔案？

## 常見誤區與邊界

本階段不導入 Spark、Airflow、Cloud；不要因 pandas 幾行程式變得簡單就跳過型別、錯誤與測試。

## 結業評核

填寫 [Phase 提交表](../templates/PHASE-SUBMISSION.md)，附真實執行證據、失敗測試、SQL/分析核對、Git Commit/PR。依 [統一評量規則](../04-ASSESSMENT.md) 計分，**滿 70 分、各項至少 2/5、所有硬性 Gate 通過**才算本階段 Pass。

只完成教學操作、只貼截圖、由 AI 代做後不懂原理，一律 `Needs Work`。如環境受限，導師應設計等價替代實驗並標記 `NotRun`，不可虛構成功。

## 下一步

回到 [48 週 Roadmap](../01-ROADMAP-48-WEEKS.md)；通過此階段 Gate 後再開始下一 Phase。
