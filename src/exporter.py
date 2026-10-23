"""負責將 CSV 分析結果轉換並匯出為 Markdown 報告字串的模組。"""

from datetime import datetime
from typing import Optional
import pandas as pd
from src.analyzer import (
    generate_auto_insights,
    get_basic_info,
    get_groupby_summary,
    get_missing_summary,
    get_numeric_summary,
)


def generate_markdown_report(
    df: pd.DataFrame,
    source_name: str = "未命名資料集",
    preview_rows: int = 5,
    group_col: Optional[str] = None,
    target_col: Optional[str] = None,
) -> str:
    """根據傳入的 DataFrame 產生結構化的 Markdown 分析報告。

    Args:
        df: 要分析並匯出的 Pandas DataFrame。
        source_name: 資料來源名稱（例如檔案名稱）。
        preview_rows: 報告中包含的前幾筆預覽資料列數，預設為 5。
        group_col: 選擇性的分組依據欄位名稱（若與 target_col 同時提供則納入第 5 節）。
        target_col: 選擇性的分組計算目標數值欄位名稱。

    Returns:
        排版完成的 Markdown 報告字串。
    """
    basic_info = get_basic_info(df)
    missing_df = get_missing_summary(df)
    numeric_df = get_numeric_summary(df)
    insights = generate_auto_insights(df)
    total_missing = int(df.isna().sum().sum())
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"# 📊 CSV 資料分析報告：{source_name}",
        "",
        f"- **報告產生時間**：{generated_at}",
        f"- **資料來源**：`{source_name}`",
        "",
        "## 💡 自動資料洞察摘要",
        "",
        *[f"- {item}" for item in insights],
        "",
        "## 1. 資料基本概況",
        "",
        f"- **總資料筆數 (Rows)**：{basic_info['rows']}",
        f"- **總欄位數 (Columns)**：{basic_info['columns']}",
        f"- **總缺失值數量 (Missing Values)**：{total_missing}",
        f"- **欄位清單**：{', '.join(basic_info['column_names'])}",
        "",
        f"## 2. 資料內容預覽（前 {min(preview_rows, basic_info['rows'])} 筆）",
        "",
        df.head(preview_rows).astype(object).fillna("(缺失值)").to_markdown(index=False),
        "",
        "## 3. 缺失值與欄位型態統計",
        "",
        missing_df.to_markdown(index=False),
        "",
        "## 4. 數值欄位統計摘要",
        "",
    ]

    if numeric_df.empty:
        lines.append("> ⚠️ 此份資料沒有任何數值型態的欄位可供計算統計摘要。")
    else:
        lines.append(numeric_df.to_markdown(index=False))

    if group_col and target_col:
        try:
            grouped_df = get_groupby_summary(df, group_col=group_col, target_col=target_col)
            lines.extend(
                [
                    "",
                    f"## 5. 分組樞紐分析（依「{group_col}」統計「{target_col}」）",
                    "",
                    grouped_df.to_markdown(index=False),
                ]
            )
        except (KeyError, ValueError):
            pass

    lines.append("")
    return "\n".join(lines)
