"""負責讀取與分析 CSV 資料的核心模組。"""

from typing import Any, Dict, IO, List, Optional, Tuple, Union
import pandas as pd


class CSVLoadError(Exception):
    """當 CSV 檔案讀取失敗或內容無效時拋出的自訂例外。"""


def load_csv(file_source: Union[str, IO[Any]]) -> pd.DataFrame:
    """讀取 CSV 檔案並回傳 Pandas DataFrame。

    支援傳入檔案路徑或 Streamlit 上傳的檔案物件，並自動嘗試常見編碼。

    Args:
        file_source: 檔案路徑字串，或類檔案物件 (file-like object)。

    Returns:
        讀取成功後的 pd.DataFrame。

    Raises:
        CSVLoadError: 當檔案為空、格式錯誤或無法解析時。
    """
    encodings = ["utf-8", "utf-8-sig", "cp950", "big5"]
    last_error = None

    # 預先檢查是否為含有 Null Byte (\x00) 的二進位檔案（例如誤把圖片或 Excel .xlsx 改名成 .csv）
    if hasattr(file_source, "read") and hasattr(file_source, "seek"):
        file_source.seek(0)
        sample_chunk = file_source.read(1024)
        file_source.seek(0)
        if isinstance(sample_chunk, bytes) and b"\x00" in sample_chunk:
            raise CSVLoadError(
                "偵測到二進位檔案內容（可能為 Excel .xlsx 或圖片檔），請確認上傳的是純文字 CSV 檔案。"
            )

    for encoding in encodings:
        try:
            # 如果是檔案物件（例如 Streamlit UploadedFile），每次重試前須將讀取指標移回開頭
            if hasattr(file_source, "seek"):
                file_source.seek(0)

            df = pd.read_csv(file_source, encoding=encoding)

            if df.empty or len(df.columns) == 0:
                raise CSVLoadError("CSV 檔案中沒有任何資料列或欄位。")

            return df
        except UnicodeDecodeError as err:
            last_error = err
            continue
        except pd.errors.EmptyDataError as err:
            raise CSVLoadError("上傳的 CSV 檔案是空的，請確認檔案內容。") from err
        except pd.errors.ParserError as err:
            raise CSVLoadError("CSV 格式解析失敗，請確認檔案是否為有效的逗號分隔格式。") from err
        except CSVLoadError:
            raise
        except Exception as err:
            raise CSVLoadError(f"讀取 CSV 時發生未預期的錯誤：{err}") from err

    raise CSVLoadError(
        "無法識別檔案的文字編碼（已嘗試 UTF-8 與 Big5/CP950），請將檔案轉存為 UTF-8 後再試。"
    ) from last_error


def get_basic_info(df: pd.DataFrame) -> Dict[str, Any]:
    """取得 DataFrame 的基本概況資訊（列數、欄數、欄位名稱與型態）。

    Args:
        df: 要分析的 Pandas DataFrame。

    Returns:
        包含 rows（總列數）、columns（總欄數）、column_names（欄位清單）的字典。
    """
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
    }


def get_missing_summary(df: pd.DataFrame) -> pd.DataFrame:
    """計算各欄位的資料型態、缺失值數量與缺失比例。

    Args:
        df: 要分析的 Pandas DataFrame。

    Returns:
        包含欄位名稱、資料型態、缺失值數量、缺失比例 (%) 與有效筆數的 DataFrame。
    """
    total_rows = len(df)
    missing_counts = df.isna().sum()
    non_null_counts = df.notna().sum()
    missing_pct = (
        (missing_counts / total_rows * 100).round(2) if total_rows > 0 else 0.0
    )

    summary_df = pd.DataFrame(
        {
            "欄位名稱": df.columns,
            "資料型態": [str(dtype) for dtype in df.dtypes],
            "缺失值數量": missing_counts.values,
            "缺失比例 (%)": missing_pct.values,
            "有效筆數": non_null_counts.values,
        }
    )
    return summary_df.reset_index(drop=True)


def get_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    """計算所有數值欄位的描述性統計摘要（平均數、標準差、中位數、最大/最小值等）。

    Args:
        df: 要分析的 Pandas DataFrame。

    Returns:
        數值欄位統計摘要 DataFrame；若無任何數值欄位則回傳空 DataFrame。
    """
    numeric_df = df.select_dtypes(include="number")
    if numeric_df.empty or len(numeric_df.columns) == 0:
        return pd.DataFrame()

    desc = numeric_df.describe().T
    summary_df = pd.DataFrame(
        {
            "欄位名稱": desc.index,
            "有效筆數": desc["count"].astype(int).values,
            "平均數": desc["mean"].round(2).values,
            "標準差": desc["std"].round(2).values,
            "最小值": desc["min"].round(2).values,
            "25% 分位數": desc["25%"].round(2).values,
            "中位數 (50%)": desc["50%"].round(2).values,
            "75% 分位數": desc["75%"].round(2).values,
            "最大值": desc["max"].round(2).values,
        }
    )
    return summary_df.reset_index(drop=True)


def clean_missing_values(df: pd.DataFrame, strategy: str = "none") -> pd.DataFrame:
    """根據指定策略清理 DataFrame 中的缺失值（回傳新副本，不修改原始資料）。

    Args:
        df: 原始 Pandas DataFrame。
        strategy: 清理策略，支援：
            - "none": 不處理，直接回傳副本
            - "drop_rows": 刪除任何含有缺失值的資料列
            - "fill_median": 數值欄位填補中位數，非數值欄位填補 "未知"
            - "fill_mean": 數值欄位填補平均數（小數點後兩位），非數值欄位填補 "未知"

    Returns:
        清理後的全新 pd.DataFrame。

    Raises:
        ValueError: 當傳入不支援的 strategy 時。
    """
    cleaned = df.copy()

    if strategy == "none":
        return cleaned

    if strategy == "drop_rows":
        return cleaned.dropna().reset_index(drop=True)

    if strategy in ("fill_median", "fill_mean"):
        for col in cleaned.columns:
            if pd.api.types.is_numeric_dtype(cleaned[col]):
                if cleaned[col].notna().any():
                    fill_val = (
                        cleaned[col].median()
                        if strategy == "fill_median"
                        else round(float(cleaned[col].mean()), 2)
                    )
                    cleaned[col] = cleaned[col].fillna(fill_val)
            else:
                cleaned[col] = cleaned[col].fillna("未知")
        return cleaned

    raise ValueError(f"不支援的缺失值清理策略：{strategy}")


def generate_auto_insights(df: pd.DataFrame) -> List[str]:
    """利用本機統計規則自動分析 DataFrame，產生白話文重點洞察清單。

    包含三大維度：
    1. 缺失值健康度檢查
    2. 數值欄位皮爾森相關係數 (|r| >= 0.7) 強相關偵測
    3. 四分位距法 (IQR) 潛在極端值/離群值偵測

    Args:
        df: 要分析的 Pandas DataFrame。

    Returns:
        包含多條繁體中文分析結論的字串清單。
    """
    insights: List[str] = []
    total_rows = len(df)
    if total_rows == 0:
        return ["⚠️ 資料集目前沒有任何資料列可供分析。"]

    # 1. 缺失值洞察
    missing_counts = df.isna().sum()
    total_missing = int(missing_counts.sum())
    if total_missing == 0:
        insights.append("✅ **資料完整度極佳**：所有欄位皆無缺失值。")
    else:
        max_missing_col = str(missing_counts.idxmax())
        max_missing_val = int(missing_counts.max())
        max_missing_pct = round(max_missing_val / total_rows * 100, 2)
        insights.append(
            f"⚠️ **缺失值提醒**：整份資料共有 {total_missing} 個缺失值，"
            f"其中以「**{max_missing_col}**」缺漏最多（共 {max_missing_val} 筆，佔 {max_missing_pct}%）。"
        )

    # 2. 數值欄位相關性洞察 (|r| >= 0.7)
    numeric_df = df.select_dtypes(include="number")
    num_cols = list(numeric_df.columns)
    if len(num_cols) >= 2:
        corr_matrix = numeric_df.corr()
        strong_pairs = []
        for i in range(len(num_cols)):
            for j in range(i + 1, len(num_cols)):
                col1, col2 = num_cols[i], num_cols[j]
                r_val = corr_matrix.loc[col1, col2]
                if pd.notna(r_val) and abs(r_val) >= 0.7:
                    relation = "高度正相關" if r_val > 0 else "高度負相關"
                    strong_pairs.append(
                        f"「**{col1}**」與「**{col2}**」呈現{relation} ($r = {r_val:.2f}$)"
                    )
        if strong_pairs:
            insights.append("🔗 **強相關欄位發現**：" + "；".join(strong_pairs) + "。")
        else:
            insights.append("ℹ️ **欄位相關性**：數值欄位之間未發現明顯的強相關（$|r| \\ge 0.7$）。")

    # 3. 潛在離群值 (IQR 法) 洞察
    outlier_notes = []
    for col in num_cols:
        series = numeric_df[col].dropna()
        if len(series) < 4:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = series[(series < lower_bound) | (series > upper_bound)]
        if not outliers.empty:
            outlier_notes.append(f"「**{col}**」（共 {len(outliers)} 筆）")

    if outlier_notes:
        insights.append(
            "🔎 **潛在極端值（離群值）偵測**：依據四分位距 (IQR) 法，"
            + "、".join(outlier_notes)
            + " 含有超出正常範圍的極端數值，建議搭配盒鬚圖檢視。"
        )
    elif num_cols:
        insights.append("📦 **極端值檢查**：依據四分位距 (IQR) 法，各數值欄位分佈均勻，未偵測到明顯離群值。")

    return insights


def filter_dataframe(
    df: pd.DataFrame,
    categorical_filters: Optional[Dict[str, List[Any]]] = None,
    numeric_ranges: Optional[Dict[str, Tuple[float, float]]] = None,
) -> pd.DataFrame:
    """根據類別條件與數值區間篩選 DataFrame（回傳新副本，不修改原始資料）。

    Args:
        df: 要篩選的 Pandas DataFrame。
        categorical_filters: 類別欄位篩選字典，格式為 {欄位名稱: [允許的值清單]}。
        numeric_ranges: 數值欄位區間字典，格式為 {欄位名稱: (最小值, 最大值)}。

    Returns:
        篩選後的全新 pd.DataFrame。

    Raises:
        KeyError: 當指定的篩選欄位不存在於 DataFrame 時。
    """
    filtered = df.copy()

    if categorical_filters:
        for col, allowed_values in categorical_filters.items():
            if col not in filtered.columns:
                raise KeyError(f"找不到指定的篩選欄位：「{col}」。")
            filtered = filtered[filtered[col].isin(allowed_values)]

    if numeric_ranges:
        for col, (min_val, max_val) in numeric_ranges.items():
            if col not in filtered.columns:
                raise KeyError(f"找不到指定的篩選欄位：「{col}」。")
            mask = (filtered[col] >= min_val) & (filtered[col] <= max_val)
            filtered = filtered[mask]

    return filtered.reset_index(drop=True)


def get_groupby_summary(
    df: pd.DataFrame,
    group_col: str,
    target_col: str,
) -> pd.DataFrame:
    """依指定欄位進行分組樞紐分析 (GroupBy)，計算目標數值欄位的統計量。

    Args:
        df: 要分析的 Pandas DataFrame。
        group_col: 分組依據的欄位名稱（例如「部門」）。
        target_col: 要計算統計量的數值欄位名稱（例如「月薪」）。

    Returns:
        包含分組名稱、有效筆數、平均數、中位數、最小值、最大值與總和的 DataFrame。

    Raises:
        KeyError: 當 group_col 或 target_col 不存在於 DataFrame 時。
        ValueError: 當 target_col 不是數值型態，或兩欄位相同時。
    """
    if group_col not in df.columns:
        raise KeyError(f"找不到分組欄位：「{group_col}」。")
    if target_col not in df.columns:
        raise KeyError(f"找不到目標數值欄位：「{target_col}」。")
    if group_col == target_col:
        raise ValueError("分組欄位與目標數值欄位不可為同一個欄位。")
    if not pd.api.types.is_numeric_dtype(df[target_col]):
        raise ValueError(f"目標欄位「{target_col}」不是數值型態，無法進行分組統計。")

    temp_df = df[[group_col, target_col]].copy()
    temp_df[group_col] = temp_df[group_col].fillna("(缺失值)").astype(str)

    grouped = temp_df.groupby(group_col, as_index=False)[target_col].agg(
        有效筆數="count",
        平均數="mean",
        中位數="median",
        最小值="min",
        最大值="max",
        總和="sum",
    )

    for col in ["平均數", "中位數", "最小值", "最大值", "總和"]:
        grouped[col] = grouped[col].round(2)

    return grouped.sort_values(by="平均數", ascending=False).reset_index(drop=True)





